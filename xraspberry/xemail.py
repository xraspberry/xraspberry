import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .xlogger import logger

# the e-mail config
SMTP_SERVER = os.environ.get("X_EMAIL_SERVER") or "smtp.qq.com"
USERNAME = os.environ.get("X_EMAIL_USERNAME")
PASSWORD = os.environ.get("X_EMAIL_PASSWORD")
SENDER = USERNAME
RECEIVER = ["dgt_x@foxmail.com"]


def send_email(subject, msg):
    msg_root = MIMEMultipart('related')
    msg_root["To"] = ','.join(RECEIVER)
    msg_root["From"] = SENDER
    msg_root['Subject'] = subject
    msg_text = MIMEText(msg, 'html', 'utf-8')
    msg_root.attach(msg_text)

    logger.info("[X-Raspberry]: Starting Sending Email!")
    smtp = smtplib.SMTP()
    try:
        smtp.connect(SMTP_SERVER)
        smtp.starttls()
        smtp.login(USERNAME, PASSWORD)
        smtp.sendmail(SENDER, RECEIVER, msg_root.as_string())
    except Exception as e:
        logger.error("[X-Raspberry]: Sending Email Failed!", exc_info=e)
    else:
        logger.info("[X-Raspberry]: Sending Email Successfully!")
    finally:
        smtp.quit()
