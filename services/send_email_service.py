import os
import smtplib
import ssl
import json

def load_email_credentials():
    # Tìm đường dẫn tuyệt đối đến file json
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # trở về thư mục gốc project/
    filepath = os.path.join(base_dir, "data", "email_credentials.json")
    with open(filepath, "r") as f:
        return json.load(f)

def send_email(recipient_email: str, message_body: str):
    credentials = load_email_credentials()
    from_addr = credentials["email"]
    password = credentials["password"]

    # Compose message
    message = f"From: {from_addr}\r\nTo: {recipient_email}\r\n\r\n{message_body}"

    smtp_server = "smtp.gmail.com"
    port = 587
    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(from_addr, password)
        server.sendmail(from_addr, recipient_email, message)
        return {"status": "success", "detail": "Email sent successfully."}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if 'server' in locals():
            server.quit()
