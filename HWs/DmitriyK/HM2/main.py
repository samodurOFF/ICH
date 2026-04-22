import pydantic
from pydantic import (BaseModel, EmailStr, Field,
                      field_validator)


class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    name: str = Field(..., min_length=2, pattern=r"^[a-zA-Z]+$")
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool = Field(...)
    address: Address

    @field_validator("age")
    def validate_age_and_employment(cls, value: int, info):
        is_working = info.data.get("is_employed")

        if is_working is True and value < 18:
            raise ValueError(
                "A user under 18 years of age cannot have the status 'employed'"
            )

        return value


def process_user_registration(json_str: str):
    try:
        user = User.model_validate_json(json_str)
        return user.model_dump_json()
    except pydantic.ValidationError as e:
        return f"Validation error: {e.json()}"


if __name__ == "__main__":
    good_json = """
    {
        "name": "Bob",
        "age": 25,
        "email": "bob@example.com",
        "is_employed": true,
        "address": {
            "city": "Berlin",
            "street": "Strasse",
            "house_number": 10
        }
    }
    """

    bad_age_json = """
    {
        "name": "Alex",
        "age": 15,
        "email": "alex@example.com",
        "is_employed": true,
        "address": {"city": "Munich", "street": "Strasse", "house_number": 5}
    }
    """

    bad_name_json = """
    {
        "name": "Tom",
        "age": 20,
        "email": "tom@example.com",
        "is_employed": false,
        "address": {"city": "Berlin", "street": "Strasse", "house_number": 1}
    }
    """

    print("--- Successful registration ---")
    print(process_user_registration(good_json))

    print("\n--- Error (age + job) ---")
    print(process_user_registration(bad_age_json))

    print("\n--- Error (name with numbers) ---")
    print(process_user_registration(bad_name_json))
