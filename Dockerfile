FROM python:3.11
WORKDIR /backend
COPY ./requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
COPY ./ /backend
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]