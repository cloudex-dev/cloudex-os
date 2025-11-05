from fastapi import FastAPI, UploadFile, File
from typing import List
from tasks import enqueue_xml

#commit teste
app = FastAPI(title="CloudEx API")

@app.get("/")
def root():
    return {"ok": True, "app": "CloudEx API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/xml/upload")
async def upload_xml(files: List[UploadFile] = File(..., description="Envie 1+ XMLs")):
    results = []
    for f in files:
        content = await f.read()
        job_id = enqueue_xml(content, filename=f.filename)
        results.append({"filename": f.filename, "job_id": job_id})
    return {"accepted": results}
