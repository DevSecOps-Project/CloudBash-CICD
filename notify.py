import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import utils.constants
import utils.email_util


if __name__ == '__main__':
    try:
        server = smtplib.SMTP(
            utils.constants.EMAIL.SMTP_SERVER,
            utils.constants.EMAIL.SMTP_PORT
        )
        server.starttls()
        server.login(
            utils.constants.EMAIL.SENDER_EMAIL,
            'rqbn rcjk rics loud'
        )
        message = utils.email_util.get_message()
        server.sendmail(
            utils.constants.EMAIL.SENDER_EMAIL,
            utils.constants.EMAIL.MAIN_RECEIVER,
            message.as_string()
        )
        server.quit()
        print(f'Email sent successfully')
    except Exception as e:
        print(f'Failed to send email. Error: {str(e)}')
