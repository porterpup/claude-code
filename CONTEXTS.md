# Contexts — Quick Reference

Three contexts, one Chief of Staff. See `.claude/contexts/README.md` for the full architecture.

## Check current context

```bash
cat .claude/current-context          # or: ./scripts/context-path.sh
```

## Switch context

```bash
./scripts/switch-context.sh personal
./scripts/switch-context.sh 3cv
./scripts/switch-context.sh grantdrive
```

This copies `.mcp.[context].json` → `.mcp.json` and updates the marker.
**Restart Claude Code** for the MCP change to take effect.

## Sync work data into personal master

Run only on the personal master (main branch):

```bash
./scripts/sync-contexts.sh
```

This fetches `context/3cv` and `context/grantdrive` branches and merges their
data trees into `main`.

## Branches

| Branch | Purpose | Has |
|--------|---------|-----|
| `main` | Personal master | Everything |
| `context/3cv` | 3CV work instance | `skills/` + `contexts/3cv/` |
| `context/grantdrive` | Grant Drive instance | `skills/` + `contexts/grantdrive/` |

## Setup a new context (on its machine/environment)

1. Clone the repo
2. `git checkout context/3cv` (or `context/grantdrive`)
3. `./scripts/switch-context.sh 3cv` (or `grantdrive`)
   - On first run, this creates `.mcp.3cv.json` from the committed template and exits.
4. Edit the created `.mcp.3cv.json` (or `.mcp.grantdrive.json`) with real credentials.
5. Run `./scripts/switch-context.sh 3cv` again to activate.
6. Start using Claude Code normally — data writes go to `contexts/[context]/`
7. `git push` regularly — personal master will pull via `sync-contexts.sh`

**Credentials never get committed:** `.mcp.personal.json`, `.mcp.3cv.json`, and
`.mcp.grantdrive.json` are gitignored. Only the `*.template` versions are in git.

## Data isolation

- Personal context never appears on `context/3cv` or `context/grantdrive` branches.
- Work contexts never see personal data.
- Personal master sees everything (by design — that's the single source of truth).
