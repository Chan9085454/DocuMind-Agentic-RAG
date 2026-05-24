import os
import uuid
from fastapi import APIRouter, UploadFile, File
from app.ingestion.document_loader import load_document
from app.ingestion.chunker import chunk_text
import time
from threading import Thread
from app.ingestion.embedder import get_embeddings
from app.vectorstore.chroma_store import add_to_vectorstore
from app.RAG.qa_chain import answer_question
from app.core.config import UPLOAD_DIR
from app.core.job_store import create_job, set_job_result, set_job_error, get_job


router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), question: str | None = None):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, file.filename)


    t0 = time.time()
    with open(path, "wb") as f:
        f.write(await file.read())
    print(f"upload_file: saved file {file.filename} time={(time.time()-t0):.2f}s")


    t1 = time.time()
    text = load_document(path)
    print(f"upload_file: load_document time={(time.time()-t1):.2f}s text_len={len(text)}")

    t2 = time.time()
    chunks = chunk_text(text)
    print(f"upload_file: chunked into {len(chunks)} chunks time={(time.time()-t2):.2f}s")

    t3 = time.time()
    embeddings = get_embeddings(chunks)
    print(f"upload_file: embeddings computed for {len(embeddings)} chunks time={(time.time()-t3):.2f}s")


    metadatas = [{"source": file.filename}] * len(chunks)
    ids = [str(uuid.uuid4()) for _ in chunks]


    t4 = time.time()
    add_to_vectorstore(chunks, embeddings, metadatas, ids)
    print(f"upload_file: added to vectorstore time={(time.time()-t4):.2f}s")

    result = {"status": "success", "chunks": len(chunks)}

    if question:
       
        job_id = create_job()

        def _worker(jid, q):
            try:
                ans = answer_question(q)
                
                if not ans or (isinstance(ans, str) and ans.lower().startswith('llm request failed')):
                    set_job_error(jid, ans or 'LLM returned empty response')
                else:
                    set_job_result(jid, ans)
            except Exception as e:
                set_job_error(jid, str(e))

        t = Thread(target=_worker, args=(job_id, question), daemon=True)
        t.start()
        result["status"] = "processing"
        result["job_id"] = job_id

    return result
@router.get("/upload/result")
def upload_result(job_id: str):
    job = get_job(job_id)
    if not job:
        return {"status": "not_found"}
    return {"status": job["status"], "result": job.get("result"), "error": job.get("error")}