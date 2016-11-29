.PHONY: test-setup

test-setup:
	docker pull wazopbx/xivo-auth
	docker pull n3llyb0y/wait
	docker pull rabbitmq
	docker pull progrium/consul
	docker build -t wazopbx/xivo-auth-client-tests-data -f Dockerfile-data .
