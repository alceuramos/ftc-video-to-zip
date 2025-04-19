from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from core.settings import settings
from schemas.video import Video


class NotificationService:
    def __init__(self):
        self.sendgrip: SendGridAPIClient = SendGridAPIClient(
            settings.EMAIL_TOKEN
        )
        env = Environment(
            loader=FileSystemLoader("src/templates")
        )  # Folder where you saved email_template.html
        self.template = env.get_template("email_template.html")

    def send(
        self,
        user: dict,
        video: Video,
    ) -> None:

        subject = f"Unable to Process '{video.title}' - Please Review"
        context = {
            "user_name": str(user.get("name", "")),
            "video_title": str(video.title),
            "video_created_at": str(video.created_at),
            "video_status": str(video.status),
        }
        html_content = self.template.render(**context)

        message = Mail(
            from_email=settings.EMAIL_SENDER,
            to_emails=user.get("email", ""),
            subject=subject,
            html_content=html_content,
        )
        try:
            self.sendgrip.send(message)
        except Exception as e:
            print(e.message)
