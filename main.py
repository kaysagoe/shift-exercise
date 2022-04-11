import os

from fastapi import FastAPI, Body, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse
from prototype_classifier import PrototypeClassifier
from classifier_base import IETFClassifier
from functools import lru_cache
from typing import Optional
from csv import writer

app = FastAPI()

def add_to_classifier_log(input: str, result: Optional[str] = None):
    with open('/tmp/classifier_log.csv', 'a', newline='') as log_file:
        csv_writer = writer(log_file)
        csv_writer.writerow([input, result])

def get_word_file_path():
    return os.getenv('word_list_path')

@lru_cache
def get_classifier(path: str = Depends(get_word_file_path)):
    return PrototypeClassifier(path)

@app.post('/', response_class=HTMLResponse)
async def serve(background_tasks: BackgroundTasks,
                input: str = Body(..., embed=True), 
                classifier: IETFClassifier = Depends(get_classifier)):
    result = classifier.classify(input)
    background_tasks.add_task(add_to_classifier_log, input, result)
    if result:
        return result
    else:
        message = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>The browser (or proxy) sent a request that this server could not understand.</p>'''
        return HTMLResponse(message, status_code=400)