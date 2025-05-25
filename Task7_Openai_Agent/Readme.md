**1. Why is the Agent class defined as a dataclass?**

The @dataclass in Python makes it easier to create classes that store data. It automatically adds common functions like:

- __init__() – to create the object

- __repr__() – to display the object nicely

- __eq__() – to compare two objects

This saves time and keeps the code simple and clean.

## Example Without @dataclass:

```class Agent:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Agent(name={self.name}, age={self.age})"

agent1 = Agent("Ali", 25)
print(agent1)
```

## Example With @dataclass:

```from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    age: int

agent1 = Agent("Ali", 25)
print(agent1)
```

Both examples give the same result, but the second one is much shorter and easier to read - that's the power of @dataclass!


**2a. Why is the system prompt in the Agent class? And why can it be callable?**

The system prompt gives instructions to the Agent - like how it should behave or answer. We keep it inside the Agent class so everything about the Agent is in one place.

We make the Agent callable so we can use it like a function:

```response = agent("Hello")
```

This is shorter and easier than writing a full method name.

## Easy Example:

```class Agent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def __call__(self, message):
        return f"{self.system_prompt} | Message: {message}"

agent = Agent("Helper", "Be friendly")
print(agent("How are you?"))
```
### Output:
Be friendly | Message: How are you?


**2b. Why is the user prompt passed as a parameter in the run method of Runner, and why is run a classmethod?**

The user prompt is the message or question from the user. It is passed as a parameter so the Runner knows what the user wants to ask or say.

The run method is a classmethod because it can be called without creating an object of the class. It works directly with the class itself.

## Simple Example:
```class Runner:
    @classmethod
    def run(cls, user_prompt):
        return f"User asked: {user_prompt}"

print(Runner.run("What is AI?"))
```
### Output:
User asked: What is AI?


**3. What is the purpose of the Runner class?**

The Runner class is used to control the process of running the Agent. It acts like a manager that:

- Takes the user prompt (message or question),

- Sends it to the Agent,

- And returns the final response.

It helps keep the code clean and organized by separating the logic of handling user input and getting a response.

## Simple Example:
```lass Agent:
    def __call__(self, message):
        return f"Agent says: {message}"

class Runner:
    agent = Agent()

    @classmethod
    def run(cls, user_prompt):
        return cls.agent(user_prompt)

print(Runner.run("Hello, how are you?"))
```

### Output:
Agent says: Hello, how are you?


So, the Runner is like a helper that runs the whole process smoothly.

**4. What are Generics in Python? Why do we use Generics for TContext?**

## Generics

Generics in Python help us write flexible and reusable code. They allow us to create functions or classes that can work with any data type, not just one specific type.

Python supports generics using TypeVar from the typing module.

## Use Generics for TContext

We use a generic like TContext when we don’t know the exact type of data the context will hold. This makes the code:

- Reusable for different types of context data

- Type-safe, meaning Python can help check for type errors

- Clear, as we can define what kind of data to expect

## Simple Example:
```from typing import TypeVar, Generic

TContext = TypeVar('TContext')

class Agent(Generic[TContext]):
    def __init__(self, context: TContext):
        self.context = context

# Now we can use any type for context
agent1 = Agent(context={"name": "Ali"})  # context is a dict
agent2 = Agent(context="Admin")          # context is a string
```
