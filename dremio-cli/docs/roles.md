# Role Management

This guide covers role management operations for administering roles and role memberships in Dremio.

## Overview

**Role Management** allows administrators to create roles, assign users to roles, and manage role-based access control. This is primarily available in Dremio Software.

## Commands

### List Roles

```bash
alt-dremio-cli role list
```

### Get Role

```bash
alt-dremio-cli role get <ROLE_ID>
```

### Create Role

```bash
alt-dremio-cli role create --name "Analyst"
alt-dremio-cli role create --from-file role.json
```

### Update Role

```bash
alt-dremio-cli role update <ROLE_ID> --from-file updated_role.json
```

### Delete Role

```bash
alt-dremio-cli role delete <ROLE_ID>
```

### Add Member

```bash
alt-dremio-cli role add-member <ROLE_ID> --user <USER_ID>
```

### Remove Member

```bash
alt-dremio-cli role remove-member <ROLE_ID> --user <USER_ID>
```

## Examples

```bash
# List all roles
alt-dremio-cli role list

# Create role
alt-dremio-cli role create --name "Data Analyst"

# Add user to role
alt-dremio-cli role add-member role-123 --user user-456

# Remove user from role
alt-dremio-cli role remove-member role-123 --user user-456

# Delete role
alt-dremio-cli role delete role-123
```

## Role File Format

```json
{
  "name": "Data Analyst",
  "description": "Analysts with read access to datasets"
}
```

## Workflows

### Role-Based Access Control

```bash
# 1. Create roles
alt-dremio-cli role create --name "Analyst"
alt-dremio-cli role create --name "Engineer"

# 2. Add users to roles
alt-dremio-cli role add-member analyst-role-id --user user-1
alt-dremio-cli role add-member engineer-role-id --user user-2

# 3. Grant permissions to roles
alt-dremio-cli grant add dataset-id --grantee-type ROLE --grantee-id analyst-role-id --privileges SELECT
alt-dremio-cli grant add dataset-id --grantee-type ROLE --grantee-id engineer-role-id --privileges SELECT,ALTER,MODIFY
```

## Notes

- Role management requires administrative privileges
- Primarily available in Dremio Software
- Cloud has different role management (via cloud console)
- Use roles with grant management for access control
