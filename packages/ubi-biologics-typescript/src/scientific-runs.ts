import type { components } from './schema.js';

type RunCreateRequest = components['schemas']['RunCreateRequest'];
type RunExecuteRequest = components['schemas']['RunExecuteRequest'] & { preview_receipt: string };
export type RunPreview = components['schemas']['RunPreviewResponse'] & {
	preview_receipt?: string | null;
	preview_receipt_expires_at?: string | null;
};
export type RunSubmission = components['schemas']['RunSubmissionResponse'];
export type Job = components['schemas']['JobResponse'];
export type Artifact = components['schemas']['ArtifactResponse'];
export type JobEvent = components['schemas']['JobEventResponse'];

export type ScientificRunDraft = Omit<RunCreateRequest, 'mode' | 'destination_project_id'> & {
	destination_project_id?: string;
};

const TERMINAL_STATES = new Set<Job['state']>([
	'succeeded',
	'failed',
	'cancelled',
	'timed_out',
	'expired'
]);

export class ScientificRunError extends Error {
	constructor(
		message: string,
		readonly code: string,
		readonly status?: number,
		readonly retryable = false,
		readonly details?: Record<string, unknown>
	) {
		super(message);
		this.name = new.target.name;
	}
}

export class AdmissionError extends ScientificRunError {}
export class ApprovalRequiredError extends AdmissionError {}
export class ExecutionError extends ScientificRunError {}
export class PublicationError extends ScientificRunError {}
export class WorkflowTimeoutError extends ScientificRunError {}
export class WorkflowCancelledError extends ScientificRunError {}

export interface ScientificRunResult {
	preview?: RunPreview;
	submission?: RunSubmission;
	jobs: Job[];
	artifacts: Artifact[];
	artifactContents: Map<string, Uint8Array>;
}

export interface ScientificRunsClientOptions {
	/** Empty means same-origin; external agents should use the canonical product origin. */
	baseUrl?: string;
	accessToken: () => string | null | Promise<string | null>;
	fetch?: typeof globalThis.fetch;
	random?: () => number;
	sleep?: (milliseconds: number, signal?: AbortSignal) => Promise<void>;
}

export interface WaitOptions {
	timeoutMs?: number;
	signal?: AbortSignal;
	useSse?: boolean;
	onEvent?: (event: JobEvent) => void | Promise<void>;
	onStateChange?: (job: Job) => void | Promise<void>;
	initialPollMs?: number;
	maxPollMs?: number;
}

export interface RunOptions extends WaitOptions {
	idempotencyKey?: string;
	submissionAttempts?: number;
	downloadArtifacts?: boolean;
	approve?: (preview: RunPreview) => boolean | void | Promise<boolean | void>;
	onSubmitted?: (submission: RunSubmission) => void | Promise<void>;
}

type ErrorBody = components['schemas']['ErrorBody'];

function randomId(): string {
	if (!globalThis.crypto?.randomUUID) {
		throw new ScientificRunError(
			'crypto.randomUUID is required to create stable idempotency keys.',
			'CRYPTO_UNAVAILABLE'
		);
	}
	return globalThis.crypto.randomUUID();
}

function defaultSleep(milliseconds: number, signal?: AbortSignal): Promise<void> {
	return new Promise((resolve, reject) => {
		if (signal?.aborted) {
			reject(new DOMException('Aborted', 'AbortError'));
			return;
		}
		const timer = setTimeout(resolve, milliseconds);
		signal?.addEventListener(
			'abort',
			() => {
				clearTimeout(timer);
				reject(new DOMException('Aborted', 'AbortError'));
			},
			{ once: true }
		);
	});
}

function retryAfterMilliseconds(value: string | null): number | undefined {
	if (!value) return undefined;
	const seconds = Number(value);
	if (Number.isFinite(seconds)) return Math.max(0, seconds * 1000);
	const at = Date.parse(value);
	return Number.isFinite(at) ? Math.max(0, at - Date.now()) : undefined;
}

function isAbort(error: unknown): boolean {
	return error instanceof DOMException && error.name === 'AbortError';
}

export class ScientificRunsClient {
	private readonly baseUrl: string;
	private readonly accessToken: ScientificRunsClientOptions['accessToken'];
	private readonly fetcher: typeof globalThis.fetch;
	private readonly random: () => number;
	private readonly sleep: NonNullable<ScientificRunsClientOptions['sleep']>;
	private defaultProject?: Promise<string>;
	private readonly defaultProjectKey = randomId();

	constructor(options: ScientificRunsClientOptions) {
		this.baseUrl = (options.baseUrl ?? '').replace(/\/$/, '');
		this.accessToken = options.accessToken;
		this.fetcher = options.fetch ?? globalThis.fetch.bind(globalThis);
		this.random = options.random ?? Math.random;
		this.sleep = options.sleep ?? defaultSleep;
	}

	clearDefaultProject(): void {
		this.defaultProject = undefined;
	}

	private url(path: string): string {
		return `${this.baseUrl}${path}`;
	}

	private async request(path: string, init: RequestInit = {}): Promise<Response> {
		const token = await this.accessToken();
		if (!token) {
			throw new AdmissionError('Authentication is required.', 'AUTHENTICATION_REQUIRED', 401);
		}
		const headers = new Headers(init.headers);
		headers.set('X-Ubi-Client', 'sdk');
		headers.set('Authorization', `Bearer ${token}`);
		if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
		const response = await this.fetcher(this.url(path), { ...init, headers });
		if (!response.ok) throw await this.apiError(response);
		return response;
	}

	private async apiError(response: Response): Promise<ScientificRunError> {
		let body: Partial<ErrorBody> = {};
		try {
			const envelope = (await response.clone().json()) as { error?: Partial<ErrorBody> };
			body = envelope.error ?? {};
		} catch {
			// The stable HTTP fallback below still fails closed.
		}
		const code = body.code ?? `HTTP_${response.status}`;
		const ErrorType = code === 'APPROVAL_REQUIRED' ? ApprovalRequiredError : AdmissionError;
		return new ErrorType(
			body.message ?? `API request failed with HTTP ${response.status}.`,
			code,
			response.status,
			body.retryable === true || response.status === 429 || response.status === 503,
			body.details as Record<string, unknown> | undefined
		);
	}

	private async jsonData<T>(
		path: string,
		init?: RequestInit
	): Promise<{ data: T; response: Response }> {
		const response = await this.request(path, init);
		const payload = (await response.json()) as { data?: T };
		if (payload.data === undefined) {
			throw new ScientificRunError(
				'The API returned an invalid success envelope.',
				'INVALID_API_ENVELOPE'
			);
		}
		return { data: payload.data, response };
	}

	async ensureDefaultProject(signal?: AbortSignal): Promise<string> {
		this.defaultProject ??= this.jsonData<components['schemas']['ProjectResponse']>(
			'/api/v1/projects/default',
			{
				method: 'POST',
				headers: { 'Idempotency-Key': this.defaultProjectKey },
				signal
			}
		).then(({ data }) => data.id);
		try {
			return await this.defaultProject;
		} catch (error) {
			this.defaultProject = undefined;
			throw error;
		}
	}

	private async body(
		draft: ScientificRunDraft,
		mode: components['schemas']['RunMode'],
		signal?: AbortSignal
	): Promise<RunCreateRequest> {
		return {
			...draft,
			destination_project_id:
				draft.destination_project_id ?? (await this.ensureDefaultProject(signal)),
			inputs: draft.inputs ?? [],
			parameters: draft.parameters ?? {},
			mode
		};
	}

	async preview(draft: ScientificRunDraft, signal?: AbortSignal): Promise<RunPreview> {
		const body = await this.body(draft, 'preview', signal);
		return (
			await this.jsonData<RunPreview>('/api/v1/runs/preview', {
				method: 'POST',
				body: JSON.stringify(body),
				signal
			})
		).data;
	}

	async submit(
		draft: ScientificRunDraft,
		expectedPreviewDigest: string,
		previewReceipt: string,
		idempotencyKey: string,
		signal?: AbortSignal
	): Promise<RunSubmission> {
		const body: RunExecuteRequest = {
			...(await this.body(draft, 'execute', signal)),
			expected_preview_digest: expectedPreviewDigest,
			preview_receipt: previewReceipt
		};
		return (
			await this.jsonData<RunSubmission>('/api/v1/runs', {
				method: 'POST',
				headers: { 'Idempotency-Key': idempotencyKey },
				body: JSON.stringify(body),
				signal
			})
		).data;
	}

	private async submitWithRetry(
		draft: ScientificRunDraft,
		previewDigest: string,
		previewReceipt: string,
		idempotencyKey: string,
		attempts: number,
		signal?: AbortSignal
	): Promise<RunSubmission> {
		for (let attempt = 0; ; attempt += 1) {
			try {
				return await this.submit(draft, previewDigest, previewReceipt, idempotencyKey, signal);
			} catch (error) {
				if (isAbort(error)) throw this.cancelled();
				const retryable =
					error instanceof TypeError || (error instanceof ScientificRunError && error.retryable);
				if (!retryable || attempt + 1 >= attempts) throw error;
				await this.sleep(Math.min(4000, 250 * 2 ** attempt), signal);
			}
		}
	}

	private cancelled(): WorkflowCancelledError {
		return new WorkflowCancelledError(
			'The local wait was cancelled; the durable Job was not cancelled.',
			'LOCAL_WAIT_CANCELLED'
		);
	}

	private checkDeadline(deadline: number, signal?: AbortSignal): void {
		if (signal?.aborted) throw this.cancelled();
		if (Date.now() >= deadline) {
			throw new WorkflowTimeoutError(
				'Timed out waiting for the durable Job. Resume later with its Job ID.',
				'LOCAL_WAIT_TIMEOUT',
				undefined,
				true
			);
		}
	}

	private terminal(job: Job): boolean {
		if (!TERMINAL_STATES.has(job.state)) return false;
		if (job.state !== 'succeeded') {
			throw new ExecutionError(
				`Job ${job.id} ended in state ${job.state}.`,
				`JOB_${job.state.toUpperCase()}`,
				undefined,
				false,
				{ job }
			);
		}
		if (job.publication_state !== 'published') {
			throw new PublicationError(
				`Job ${job.id} succeeded without published outputs.`,
				'JOB_PUBLICATION_INCOMPLETE',
				undefined,
				false,
				{ job }
			);
		}
		return true;
	}

	private async sseOnce(
		jobId: string,
		afterSequence: number,
		timeoutSeconds: number,
		signal?: AbortSignal
	): Promise<JobEvent[]> {
		const response = await this.request(
			`/api/v1/jobs/${encodeURIComponent(jobId)}/events/stream?after_sequence=${afterSequence}&timeout_seconds=${timeoutSeconds}`,
			{ headers: { Accept: 'text/event-stream' }, signal }
		);
		if (!response.body || !response.headers.get('content-type')?.includes('text/event-stream')) {
			throw new TypeError('SSE stream is unavailable.');
		}
		const reader = response.body.getReader();
		const decoder = new TextDecoder();
		let text = '';
		while (true) {
			const { done, value } = await reader.read();
			if (done) break;
			text += decoder.decode(value, { stream: true });
		}
		text += decoder.decode();
		const events: JobEvent[] = [];
		for (const block of text.split(/\r?\n\r?\n/)) {
			const data = block
				.split(/\r?\n/)
				.filter((line) => line.startsWith('data:'))
				.map((line) => line.slice(5).trimStart())
				.join('\n');
			if (!data) continue;
			try {
				events.push(JSON.parse(data) as JobEvent);
			} catch {
				// Ignore malformed individual events; the durable Job GET remains authoritative.
			}
		}
		return events;
	}

	async waitForJob(jobId: string, options: WaitOptions = {}): Promise<Job> {
		const deadline = Date.now() + (options.timeoutMs ?? 3_600_000);
		let sequence = 0;
		let pollAttempt = 0;
		let streamEnabled = options.useSse ?? true;
		let lastState: Job['state'] | undefined;
		while (true) {
			this.checkDeadline(deadline, options.signal);
			if (streamEnabled) {
				try {
					const seconds = Math.max(1, Math.min(30, Math.floor((deadline - Date.now()) / 1000)));
					for (const event of await this.sseOnce(jobId, sequence, seconds, options.signal)) {
						sequence = Math.max(sequence, event.sequence);
						await options.onEvent?.(event);
					}
				} catch (error) {
					if (isAbort(error)) throw this.cancelled();
					if (error instanceof ScientificRunError && !error.retryable) throw error;
					streamEnabled = false;
				}
			}

			const { data: job, response } = await this.jsonData<Job>(
				`/api/v1/jobs/${encodeURIComponent(jobId)}`,
				{ signal: options.signal, cache: 'no-store' }
			);
			if (job.state !== lastState) {
				lastState = job.state;
				await options.onStateChange?.(job);
			}
			if (this.terminal(job)) return job;
			let delay = retryAfterMilliseconds(response.headers.get('Retry-After'));
			if (delay === undefined) {
				delay = Math.min(
					options.maxPollMs ?? 8000,
					(options.initialPollMs ?? 500) * 2 ** pollAttempt
				);
				delay *= 0.75 + this.random() * 0.5;
			}
			pollAttempt += 1;
			try {
				await this.sleep(Math.min(delay, Math.max(0, deadline - Date.now())), options.signal);
			} catch (error) {
				if (isAbort(error)) throw this.cancelled();
				throw error;
			}
		}
	}

	async downloadArtifact(artifactId: string, signal?: AbortSignal): Promise<Uint8Array> {
		try {
			const response = await this.request(
				`/api/v1/artifacts/${encodeURIComponent(artifactId)}/content`,
				{ signal }
			);
			return new Uint8Array(await response.arrayBuffer());
		} catch (error) {
			if (isAbort(error)) throw this.cancelled();
			if (error instanceof PublicationError) throw error;
			throw new PublicationError(
				error instanceof Error ? error.message : 'Artifact download failed.',
				'ARTIFACT_DOWNLOAD_FAILED',
				error instanceof ScientificRunError ? error.status : undefined,
				false
			);
		}
	}

	/** Explicitly request durable server-side cancellation of a Job. */
	async cancel(
		jobId: string,
		reason?: string,
		idempotencyKey = randomId(),
		signal?: AbortSignal
	): Promise<Job> {
		return (
			await this.jsonData<Job>(`/api/v1/jobs/${encodeURIComponent(jobId)}/cancel`, {
				method: 'POST',
				headers: { 'Idempotency-Key': idempotencyKey },
				body: JSON.stringify({ reason: reason ?? null }),
				signal
			})
		).data;
	}

	async resume(
		jobId: string,
		options: WaitOptions & { downloadArtifacts?: boolean } = {}
	): Promise<ScientificRunResult> {
		const job = await this.waitForJob(jobId, options);
		let detail: components['schemas']['JobDetailResponse'];
		try {
			detail = (
				await this.jsonData<components['schemas']['JobDetailResponse']>(
					`/api/v1/jobs/${encodeURIComponent(jobId)}/detail`,
					{ signal: options.signal, cache: 'no-store' }
				)
			).data;
		} catch (error) {
			if (isAbort(error)) throw this.cancelled();
			throw new PublicationError(
				error instanceof Error ? error.message : 'Job Artifact manifest retrieval failed.',
				error instanceof ScientificRunError ? error.code : 'JOB_DETAIL_FAILED',
				error instanceof ScientificRunError ? error.status : undefined,
				error instanceof ScientificRunError ? error.retryable : false,
				error instanceof ScientificRunError ? error.details : undefined
			);
		}
		const artifactContents = new Map<string, Uint8Array>();
		if (options.downloadArtifacts) {
			await Promise.all(
				detail.artifacts.map(async (artifact) => {
					artifactContents.set(
						artifact.id,
						await this.downloadArtifact(artifact.id, options.signal)
					);
				})
			);
		}
		return { jobs: [job], artifacts: detail.artifacts, artifactContents };
	}

	async run(draft: ScientificRunDraft, options: RunOptions = {}): Promise<ScientificRunResult> {
		const deadline = Date.now() + (options.timeoutMs ?? 3_600_000);
		const preview = await this.preview(draft, options.signal);
		if ((await options.approve?.(preview)) === false) {
			throw new AdmissionError(
				'The caller rejected the server-authored preview.',
				'PREVIEW_REJECTED'
			);
		}
		if (preview.approval_required) {
			throw new ApprovalRequiredError(
				"This preview requires the platform's digest-bound approval workflow.",
				'APPROVAL_REQUIRED',
				409,
				false,
				{ preview }
			);
		}
		if (!preview.preview_receipt) {
			throw new AdmissionError(
				'The server preview did not include the required signed receipt.',
				'PREVIEW_RECEIPT_REQUIRED'
			);
		}
		const idempotencyKey = options.idempotencyKey ?? randomId();
		const submission = await this.submitWithRetry(
			draft,
			preview.preview_digest,
			preview.preview_receipt,
			idempotencyKey,
			Math.max(1, options.submissionAttempts ?? 3),
			options.signal
		);
		await options.onSubmitted?.(submission);
		if (submission.jobs.length === 0) {
			throw new ScientificRunError(
				'Run submission did not return a durable Job.',
				'SUBMISSION_WITHOUT_JOB'
			);
		}
		const results = await Promise.all(
			submission.jobs.map((job) =>
				this.resume(job.id, {
					...options,
					timeoutMs: Math.max(0, deadline - Date.now())
				})
			)
		);
		return {
			preview,
			submission,
			jobs: results.flatMap((result) => result.jobs),
			artifacts: results.flatMap((result) => result.artifacts),
			artifactContents: new Map(results.flatMap((result) => [...result.artifactContents.entries()]))
		};
	}
}
