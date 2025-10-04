import smtplib
from email.message import EmailMessage

def send_email(to_email, subject, body, smtp_server, smtp_port, username, password):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = username
        msg['To'] = to_email
        msg.set_content(body)
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.send_message(msg)
        return f"Email sent successfully to {to_email}."
    except Exception as e:
        return f"Failed to send email: {e}"
