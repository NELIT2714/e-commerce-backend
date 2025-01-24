FROM python:3.11.7-slim
COPY . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "run_api.py"]