import imaplib
import email
import os
from dotenv import load_dotenv
from email.header import decode_header

load_dotenv()
EMAIL_USER = os.getenv("GMAIL_USER")
EMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD")

def decode_subject(raw_subject):
    decoded_parts = decode_header(raw_subject)
    subject = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            subject += part.decode(encoding or 'utf-8', errors='ignore')
        else:
            subject += part
    return subject

def fetch_primary_subjects(max_count=10):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    _, data = mail.search(None, 'ALL')
    email_ids = data[0].split()[-max_count:]

    subjects = []
    for eid in reversed(email_ids):
        _, msg_data = mail.fetch(eid, "(RFC822)")
        for part in msg_data:
            if isinstance(part, tuple):
                msg = email.message_from_bytes(part[1])
                subject_raw = msg["subject"]
                if subject_raw:
                    decoded = decode_subject(subject_raw)
                    subjects.append(decoded)

    mail.logout()
    return subjects

if __name__ == "__main__":
    subjects = fetch_primary_subjects()
    print("📧 Primary Inbox Subjects:")
    for i, sub in enumerate(subjects, 1):
        print(f"{i}. {sub}")