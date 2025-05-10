from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None  

# Valid data
user_data = {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25}
user = User(**user_data)
print(user)  
print(user.model_dump())  

# Invalid data 
try:
    invalid_user = User(id="not_an_int", name="Bob", email="bob@example.com")
except ValidationError as e:
    print(e)