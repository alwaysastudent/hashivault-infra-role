.DEFAULT_GOAL := help

# outcomment to echo commands
MAKEFLAGS += --silent

ACTION='test'
VAULT_IMAGE="vault:1.5.4"
MOLECULE_IMAGE="registry.kvk.nl/ams-ansible/molecule:stable"
VAULT_ADDR="$(shell ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127' | awk '{print $1}' | head -1)"

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: molecule
molecule:
	@echo >&2 "Vault address: ${VAULT_ADDR}"
	@echo >&2 "Pulling docker images ..."
	@docker pull "${VAULT_IMAGE}" >/dev/null
	@docker pull "${MOLECULE_IMAGE}" >/dev/null
	@docker container run \
	  --rm \
	  --tty \
	  --volume /var/run/docker.sock:/var/run/docker.sock \
	  --volume $(CURDIR):$(CURDIR):ro \
	  --env "VAULT_IMAGE=${VAULT_IMAGE}" \
		--env "VAULT_ADDR=${VAULT_ADDR}" \
	  --workdir $(CURDIR) \
	  "${MOLECULE_IMAGE}" \
	    molecule '$(ACTION)'

.PHONY: create
create: ACTION='create'
create: molecule ## Run the prepare playbook and keep the container running

.PHONY: converge
converge: ACTION='converge'
converge: molecule ## Run the test playbook and keep the container running

.PHONY: verify
verify: ACTION='verify'
verify: molecule ## Run the tests against a running container

.PHONY: destroy
destroy: ACTION='destroy'
destroy: molecule ## Destroy the created test container

.PHONY: test
test: ACTION='test'
test: molecule ## Run the tests and destroy the container
