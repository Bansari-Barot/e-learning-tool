FROM python:3.6.7
ADD . /webapp
WORKDIR /webapp
EXPOSE 5000
RUN pip install -r requirements.txt
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.3.0/wait /wait
RUN chmod +x /wait
#CMD ["./startup"]
#ENTRYPOINT ["python","chatbot.py"]
