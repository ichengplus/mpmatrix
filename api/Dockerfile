FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --extra-index-url https://pypi.python.org/simple --trusted-host mirrors.aliyun.com

