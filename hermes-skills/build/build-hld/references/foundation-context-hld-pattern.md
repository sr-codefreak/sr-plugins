# Foundation / context HLD pattern

Reference for BUILD HLD work when the approved PRD is primarily a foundation or context setup rather than feature implementation.

## Pattern

1. Record PRD approval first.
   - Update `01-prd.md` status to `Approved`.
   - Add approver, date, next phase, and decision-log entry.

2. Run RUFLO-compatible reviewers before drafting final HLD.
   - Architecture/options reviewer.
   - Risk/security reviewer.
   - Requirement coverage validator.

3. Draft HLD and ADRs.
   - `02-hld.md` should include current/proposed architecture, diagrams, options, accepted/rejected flows, ADR list, requirement coverage matrix, risks, and validation result.
   - Create separate ADR markdown files for each major decision.

4. Re-run/perform validation after the HLD exists.
   - A validator invoked before `02-hld.md` exists may correctly fail with “HLD missing.” This is not a final HLD failure; it means draft first, then validate.

5. Create a user-review artifact.
   - Generate a DOCX via `pandoc` when available:
     `pandoc 02-hld.md -o <slug>-HLD-for-approval.docx --metadata title="<title> HLD"`
   - On Telegram, deliver with a standalone `MEDIA:/absolute/path/to/file.docx` line.

## Decisions captured in this session

Useful HLD decisions for MCP/code-context foundation work:

- Preserve existing multi-repo architecture if PRD does not require repo restructuring.
- Use MCP as the primary context interface for Hermes BUILD agents.
- Treat code graph MCP as best-effort, not authoritative.
- Treat generated OpenAPI as a draft planning contract; validate schemas during LLD before contract-changing implementation.
- Use Hermes `delegate_task` for HLD/LLD reviews when native RUFLO is unavailable.
- Create Hermes Kanban implementation tasks only after approved LLD.

## Risks to remember

- Filesystem MCP scope should stay bounded to the project workspace, not `$HOME` or `/`.
- Inline secrets do not belong in MCP config; future credentials should use env/secret storage with explicit approval.
- `npx ...@latest` MCP commands are convenient but should be pinned during hardening/LLD if reproducibility matters.
- OpenAPI MCP mutating tools should be treated as schema exploration by default; require explicit user approval before mutating a live backend.
