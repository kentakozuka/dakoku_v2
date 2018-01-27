#!/bin/sh

docker run \
		-it \
		-d \
		--privileged \
		--name dakoku \
		-v ${PWD}:/home/work/app \
		--link  db:db \
		kentakozuka/dev-tools \
		/bin/bash
docker exec -it dakoku /bin/bash
