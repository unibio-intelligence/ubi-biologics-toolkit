import assert from 'node:assert/strict';
import test from 'node:test';

import {
	ExecutionError,
	PublicationError,
	ScientificRunsClient,
	type Job,
	type RunPreview,
	type RunSubmission
} from '../src/scientific-runs.js';

const envelope = <T>(data: T) => ({
	data,
	meta: { request_id: 'req_test', trace_id: 'trace_test' }
});

function job(state: Job['state'] = 'succeeded', publication_state = 'published'): Job {
	return {
		id: 'job_1',
		run_id: 'run_1',
		destination_project_id: 'project_1',
		state,
		resource_class: 'cpu-small',
		attempt_count: 1,
		max_attempts: 3,
		cancellation_requested: false,
		publication_state,
		staged_outputs: [],
		pricing: {
			credit_cost: 2,
			pricing_note: 'fixed',
			billing_unit: 'credits',
			pricing_model: 'ubi_fixed_operation_credits_v1'
		},
		created_at: '2026-08-19T00:00:00Z',
		updated_at: '2026-08-19T00:00:01Z'
	};
}

const preview: RunPreview = {
	approval_required: false,
	binding_digest: 'binding_1',
	capability_id: 'abnumber.annotate',
	capability_version: '1.0.0',
	estimates: {},
	expected_outputs: [],
	normalized_inputs: [],
	normalized_parameters: {},
	policy: {},
	preview_digest: 'preview_1',
	preview_receipt: 'signed-preview-receipt',
	pricing: {
		credit_cost: 2,
		pricing_note: 'fixed',
		billing_unit: 'credits',
		pricing_model: 'ubi_fixed_operation_credits_v1'
	},
	side_effect_class: 'reversible_write',
	valid: true,
	workbench_href: '/projects/project_1'
};

const submission: RunSubmission = {
	expected_outputs: [],
	jobs: [job('queued', 'pending')],
	pricing: {
		credit_cost: 2,
		pricing_note: 'fixed',
		billing_unit: 'credits',
		pricing_model: 'ubi_fixed_operation_credits_v1'
	},
	run: {
		id: 'run_1',
		binding_digest: 'binding_1',
		capability_id: 'abnumber.annotate',
		capability_version: '1.0.0',
		created_at: '2026-08-19T00:00:00Z',
		destination_project_id: 'project_1',
		initiating_principal_id: 'principal_1',
		mode: 'execute',
		output_manifest: [],
		parameters: {},
		side_effect_class: 'reversible_write',
		state: 'ready',
		updated_at: '2026-08-19T00:00:00Z'
	},
	status_href: '/api/v1/jobs/job_1',
	workbench_href: '/projects/project_1'
};

test('automatic workflow reuses one idempotency key and calls onSubmitted before waiting', async () => {
	const calls: string[] = [];
	const keys: string[] = [];
	let submissions = 0;
	const fetcher: typeof fetch = async (input, init) => {
		assert.equal(new Headers(init?.headers).get('X-Ubi-Client'), 'sdk');
		const url = new URL(String(input));
		calls.push(`${init?.method ?? 'GET'} ${url.pathname}`);
		if (url.pathname === '/api/v1/projects/default') {
			return Response.json(envelope({ id: 'project_1' }));
		}
		if (url.pathname === '/api/v1/runs/preview') return Response.json(envelope(preview));
		if (url.pathname === '/api/v1/runs') {
			submissions += 1;
			keys.push(new Headers(init?.headers).get('Idempotency-Key') ?? '');
			assert.equal(JSON.parse(String(init?.body)).preview_receipt, 'signed-preview-receipt');
			if (submissions === 1) {
				return Response.json(
					{ error: { code: 'CAPACITY_UNAVAILABLE', message: 'retry', retryable: true } },
					{ status: 503 }
				);
			}
			return Response.json(envelope(submission), { status: 202 });
		}
		if (url.pathname.endsWith('/events/stream')) {
			return new Response(': no new events\n\n', {
				headers: { 'content-type': 'text/event-stream' }
			});
		}
		if (url.pathname === '/api/v1/jobs/job_1') return Response.json(envelope(job()));
		if (url.pathname === '/api/v1/jobs/job_1/detail') {
			return Response.json(envelope({ artifacts: [{ id: 'artifact_1' }] }));
		}
		if (url.pathname === '/api/v1/artifacts/artifact_1/content') {
			return new Response('artifact');
		}
		throw new Error(`Unexpected request: ${url}`);
	};
	let submittedCall = -1;
	const stateChanges: Job['state'][] = [];
	const client = new ScientificRunsClient({
		baseUrl: 'https://biologics.unibiointelligence.com',
		accessToken: () => 'token',
		fetch: fetcher,
		sleep: async () => undefined
	});

	const result = await client.run(
		{ capability_id: 'abnumber.annotate' },
		{
			idempotencyKey: 'stable-key',
			downloadArtifacts: true,
			onSubmitted: () => {
				submittedCall = calls.length;
			},
			onStateChange: (job) => {
				stateChanges.push(job.state);
			}
		}
	);

	assert.deepEqual(keys, ['stable-key', 'stable-key']);
	assert.ok(submittedCall < calls.findIndex((call) => call === 'GET /api/v1/jobs/job_1') + 1);
	assert.equal(calls.filter((call) => call.endsWith('/api/v1/projects/default')).length, 1);
	assert.equal(result.jobs[0].state, 'succeeded');
	assert.deepEqual(stateChanges, ['succeeded']);
	assert.equal(new TextDecoder().decode(result.artifactContents.get('artifact_1')), 'artifact');
});

test('cancel uses the governed Job endpoint with caller-stable idempotency', async () => {
	const client = new ScientificRunsClient({
		baseUrl: 'https://example.test',
		accessToken: () => 'token',
		fetch: async (input, init) => {
			const url = new URL(String(input));
			assert.equal(url.pathname, '/api/v1/jobs/job_1/cancel');
			assert.equal(new Headers(init?.headers).get('Idempotency-Key'), 'cancel-key');
			assert.deepEqual(JSON.parse(String(init?.body)), { reason: 'user request' });
			return Response.json(envelope(job('cancel_requested', 'pending')));
		}
	});

	assert.equal(
		(await client.cancel('job_1', 'user request', 'cancel-key')).state,
		'cancel_requested'
	);
});

test('SSE failure falls back to Retry-After-aware polling', async () => {
	const states = [job('running', 'pending'), job()];
	const sleeps: number[] = [];
	const client = new ScientificRunsClient({
		baseUrl: 'https://example.test',
		accessToken: () => 'token',
		fetch: async (input) => {
			const url = new URL(String(input));
			if (url.pathname.endsWith('/events/stream')) return Response.json({ no: 'stream' });
			if (url.pathname === '/api/v1/jobs/job_1') {
				return Response.json(envelope(states.shift()), { headers: { 'Retry-After': '0.01' } });
			}
			throw new Error(`Unexpected request: ${url}`);
		},
		sleep: async (ms) => {
			sleeps.push(ms);
		}
	});

	assert.equal((await client.waitForJob('job_1')).state, 'succeeded');
	assert.deepEqual(sleeps, [10]);
});

test('terminal execution and publication failures are typed', async () => {
	for (const [terminal, ErrorType] of [
		[job('failed', 'failed'), ExecutionError],
		[job('succeeded', 'failed'), PublicationError]
	] as const) {
		const client = new ScientificRunsClient({
			baseUrl: 'https://example.test',
			accessToken: () => 'token',
			fetch: async (input) => {
				const url = new URL(String(input));
				if (url.pathname === '/api/v1/jobs/job_1') return Response.json(envelope(terminal));
				throw new Error('SSE intentionally disabled');
			}
		});
		await assert.rejects(() => client.waitForJob('job_1', { useSse: false }), ErrorType);
	}
});
