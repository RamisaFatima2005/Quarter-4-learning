##Why is the Agent class defined as a dataclass?

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
print(agent1)```
