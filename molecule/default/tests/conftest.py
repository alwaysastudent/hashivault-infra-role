import os
import pytest
import hvac
from hvac.exceptions import VaultError
import testinfra.utils.ansible_runner

vault_host_ports={}
vault_host_ports['vault_infra'] = 8200
vault_host_ports['vault_k8s'] = 8201

vault_runner = testinfra.utils.ansible_runner.AnsibleRunner(os.environ['MOLECULE_INVENTORY_FILE'])
vault_host_ips = {}
for host in vault_runner.get_hosts():
  vault_host = vault_runner.get_host(host)
  vault_host_ips[host] = vault_host.backend.run('hostname -i').stdout.rstrip('\n')

vault_host_ips['localhost'] = 'localhost'
vault_host_ips['127.0.0.1'] = '127.0.0.1'
vault_host_ips['VAULT_ADDR'] = os.getenv('VAULT_ADDR', '127.0.0.1')
os.environ['no_proxy'] = ",".join(vault_host_ips.values())

class VaultResult():

  def __init__(self):
    self.rc = -1
    self.output = {}
    self.errors = []
    self.stderr = ""
    self.stdout = ""

  @staticmethod
  def create_result(output):
    result = VaultResult()
    result.output = output
    result.stdout = str(output)
    result.rc = 0
    return result

  @staticmethod
  def create_error(output):
    result = VaultResult()
    result.errors = output.errors
    result.stderr = str(output)
    result.rc = 1
    return result


class VaultSession():
  def __init__(self, host, port=8200):
    self.client = hvac.Client(
      url=f"http://{host}:{port}"
    )

  def login(self, user, password):
    self.client.auth_userpass(user, password)

  def is_authenticated(self):
    return self.client.is_autthenticated()

  def is_sealed(self):
    return self.client.sys.is_sealed()

  def is_initialized(self):
    return self.client.sys.is_initialized()

  def can_create_or_update_secret(self, path, secret):
    return self.create_or_update_secret(path, secret).rc == 0

  def can_delete(self, path):
    return self.delete(path).rc == 0

  def can_read(self, path):
    return self.read(path).rc == 0

  def can_list(self, path):
    return self.list(path).rc == 0

  def create_or_update_secret(self, path, secret):
    try:
      output = self.client.secrets.kv.v1.create_or_update_secret(
        path=path,
        secret=secret,
        mount_point="",
      )
      return VaultResult.create_result(output)
    except VaultError as output:
      return VaultResult.create_error(output)
	
  def delete(self, path):
    try:
      output = self.client.secrets.kv.v1.delete_secret(
        path=path,
        mount_point="",
      )
      return VaultResult.create_result(output)
    except VaultError as output:
      return VaultResult.create_error(output)

  def read(self, path):
    try:
      output = self.client.secrets.kv.v1.read_secret(
        path=path,
        mount_point="",
      )
      return VaultResult.create_result(output)
    except VaultError as output:
      return VaultResult.create_error(output)

  def list(self, path):
    try:
      output = self.client.secrets.kv.v1.read_secret(
        path=path,
        mount_point=""
      )
      return VaultResult.create_result(output)
    except VaultError as output:
      return VaultResult.create_error(output)


@pytest.fixture(
  scope="module"
)
def vault(request):
  user = "none"
  host = request.param
  if '@' in host:
    user = request.param.split('@')[0]
    host = request.param.split('@')[1]

  if not host in vault_host_ips.keys():
    raise ValueError(f'unsupported vault host: {host}')

  if not host in vault_host_ports.keys():
    raise ValueError(f'unsupported vault ip: {host}')

  session = VaultSession(vault_host_ips['VAULT_ADDR'], vault_host_ports[host])
  if user == "none":
    pass
  elif user == "viewer":
    session.login("viewer", "password")
  elif user == "svccps2npo":
    session.login("svccps2npo", "password")
  else:
    raise ValueError(f'unsupported vault account: {account}')

  return session