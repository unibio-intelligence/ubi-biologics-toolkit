"""Bound CLI inputs before reading/decoding and accept supported evidence sizes."""
import io
import json
import os
import sys
import pytest
from ubi_cli.errors import ServiceError
from ubi_cli.cli import MAX_ARGUMENT_BYTES, main, read_arguments

def test_regular_input_is_bounded_in_bytes_before_full_read(tmp_path):
    path = tmp_path / 'oversized.json'
    with path.open('wb') as stream:
        stream.truncate(MAX_ARGUMENT_BYTES + 1)
    with pytest.raises(ServiceError):
        read_arguments('@' + str(path))
    raw = json.dumps({'text': '界' * (MAX_ARGUMENT_BYTES // 2)}, ensure_ascii=False)
    assert len(raw) < MAX_ARGUMENT_BYTES
    with pytest.raises(ServiceError) as exc:
        read_arguments(raw)
    assert exc.value.code == 'arguments_too_large'

def test_fifo_input_is_rejected_without_blocking(tmp_path):
    path = tmp_path / 'pipe'
    os.mkfifo(path)
    with pytest.raises(ServiceError, match='regular'):
        read_arguments('@' + str(path))

def test_stdin_reads_at_most_budget_plus_one_byte(monkeypatch):

    class Tracking(io.BytesIO):

        def read(self, count=-1):
            assert count == MAX_ARGUMENT_BYTES + 1
            return super().read(count)
    stream = Tracking(b'x' * (MAX_ARGUMENT_BYTES + 100))
    monkeypatch.setattr(sys, 'stdin', io.TextIOWrapper(stream))
    with pytest.raises(ServiceError) as exc:
        read_arguments('-')
    assert exc.value.code == 'arguments_too_large'
    assert stream.tell() == MAX_ARGUMENT_BYTES + 1

@pytest.mark.parametrize('raw', ['[]', '{"value": NaN}', '{"value": Infinity}', 'private-secret-invalid-json', '{"nested":' + '[' * 1500 + '0' + ']' * 1500 + '}'], ids=['array-root', 'nan', 'infinity', 'private-invalid', 'deep'])
def test_invalid_inputs_have_safe_errors(raw):
    with pytest.raises(ServiceError) as exc:
        read_arguments(raw)
    assert exc.value.code == 'invalid_arguments' and 'private-secret' not in str(exc.value)

def test_cli_foreign_failure_never_prints_raw_authentication_material(monkeypatch, capsys):
    import ubi_cli.cli as module

    async def fail(*args, **kwargs):
        raise RuntimeError('synthetic-token-and-secret-url')
    monkeypatch.setattr(module, 'call', fail)
    monkeypatch.setattr(sys, 'argv', ['ubi-biologics-cli', 'quota'])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ''
    assert json.loads(captured.err)['error']['code'] == 'cli_failed'
    assert 'synthetic-token' not in captured.err

def test_cli_preserves_safe_oauth_error_inside_task_group(monkeypatch, capsys):
    import ubi_cli.cli as module

    async def fail(*args, **kwargs):
        raise ExceptionGroup('private SDK details', [RuntimeError('synthetic-secret'), ServiceError('login_required', 'Run ubi-biologics-cli login.')])
    monkeypatch.setattr(module, 'call', fail)
    monkeypatch.setattr(sys, 'argv', ['ubi-biologics-cli', 'quota'])
    with pytest.raises(SystemExit):
        main()
    error = json.loads(capsys.readouterr().err)['error']
    assert error['code'] == 'login_required' and 'synthetic-secret' not in str(error)
