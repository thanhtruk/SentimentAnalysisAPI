import os
import smtplib
import ssl
import json
from email.message import EmailMessage


def load_email_credentials():
    # Tìm đường dẫn tuyệt đối đến file json
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # trở về thư mục gốc project/
    filepath = os.path.join(base_dir, "data", "email_credentials.json")
    with open(filepath, "r") as f:
        return json.load(f)

# def send_email(recipient_email: str, message_body: str):
#     credentials = load_email_credentials()
#     from_addr = credentials["email"]
#     password = credentials["password"]
#
#     msg = EmailMessage()
#     msg["Subject"] = "Đánh giá/Câu hỏi từ hệ thống góp ý"
#     msg["From"] = from_addr
#     msg["To"] = recipient_email
#     msg.set_content(message_body, charset="utf-8")
#
#     smtp_server = "smtp.gmail.com"
#     port = 587
#     context = ssl.create_default_context()
#
#     try:
#         server = smtplib.SMTP(smtp_server, port)
#         server.starttls(context=context)
#         server.login(from_addr, password)
#         server.send_message(msg)
#         return {"status": "success", "detail": "Email sent successfully."}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
#     finally:
#         if 'server' in locals():
#             server.quit()

def send_email(recipient_email: str, subject: str, message_body: str):
    credentials = load_email_credentials()
    from_addr = credentials["email"]
    password = credentials["password"]

    smtp_server = "smtp.gmail.com"
    port = 587
    context = ssl.create_default_context()

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    try:
        # Tạo email MIME
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = recipient_email

        # Thêm HTML content
        html_part = MIMEText(message_body, "html", "utf-8")
        msg.attach(html_part)

        # Gửi
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(from_addr, password)
        server.sendmail(from_addr, recipient_email, msg.as_string())

        return {"status": "success", "detail": "Email sent (HTML) successfully."}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if 'server' in locals():
            server.quit()

