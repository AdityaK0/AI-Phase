from pydantic import Field,BaseModel,EmailStr


class CreateUser(BaseModel):
    username : str = Field(..., description="The username of the user.",min_length=3,max_length=70)
    fullname: str = Field(..., description="The full name of the user.",min_length=2)
    email: EmailStr = Field(..., description="The email address of the user.")
    phone_number : str | None = Field(None, description="The phone number of the user.",min_length=10,max_length=15)
    password: str = Field(..., description="The password for the user account.",min_length=6,max_length=70)
    

class LoginSchema(BaseModel):
    username : str = Field(required=True,min_length=3,max_length=50)
    password : str = Field(required=True,min_length=6,max_length=70)