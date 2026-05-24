import threading
import uuid

_jobs = {}
_lock = threading.Lock()


def create_job():
    job_id = str(uuid.uuid4())
    with _lock:
        _jobs[job_id] = {"status": "pending", "result": None, "error": None}
    return job_id


def set_job_result(job_id, result):
    with _lock:
        if job_id in _jobs:
            _jobs[job_id]["status"] = "done"
            _jobs[job_id]["result"] = result


def set_job_error(job_id, error):
    with _lock:
        if job_id in _jobs:
            _jobs[job_id]["status"] = "error"
           
            try:
                msg = str(error) if error is not None else "Unknown error"
            except Exception:
                msg = "Unknown error"
            _jobs[job_id]["error"] = msg


def get_job(job_id):
    with _lock:
        return _jobs.get(job_id)
