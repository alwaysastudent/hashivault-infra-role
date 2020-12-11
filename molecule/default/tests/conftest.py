import os
import pytest
import hvac
from hvac.exceptions import VaultError
import testinfra.utils.ansible_runner

vault_runner = testinfra.utils.ansible_runner.AnsibleRunner(os.environ['MOLECULE_INVENTORY_FILE'])

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
  def __init__(self, url):
    self.client = hvac.Client(url=url)

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


# supplies a VaultSession to the test fixture, expecting url in the request.param
@pytest.fixture(scope="module")
def vault(request):
  return VaultSession(request.param)
