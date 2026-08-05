# Provenance — `journey-mapping`

| | |
|---|---|
| Source | MCPmarket plugin `mcpmarket-me` v0.1.0 (`github.com/knoxgraeme/mcpmarket-plugin`, MIT) |
| Added | 2026-08-04, at Tom's request |
| Authority grade | **`inferred`** — third-party generic template. **Never policy** (truth rule 1). |
| Freshness | `stable` (external content; it does not track GT) |
| GT-specific content | none |

## How it got here

Extracted verbatim from the vendor's install script. **The installer itself was not run** — it also
registers a Claude Code plugin with a `SessionStart` sync hook, a `PostToolUse` skill-telemetry hook that
reports skill usage off-machine, and an MCP server entry holding a bearer token in plaintext. None of that
is needed to use the skill text, and installing it sits against D-004 (no framework layer with auto-hooks
and unrequested MCP servers).

`SKILL.md` is byte-identical to the vendor's file, frontmatter included, so it stays swappable if the
upstream version changes.

## Honest assessment

This is a generic facilitation framework — five phases, three template names, three tips. It contains no
GT data, calls no tools, and knows nothing about beverages, HoReCa, or this business.

**`doctrine/customer-journey.md` is strictly stronger for GT's actual journey** — it names real stages,
real owners, real artifacts and seven verified frictions. Keep this file for what it is good at: a checklist
when facilitating a *workshop* with other people, where a neutral outside structure helps. It should never
override the doctrine.

## Structural note (needs Tom)

`CLAUDE.md` §Repo map does not list a `skills/` directory. Tom is the sole writer of that file — the map
needs a one-line addition, or this directory should move under an existing one.
