import os


def get_job_data():
    job_data = {}
    job_data['job_name'] = os.getenv('JOB_NAME')
    job_data['build_number'] = os.getenv('BUILD_NUMBER')
    job_data['build_url'] = os.getenv('BUILD_URL')
    job_data['build_status'] = os.getenv('BUILD_STATUS')
    return job_data