# TODO: Enable reporting on if a job is valid of not. See notes.
from schemas.stage import StageSchema
from marshmallow.exceptions import ValidationError
from exceptions import JobInvalidFormatException, JobValidationException

class JobConstructor:
    def __init__(self, content: dict):
        self.base_content = content

    def _create_payload(self):
        return {
            "payload": {
                "jobs": self._create_jobs()
            }
        }

    def _validate_base(self, k, v):
        return type(k) is str and type(v) is dict

    def _create_jobs(self):
        jobs = []

        for job, val in self.base_content.items():
            if not self._validate_base(job, val):
                raise JobInvalidFormatException(
                    f"Should be string, map.. Got ({'='.join([type(job), job])}), ({'='.join([type(val), val])})."
                )

            jobs.append({
                "name": job,
                "stages": self._create_stages(val)
            })

        return jobs

    def _create_stages(self, definition):
        stages = []

        for name, val in definition.items():
            if not self._validate_base(name, val):
                raise JobInvalidFormatException(
                    f"Should be string, map.. Got ({'='.join([type(name), name])}), ({'='.join([type(val), val])})."
                )

            schema = StageSchema()

            try:
                stages.append({
                    "name": name,
                    "stages": schema.load(val)
                })
            except ValidationError as e:
                raise JobValidationException(
                    e.messages
                )

        return stages

    def create(self) -> dict:
        return self._create_payload()
