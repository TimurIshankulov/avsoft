import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (SMTP_HOST_USER, SMTP_HOST_PASSWORD, SMTP_RECEIVER, SMTP_HOST, SMTP_PORT)
from celery_module.celery_app import app


@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 99, 'countdown': 10})
def send_email(filename):
    """
    Tries to send email to SMTP_RECEIVER. If sending will fail, task will
    retry to send it up to 99 times with interval of 10 seconds.
    """
    body_html = MIMEText(f'Error occurred with file: {filename}.', 'html', 'utf-8')
    message = MIMEMultipart()
    message['Subject'] = 'Error occurred'
    message['From'] = SMTP_HOST_USER
    message['To'] = SMTP_RECEIVER
    message.attach(body_html)

    try:
        server = smtplib.SMTP_SSL(host=SMTP_HOST, port=SMTP_PORT)
        server.login(SMTP_HOST_USER, SMTP_HOST_PASSWORD)
        server.sendmail(SMTP_HOST_USER, SMTP_RECEIVER, message.as_string())
    except smtplib.SMTPException:
        print(sys.exc_info()[1])
        raise smtplib.SMTPException
    except Exception:
        raise Exception
