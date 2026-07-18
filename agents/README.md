# Agents — declarations only, no agent without one

Rule: an agent exists here only when its declaration file exists (mission, allowed
paths, read/write boundaries, stop conditions, evidence standard — the PRODUCTION
`AGENT_TEMPLATE.md` pattern). Build order: **read-only intelligence agents first;
anything that writes — last, and gated.**

## Planned (declarations to be authored at Phase 4)

| Agent | Role | Writes? |
|---|---|---|
| `sales-architect` | guards this repo's constitution; routes work | repo docs only |
| `account-intel` | runs recipes, builds evidence snapshots, answers account questions | evidence/ only |
| `retention-radar` | scheduled sleeping-radar runs + needs-check briefs | evidence/ + brief delivery |
| `brief-composer` | weekly "six things" + 5–9 KPIs (daily-ops-guardian mold) | brief delivery only |
| `outreach-drafter` | drafts (never sends) win-back / dream-100 touches | drafts only; sending gated by frozen flag |

Phase 4 does not start until Phases 2–3 close (CURRENT_STATE ladder).
