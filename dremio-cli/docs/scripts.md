# Script Management

Manage Dremio scripts (Cloud Only).

## Commands

### List Scripts

List scripts.

```bash
alt-dremio-cli script list [OPTIONS]
```

**Options:**
- `--limit INT` - Number of results to return (default: 25)
- `--offset INT` - Offset for pagination (default: 0)

**Examples:**
```bash
alt-dremio-cli script list
alt-dremio-cli script list --limit 10
```

### Get Script

Get details and content of a specific script.

```bash
alt-dremio-cli script get <SCRIPT_ID>
```

**Examples:**
```bash
alt-dremio-cli script get abc-123-def-456
```

### Create Script

Create a new script.

```bash
alt-dremio-cli script create [OPTIONS]
```

**Options:**
- `--name TEXT` - Name of the script (Required)
- `--content TEXT` - SQL content of the script (Required)
- `--context TEXT` - Context for the script (e.g., "Space.Folder")

**Examples:**
```bash
alt-dremio-cli script create --name "Monthly Report" --content "SELECT * FROM sales"
alt-dremio-cli script create --name "Analysis" --content "SELECT 1" --context "Marketing"
```

### Update Script

Update an existing script.

```bash
alt-dremio-cli script update <SCRIPT_ID> [OPTIONS]
```

**Options:**
- `--name TEXT` - Name of the script (Required)
- `--content TEXT` - SQL content of the script (Required)
- `--context TEXT` - Context for the script

**Examples:**
```bash
alt-dremio-cli script update abc-123 --name "Updated Report" --content "SELECT * FROM new_sales"
```

### Delete Script

Delete a script.

```bash
alt-dremio-cli script delete <SCRIPT_ID>
```

**Examples:**
```bash
alt-dremio-cli script delete abc-123
```
