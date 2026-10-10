# Phone intake: ElevenLabs voice agent on a Twilio number

Tenants can phone in a maintenance problem. An ElevenLabs voice agent answers the Twilio number, collects the details, reads a summary back and, once the caller says yes, sends it to Property Desk. From there the report follows the same path as a confirmed tenant-portal report: `Service.intake` stores it, the native case coordinator wakes, Claude triage routes it, and the policy engine and staff decide what happens next.

```
caller ─► Twilio number ─► ElevenLabs agent (questions, read-back, "is that correct?")
                               │ caller says yes
                               ├─► POST /api/voice/report    ─► Service.intake ─► wake(case) ─► Claude triage, policy, staff
                               │      returns a reference read out to the caller
                               └─► POST /api/voice/post-call  (after hang-up, HMAC-signed)
                                      transcript attached to the case, or kept as an unconfirmed call
```

## What the agent asks

The prompt is in [`voice/agent_prompt.md`](../voice/agent_prompt.md). Its questions come from what staff repeatedly had to chase in the BUILD cases:

- **Required:** name, full address with flat number and postcode (read back letter by letter), and each problem kept separate.
- **For each problem:** what and where, since when, whether it is getting worse, appliance make or error code, and what the caller already tried. Trying a plunger or cleaning a filter changes who handles the job.
- **Then:** availability, whether a contractor may contact them directly, access notes (pets, alarm, keys), and whether they have photos.
- **Safety first:** for a gas smell, 999 situations, water near electrics or flooding, the agent gives the safety step, then still sends a short report with the `danger` field filled so a person sees it.
- **Never:** promises a visit, time, cost or approval; says who pays; invents a reference; claims something was logged unless the tool returned a reference.

## Trust boundary

- Everything from a call is an **unverified statement**. The case is created by the `phone-voice-bridge` actor with `property_ref = "Unverified address: …"`. Identity and contact route still need staff review, exactly as for the portal.
- `POST /api/voice/report` requires the `X-Voice-Tool-Secret` header (`VOICE_TOOL_SECRET`). The check runs before body validation and returns 503 if the secret is not configured. `caller_confirmed: false` is refused with 422.
- `POST /api/voice/post-call` requires a valid `ElevenLabs-Signature` (`t=…,v0=HMAC-SHA256(secret, "t.body")`, 30-minute window).
- One case per call: the idempotency key is `phone-call:{conversation_id}`. A retried tool call returns the same reference. A *different* read-back on the same call is added to that case as a correction.
- The transcript is stored as `triage: not_required` evidence, so it does not trigger a second triage or split.
- **Tunnel guard:** in demo mode, any request carrying `X-Forwarded-*` / `Forwarded` headers (for example via ngrok) can reach only the two webhook paths. The loopback-only staff and tenant demo sessions are not exposed.
- Staff can list calls, including unconfirmed ones, at `GET /api/voice/calls` (case manager).

## Run it (hackathon setup)

1. Put secrets in the git-ignored `.env.local`: `ANTHROPIC_API_KEY` (for triage) and optionally `ELEVENLABS_API_KEY`. `voice/sync.py` creates `VOICE_TOOL_SECRET` and, when permitted, `ELEVENLABS_WEBHOOK_SECRET`.
2. Start the app on port 8027, using the README's native local command.
3. `ngrok http 8027`
4. `.venv/bin/python voice/sync.py` reads the ngrok URL and creates or updates the ElevenLabs secret, tool, post-call webhook and agent. Add `--phone-number-id phnum_…` to route an imported Twilio number to the agent. Re-run whenever the ngrok URL changes, and restart the app if it reports a new webhook secret.
5. Ring the number. The case appears in the staff view with the reference's first six characters.

Non-secret IDs are kept in `voice/elevenlabs/ids.json`. The agent config is in `voice/elevenlabs/agent_configs/` and the tool config in `voice/elevenlabs/tool_configs/`. Model: `claude-sonnet-5` inside ElevenLabs. Voice: Alice (British). Audio recording is off and transcripts are kept for 30 days in ElevenLabs.

## Verification so far

- `tests/test_voice.py` (offline): one case per call, retries, corrections, secret and confirmation checks, signed or forged/stale/tampered webhooks, transcript attached once without re-triage, unconfirmed calls, tunnel guard, unconfigured server.
- ElevenLabs `simulate_conversation` against the real agent, with a simulated caller built from case 027's **initial request only**. The simulator mocks tools, so these runs check conversation behaviour:
  - full report with postcode read-back;
  - gas-smell safety flow followed by a short report;
  - tool error leading to an apology with no reference.
  - An early run showed the agent inventing a reference when the tool result had none. The prompt was tightened, and later runs gave no invented reference.
- Real HTTP path: the agent's exact tool arguments were replayed through ngrok. The case was created, Claude triage ran in the native workflow (plumbing, request quote) and the policy held it for identity and route review.

**Not yet verified:** a real phone call through Twilio, and the post-call webhook from ElevenLabs. The available ElevenLabs credentials lack `webhooks_write`, so the webhook could not be created and transcripts are not attached yet. Enable that permission on the API key, or create the webhook in the ElevenLabs dashboard, then re-run `voice/sync.py`.
