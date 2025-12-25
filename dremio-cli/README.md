# Dremio CLI

A comprehensive command-line interface for Dremio Cloud and Dremio Software.

## Features

- 🚀 **Dual Mode Operation**: Command-based and interactive REPL modes
- 🔐 **Multi-Profile Support**: Manage multiple Dremio environments seamlessly
- 🌐 **Universal Coverage**: Works with both Dremio Cloud and Dremio Software
- 📊 **Rich Output**: Beautiful terminal output with multiple format options (table, JSON, YAML)
- 🔄 **Complete API Coverage**: All REST API operations supported

## Quick Start

### Installation

```bash
pip install dremio-cli
```

### Create Your First Profile

```bash
dremio profile create production \
  --type cloud \
  --base-url https://api.dremio.cloud/v0 \
  --project-id your-project-id \
  --auth-type pat \
  --token your-personal-access-token
```

### Run Your First Command

```bash
# List catalog
dremio catalog list

# Execute SQL
dremio sql execute "SELECT * FROM MySource.MyTable LIMIT 10"

# Start interactive mode
dremio repl
```

## Documentation

- [Installation Guide](docs/installation.md)
- [Quick Start Guide](docs/quickstart.md)
- [Command Reference](docs/commands/)
- [Examples](docs/examples/)

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/your-org/dremio-cli/issues)
- 💬 [Discussions](https://github.com/your-org/dremio-cli/discussions)
