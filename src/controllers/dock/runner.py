# TODO: Enable reporting on if a job is valid of not. See notes.
from exceptions import JobInvalidFormatException

class JobConstructor:
    def __init__(self, content: dict):
        self.base_content = content

    def _create_payload(self):
        return {
            "payload": {
                "jobs": self._create_jobs()
            }
        }

    def _validate_job(self, k, v):
        return type(k) is str and type(v) is dict

    def _create_jobs(self):
        jobs = []

        for job, val in self.base_content.items():
            if not self._validate_job(job, val):
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
            if not self._validate_stage(name, val):
                raise JobInvalidFormatException(
                    f"Should be string, map.. Got ({'='.join([type(name), name])}), ({'='.join([type(val), val])})."
                )

            jobs.append({
                "name": job,
                "stages": self._create_stages(val)
            })


        print(definition)

    def create(self) -> dict:
        payload = self._create_payload()
