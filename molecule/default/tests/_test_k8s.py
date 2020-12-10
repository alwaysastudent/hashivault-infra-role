import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('vault_k8s')


@pytest.mark.parametrize("vault", ["vault_k8s"], indirect=True)
def test_autounseal(host, vault):
  assert vault.is_initialized()
  assert not vault.is_sealed()