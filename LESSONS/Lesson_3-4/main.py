from datetime import datetime

from pydantic import BaseModel, EmailStr, ValidationError, Field, field_validator


class Address(BaseModel):
    city: str
    street: str
    house_number: int


class User(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    created_at: datetime = datetime.now()
    is_active: bool = True
    address: Address

    # old
    # class Config:
    #     str_min_length = 2
    #     str_strip_whitespace = True
    #     json_encoders = {
    #         datetime: lambda v: v.strftime('%y-%m-%d %H:%M')
    #     }

    model_config = dict(
        str_min_length=2,
        str_strip_whitespace=True,
        json_encoders={
            datetime: lambda v: v.strftime('%y-%m-%d %H:%M')
        }
    )

    @field_validator('email')
    def check_email_domain(cls, value):
        allowed_domains = ['example.com', 'test.com']
        email_domain = value.split('@')[-1]
        if email_domain not in allowed_domains:
            raise ValueError(f"Email must be from one of the following domains: {', '.join(allowed_domains)}")
        return value

    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

    def __str__(self):
        return f"User {self.name}, {self.age} years old. Email: {self.email}. City: {self.address.city}"


class AdminUser(User):
    is_superuser: bool
    access_level: int

    def __str__(self):
        return f"Admin {self.name}, Email: {self.email}, Access Level: {self.access_level}"

    def promote_user(self):
        # print(f"Promoting {self.name} to higher privileges")
        self.access_level = self.access_level + 1


class Item(BaseModel):
    is_available: bool = Field(default=True, alias="available", description="Whether the item is available for order")
    price: float = Field(default=0.0, gt=0, description="The price of the item must be greater than zero")


if __name__ == '__main__':
    # item = Item(available=False, price=0.0)
    # print(item.is_available)
    # # print(item.available)
    # print(item.price)
    # item.price = 10
    # print(item.price)
    # item.price = 0.0
    # print(item.price)

    json_string = """{
        "id": 1,
        "name": "John Doe",
        "age": 22,
        "email": "john.doe@test.com",
        "is_active": false,
        "is_superuser": false,
        "access_level": 0,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""

    # user = User.model_validate_json(json_string,
    #                                 strict=True
    #                                 )  # Десериализация
    admin = AdminUser.model_validate_json(json_string,
                                          strict=True)
    print(admin.__repr__)
    # # print(user.id, type(user.id))
    print(admin.model_dump_json())  # сериализация
    # print(admin.greet())
    # print(admin.access_level)
    # admin.promote_user()
    # print(admin.access_level)
