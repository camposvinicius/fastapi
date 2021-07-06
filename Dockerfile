FROM python:3.8.10
RUN pip3 install fastapi uvicorn awswrangler boto3 python-dotenv
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]