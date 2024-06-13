import email.mime.multipart
import email.mime.text

import utils.constants
import utils.jenkins_util

def get_message():
    job_data = utils.jenkins_util.get_job_data()
    subject = f"Jenkins Job {job_data['job_name']} Build #{job_data['build_number']}"
    body = f"""
    <html>
    <body>
        <p>Hi,</p>
        <p>Jenkins job: <b>{job_data['job_name']}</b></p>
        <p>Build: <b>{job_data['build_number']}</b></p>
        <p>Finished with status: <b>{job_data['build_status']}</b>.</p>
        <p>Details at: <a href="{job_data['build_url']}">here</a>.</p>
        <p>Regards,<br>Jenkins</p>
    </body>
    </html>
    """
    message = email.mime.multipart.MIMEMultipart()
    message['From'] = utils.constants.EMAIL.SENDER_EMAIL
    message['To'] = utils.constants.EMAIL.MAIN_RECEIVER
    message['Subject'] = subject
    message.attach(email.mime.text.MIMEText(body, 'html'))
    return message
