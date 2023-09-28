THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help up down test
help:
	@make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -v -e '^[^[:alnum:]]' -e '^$@$$'
up:
	@docker compose up --build -d backend
down:
	@docker compose down
test:
	@docker compose up --build tests