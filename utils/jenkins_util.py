import os

import utils.constants

def get_job_data():
    job_data = {}
    job_data['job_name'] = os.getenv('JOB_NAME')
    job_data['build_number'] = os.getenv('BUILD_NUMBER')
    job_data['build_url'] = os.getenv('BUILD_URL')
    job_data['build_status'] = os.getenv('BUILD_STATUS')
    job_data['build_url'] = "".join(
        "http://localhost:{}/job/{}/{}".format(
            utils.constants.JENKINS.PORT,
            job_data['job_name'],
            job_data['build_number']
        )
    )
    return job_data
