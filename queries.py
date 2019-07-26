from models import db, Job, JobHistory
from sqlalchemy.sql import exists

def job_history_exists(hid) -> bool:
    return bool(db.session.query(exists().where(JobHistory.id == hid)).scalar())

def get_job_history_condition(condition):
    return JobHistory.query.filter(condition)

def get_job_history(hid):
    return JobHistory.query.get(hid)
