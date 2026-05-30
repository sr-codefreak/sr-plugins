# Async processing finalization pattern

Use this reference when fixing bugs where an entity is stuck in `processing`, `queued`, `uploading`, or another async handoff state.

## Durable invariant
A record must not be marked `processing` until both prerequisites are true:
1. The durable payload exists at a retrievable location, e.g. an uploaded audio file with a storage URL.
2. The downstream worker task/job has been successfully queued with enough identifiers to process that payload.

If either prerequisite fails, leave the record in its prior state or mark it `failed` with enough metadata/logging to recover. Never expose a public API that lets clients set `status=processing` directly without performing the durable upload + queue handoff.

## Implementation checklist
- Add a finalization endpoint/command that performs the whole state transition atomically from the product perspective:
  1. validate ownership and current state;
  2. accept or locate the final payload;
  3. upload/store it durably;
  4. discover required processing context, e.g. active requirements;
  5. publish the worker task;
  6. only then update status to `processing` and persist payload metadata.
- If queue publish fails after storage upload, mark the record `failed` or otherwise make it recoverable; do not leave it `processing`.
- Reject public status-only transitions into async processing states.
- Update alternate ingestion paths, e.g. WebSocket stop/finalize, to use the same publish-before-processing invariant.
- Add regression tests for:
  - successful finalization stores payload, queues task, and marks `processing`;
  - publish failure does not leave `processing`;
  - public status update to `processing` is rejected;
  - client stop flow calls finalization endpoint with the actual payload.
- Update API contract docs/OpenAPI when adding the finalization endpoint.

## CI/watchout
If full-project analyzers fail due to pre-existing warnings unrelated to the bug, still verify changed files cleanly and run tests. Do not silently ignore CI failures; either fix the CI policy deliberately in the PR or document the pre-existing failures with evidence.
