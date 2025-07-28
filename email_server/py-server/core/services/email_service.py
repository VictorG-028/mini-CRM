import random
from typing import Any, Optional
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from fastapi import BackgroundTasks
from config.global_env_vars import (GOOGLE_SENDER_EMAIL) 
from core.ports.driving_ports import IEmailService
from core.ports.driven_ports import IEmailSender, ISenderBehaviorRepository, IUserRepository, ILogger
from core.domain.email import Email
from core.domain.user import User
from core.domain.sender_behavior_enum import SenderBehaviorEnum
from core.domain.template_catalog_enum import TemplateCatalogEnum
from core.domain.email_templates import DISCOUNT_CUPOM_TEMPLATE


CHANCE_HIGH = 0.85
CHANCE_MODERATE = 0.50
CHANCE_LOW = 0.25


class EmailService(IEmailService):
    def __init__(self, 
                 email_sender: IEmailSender, 
                 sender_behavior_repository: ISenderBehaviorRepository, 
                 user_repository: IUserRepository, 
                 logger: ILogger
                ):
        self._email_sender = email_sender
        self._sender_behavior_repository = sender_behavior_repository
        self._user_repository = user_repository
        self._logger = logger

    def send_emails(self, 
                    background_tasks: BackgroundTasks, 
                    count: int, 
                    subject: str, 
                    template_name: TemplateCatalogEnum, 
                    fill_values: dict[str, Any]
                    ) -> None:
        current_behavior = self._sender_behavior_repository.get_current_behavior()
        chance_to_send: float = None

        if current_behavior == SenderBehaviorEnum.NOT_DEFINED:
            users = self._user_repository.find_random_users(count)
            chance_to_send = 1.0
        elif current_behavior == SenderBehaviorEnum.BY_BIRTHDAY:
            users = self._user_repository.find_by_birthday(count)
            chance_to_send = 1.0
        elif current_behavior == SenderBehaviorEnum.LOW_CHANCE:
            users = self._user_repository.find_random_users(count)
            chance_to_send = CHANCE_LOW
        elif current_behavior == SenderBehaviorEnum.MODERATE_CHANCE:
            users = self._user_repository.find_random_users(count)
            chance_to_send = CHANCE_MODERATE
        elif current_behavior == SenderBehaviorEnum.HIGH_CHANCE:
            users = self._user_repository.find_random_users(count)
            chance_to_send = CHANCE_HIGH

        mime_email = self._generate_email_body(template_name, fill_values)
        # mime_email['Subject'] = subject
        # mime_email['To'] = "victor6g0@gmail.com"

        # background_tasks.add_task(
        #     self._send_emails_in_background, 
        #     background_tasks=background_tasks,
        #     users=users, 
        #     chance_to_send=chance_to_send,
        #     subject=subject,
        #     mime_email=mime_email
        # )
        self._send_emails_in_background(
            background_tasks=background_tasks,
            users=users, 
            chance_to_send=chance_to_send,
            subject=subject,
            mime_email=mime_email
        )
    

    def change_sender_behavior(self, new_behavior: SenderBehaviorEnum) -> None:
        self._sender_behavior_repository.update_behavior(new_behavior)
    
    def get_sender_behavior(self) -> SenderBehaviorEnum:
        return self._sender_behavior_repository.get_current_behavior()
    
    ############################################################################
    #### Private functions 

    def _generate_email_body(self, 
                             template_name: TemplateCatalogEnum, 
                             fill_values: dict[str, Any]
                             ) -> MIMEMultipart | MIMEText:
        """
        Chaining of if-else cases to select and return the generated 
        MimeText email as str.
        """

        if template_name == TemplateCatalogEnum.DISCOUNT_CUPOM:
            return self._generate_discount_email_body(
                fill_values['image_name'],
                fill_values['discount_value'],
                fill_values['cupom_code'],
                fill_values['valid_dates_start'],
                fill_values['valid_dates_end']
            )
        else:
            raise ValueError(f"Unknown template name: {template_name}")


    def _generate_discount_email_body(self, 
                                    #   subject: str, 
                                    #   to: str, 
                                      img_name: str,
                                      discount_value: int, 
                                      cupom_code: str, 
                                      valid_dates_start: date, 
                                      valid_dates_end: date
                                      ) -> MIMEMultipart:
        """
        Generate the email body for the discount email template.
        """

        msg = MIMEMultipart('related')
        msg['MIME-Version'] = '1.0'
        # msg['Subject'] = subject
        msg['From'] = GOOGLE_SENDER_EMAIL
        # msg['To'] = to
        
        email_html_body = DISCOUNT_CUPOM_TEMPLATE.format(
            cupom_code=cupom_code,
            discount_value=f"{discount_value}%",
            start_date=valid_dates_start.strftime("%d/%m/%Y"),
            end_date=valid_dates_end.strftime("%d/%m/%Y")
        )
        msg.attach(MIMEText(email_html_body, 'html', 'utf-8'))

        try:
            image_path = f'core/domain/template_images/{img_name}'
            with open(image_path, 'rb') as image_file:
                image_part = MIMEImage(image_file.read())
                image_part.add_header('Content-ID', '<promo_header>')
                msg.attach(image_part)
        except FileNotFoundError:
            self._logger.log_error(f"A imagem '{image_path}' não foi encontrada. O e-mail será enviado sem ela.")

        return msg
    

    def _send_emails_in_background(self,
                                   background_tasks: BackgroundTasks,
                                   users: list[User],
                                   chance_to_send: float,
                                   subject: str,
                                   mime_email: MIMEMultipart | MIMEText
                                   ) -> None:
        """
        Send emails asyncronously to give response early.
        """

        # succes_counter = 0
        for i, user in enumerate(users):

            if random.random() > chance_to_send:
                self._logger.log_info(f"Skipping email {i+1} due to chance threshold.")
                continue
            
            background_tasks.add_task(
                self._send_email_in_background,
                mime_email=mime_email,
                subject=subject,
                to=user.email
            )
            
            # if was_sent:
            #     succes_counter += 1

        # if succes_counter == 0:
        #     self._logger.log_info(f"Falha ao enviar todos os {count} e-mails.")
        # elif succes_counter < count:
        #     self._logger.log_info(f"Apenas {succes_counter}/{count} e-mails foram enviados com sucesso.")
        # else:
        #     self._logger.log_info(f"Todos os {count} e-mails foram enviados com sucesso.")
        

    def _send_email_in_background(self,
                                   mime_email: MIMEMultipart | MIMEText,
                                   subject: str,
                                   to: str
                                   ) -> bool:
        """
        Send emails asyncronously to give response early.
        """

        mime_email['Subject'] = subject
        mime_email['To'] = to
            
        was_sent = self._email_sender.send(mime_email, to)
        if was_sent:
            self._logger.log_info(f"Email sent successfully to {to}")
        else:
            self._logger.log_error(f"Failed to send email to {to}")

        return was_sent
