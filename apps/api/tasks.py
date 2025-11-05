import os, redis, rq, base64
import base64

def _queue():
    host = os.getenv("REDIS_HOST", "127.0.0.1")
    r = redis.Redis(host=host, port=6379, db=0)
    return rq.Queue("xml", connection=r)

def enqueue_xml(content: bytes, filename: str) -> str:
    # manda o processamento para o worker
    job = _queue().enqueue("worker.process_xml", base64.b64encode(content).decode(), filename)
    return job.get_id()
