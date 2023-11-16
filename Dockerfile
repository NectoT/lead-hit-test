FROM python:3

WORKDIR /project

COPY app/requirements.txt app/
RUN pip install -r app/requirements.txt

COPY run.sh .

COPY . .

EXPOSE 8000

ENTRYPOINT [ "bash", "run.sh" ]
CMD [ "app" ]