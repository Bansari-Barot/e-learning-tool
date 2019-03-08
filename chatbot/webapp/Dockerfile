FROM python:3.6.7
ADD . /webapp
WORKDIR /webapp
EXPOSE 5000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV TZ=US/Pacific
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.3.0/wait /wait
RUN chmod +x /wait
#CMD ["./startup"]
#ENTRYPOINT ["python","chatbot.py"]
