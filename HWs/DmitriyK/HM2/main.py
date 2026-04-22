import pydantic
from pydantic import BaseModel, EmailStr, Field, model_validator

class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)

class User(BaseModel):
    name: str = Field(..., min_length=2, pattern=r"^[a-zA-Z\s]+$")
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode='after')
    def validate_employment_age(self) -> 'User':
        if self.is_employed:
            if not (18 <= self.age <= 65):
                raise ValueError(
                    f"Employed users must be between 18 and 65 years old. "
                    f"Current age provided: {self.age}"
                )
        return self


def process_user_registration(json_str: str) -> str:
    """
    Deserializes JSON, validates data using Pydantic,
    and serializes it back to JSON.
    """
    try:
        user = User.model_validate_json(json_str)
        return user.model_dump_json(indent=4)
    except pydantic.ValidationError as e:
        return f"Validation error: {e.json()}"

if __name__ == "__main__":
    success_json = """{
        "name": "John Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "Berlin",
            "street": "Friedrichstrasse",
            "house_number": 101
        }
    }"""

    failed_age_json = """{
        "name": "Old Working Man",
        "age": 70,
        "email": "oldman@example.com",
        "is_employed": true,
        "address": {"city": "Hamburg", "street": "Reeperbahn", "house_number": 5}
    }"""

    print("--- SUCCESS CASE ---")
    print(process_user_registration(success_json))

    print("\n--- FAILED CASE (Age 70 + Employed) ---")
    print(process_user_registration(failed_age_json))