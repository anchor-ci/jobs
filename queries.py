from models import db, Job, JobHistory
from sqlalchemy.sql import exists

def job_history_exists(hid) -> bool:
    return bool(db.session.query(exists().where(JobHistory.id == hid)).scalar())

def get_job_history_condition(condition):
    return JobHistory.query.filter(condition)

def get_job_history(hid):
    return JobHistory.query.get(hid)

def get_job(jid):
    return Job.query.get(jid)

def job_exists(jid):
    return bool(db.session.query(exists().where(Job.id == jid)).scalar())

def get_job_condition(condition):
    return Job.query.filter(condition)
