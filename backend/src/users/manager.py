from typing import Optional
from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from celery import Celery
from smtplib import SMTP_SSL
from email.message import EmailMessage

from src.users.models import User
from src.config import SMTP_USER, SMTP_HOST, SMTP_PASS, SMTP_PORT, CELERY_BROKER_URL, USER_MANAGER_SECRET

celery_app = Celery("users", broker_url=CELERY_BROKER_URL)


def get_email(
        username: str,
        user_email: str,
        token: str,
        subject: str
) -> EmailMessage:
    """
    Returns an email template for verification email
    """
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'{username}, Ваш код подтверждения: {token}'
        '</div>',
        subtype='html'
    )
    return email


@celery_app.task
def send_email(
        username: str,
        user_email: str,
        token: str,
        subject: str
) -> None:
    """
    Sends an email to user email
    """
    email = get_email(username, user_email, token, subject)
    with SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = USER_MANAGER_SECRET
    verification_token_secret = USER_MANAGER_SECRET

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        """
        Creates a new user in the database
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict['role_id'] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_request_verify(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ) -> None:
        """
        Sends a verification email to the user to verify user`s email
        """
        send_email.delay(user.username, user.email, token, "Подтверждение аккаунта")
        print(user.id, token)

    async def on_after_forgot_password(
            self,
            user: User,
            token: str,
            request: Optional[Request] = None
    ) -> None:
        """
        Sends a verification email to the user to verify reset password
        """
        send_email.delay(user.username, user.email, token, "Восстановление пароля")


