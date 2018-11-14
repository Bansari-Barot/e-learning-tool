FROM python:3.6.7
ADD . /webapp
WORKDIR /webapp
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["./startup"]
#ENTRYPOINT ["python","chatbot.py"]
