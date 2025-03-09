DATA?="${PWD}"
DOCKER_FILE=Dockerfile
NAME?=spreadsheet-llm
WORKING_DIR=/workspace
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

build:
	docker build -t $(NAME) -f $(DOCKER_FILE) .

app: build
	docker run --rm  -p 8501:8501 -w $(WORKING_DIR) --shm-size=10.07gb -v $(DATA):/workspace $(NAME)
