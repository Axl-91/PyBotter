import requests
import schedule
import time
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def send_email(rate):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    try:
        subject = "USD/ARS Exchange Rate"
        body = f"""
        Daily Exchange Rate Update
        
        1 USD = {rate} ARS
        
        Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        ---
        Sent by your friendly Python bot 🤖
        """

        # Create email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")


def get_usd_to_ars():
    try:
        url = "https://open.er-api.com/v6/latest/USD"

        response = requests.get(url)
        data = response.json()

        ars_rate = data["rates"]["ARS"]

        print(f"1 USD = {ars_rate} ARS")
        return ars_rate

    except Exception as e:
        print(f"Error getting exchange rate: {e}")
        return None


def email_sender():
    rate = get_usd_to_ars()
    send_email(rate)


if __name__ == "__main__":
    email_sender()

    # Send email everyday at 12:00 PM
    schedule.every().day.at("12:00").do(email_sender)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nBot stopped!")
