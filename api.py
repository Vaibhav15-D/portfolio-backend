from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.message import EmailMessage
from db import get_connection

app = FastAPI(title="Portfolio Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ContactIn(BaseModel):
    name: str
    email: str
    mobile: str
    profession: str
    purpose: str
    message: str = ""





@app.post("/contact")
def save_message(data: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO messages(name,email,mobile,profession,purpose,message) VALUES(%s,%s,%s,%s,%s,%s)",
        (
            data.get("name",""),
            data.get("email",""),
            data.get("mobile",""),
            data.get("profession",""),
            data.get("purpose",""),
            data.get("message","")
        )
    )

    conn.commit()
    send_email(type("obj",(object,),data))  # converts dict → object for email
    conn.close()

    return {"status": "Message saved & email sent"}



@app.get("/messages")
def get_messages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name,email,message,created_at FROM messages ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return {"messages": rows}

def send_email(data):
    msg = EmailMessage()
    msg["Subject"] = "New Portfolio Contact"
    msg["From"] = "vaibhavdukare02@gmail.com"
    msg["To"] = "vaibhavdukare02@gmail.com"

    msg.set_content(f"""
Name: {data.name}
Email: {data.email}
Mobile: {data.mobile}
Profession: {data.profession}
Purpose: {data.purpose}

Message:
{data.message}
""")

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login("vaibhavdukare02@gmail.com","ejwk fxpa yyfv imjd")
        smtp.send_message(msg)
