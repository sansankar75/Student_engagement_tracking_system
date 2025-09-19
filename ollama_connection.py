from caption import data
import requests
import re
import subprocess
import time
import ollama

## template for my notes making

template_for_class_notes="""
can you find the core of the meeting like what they try to teach , make a detail scripts to make a quick analysis what
is the previous class teach ,like a notes with clearness and use this template and make a five questions related to the topic 
that teacher teach
 Lesson: [Topic Name]
####
Script:
"[Full paragraph in natural speech format]"
####
 Notes:
- [Fact 1]
- [Fact 2]
- [Subpoint or example]
-....
####
 Questions:
 1.
 2.
 3.
 4.
 5.
Answer for above questions and make a list of option for the question to answer 
"""



## class notes 

lesson=""
script=""
notes=""





## connection with ollama model

def chat_with_ollama(data):
    
    # Start Ollama
    ollama_process = subprocess.Popen(['ollama', 'serve'])
    time.sleep(3)  # give time to start

    # Use Ollama Python API
    result = ollama.generate(model='llama3', prompt=data)
    #print(result['response'])
    return result['response']

    # Shutdown Ollama
    ollama_process.terminate()


## split the output into lesson,scripts,notes 

def output_split(output):
     
    #pattern = r"Lesson:(.*?)Script:(.*?)Notes:(.?*)Questions:(.*)"
    pattern=r"Lesson:(.*?)Script:(.*?)Notes:(.*?)Questions:(.*)"
    matches = re.search(pattern,output,re.DOTALL)

    if matches:
        lesson = matches.group(1).strip().replace("*","").replace("\n","")
        script = matches.group(2).strip().replace("*","").replace("\n","")
        notes = matches.group(3).strip().replace("*","").replace("\n","")
        questions=matches.group(4).strip().replace("*","").replace("\n","")
    return lesson,script,notes,questions

## provide a class notes     

def get_class_notes():
    output = chat_with_ollama(data+template_for_class_notes)
    lesson,script,notes,questions=output_split(output)
    return lesson,script,notes,questions
