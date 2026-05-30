# Hermes skill packs (sr-plugins)

Optional skill packs for [Hermes Agent](https://github.com/NousResearch/hermes-agent), installable under `~/.hermes/skills/`.

> **Not investment advice.** The investing pack produces research aids only. See [DISCLAIMER.md](../DISCLAIMER.md).

## Packs

| Directory | Purpose |
| --------- | ------- |
| [`investing/`](./investing/) | Phase 1 fundamental analysis for NSE equities (orchestrator + sub-skills + PDF scripts) |
| [`build/`](./build/) | Generic idea-to-production BUILD pipeline (PRD → HLD → LLD → Kanban → PR → deploy) |

## Install

```bash
git clone https://github.com/sr-codefreak/sr-plugins.git
cd sr-plugins

# Investing FA skills + PDF tools
rsync -a hermes-skills/investing/ ~/.hermes/skills/investing/

# BUILD pipeline (optional)
rsync -a hermes-skills/build/ ~/.hermes/skills/build/
```

Restart Hermes or start a new session so skills reload.

### BUILD specialist profiles

If you use dedicated BUILD profiles (`buildprd`, `buildhld`, etc.), mirror the build pack into each profile:

```bash
for p in buildprd buildhld buildlld buildcoder buildtester builddeployer; do
  rsync -a hermes-skills/build/ ~/.hermes/profiles/$p/skills/build/
done
```

## Claude Code / Cowork

For Claude Code plugins (same methodology, different layout), use [`fa-plugin/`](../fa-plugin/) instead.

## License

MIT — see [LICENSE](../LICENSE).
