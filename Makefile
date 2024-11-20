ifneq (,$(wildcard ./.env))
	include .env
	export
endif

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

install: ## Poetry install
	poetry install

run: ## FastApi dev
	poetry run fastapi dev

##@ Database
db-compose-up: ## Launch database+adminer from docker-compose
	docker compose up db adminer --build -d
	@echo "Adminer: http://localhost:1000/?pgsql=db&username=$(POSTGRES_USER)&database=$(POSTGRES_DB)" with password: $(POSTGRES_PASSWORD)

