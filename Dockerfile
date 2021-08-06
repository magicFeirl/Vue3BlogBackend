FROM python:3.8
WORKDIR /code
COPY requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt
COPY . .
CMD uvicorn app:app --host=0.0.0.0 --port=8080