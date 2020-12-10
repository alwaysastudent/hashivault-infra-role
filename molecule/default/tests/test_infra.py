import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('vault_infra')


@pytest.mark.parametrize("vault", ["svccps2npo@vault_infra"], indirect=True)
def test_autounseal(host, vault):
  assert vault.is_initialized()
  assert not vault.is_sealed()
