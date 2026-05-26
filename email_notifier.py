# ===== 이메일 알림 =====
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_TO

def send_kakao_message(message):  # 함수명 유지 (main.py 호환)
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_TO
        msg['Subject'] = "📚 DGIST LMS 새 파일 알림"
        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("이메일 전송 완료!")
        return True
    except Exception as e:
        print(f"이메일 전송 실패: {e}")
        return False