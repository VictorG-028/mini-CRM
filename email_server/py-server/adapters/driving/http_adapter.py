from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, PastDate, field_validator, FieldValidationInfo
from datetime import date, datetime
from core.ports.driving_ports import IEmailService, IUserService
from core.domain.sender_behavior_enum import SenderBehaviorEnum
from core.domain.template_catalog_enum import TemplateCatalogEnum
from typing import Any, Literal, Optional, Union
from typing_extensions import Annotated
from uuid import UUID

################################################################################
#### Modelos Pydantic para validação de entrada

class UserCreateRequest(BaseModel):
    client_full_name: str = Field(min_length=3, description="Full name of the client.")
    birth_date: PastDate = Field(description="Client's birth date (DD-MM-YYYY).")
    email: EmailStr = Field(description="Client's email address (must be unique).", pattern=r"[^@]+@[^@]+\.[^@]+")
    telephone: Optional[str] = Field(None, description="Client's telephone number.", pattern=r"^\+?\d{9,14}$")
    cpf: str = Field(pattern=r"^\d{11}$", description="Client's CPF (must be unique, 11 digits).")

    class Config:
        extra = "forbid"
    
    # @field_validator("birth_date")
    # @classmethod
    # def parse_birth_date(cls, value) -> date:
    #     if isinstance(value, date):
    #         return value
        
    #     try:
    #         return datetime.strptime(value, "%d/%m/%Y").date()
    #     except ValueError:
    #         raise ValueError("Formato de data inválido. Use DD/MM/YYYY.")


class UserUpdateRequest(BaseModel):
    client_full_name: Optional[str] = Field(None, min_length=3, description="Full name of the client.")
    birth_date: Optional[PastDate] = Field(None, description="Client's birth date (YYYY-MM-DD).")
    email: Optional[EmailStr]= Field(None, description="Client's email address (must be unique).")
    telephone: Optional[str] = Field(None, description="Client's telephone number.")
    cpf: Optional[str] = Field(None, pattern=r"^\d{11}$", description="Client's CPF (must be unique, 11 digits).")

    class Config:
        extra = "forbid"

class DiscountCupomFillValues(BaseModel):
    email_template: Literal[TemplateCatalogEnum.DISCOUNT_CUPOM] = TemplateCatalogEnum.DISCOUNT_CUPOM
    image_name: str = Field("discount_cupom_header.png", description="Image to be used in the email header.")
    discount_value: int = Field(..., gt=0, le=100, description="Discount percentage (0 to 100).")
    cupom_code: str = Field(..., description="Human-readable coupon code.")
    valid_dates_start: date = Field(..., description="Coupon valid from date (YYYY-MM-DD).")
    valid_dates_end: date = Field(..., description="Coupon valid until date (YYYY-MM-DD).")

    @field_validator("valid_dates_end")
    @classmethod
    def check_image_has_extension(cls, value: date, info: FieldValidationInfo) -> date:
        if not info.data['image_name'].endswith(('.png', '.jpg', '.jpeg')):
            raise ValueError("Image must be a PNG or JPG|JPEG file.")
        return value
    
    @field_validator("valid_dates_end")
    @classmethod
    def check_end_date_after_start_date(cls, value: date, info: FieldValidationInfo) -> date:
        if value < info.data['valid_dates_start']:
            raise ValueError("End date must be after start date.")
        return value
    
    class Config:
        extra = "forbid"

class SendEmailsReqBody(BaseModel):
    email_template: TemplateCatalogEnum = Field("discount_cupom", description="What email template to use.")
    subject: str = Field(..., description="Subject of the email to be sent.")
    template_fill_values: Annotated[
        Union[
            DiscountCupomFillValues,
            # Add here a new element to this Union list defining fill values as needed (don't remove this comment)
        ],
        Field(discriminator='email_template', description="Template name to determine which fill values to use.")
    ] = Field(None, description="Dictionary of values to fill the template.")

    class Config:
        use_enum_values = True
        extra = "forbid"

class SenderBehaviorUpdateRequest(BaseModel):
    strategy: SenderBehaviorEnum = Field(description="Unique name for the sender behavior.")

    class Config:
        use_enum_values = False

################################################################################
#### Endpoints mapping

class HTTPAdapter:
    def __init__(self, email_service: IEmailService, user_service: IUserService):
        self._email_service = email_service
        self._user_service = user_service
        self.router = APIRouter()

        # Endpoints de Usuário
        self.router.post("/users", status_code=status.HTTP_201_CREATED)(self.create_user_endpoint)
        self.router.get("/users/total", status_code=status.HTTP_200_OK)(self.get_total_users_endpoint)
        self.router.put("/users/{user_id}", status_code=status.HTTP_200_OK)(self.update_user_endpoint)
        self.router.get("/users/{user_id}", status_code=status.HTTP_200_OK)(self.get_user_by_id_endpoint)
        

        # Endpoints de E-mail
        self.router.post("/emails/send-emails", status_code=status.HTTP_202_ACCEPTED)(self.send_emails_endpoint)
        self.router.patch("/emails/behavior", status_code=status.HTTP_200_OK)(self.change_sender_behavior_endpoint)
        self.router.get("/emails/behavior", status_code=status.HTTP_200_OK)(self.get_sender_behavior_endpoint)

    ############################################################################
    #### --- User Endpoints ---

    async def create_user_endpoint(self, user_request: UserCreateRequest):
        try:
            user = self._user_service.create_user(user_request.model_dump())
            return {"message": "User created successfully", "user_id": user._id}
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create user: {e}")

    async def update_user_endpoint(self, user_id: UUID, user_request: UserUpdateRequest):
        # user_request.dict(exclude_unset=True) envia apenas campos que foram setados na requisição
        if not user_request.model_dump(exclude_unset=True):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided for update")
        try:
            user = self._user_service.update_user(user_id, user_request.model_dump(exclude_unset=True))
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return {"message": "User updated successfully", "user_id": user._id}
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update user: {e}")

    async def get_user_by_id_endpoint(self, user_id: UUID):
        user = self._user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user.to_dict()

    async def get_total_users_endpoint(self):
        total_users = self._user_service.get_total_users()
        return {"total_users": total_users}

    ############################################################################
    #### --- Email Endpoints ---

    async def send_emails_endpoint(self, request_body: SendEmailsReqBody, background_tasks: BackgroundTasks):
        try:
            self._email_service.send_emails(
                background_tasks=background_tasks,
                count=1, 
                subject=request_body.subject,
                template_name=request_body.email_template, 
                fill_values=request_body.template_fill_values.model_dump()
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to send emails: {e}")
        
        return {"message": "Emails sent successfully"}


    async def change_sender_behavior_endpoint(self, request_body: SenderBehaviorUpdateRequest):
        self._email_service.change_sender_behavior(request_body.strategy)
        return {"message": f"Sender behavior was updated to '{request_body.strategy}'."}

    async def get_sender_behavior_endpoint(self):
        behavior = self._email_service.get_sender_behavior()
        return {"strategy": behavior.value}
