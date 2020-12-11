import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('vault_k8s')

vault_host_ip = os.getenv('VAULT_ADDR', '127.0.0.1')

@pytest.mark.parametrize("vault", [f"http://{vault_host_ip}:8201"], indirect=True)
def test_autounseal(host, vault):
  assert vault.is_initialized()
  assert not vault.is_sealed()
