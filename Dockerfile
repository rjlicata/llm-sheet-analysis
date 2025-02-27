FROM python:3.10.12

WORKDIR /tmp
COPY src/ ./src
COPY pyproject.toml/ ./pyproject.toml

RUN pip install .

WORKDIR /workspace

ENTRYPOINT []

CMD ["/bin/bash"]