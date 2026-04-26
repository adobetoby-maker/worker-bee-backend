import os, pathlib
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.readonly"
]

TOKEN_PATH = pathlib.Path.home() / ".workerbee_gmail_token.json"
CREDS_PATH = pathlib.Path.home() / ".workerbee_gmail_creds.json"

class GmailTool:
    def __init__(self):
        self._service = None

    def _auth(self):
        creds = None
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(
                str(TOKEN_PATH), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CREDS_PATH.exists():
                    raise FileNotFoundError(
                        f"Gmail credentials not found at {CREDS_PATH}. "
                        "Download OAuth credentials from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDS_PATH), SCOPES)
                creds = flow.run_local_server(port=0)
            TOKEN_PATH.write_text(creds.to_json())
        self._service = build("gmail", "v1", credentials=creds)
        return self._service

    def service(self):
        if not self._service:
            self._auth()
        return self._service

    def get_inbox_summary(self) -> dict:
        svc = self.service()
        categories = {
            "unread":      "is:unread",
            "promotions":  "category:promotions",
            "social":      "category:social",
            "updates":     "category:updates",
            "newsletters": "list:* OR unsubscribe",
            "old_unread":  "is:unread older_than:30d",
        }
        summary = {}
        for name, query in categories.items():
            result = svc.users().messages().list(
                userId="me", q=query, maxResults=1).execute()
            summary[name] = result.get("resultSizeEstimate", 0)
        inbox = svc.users().labels().get(
            userId="me", id="INBOX").execute()
        summary["total_inbox"] = inbox.get("messagesTotal", 0)
        return summary

    def get_emails(self, query: str, max_results: int = 20) -> list:
        svc = self.service()
        results = svc.users().messages().list(
            userId="me", q=query, maxResults=max_results).execute()
        emails = []
        for m in results.get("messages", []):
            msg = svc.users().messages().get(
                userId="me", id=m["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"]).execute()
            headers = {h["name"]: h["value"]
                      for h in msg["payload"]["headers"]}
            emails.append({
                "id": m["id"], "from": headers.get("From", ""),
                "subject": headers.get("Subject", ""),
                "date": headers.get("Date", ""),
                "snippet": msg.get("snippet", "")[:100]
            })
        return emails

    def archive_emails(self, query: str, max_results: int = 500) -> dict:
        svc = self.service()
        results = svc.users().messages().list(
            userId="me", q=query, maxResults=max_results).execute()
        messages = results.get("messages", [])
        if not messages:
            return {"archived": 0, "message": "No emails found"}
        ids = [m["id"] for m in messages]
        svc.users().messages().batchModify(
            userId="me",
            body={"ids": ids, "removeLabelIds": ["INBOX"]}).execute()
        return {"archived": len(ids), "message": f"Archived {len(ids)} emails"}

    def delete_emails(self, query: str, max_results: int = 500) -> dict:
        svc = self.service()
        results = svc.users().messages().list(
            userId="me", q=query, maxResults=max_results).execute()
        messages = results.get("messages", [])
        if not messages:
            return {"deleted": 0, "message": "No emails found"}
        ids = [m["id"] for m in messages]
        svc.users().messages().batchModify(
            userId="me",
            body={"ids": ids, "addLabelIds": ["TRASH"]}).execute()
        return {"deleted": len(ids), "message": f"Moved {len(ids)} to trash"}

    def unsubscribe_sender(self, sender_email: str) -> dict:
        return self.archive_emails(
            f"from:{sender_email}", max_results=1000)

    def get_top_senders(self, max_results: int = 200) -> list:
        svc = self.service()
        results = svc.users().messages().list(
            userId="me", q="in:inbox", maxResults=max_results).execute()
        senders = {}
        for m in results.get("messages", []):
            msg = svc.users().messages().get(
                userId="me", id=m["id"], format="metadata",
                metadataHeaders=["From"]).execute()
            sender = next(
                (h["value"] for h in msg["payload"]["headers"]
                 if h["name"] == "From"), "Unknown")
            senders[sender] = senders.get(sender, 0) + 1
        return [{"sender": s, "count": c}
                for s, c in sorted(senders.items(),
                                   key=lambda x: x[1],
                                   reverse=True)[:20]]
