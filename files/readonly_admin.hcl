#This policy is meant to grant an admin unlimited READONLY rights within Vault

#List and read audit devices
path "sys/audit/*"
{
    capabilities = ["list", "read"]
}

#List audit configurations
path "sys/config/auditing"
{
    capabilities = ["read","list"]
}
#List and read audit settings for a device
path "sys/config/auditing/*"
{
    capabilities = ["list", "read"]
}

# List and read auth backends broadly across Vault
path "auth/*"
{
  capabilities = ["list", "read"]
}

# List and read auth backends
path "sys/auth/*"
{
  capabilities = ["list", "read"]
}

path "sys/auth"
{
    capabilities = ["read"]
}

# List existing policies
path "sys/policies"
{
  capabilities = ["list", "read"]
}

# List and read ACL policies broadly across Vault
path "sys/policies/*"
{
  capabilities = ["list", "read"]
}

# List key/value secrets
path "secret/*"
{
  capabilities = ["list"]
}

# List and read secret backends broadly across Vault.
path "sys/mounts/*"
{
  capabilities = ["list", "read"]
}

# List and read entities, aliases, and groups
path "identity/*"
{
  capabilities = ["list", "read"]
}

# Read health checks
path "sys/health"
{
  capabilities = ["read", "sudo"]
}