DATA?="${PWD}"
DOCKER_FILE=Dockerfile
NAME?=spreadsheet-llm
WORKING_DIR=/workspace
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

build:
	docker build -t $(NAME) -f $(DOCKER_FILE) .

bash: build
	docker run -it --rm --net=host -w $(WORKING_DIR) --shm-size=10.07gb -v $(DATA):/workspace $(NAME) /bin/bash

converse: build
	docker run -it --rm --net=host -w $(WORKING_DIR) --shm-size=10.07gb -v $(DATA):/workspace $(NAME) python main.py