import os
import requests
from dotenv import load_dotenv
import jinja2

load_dotenv()

templateLoader = jinja2.FileSystemLoader("templates")
templateEnv = jinja2.Environment(loader=templateLoader)

def renderTemplate(templateFilename, **context):
    return templateEnv.get_template(templateFilename).render(**context)

# send confirmation email via mailgun
domain = os.getenv("MAILGUN_DOMAIN")
def send_simple_message(to, subject, body, html):
    
    result =  requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"Maheen Amin <mailgun@{domain}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html,
        },
    )
    return result

def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        'Successfully signed up',
        f'Hi {username}! You have successfully signed up to the Stores REST API.',
        renderTemplate("email/registration.html", username=username),
    )