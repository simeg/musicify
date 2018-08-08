.PHONY: ci

SERVER = ./server
WEB_APP = ./web_app

ci:
	@make -C $(SERVER) ci
	@make -C $(WEB_APP) ci

py-%: FORCE
	@$(MAKE) -C $(SERVER) $*

js-%: FORCE
	@$(MAKE) -C $(WEB_APP) $*

FORCE:
