"""JSON CLI for the canonical Ubi platform tool contract."""
from __future__ import annotations
import argparse
import asyncio
import json
import math
from importlib.metadata import version
import os
import stat
import sys
from fastmcp.client.transports import StreamableHttpTransport
from .errors import ServiceError
from .errors import safe_error as common_safe_error
from .cli_auth import NativeClient, NativeOAuth, SecureKeyringStore, credential_status, http_factory, resource_url, revoke
from .transport import decode_result
from .transport import Client
MAX_ARGUMENT_BYTES = 1048576
AUTH_COMMANDS = {'login', 'status', 'logout', 'revoke', 'doctor'}

def read_arguments(argument):
    try:
        if argument == '-':
            stream = getattr(sys.stdin, 'buffer', sys.stdin)
            raw = stream.read(MAX_ARGUMENT_BYTES + 1)
        elif argument.startswith('@'):
            before = os.stat(argument[1:])
            if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_ARGUMENT_BYTES:
                raise ValueError
            descriptor = os.open(argument[1:], os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_BINARY', 0))
            with os.fdopen(descriptor, 'rb') as stream:
                metadata = os.fstat(stream.fileno())
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_ARGUMENT_BYTES:
                    raise ValueError
                raw = stream.read(MAX_ARGUMENT_BYTES + 1)
        else:
            raw = argument
        if isinstance(raw, str):
            raw = raw.encode('utf-8')
        if len(raw) > MAX_ARGUMENT_BYTES:
            raise ServiceError('arguments_too_large', 'Arguments exceed the 1 MiB byte budget.')
        value = json.loads(raw.decode('utf-8'), parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
        if not isinstance(value, dict):
            raise TypeError
        pending = [(value, 0)]
        nodes = 0
        while pending:
            item, depth = pending.pop()
            nodes += 1
            if depth > 32 or nodes > 100000:
                raise ServiceError('invalid_arguments', 'Arguments exceed the JSON depth or node budget.')
            if isinstance(item, float) and not math.isfinite(item):
                raise ServiceError('invalid_arguments')
            if isinstance(item, dict):
                pending.extend(((child, depth + 1) for child in item.values()))
            elif isinstance(item, list):
                pending.extend(((child, depth + 1) for child in item))
        return value
    except ServiceError:
        raise
    except (OSError, ValueError, TypeError, UnicodeError, RecursionError):
        raise ServiceError('invalid_arguments', 'Use a bounded UTF-8 JSON object, a regular @file.json, or stdin.') from None

async def call(operation, arguments, *, url=None, login=False, forget_local=False):
    target = resource_url(url or os.getenv('UBI_MCP_URL', 'https://mcp.unibiointelligence.com/mcp'))
    interactive = login or operation == 'login'
    bearer = os.getenv('UBI_MCP_TOKEN') if not interactive else None
    if bearer and operation in {'logout', 'revoke'}:
        raise ServiceError('environment_token_not_managed', 'Environment credentials are not managed by this CLI. Unset UBI_MCP_TOKEN to manage the saved OAuth grant.')
    if bearer:
        if operation == 'status':
            return {'resource': target, 'credential_source': 'environment', 'server_authorization_checked': False}
        auth = bearer
    else:
        native = NativeClient.configured(target)
        store = SecureKeyringStore(target, native.identity)
        if operation == 'status':
            return await credential_status(target, native, store)
        if operation in {'logout', 'revoke'}:
            return await revoke(target, native, store, forget_local=forget_local, logout=operation == 'logout')
        auth = NativeOAuth(target, native, store, interactive=interactive)
    resource = target
    target = StreamableHttpTransport(resource, auth=auth, httpx_client_factory=http_factory(resource))
    async with Client(target, auth=auth, preserve_service_error=True) as client:
        if operation == 'login':
            await client.list_tools()
            status = await credential_status(resource, native, store)
            if not status['tokens_present']:
                raise ServiceError('login_not_completed', 'The resource did not establish an OAuth grant.')
            return {**status, 'server_authorization_checked': True}
        if operation == 'doctor':
            tools = await client.list_tools()
            return {'resource': resource, 'connected': True, 'tool_count': len(tools), 'client_id': native.identity if not bearer else None, 'credential_source': 'environment' if bearer else 'os_keyring'}
        primitive = await protocol_call(client, operation, arguments)
        if primitive is not None:
            return primitive
        return decode_result(await client.call_tool(operation, arguments, raise_on_error=False), preserve_service_error=True)

def safe_error(error):
    return common_safe_error(error, fallback='cli_failed').as_dict()

def main():
    parser = argparse.ArgumentParser(description='Ubi platform: data, tools and modeling')
    parser.add_argument('--version', action='version', version=version('ubi-biologics-cli'))
    parser.add_argument('operation')
    parser.add_argument('arguments', nargs='?', default='{}', help='JSON, @file.json or - for stdin')
    parser.add_argument('--url')
    parser.add_argument('--login', action='store_true', help='Use the client OAuth login flow for hosted calls')
    parser.add_argument('--forget-local', action='store_true', help='Remove saved local credentials without server revocation (logout only)')
    args = parser.parse_args()
    if args.operation in {'servers', 'query', 'query_batch', 'action', 'preview_run', 'submit_run'}:
        parser.error('Retired command; inspect tools and use a named platform tool.')
    if args.forget_local and args.operation != 'logout':
        parser.error('--forget-local applies only to logout')
    try:
        arguments = read_arguments(args.arguments)
        if args.operation in AUTH_COMMANDS and arguments:
            raise ServiceError('invalid_arguments', 'Authentication commands take no JSON arguments.')
        print(json.dumps(asyncio.run(call(args.operation, arguments, url=args.url, login=args.login, forget_local=args.forget_local)), allow_nan=False))
    except Exception as exc:
        print(json.dumps({'error': safe_error(exc)}), file=sys.stderr)
        raise SystemExit(2) from None

async def protocol_call(client, operation, params):
    if operation in {'resources', 'prompts', 'tools', 'read-resource', 'get-prompt'}:
        required = {'read-resource': 'uri', 'get-prompt': 'name'}.get(operation)
        allowed = {required} if required else set()
        if operation == 'get-prompt':
            allowed.add('arguments')
        if set(params) - allowed:
            raise ServiceError('invalid_parameters', field_paths=['$'])
        if required and required not in params:
            raise ServiceError('missing_input', field_paths=['$.' + required])
        if required and (not isinstance(params[required], str) or not params[required]):
            raise ServiceError('invalid_parameters', field_paths=['$.' + required])

    def serial(value):
        if isinstance(value, list):
            return [serial(item) for item in value]
        return value.model_dump(mode='json') if hasattr(value, 'model_dump') else value
    if operation == 'resources':
        return serial(await client.list_resources())
    if operation == 'read-resource':
        return serial(await client.read_resource(params['uri']))
    if operation == 'prompts':
        return serial(await client.list_prompts())
    if operation == 'get-prompt':
        return serial(await client.get_prompt(params['name'], params.get('arguments', {})))
    if operation == 'tools':
        return serial(await client.list_tools())
    return None
