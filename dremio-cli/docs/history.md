# Query History

View and manage your local query execution history.

## Commands

### List History

List recent query history.

```bash
alt-dremio-cli history list [OPTIONS]
```

**Options:**
- `--limit INT` - Maximum number of entries to show (Default: 50)

**Examples:**
```bash
alt-dremio-cli history list
alt-dremio-cli history list --limit 10
```

### Run History

Re-run a command from history.

```bash
alt-dremio-cli history run <HISTORY_ID>
```

**Examples:**
```bash
alt-dremio-cli history run 5
```

### Clear History

Clear all query history.

```bash
alt-dremio-cli history clear
```

**Examples:**
```bash
alt-dremio-cli history clear
```
