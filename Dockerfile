FROM python:3.12.9

WORKDIR /tmp
COPY src/ ./src
COPY pyproject.toml/ ./pyproject.toml

RUN pip install .

USER nobody

WORKDIR /workspace
COPY main.py ./main.py

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py"]
# ENTRYPOINT ["streamlit", "run", "main.py", "--server.runOnSave", "false"]