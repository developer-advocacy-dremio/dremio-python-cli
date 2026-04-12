# Quick Start Guide

## 1. Create Your First Profile

### For Dremio Cloud

```bash
alt-dremio-cli profile create production \
  --type cloud \
  --base-url https://api.dremio.cloud/v0 \
  --project-id your-project-id \
  --auth-type pat \
  --token your-personal-access-token
```

### For Dremio Software

```bash
alt-dremio-cli profile create local \
  --type software \
  --base-url http://localhost:9047/api/v3 \
  --auth-type username_password \
  --username alt-dremio-cli \
  --password dremio123
```

## 2. Verify Your Profile

```bash
# List all profiles
alt-dremio-cli profile list

# Show current profile
alt-dremio-cli profile current
```

## 3. Run Your First Commands

### List Catalog

```bash
alt-dremio-cli catalog list
```

### Execute SQL

```bash
alt-dremio-cli sql execute "SELECT * FROM MySource.MyTable LIMIT 10"
```

### List Sources

```bash
alt-dremio-cli source list
```

## 4. Try Interactive Mode

```bash
alt-dremio-cli repl
```

In REPL mode, you can run commands without the `dremio` prefix:

```
dremio> catalog list
dremio> sql execute "SELECT COUNT(*) FROM MyTable"
dremio> exit
```

## 5. Explore More Commands

```bash
# Get help for any command
alt-dremio-cli --help
alt-dremio-cli catalog --help
alt-dremio-cli source --help

# Use different output formats
alt-dremio-cli catalog list --output json
alt-dremio-cli catalog list --output yaml
```

## Next Steps

- Browse the [Command Reference](commands/) for detailed documentation
- Check out [Examples](examples/) for common use cases
- Learn about [Profile Management](commands/profile.md)
