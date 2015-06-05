.PHONY: test-setup

test-setup:
	docker pull xivo/xivo-auth
	docker pull n3llyb0y/wait
	docker pull rabbitmq
	docker pull progrium/consul
	docker build -t xivo/xivo-auth-client-tests-data -f Dockerfile-data .
