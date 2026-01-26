# uvicorn main:app --reload --port 8000 to run fastapi
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Query
from client.rq_client import queue
from queues.worker import process_query


app = FastAPI()


@app.get("/")
def root():
    return {"status": "Server is up and running"}


@app.post("/chat")
def chat(query: str = Query(..., description="The query of the user...")):
    # pass user query to the process_query function and add it to the queue
    # job means ==> A task that the server runs in the background, usually automatically, without waiting for the user
    # here mean Going to the queue and add the query
    job = queue.enqueue(process_query, query)

    return {"status": "queued", "job_id": job.id}


@app.get("/job_status")
def get_result(job_id: str = Query(..., description="Job ID")):
    job = queue.fetch_job(job_id)
    result = job.return_value()

    return {"result": result}
'''
about debugging
{
  "status": "queued",
  "job_id": "fde7e041-f7ca-4dfe-943c-c2bda94c5172"
}

Interfaces
{
  "status": "queued",
  "job_id": "c2d45494-c04a-4b87-b4d0-81ba45e1dc7b"
}

'''