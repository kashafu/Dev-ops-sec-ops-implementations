From python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt
COPY ./taskman /code/taskman
CMD ["uvicorn", "taskman.main:app", "--host", "0.0.0.0", "--port", "80"]