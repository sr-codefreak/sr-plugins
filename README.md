# sr-plugins

A small collection of [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
/ Cowork plugins for personal investing workflows. Each plugin lives in its
own folder and ships with the standard `.claude-plugin/plugin.json` so it
can be installed standalone.

> [!CAUTION]
> **Not investment advice. Read [DISCLAIMER.md](./DISCLAIMER.md) before use.**
> The plugins here drive an LLM to produce research notes; the output may be
> wrong, stale, or misleading. You are responsible for verifying everything
> against primary sources before acting on it.

## Plugins

| Plugin                       | What it does                                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| [`fa-plugin`](./fa-plugin/)  | Phase 1 fundamental analysis for NSE-listed stocks (Claude Code / Cowork plugin). |
| [`hermes-skills`](./hermes-skills/) | Same FA workflow + optional BUILD pipeline as Hermes Agent skills under `~/.hermes/skills/`. |

More may show up here over time (e.g. a technical-analysis plugin, an annual-report
extractor). Each is independent — install only what you want.

## Installing a plugin

### Claude Code

```bash
/plugin install https://github.com/sr-codefreak/sr-plugins/tree/main/fa-plugin
```

Or via the **marketplace** catalog ([`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json)):

```bash
/plugin marketplace add sr-codefreak/sr-plugins
/plugin install fa-plugin@sr-plugins
```

### Cowork

1. Open Cowork → **Customize** in the left sidebar.
2. **Add plugin** → paste the GitHub URL of the plugin folder.
3. Restart the session if prompted.

### Local install (for developing or modifying)

```bash
git clone https://github.com/sr-codefreak/sr-plugins.git
# In Claude Code:
/plugin install ./sr-plugins/fa-plugin
```

## Repository layout

```
sr-plugins/
├── README.md                # this file
├── DISCLAIMER.md            # legal / risk disclaimers — read before use
├── LICENSE                  # MIT
├── CONTRIBUTING.md          # how to propose changes
├── CODE_OF_CONDUCT.md       # community guidelines
├── .gitignore
├── .claude-plugin/
│   └── marketplace.json     # Claude Code marketplace catalog (lists fa-plugin)
├── fa-plugin/               # Claude Code / Cowork plugin
│   ├── skills/, agents/, scripts/
└── hermes-skills/           # Hermes Agent installable packs
    ├── investing/           # FA orchestrator + sub-skills + PDF scripts
    └── build/               # Generic BUILD pipeline (PRD → deploy)
```

## Development

These plugins are mostly Markdown (skills + agents + commands) plus a small
Python helper for PDF rendering. There is nothing to "build". To iterate
locally:

1. Edit a `SKILL.md` or `agent.md`.
2. Re-run the plugin in Claude Code / Cowork on a sample ticker.
3. Diff the output report.

For non-trivial methodology changes, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Costs

Running these plugins consumes LLM tokens via your own Claude / Cowork
subscription. A single end-to-end FA report typically uses a few hundred
thousand tokens (orchestrator + 8 parallel subagents + synthesis). Budget
accordingly; the plugin itself is free, the LLM calls are not.

## License

[MIT](./LICENSE) — © 2026 Sai Rajesh. See LICENSE for the full text and the
"AS IS, no warranty" clause.

## Disclaimer (short version)

Nothing produced by these plugins is investment, legal, tax, or accounting
advice. The author is not a SEBI-registered investment adviser. Outputs are
research aids only. **Verify independently. Use at your own risk.**

For the full disclaimer, see [DISCLAIMER.md](./DISCLAIMER.md).
