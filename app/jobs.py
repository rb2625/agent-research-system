import threading
import uuid

_jobs = {}
_lock = threading.Lock()


def create_job() -> str:
    job_id = str(uuid.uuid4())
    with _lock:
        _jobs[job_id] = {"status": "running", "steps": [], "result": None, "error": None}
    return job_id


def add_step(job_id: str, message: str):
    with _lock:
        if job_id in _jobs:
            _jobs[job_id]["steps"].append(message)


def complete_job(job_id: str, result: dict):
    with _lock:
        if job_id in _jobs:
            _jobs[job_id]["status"] = "done"
            _jobs[job_id]["result"] = result


def fail_job(job_id: str, error: str):
    with _lock:
        if job_id in _jobs:
            _jobs[job_id]["status"] = "error"
            _jobs[job_id]["error"] = error


def get_job(job_id: str):
    with _lock:
        return _jobs.get(job_id)