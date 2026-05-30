# ==========================================
# SYNOPTIMESH — AUTO EMAIL (PUSH MAIL)
# Sends a formatted email via Gmail API
# using OAuth2 credentials
# ==========================================
#
# SETUP (one time only):
# 1. Go to https://console.cloud.google.com
# 2. Create a project → Enable Gmail API
# 3. Create OAuth2 credentials (Desktop App)
# 4. Download credentials → save as credentials.json
#    in the same folder as this file
# 5. pip install google-auth google-auth-oauthlib
#              google-auth-httplib2 google-api-python-client
#
# First run: browser opens for Google login.
# After that: token.json is saved and reused silently.
# ==========================================

import os
import base64
from email.mime.text        import MIMEText
from email.mime.multipart   import MIMEMultipart
from datetime               import datetime

from google.oauth2.credentials          import Credentials
from google_auth_oauthlib.flow          import InstalledAppFlow
from google.auth.transport.requests     import Request
from googleapiclient.discovery          import build

# ==========================================
# CONFIG
# ==========================================

SCOPES            = ["https://www.googleapis.com/auth/gmail.send"]
CREDENTIALS_FILE  = "credentials.json"   # downloaded from Google Cloud Console
TOKEN_FILE        = "token.json"          # auto-generated after first login

# ==========================================
# OAUTH — GET GMAIL SERVICE
# Handles first-time browser login + token
# refresh silently on subsequent runs
# ==========================================

def get_gmail_service():

    creds = None

    # Load saved token if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid token, log in via browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print("\n[MAIL] ERROR: 'credentials.json' not found.")
                print("[MAIL] Download it from Google Cloud Console → OAuth2 → Desktop App.\n")
                return None

            flow  = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

# ==========================================
# EMAIL BODY BUILDER
# Formats a clean auto-typed email using
# the inputs collected from the user
# ==========================================

def build_email_body(name, subject, date, sender_email):

    body = f"""Dear {name},

I hope this message finds you well.

I am writing to you regarding: {subject}

Please note the relevant date: {date}

Should you have any questions or require further information,
please do not hesitate to reach out.

Best regards,
{sender_email}

--
Sent via Synoptimesh BCI Desktop Node
"""
    return body

# ==========================================
# BUILD RAW MIME MESSAGE
# ==========================================

def build_message(to, sender_email, subject, body):

    message             = MIMEMultipart()
    message["To"]       = to
    message["From"]     = sender_email
    message["Subject"]  = subject
    message.attach(MIMEText(body, "plain"))

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}

# ==========================================
# SEND EMAIL
# ==========================================

def send_email(service, message):
    sent = service.users().messages().send(
        userId="me",
        body=message
    ).execute()
    return sent.get("id")

# ==========================================
# PUSH MAIL — MAIN FUNCTION
# Call this from desktop_node.py
# ==========================================

def push_mail():

    print("\n" + "=" * 45)
    print("         PUSH MAIL — AUTO EMAIL")
    print("=" * 45)

    # ----------------------------------------
    # COLLECT INPUTS
    # ----------------------------------------

    recipient   = input("\nRecipient Email ID  : ").strip()
    sender      = input("Your    Email ID    : ").strip()
    name        = input("Recipient Name      : ").strip()
    subject     = input("Subject             : ").strip()
    date        = input("Date (e.g. 26 May 2026): ").strip()

    # ----------------------------------------
    # CONFIRM BEFORE SENDING
    # ----------------------------------------

    print(f"""
----------------------------------------
  TO      : {recipient}
  FROM    : {sender}
  NAME    : {name}
  SUBJECT : {subject}
  DATE    : {date}
----------------------------------------""")

    confirm = input("\nSend this email? (yes / no): ").strip().lower()

    if confirm != "yes":
        print("\n[MAIL] Email cancelled.\n")
        return

    # ----------------------------------------
    # AUTHENTICATE + SEND
    # ----------------------------------------

    print("\n[MAIL] Authenticating with Gmail...\n")

    service = get_gmail_service()
    if service is None:
        return

    body    = build_email_body(name, subject, date, sender)
    message = build_message(recipient, sender, subject, body)

    try:
        msg_id = send_email(service, message)
        print(f"\n[MAIL] Email sent successfully!")
        print(f"[MAIL] Message ID : {msg_id}\n")

    except Exception as e:
        print(f"\n[MAIL] Failed to send email: {e}\n")
        print("[MAIL] Check your credentials.json and internet connection.\n")