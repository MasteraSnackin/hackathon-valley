# Per-case audit trail

Every case has a readable trace of what happened: who decided (Jev, Claude, the policy engine, a named staff member or the workflow), which tool ran (TypeSafe `system_one`, the Anthropic `ai.*` calls, the simulated provider and messaging adapters) and why.

It is rendered by `app/audit.py` from the immutable `records` table, which stays the source of truth.

```
.audit/<case_id>/history.md     one numbered entry per step: actor, tool, decision, reason, quoted source
.audit/<case_id>/records.jsonl  every raw record for the case, in order
```

The markdown leaves out bookkeeping (outbox signals, cycle checkpoints, intake receipts) and shows a policy assessment only when its outcome or blockers changed. A claim shows whether it is verified, an unverified assertion or hearsay. Model entries show the model, token use and the workflow step.

## How it is produced

- **Local server:** written automatically after every committed transaction to `./.audit/` when the default SQLite store is used. Set `AUDIT_DIR=<path>` to choose the folder, or `AUDIT_DIR=off` to disable it. A write failure is logged and never fails the request.
- **Deployed (Vercel, or any explicit `DATABASE_URL`):** no files are written unless `AUDIT_DIR` is set. Use the API instead.
- **API:** `GET /api/cases/{id}/audit` returns the same markdown (staff session required).
- **CLI:** `uv run python -m app.audit [--case ID ...] [--out DIR]` exports every case, or the named ones.

`.audit/` is git-ignored and excluded from Vercel uploads: it can contain message text.
