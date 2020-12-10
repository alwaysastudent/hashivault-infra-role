import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('vault_infra')


@pytest.mark.parametrize("capabilities,path",[
  (["read"], "identity/entity/name/viewer"),
  (["read"], "sys/health"),
])
@pytest.mark.parametrize("vault", ["viewer@vault_infra"], indirect=True)
def test_viewer_good_results(host, vault, capabilities, path):
  for capability in capabilities:
    if capability == "read":
      result = vault.read(path)
      assert vault.can_read(path)
    else:
      result = vault.list(path)
      assert vault.can_list(path)

    assert result.rc == 0
    assert len(result.stderr) == 0
    assert len(result.errors) == 0


@pytest.mark.parametrize("capabilities,path", [
  (["list", "read"], "sys"),
])
@pytest.mark.parametrize("vault", ["viewer@vault_infra"], indirect=True)
def test_viewer_bad_results(host, vault, path, capabilities):
  for capability in capabilities:
    if capability == "read":
      result = vault.read(path)
      assert not vault.can_read(path)
    else:
      result = vault.list(path)
      assert not vault.can_list(path)

    assert result.rc == 1
    assert "permission denied" in result.stderr
    assert len(result.errors) == 1


@pytest.mark.parametrize("vault", ["viewer@vault_infra"], indirect=True)
def test_viewer_result(host, vault):
  result = vault.read("identity/entity/name/viewer")
  assert result.rc == 0
  data = result.output['data']
  assert data['disabled'] == False
  assert data['name'] == 'viewer'
  assert data['namespace_id'] == 'root'
  assert data['aliases'][0]['name'] == 'viewer'
