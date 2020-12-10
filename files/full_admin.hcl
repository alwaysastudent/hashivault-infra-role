#This policy is meant to grant an admin almost unlimited rights within Vault

#Configure audit devices
path "sys/audit/*"
{
    capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

#List audit configurations
path "sys/config/auditing"
{
    capabilities = ["read","list"]
}
#Configure audit settings for a device
path "sys/config/auditing/*"
{
    capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Manage auth backends broadly across Vault
path "auth/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# List, create, update, and delete auth backends
path "sys/auth/*"
{
  capabilities = ["create", "read", "update", "delete", "sudo"]
}

path "sys/auth"
{
    capabilities = ["read"]
}

# List existing policies
path "sys/policies"
{
  capabilities = ["read"]
}

# Create and manage ACL policies broadly across Vault
path "sys/policies/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# List, create, update, and delete key/value secrets
# NO READ ACCESS TO SECRETS
path "secret/*"
{
  capabilities = ["create", "update", "delete", "list", "sudo"]
}

# Manage secret backends broadly across Vault.
path "sys/mounts/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Manage entities, aliases, and groups
path "identity/*"
{
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Read health checks
path "sys/health"
{
  capabilities = ["read", "sudo"]
}