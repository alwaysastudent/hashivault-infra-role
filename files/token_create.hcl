#This policy is meant to give someone the capability to create new Vault tokens
path "auth/*"
{
  capabilities = ["create", "update"]
}