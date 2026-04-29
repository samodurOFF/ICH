'''Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных, обработки
вложенных структур и сериализации. Система должна обрабатывать данные в формате JSON.

Задачи:
1. Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
2. Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic, валидирует данные, и в
случае успеха сериализует объект обратно в JSON и возвращает его.
3. Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
4. Написать несколько примеров JSON строк для проверки различных сценариев валидации: успешные регистрации и случаи,
когда валидация не проходит (например возраст не соответствует статусу занятости).

Модели:
Address: Должен содержать следующие поля:
city: строка, минимум 2 символа.
street: строка, минимум 3 символа.
house_number: число, должно быть положительным.

User: Должен содержать следующие поля:
name: строка, должна быть только из букв, минимум 2 символа.
age: число, должно быть между 0 и 120.
email: строка, должна соответствовать формату email.
is_employed: булево значение, статус занятости пользователя.
address: вложенная модель адреса.

Валидация:
Проверка, что если пользователь указывает, что он занят (is_employed = true), его возраст должен быть от 18 до 65
лет.

# Пример JSON данных для регистрации пользователя
json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
        }
    }"""
'''

from pydantic import BaseModel, ValidationError, Field, EmailStr, model_validator


class Address(BaseModel):
    city: str = Field(min_length=2, description='Min length 2 characters')
    street: str = Field(min_length=3, description='Min length 3 characters')
    house_number: int = Field(gt=0, description='Always positive integer')


class User(BaseModel):
    name: str = Field(pattern=r'^[a-zA-Zа-яА-Я -]+$', min_length=2, description='Only letters and min 2 characters')
    age: int = Field(gt=0, le=120, description='Between 0 and 120')
    email: EmailStr = Field(description='Email address format')
    is_employed: bool
    address: Address


    @model_validator(mode='after')
    def check_is_employed(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError("If user is employed, age must be between 18 and 65")
        return self


def data_validator(data):
    try:
        user = User.model_validate_json(data, strict=True)
        return user.model_dump_json()
    except ValidationError as err:
        return err.json()
    # except ValueError as err:
    #     print("ValueError error:", err)


if __name__ == '__main__':
    # valid
    # json_input = """{
    #     "name": "John Doe",
    #     "age": 70,
    #     "email": "john.doe@example.com",
    #     "is_employed": true,
    #     "address": {
    #         "city": "New York",
    #         "street": "5th Avenue",
    #         "house_number": 123
    #         }
    #     }"""

    json_input = """{
        "name": "Michael Johnson",
        "age": 52,
        "email": "mjohnson@gmail.com",
        "is_employed": false,
        "address": {
            "city": "New York",
            "street": "7th Avenue",
            "house_number": 25
            }
        }"""
    print('User registration is successful')
    print(data_validator(json_input))

    # invalid email and house_number
    # json_input = """{
    #     "name": "Barak Obama",
    #     "age": 61,
    #     "email": "@icloud.co",
    #     "is_employed": false,
    #     "address": {
    #         "city": "Washington",
    #         "street": "1",
    #         "house_number": "12a"
    #         }
    #     }"""

    # invalid age
    json_invalid = """{
        "name": "Timbuktu",
        "age": 70,
        "email": "tb@icloud.com",
        "is_employed": true,
        "address": {
            "city": "Boston",
            "street": "Baker Street",
            "house_number": 124
            }
        }"""
    print('User registration is not successful')
    print(data_validator(json_invalid))
