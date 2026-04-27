---
name: obsidian
description: Read, search, and create notes in the Obsidian vault.
metadata:
  worker_bee:
    imported_from: hermes-agent
    available_to: [QueenB, Scout, Builder, Watcher]
    routing_context: "Available via skill library - models can request when relevant"
---
## Worker Bee Context

**Integration:** This skill is available to all Worker Bee models via the skill library.

**Orchestration:** 
- QueenB can route tasks to this skill when keywords/context match
- Scout can use when planning requires this capability
- Builder can reference when implementing related features
- Watcher can apply when validating this type of work

**Status emissions:** Models should emit `[MODEL:SKILL_ACTIVE]` when using, `[MODEL:SKILL_COMPLETE]` when done.

---


# Obsidian Vault

**Location:** Set via `OBSIDIAN_VAULT_PATH` environment variable (e.g. in `~/.hermes/.env`).

If unset, defaults to `~/Documents/Obsidian Vault`.

Note: Vault paths may contain spaces - always quote them.

## Read a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
cat "$VAULT/Note Name.md"
```

## List notes

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# All notes
find "$VAULT" -name "*.md" -type f

# In a specific folder
ls "$VAULT/Subfolder/"
```

## Search

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# By filename
find "$VAULT" -name "*.md" -iname "*keyword*"

# By content
grep -rli "keyword" "$VAULT" --include="*.md"
```

## Create a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
cat > "$VAULT/New Note.md" << 'ENDNOTE'
# Title

Content here.
ENDNOTE
```

## Append to a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
echo "
New content here." >> "$VAULT/Existing Note.md"
```

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.
