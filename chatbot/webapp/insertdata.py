from config import Config
from app.models import Agent
from pymodm import connect
import json
#connect(Config.Mongo_URI)
# get the agent data from file and store it into data variable which is of type list
with open('agent_record.json') as json_file:
    data = json.load(json_file)
print(data)
print(type(data))
print(data[0]['course_id'])
print(type(data[0]))
print(len(data))
for i in range(len(data)):
    print(data[i])
    print(data[i]['course_id'])
# connect to database and insert record into database
connect(Config.MONGO_URI)
for i in range(len(data)):
    try:
        agent = Agent.objects.get({'course_id':data[i]['course_id']})
        print(agent)
    except Agent.DoesNotExist:
        agent = Agent(course_id=data[i]['course_id'], file_name=data[i]['file_name'], project_id=data[i]['project_id']).save()
        print(agent)
        #print(type(data))
