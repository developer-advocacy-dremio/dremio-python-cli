# Reflection Management

Manage Dremio reflections (Software and Cloud).

## Commands

### List Reflections

List all reflections.

```bash
alt-dremio-cli reflection list [OPTIONS]
```

**Options:**
- `--summary` - Show summary only

**Examples:**
```bash
alt-dremio-cli reflection list
alt-dremio-cli --output json reflection list
```

### Get Reflection

Get details of a specific reflection.

```bash
alt-dremio-cli reflection get <REFLECTION_ID>
```

**Examples:**
```bash
alt-dremio-cli reflection get abc-123-def-456
alt-dremio-cli reflection get abc-123-def-456 --output yaml
```

### Create Reflection

Create a reflection using a JSON definition.

```bash
alt-dremio-cli reflection create [OPTIONS]
```

**Options:**
- `--file PATH` - Path to JSON file containing reflection definition
- `--json STRING` - JSON string containing reflection definition

**Examples:**
```bash
# From file
alt-dremio-cli reflection create --file reflection_def.json

# From JSON string
alt-dremio-cli reflection create --json '{"name": "my_reflection", "datasetId": "...", "type": "RAW", ...}'
```

**Reflection Definition Format:**
Refer to Dremio API documentation for the full reflection object structure.

### Update Reflection

Update an existing reflection.

```bash
alt-dremio-cli reflection update <REFLECTION_ID> [OPTIONS]
```

**Options:**
- `--file PATH` - Path to JSON file containing updated reflection definition
- `--json STRING` - JSON string containing updated reflection definition

**Examples:**
```bash
alt-dremio-cli reflection update abc-123 --file update.json
```

### Delete Reflection

Delete a reflection.

```bash
alt-dremio-cli reflection delete <REFLECTION_ID>
```

**Examples:**
```bash
alt-dremio-cli reflection delete abc-123
```
