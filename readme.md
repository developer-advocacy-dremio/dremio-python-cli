# Dremio CLI Project

This repository contains the Dremio Command Line Interface - a comprehensive CLI tool for managing Dremio Cloud and Dremio Software.

## 📚 Documentation

See the **[complete documentation](https://github.com/developer-advocacy-dremio/dremio-python-cli)** for detailed guides on all features.

## 📁 Project Structure

- **[dremio-cli/](./dremio-cli/)** - The Dremio CLI implementation
  - **[docs/](./dremio-cli/docs/)** - Complete documentation
  - **[dremio_cli/](./dremio-cli/dremio_cli/)** - Source code
  - **[tests/](./dremio-cli/tests/)** - Unit tests
  - **[scripts/](./dremio-cli/scripts/)** - Live test scripts

## 🚀 Quick Links

- **[CLI Documentation](./dremio-cli/docs/README.md)** - Complete user guide
- **[Dremio-as-Code Guide](./dremio-cli/docs/dac.md)** - GitOps for Dremio
- **[Installation Guide](./dremio-cli/docs/installation.md)** - Get started
- **[Main README](./dremio-cli/README.md)** - CLI overview

## 🎯 Features

The Dremio CLI provides **100% API coverage** with support for:

- ✅ Catalog Operations
- ✅ SQL Execution & Analysis
- ✅ Job Management
- ✅ Source Management
- ✅ View Management
- ✅ Space & Folder Management
- ✅ Tag & Wiki Management
- ✅ Grant & Permission Management
- ✅ User & Role Management
- [x] User & Role Management
- [x] Table Operations
- [x] Dremio-as-Code (GitOps)

## 📦 Installation

```bash
pip install alt-dremio-cli
```

## ⚡ Quick Start

```bash
# Configure profile
alt-dremio-cli profile create --name myprofile --type software \
  --base-url https://dremio.company.com \
  --username admin --password secret

# Execute SQL
alt-dremio-cli sql execute "SELECT * FROM customers LIMIT 10"

# List catalog
alt-dremio-cli catalog list
```

## 📚 Documentation

See the **[complete documentation](https://github.com/developer-advocacy-dremio/dremio-python-cli)** for detailed guides on all features.

## 🔗 Additional Resources

- [Dremio Documentation](https://docs.dremio.com)
- [Dremio Cloud](https://www.dremio.com/cloud/)
- [Dremio Software](https://www.dremio.com/platform/)
