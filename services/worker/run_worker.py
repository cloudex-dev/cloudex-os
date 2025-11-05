import os, sys, pathlib
# garante import do módulo worker.py
sys.path.append(str(pathlib.Path(__file__).parent.resolve()))
from worker import process_xml  # noqa: F401

from redis import Redis
from rq import Queue, SimpleWorker

redis_url = os.getenv("RQ_REDIS_URL", "redis://127.0.0.1:6379/0")
conn = Redis.from_url(redis_url)
q = Queue("xml", connection=conn)

if __name__ == "__main__":
    print("Starting RQ SimpleWorker (no fork, Windows-friendly)…")
    SimpleWorker([q], connection=conn).work()  # sem fork
