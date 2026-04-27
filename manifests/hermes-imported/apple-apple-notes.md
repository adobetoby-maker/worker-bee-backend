---
name: apple-notes
description: Manage Apple Notes via the memo CLI on macOS (create, view, search, edit).
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  worker_bee:
    imported_from: hermes-agent
    available_to: [QueenB, Scout, Builder, Watcher]
    routing_context: "Available via skill library - models can request when relevant"
  hermes:
    tags: [Notes, Apple, macOS, note-taking]
    related_skills: [obsidian]
prerequisites:
  commands: [memo]
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


# Apple Notes

Use `memo` to manage Apple Notes directly from the terminal. Notes sync across all Apple devices via iCloud.

## Prerequisites

- **macOS** with Notes.app
- Install: `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`
- Grant Automation access to Notes.app when prompted (System Settings → Privacy → Automation)

## When to Use

- User asks to create, view, or search Apple Notes
- Saving information to Notes.app for cross-device access
- Organizing notes into folders
- Exporting notes to Markdown/HTML

## When NOT to Use

- Obsidian vault management → use the `obsidian` skill
- Bear Notes → separate app (not supported here)
- Quick agent-only notes → use the `memory` tool instead

## Quick Reference

### View Notes

```bash
memo notes                        # List all notes
memo notes -f "Folder Name"       # Filter by folder
memo notes -s "query"             # Search notes (fuzzy)
```

### Create Notes

```bash
memo notes -a                     # Interactive editor
memo notes -a "Note Title"        # Quick add with title
```

### Edit Notes

```bash
memo notes -e                     # Interactive selection to edit
```

### Delete Notes

```bash
memo notes -d                     # Interactive selection to delete
```

### Move Notes

```bash
memo notes -m                     # Move note to folder (interactive)
```

### Export Notes

```bash
memo notes -ex                    # Export to HTML/Markdown
```

## Limitations

- Cannot edit notes containing images or attachments
- Interactive prompts require terminal access (use pty=true if needed)
- macOS only — requires Apple Notes.app

## Rules

1. Prefer Apple Notes when user wants cross-device sync (iPhone/iPad/Mac)
2. Use the `memory` tool for agent-internal notes that don't need to sync
3. Use the `obsidian` skill for Markdown-native knowledge management
