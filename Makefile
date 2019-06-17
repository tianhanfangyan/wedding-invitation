APP?=wedding_invitation
PORT?=9004

RELEASE?=$(shell git describe --tags --abbrev=0 --exact-match 2>/dev/null || echo "latest")
COMMIT?=$(shell git rev-parse --short HEAD)
BUILT?=$(shell date +"%Y-%m-%d_%H:%M:%S_%Z")

REGISTRY_PREFIX?=dystargate
CONTAINER_IMAGE?=${REGISTRY_PREFIX}/${APP}:${RELEASE}

.PHONY:test

clean:
	rm -rf *.pyc && rm -rf app/*.pyc

built: clean
	pip install -r ./requirements.txt &&  python manage.py db init &&  python manage.py db migrate && \
	    python manage.py db upgrade && python db_user.py

image:
	docker build -t ${CONTAINER_IMAGE} --build-arg RELEASE=${RELEASE} --build-arg COMMIT=${COMMIT}  \
                 --build-arg  BUILT=${BUILT}   .

test:
	python manage.py runserver --port ${PORT}

push: image
	docker push ${CONTAINER_IMAGE}
