FROM python:3.12.9

RUN pip install matplotlib
RUN pip install pandas
RUN pip install numpy
RUN pip install scikit-learn
RUN pip install scipy
RUN pip install openai
RUN pip install streamlit

WORKDIR /tmp
COPY src/ ./src
COPY pyproject.toml/ ./pyproject.toml

RUN pip install .

USER nobody

WORKDIR /workspace
COPY main.py ./main.py

COPY temp_data ./temp_data

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.runOnSave", "false"]