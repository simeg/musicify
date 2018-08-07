.PHONY: ci

SERVER = ./server
WEB_APP = ./web_app

ci:
	@make -C $(SERVER) ci
	@make -C $(WEB_APP) ci
