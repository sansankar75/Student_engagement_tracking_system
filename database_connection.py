from ollama_connection import get_class_notes
from pymongo import MongoClient
import time 


url="mongodb://localhost:27017/?directConnection=true"     # connection string in mongo db
client=MongoClient(url)

now = time.localtime()
def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S (%A)", now)  

def store_class_notes():
    lesson,script,notes,questions=get_class_notes()       # Get a input form ollama form ollama_connection file
    ## for storing class notes in the name of lesson,scripts,notes

    db=client["class_notes_db"]                 # create a db 
    collection=db["notes"]                      # create a collection 
    formatted = time.strftime("%Y-%m-%d %H:%M:%S (%A)", now)               
    data=collection.insert_one({"lesson":lesson,"script":script,"notes":notes,"questions":questions,"geotag":formatted})                    

"""def students_emotions(emotions):
    db = client['emotion_of_students']
    collection = db["emotion"]
    
    if isinstance(emotions, list) and emotions:
        data = collection.insert_many(emotions)
    else:
        print("No emotion data to insert or invalid format.")"""

def emotion_in_real_time(emotion):
    db = client['emotion']
    for i in emotion:
        if i:
            em=i[1]
            collection=db[em]
            collection.insert_one({
                    'Class':i[1],
                    'Name':i[0],
                    'emotion':i[3],
                    'timestamp':i[2]
            })    

    
    if isinstance(emotion, list) and emotion:
        for i in emotion:
            timesnow=current_time()
            data = collection.insert_one({"emotion":i,"time":timesnow})



#store_class_notes()




