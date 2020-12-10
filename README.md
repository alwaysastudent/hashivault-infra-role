# hashicorp-infra-role rol

Deze rol managed een hashicorp-vault instantie.

1. beheer policies
2. beheer configuratie

De volgende parameters moeten worden meegegeven:

* `vault_root_token`  
  Token met admin rechten om policies en andere tokens te kunnen aanmaken.

## RACI Matrix

| Vaults            | Owner        | Users         |
| ----------------- | ------------ | ------------- |
| Infra vault       | Windows Team | IAM           |
| Downstream vaults | Aanvrager    | Product Teams |

| Procedure                       | Windows Team | IAM | AMS | Aanvrager | Product Teams |
| ------------------------------- |:------------:|:---:|:---:|:---------:|:-------------:|
| Unseal infra vault              | RAI          | ACI |     |           |               |
| Unseal downstream vault         |              | ACI | C   | RAI       | I             |
| Infra vault configuration       |              | RAI | C   |           |               |
| Downstream vaults configuration |              | AC  | C   | RAI       | I             |

# Development

Dependencies:

* make
* docker
* python

Om op de hashicorp-infra-role te ontwikkelen, zijn er verschillende stappen die genomen moeten worden.

1. Schrijf een pytest
2. Ontwikkel de ansible tasks
3. Draai de molecule test lokaal.

### 1. Schrijf een pytest

De eerste stap is testen schrijven, zodat dit reflecteerd wat je zou willen.  
Deze testen zijn te vinden in deze repo, onder: `molecule/default/tests`  
Voorbeelden zijn te vinden in `test_default.py`  
Gebruik een nieuw test bestand: test_<screnario>.py

Hiervoor wordt `test-infra` gebruikt in combinatie met de hvac python module.

* https://testinfra.readthedocs.io/en/latest/modules.html#
* https://hvac.readthedocs.io/en/stable/usage/index.html

De volgende parameter moet meegegeven worden om de user context te bepalen:

```
@pytest.mark.parametrize("vault", ["viewer"], indirect=True)
def test_iets(vault):
  vault.read('sys')
```

* `vault`  
  Dit is de variabele die je meegeeft.
* `["viewer"]`  
  Een lijst met gebruikers, waaronder de test moet draaien.  
  De gebruikers zijn terug te vinden in `conftest.py`

### Ontwikkel de ansible tasks

De modules die gebruikt kunnen worden zijn van terryhowe.

* https://terryhowe.github.io/ansible-modules-hashivault/modules/list_of_hashivault_modules.html

### Draai de molecule test lokaal.

Voordat een converge gestart kan worden moet er een proxy worden toegevoegd aan de client van docker.  
https://docs.docker.com/network/proxy/#configure-the-docker-client

Om ontwikkeling te versoepelen is er een Makefile toegevoegd.  
Dit voegt de volgende commando's toe vanuit de root van de git repo.

* `make help`  
  Overview van ondersteunende commando's.
* `make create`  
  Aanmaken van de vault container.
* `make destroy`  
  Afbreken van de vault container.
* `make converge`  
  De ansible tasks afspelen tegen de container.
* `make verify`  
  De pytesten afsprelen tegen de container.
* `make test`  
  Loopt een volledige cycles af van een ansible role.  
  Dit is ook de task succesvol moet lopen, voordat er een merge request geaccepteerd mag worden.

## Debug vault container

Stappen om in de container de vault cli te gebruiken.  
Deze container wordt gemaakt tijdens de `make create` stap.

```
docker exec -it vault_infra /bin/sh
export VAULT_ADDR=http://127.0.0.1:8200
cat /etc/ansible/facts.d/secrets.fact  # Hier vind je `vault_root_token`
export VAULT_TOKEN="${vault_root_token}"
vault read identity/entity/name/viewer
```
