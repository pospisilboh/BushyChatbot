# docker build -t st_demo:v1.0 .
# docker run --rm --name mytest -p 8900:8501 -e PORT=8900 st_demo:v1.0
# docker run --rm --name mytest -p 8501:8501 -e PORT=8501 st_demo:v1.0
# docker run --rm --name mytest -p 8501:8000 -e PORT=8000 st_demo:v1.0
# http://localhost:8900

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8501

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]