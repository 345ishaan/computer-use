# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for the request body
class EmailRequest(BaseModel):
    email: str
    answers: dict

# Email sending function using SendGrid
def send_email(email: str, answers: dict):
    sender_email = "ishan@genime.art"  # Replace with your sender email
    sender_password = ".."  # Your SendGrid API key

    msg = MIMEText(str(answers), "plain")
    msg["Subject"] = "Questionnaire Answers"
    msg["From"] = sender_email
    msg["To"] = email

    try:
        with smtplib.SMTP("smtp.sendgrid.net", 587) as server:  # Use port 587 for TLS
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login("apikey", sender_password)  # Use "apikey" as the username
            server.sendmail(sender_email, email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")  # Log the error to the console
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

# Endpoint to send email
@app.post("/send-email")
async def send_email_endpoint(request: EmailRequest):
    send_email(request.email, request.answers)
    return {"message": "Email sent successfully!"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
