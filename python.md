# Python Scripting Guide

## Table of Contents
1. [Introduction to Python](#introduction-to-python)
2. [Basic Syntax](#basic-syntax)
3. [Data Types](#data-types)
4. [Control Flow](#control-flow)
5. [Functions](#functions)
6. [File Operations](#file-operations)
7. [Error Handling](#error-handling)
8. [Modules and Packages](#modules-and-packages)
9. [Object-Oriented Programming](#object-oriented-programming)
10. [Common Libraries](#common-libraries)
11. [Best Practices](#best-practices)

---

## Introduction to Python

Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used for:
- Web development
- Data science and machine learning
- Automation and scripting
- DevOps and system administration
- API development

### Why Python?
- **Easy to learn**: Clean and readable syntax
- **Versatile**: Can be used for almost anything
- **Large ecosystem**: Extensive standard library and third-party packages
- **Cross-platform**: Runs on Windows, Linux, macOS

---

## Basic Syntax

### Hello World
```python
# This is a comment
print("Hello, World!")
```

### Variables and Assignment
```python
# Variables don't need type declaration
name = "John"
age = 30
height = 5.9
is_student = True

# Multiple assignment
x, y, z = 1, 2, 3

# Swapping values
a, b = 10, 20
a, b = b, a  # Now a=20, b=10
```

### Input from User
```python
# Get user input (always returns string)
name = input("Enter your name: ")
age = int(input("Enter your age: "))  # Convert to integer

print(f"Hello {name}, you are {age} years old")
```

---

## Data Types

### Strings
```python
# String creation
text = "Hello, World!"
multiline = """This is
a multiline
string"""

# String operations
name = "john doe"
print(name.upper())           # JOHN DOE
print(name.capitalize())      # John doe
print(name.title())           # John Doe
print(name.replace("john", "Jane"))  # Jane doe

# String slicing
text = "Python Programming"
print(text[0:6])    # Python
print(text[:6])     # Python
print(text[7:])     # Programming
print(text[-4:])    # ming

# String formatting
name = "Alice"
age = 25
print(f"My name is {name} and I'm {age} years old")  # f-string (Python 3.6+)
print("My name is {} and I'm {} years old".format(name, age))
print("My name is %s and I'm %d years old" % (name, age))

# String methods
text = "  Python  "
print(text.strip())           # Remove whitespace
print(text.split())           # Split into list
print("-".join(["a", "b", "c"]))  # Join list into string
```

### Lists
```python
# List creation
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# Accessing elements
print(fruits[0])      # apple
print(fruits[-1])     # cherry (last element)

# List methods
fruits.append("orange")           # Add to end
fruits.insert(1, "mango")        # Insert at position
fruits.remove("banana")          # Remove by value
popped = fruits.pop()            # Remove and return last item
fruits.extend(["grape", "melon"])  # Add multiple items

# List operations
numbers = [1, 2, 3]
doubled = [x * 2 for x in numbers]  # List comprehension: [2, 4, 6]
evens = [x for x in numbers if x % 2 == 0]  # Filter evens

# Slicing
numbers = [0, 1, 2, 3, 4, 5]
print(numbers[1:4])   # [1, 2, 3]
print(numbers[::2])   # [0, 2, 4] (every 2nd element)
print(numbers[::-1])  # [5, 4, 3, 2, 1, 0] (reverse)

# Sorting
numbers = [3, 1, 4, 1, 5, 9, 2]
numbers.sort()        # Sort in place
sorted_nums = sorted(numbers)  # Return new sorted list
```

### Tuples
```python
# Tuples are immutable (cannot be changed)
coordinates = (10, 20)
rgb = (255, 0, 128)

# Unpacking
x, y = coordinates
r, g, b = rgb

# Tuple with one element (note the comma)
single = (5,)
```

### Dictionaries
```python
# Dictionary creation
person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Accessing values
print(person["name"])           # John
print(person.get("age"))        # 30
print(person.get("country", "USA"))  # Default value if key doesn't exist

# Adding/updating
person["email"] = "john@example.com"
person["age"] = 31

# Dictionary methods
print(person.keys())     # Get all keys
print(person.values())   # Get all values
print(person.items())    # Get key-value pairs

# Iterating
for key, value in person.items():
    print(f"{key}: {value}")

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Sets
```python
# Sets contain unique elements
numbers = {1, 2, 3, 4, 5}
fruits = {"apple", "banana", "cherry"}

# Set operations
numbers.add(6)
numbers.remove(3)

# Set math operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b)  # Union: {1, 2, 3, 4, 5, 6}
print(a & b)  # Intersection: {3, 4}
print(a - b)  # Difference: {1, 2}
```

---

## Control Flow

### If-Else Statements
```python
# Basic if-else
age = 18
if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

# If-elif-else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

# Ternary operator
status = "adult" if age >= 18 else "minor"

# Multiple conditions
x = 10
if x > 5 and x < 15:
    print("x is between 5 and 15")

if x < 0 or x > 100:
    print("x is out of range")
```

### Loops

#### For Loops
```python
# Iterate over list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterate with index
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Range function
for i in range(5):          # 0 to 4
    print(i)

for i in range(2, 10):      # 2 to 9
    print(i)

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8
    print(i)

# Iterate over dictionary
person = {"name": "John", "age": 30}
for key in person:
    print(f"{key}: {person[key]}")

for key, value in person.items():
    print(f"{key}: {value}")
```

#### While Loops
```python
# Basic while loop
count = 0
while count < 5:
    print(count)
    count += 1

# While with break
while True:
    user_input = input("Enter 'quit' to exit: ")
    if user_input == "quit":
        break
    print(f"You entered: {user_input}")

# While with continue
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)
```

---

## Functions

### Basic Functions
```python
# Simple function
def greet():
    print("Hello!")

greet()

# Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")

# Function with return value
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8

# Multiple return values
def get_min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([1, 2, 3, 4, 5])
```

### Default Parameters
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))              # Hello, Alice!
print(greet("Bob", "Hi"))          # Hi, Bob!
```

### Keyword Arguments
```python
def create_profile(name, age, city="Unknown"):
    return f"{name}, {age} years old, from {city}"

print(create_profile("John", 30))
print(create_profile(name="Alice", city="NYC", age=25))
```

### Variable-Length Arguments
```python
# *args for variable positional arguments
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3))        # 6
print(sum_all(1, 2, 3, 4, 5))  # 15

# **kwargs for variable keyword arguments
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="John", age=30, city="NYC")
```

### Lambda Functions
```python
# Anonymous functions
square = lambda x: x ** 2
print(square(5))  # 25

add = lambda x, y: x + y
print(add(3, 4))  # 7

# Used with map, filter, sorted
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Sorting with lambda
people = [("John", 30), ("Alice", 25), ("Bob", 35)]
sorted_by_age = sorted(people, key=lambda x: x[1])
```

---

## Advanced Functions

### Decorators
```python
# Basic decorator
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Before function call
# Hello!
# After function call

# Decorator with arguments
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Prints "Hello, Alice!" three times

# Timing decorator
import time
from functools import wraps

def timer(func):
    @wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    return "Done"

# Logging decorator
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

# Caching decorator (memoization)
def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(100))  # Much faster with memoization

# Class-based decorator
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hi():
    print("Hi!")

say_hi()  # Call 1 of say_hi
say_hi()  # Call 2 of say_hi
```

### Generators
```python
# Basic generator
def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1

counter = count_up_to(5)
for num in counter:
    print(num)  # 1, 2, 3, 4, 5

# Generator expression
squares = (x**2 for x in range(10))
print(list(squares))

# Fibonacci generator
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for _ in range(10):
    print(next(fib))

# Reading large files efficiently
def read_large_file(file_path):
    """Read file line by line without loading entire file into memory"""
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# Using generators with pipeline pattern
def filter_lines(lines, pattern):
    for line in lines:
        if pattern in line:
            yield line

def uppercase_lines(lines):
    for line in lines:
        yield line.upper()

# Pipeline usage
lines = read_large_file('data.txt')
filtered = filter_lines(lines, 'ERROR')
uppercased = uppercase_lines(filtered)
for line in uppercased:
    print(line)

# Generator for infinite sequences
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

# Send values to generators
def echo():
    while True:
        received = yield
        print(f"Received: {received}")

gen = echo()
next(gen)  # Prime the generator
gen.send("Hello")
gen.send("World")
```

### Closures
```python
# Basic closure
def outer_function(msg):
    def inner_function():
        print(msg)
    return inner_function

my_func = outer_function("Hello!")
my_func()  # Hello!

# Closure with state
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter1 = counter()
print(counter1())  # 1
print(counter1())  # 2
print(counter1())  # 3

# Closure factory
def make_multiplier(x):
    def multiplier(n):
        return x * n
    return multiplier

times3 = make_multiplier(3)
times5 = make_multiplier(5)

print(times3(10))  # 30
print(times5(10))  # 50

# Closure for data privacy
def create_account(initial_balance):
    balance = initial_balance
    
    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance
    
    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return "Insufficient funds"
        balance -= amount
        return balance
    
    def get_balance():
        return balance
    
    return {
        'deposit': deposit,
        'withdraw': withdraw,
        'balance': get_balance
    }

account = create_account(1000)
print(account['deposit'](500))    # 1500
print(account['withdraw'](200))   # 1300
print(account['balance']())       # 1300
```

### Partial Functions
```python
from functools import partial

# Create specialized functions from general ones
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# Partial with multiple arguments
def log_message(message, level, timestamp):
    print(f"[{timestamp}] {level}: {message}")

from datetime import datetime
error_log = partial(log_message, level="ERROR", timestamp=datetime.now())
info_log = partial(log_message, level="INFO", timestamp=datetime.now())

error_log("Something went wrong")
info_log("Application started")

# Partial in real-world scenarios
from functools import partial
import requests

def api_call(endpoint, base_url, method="GET", **kwargs):
    url = f"{base_url}/{endpoint}"
    return requests.request(method, url, **kwargs)

# Create specialized API callers
github_api = partial(api_call, base_url="https://api.github.com")
get_user = partial(github_api, method="GET")

# Usage
response = get_user("users/octocat")
```

### Higher-Order Functions
```python
# Functions that take functions as arguments
def apply_operation(numbers, operation):
    return [operation(x) for x in numbers]

def square(x):
    return x ** 2

def cube(x):
    return x ** 3

numbers = [1, 2, 3, 4, 5]
print(apply_operation(numbers, square))  # [1, 4, 9, 16, 25]
print(apply_operation(numbers, cube))    # [1, 8, 27, 64, 125]

# Compose functions
def compose(*functions):
    def inner(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return inner

def add_five(x):
    return x + 5

def multiply_two(x):
    return x * 2

def square(x):
    return x ** 2

# Compose: square(multiply_two(add_five(x)))
composed = compose(square, multiply_two, add_five)
print(composed(3))  # ((3 + 5) * 2) ** 2 = 256

# Map, Filter, Reduce
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Map: Apply function to each element
squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# Filter: Keep elements that match condition
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# Reduce: Reduce list to single value
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

product = reduce(lambda x, y: x * y, numbers)
print(product)  # 120

# Advanced: Chain operations
result = reduce(
    lambda x, y: x + y,
    map(lambda x: x**2,
        filter(lambda x: x % 2 == 0, numbers)
    )
)
print(result)  # Sum of squares of even numbers: 4 + 16 = 20
```

### Recursion with Memoization
```python
# Basic recursion
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120

# Recursion with memoization
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(100))  # Very fast with caching

# Manual memoization
def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def expensive_recursive_function(n):
    if n <= 1:
        return 1
    return expensive_recursive_function(n-1) + expensive_recursive_function(n-2)

# Tail recursion (Python doesn't optimize this, but good to know)
def factorial_tail(n, accumulator=1):
    if n <= 1:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)

# Tree traversal with recursion
def traverse_dict(d, level=0):
    """Recursively traverse nested dictionary"""
    for key, value in d.items():
        print("  " * level + str(key))
        if isinstance(value, dict):
            traverse_dict(value, level + 1)
        else:
            print("  " * (level + 1) + str(value))

nested = {
    'a': 1,
    'b': {
        'c': 2,
        'd': {
            'e': 3
        }
    }
}
traverse_dict(nested)
```

### Context Managers (Advanced)
```python
from contextlib import contextmanager

# Function-based context manager
@contextmanager
def file_manager(filename, mode):
    print(f"Opening {filename}")
    file = open(filename, mode)
    try:
        yield file
    finally:
        print(f"Closing {filename}")
        file.close()

with file_manager("test.txt", "w") as f:
    f.write("Hello, World!")

# Timer context manager
@contextmanager
def timer(name):
    import time
    start = time.time()
    yield
    end = time.time()
    print(f"{name} took {end - start:.4f} seconds")

with timer("My operation"):
    time.sleep(1)
    print("Doing work...")

# Multiple context managers
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        outfile.write(line.upper())

# Suppressing exceptions
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("file_that_might_not_exist.txt")

# Redirect stdout
from contextlib import redirect_stdout
import io

f = io.StringIO()
with redirect_stdout(f):
    print("This goes to the string buffer")
    print("Not to console")

output = f.getvalue()
print(output)  # Now print to console
```

### Function Introspection
```python
import inspect

def example_function(a, b, c=10, *args, **kwargs):
    """This is an example function"""
    return a + b + c

# Get function signature
sig = inspect.signature(example_function)
print(sig)  # (a, b, c=10, *args, **kwargs)

# Get function parameters
for param in sig.parameters.values():
    print(f"{param.name}: {param.default}")

# Get function source code
source = inspect.getsource(example_function)
print(source)

# Get function documentation
print(example_function.__doc__)
print(example_function.__name__)

# Check if callable
print(callable(example_function))  # True

# Get function annotations
def typed_function(x: int, y: str) -> bool:
    return True

print(typed_function.__annotations__)
# {'x': <class 'int'>, 'y': <class 'str'>, 'return': <class 'bool'>}
```

### Async Functions (asyncio)
```python
import asyncio

# Basic async function
async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Run async function
asyncio.run(say_hello())

# Multiple async tasks
async def fetch_data(id):
    print(f"Fetching data {id}...")
    await asyncio.sleep(2)
    return f"Data {id}"

async def main():
    # Run concurrently
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    print(results)

asyncio.run(main())

# Async context manager
class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource")
        await asyncio.sleep(1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        await asyncio.sleep(1)

async def use_resource():
    async with AsyncResource() as resource:
        print("Using resource")

# Async iterator
class AsyncCounter:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current < self.stop:
            await asyncio.sleep(0.1)
            self.current += 1
            return self.current
        raise StopAsyncIteration

async def count():
    async for number in AsyncCounter(5):
        print(number)

asyncio.run(count())
```

### Property Decorators and Descriptors
```python
# Property decorator
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

temp = Temperature(25)
print(temp.celsius)      # 25
print(temp.fahrenheit)   # 77.0
temp.fahrenheit = 100
print(temp.celsius)      # 37.77...

# Descriptor protocol
class Validator:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be <= {self.max_value}")
        obj.__dict__[self.name] = value

class Person:
    age = Validator(min_value=0, max_value=150)
    
    def __init__(self, age):
        self.age = age

person = Person(25)
print(person.age)  # 25
# person.age = 200  # Raises ValueError
```

---

## File Operations

### Reading Files
```python
# Read entire file
with open("file.txt", "r") as file:
    content = file.read()
    print(content)

# Read line by line
with open("file.txt", "r") as file:
    for line in file:
        print(line.strip())

# Read all lines into list
with open("file.txt", "r") as file:
    lines = file.readlines()

# Read specific number of characters
with open("file.txt", "r") as file:
    chunk = file.read(100)  # Read first 100 characters
```

### Writing Files
```python
# Write to file (overwrites existing content)
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is a new line.\n")

# Append to file
with open("output.txt", "a") as file:
    file.write("This line is appended.\n")

# Write multiple lines
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)
```

### Working with CSV Files
```python
import csv

# Read CSV
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# Read CSV as dictionary
with open("data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["name"], row["age"])

# Write CSV
data = [
    ["name", "age", "city"],
    ["John", 30, "NYC"],
    ["Alice", 25, "LA"]
]

with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)
```

### Working with JSON
```python
import json

# Read JSON
with open("data.json", "r") as file:
    data = json.load(file)

# Write JSON
data = {
    "name": "John",
    "age": 30,
    "city": "NYC"
}

with open("output.json", "w") as file:
    json.dump(data, file, indent=4)

# Convert between JSON string and Python object
json_string = '{"name": "John", "age": 30}'
python_obj = json.loads(json_string)
json_back = json.dumps(python_obj)
```

---

## Error Handling

### Try-Except
```python
# Basic exception handling
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print(result)
except ValueError:
    print("Invalid input! Please enter a number.")
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Catch multiple exceptions
try:
    # Some code
    pass
except (ValueError, TypeError) as e:
    print(f"Error: {e}")

# Catch all exceptions
try:
    # Some code
    pass
except Exception as e:
    print(f"An error occurred: {e}")

# Try-except-else-finally
try:
    file = open("file.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found!")
else:
    print("File read successfully")
    print(content)
finally:
    if 'file' in locals():
        file.close()
    print("Cleanup completed")
```

### Raising Exceptions
```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

# Custom exception
class CustomError(Exception):
    pass

def validate_age(age):
    if age < 0:
        raise CustomError("Age cannot be negative!")
    return True
```

---

## Modules and Packages

### Importing Modules
```python
# Import entire module
import math
print(math.sqrt(16))

# Import specific functions
from math import sqrt, pi
print(sqrt(16))
print(pi)

# Import with alias
import numpy as np
import pandas as pd

# Import all (not recommended)
from math import *
```

### Creating Your Own Module
```python
# mymodule.py
def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

PI = 3.14159

# main.py
import mymodule

print(mymodule.greet("Alice"))
print(mymodule.add(5, 3))
print(mymodule.PI)
```

### Common Built-in Modules
```python
# os - Operating system interface
import os
print(os.getcwd())           # Current directory
os.mkdir("new_folder")       # Create directory
os.listdir(".")              # List directory contents

# sys - System-specific parameters
import sys
print(sys.version)           # Python version
print(sys.argv)              # Command line arguments

# datetime - Date and time
from datetime import datetime, timedelta
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
tomorrow = now + timedelta(days=1)

# random - Random number generation
import random
print(random.randint(1, 10))       # Random integer
print(random.choice(["a", "b", "c"]))  # Random choice
random.shuffle([1, 2, 3, 4, 5])    # Shuffle list

# re - Regular expressions
import re
pattern = r'\d+'
text = "There are 123 apples and 456 oranges"
numbers = re.findall(pattern, text)  # ['123', '456']
```

---

## Object-Oriented Programming

### Classes and Objects
```python
# Basic class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, my name is {self.name}"
    
    def birthday(self):
        self.age += 1

# Create object
person = Person("John", 30)
print(person.greet())
person.birthday()
print(person.age)
```

### Class Variables and Methods
```python
class Employee:
    # Class variable
    company = "ABC Corp"
    num_employees = 0
    
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.num_employees += 1
    
    def get_info(self):
        return f"{self.name} works at {self.company}"
    
    @classmethod
    def set_company(cls, new_company):
        cls.company = new_company
    
    @staticmethod
    def is_workday(day):
        return day.weekday() < 5

emp1 = Employee("John", 50000)
emp2 = Employee("Alice", 60000)
print(Employee.num_employees)  # 2
```

### Inheritance
```python
# Parent class
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass

# Child classes
class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

dog = Dog("Buddy")
cat = Cat("Whiskers")
print(dog.speak())
print(cat.speak())
```

### Special Methods (Magic Methods)
```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', {self.pages})"
    
    def __len__(self):
        return self.pages
    
    def __eq__(self, other):
        return self.title == other.title and self.author == other.author

book = Book("Python Crash Course", "Eric Matthes", 544)
print(str(book))
print(len(book))
```

---

## Common Libraries

### Requests (HTTP Library)
```python
import requests

# GET request
response = requests.get("https://api.github.com")
print(response.status_code)
print(response.json())

# POST request
data = {"key": "value"}
response = requests.post("https://example.com/api", json=data)

# With headers
headers = {"Authorization": "Bearer token"}
response = requests.get("https://api.example.com", headers=headers)
```

### Argparse (Command-Line Arguments)
```python
import argparse

parser = argparse.ArgumentParser(description="Process some data")
parser.add_argument("filename", help="Input file name")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
parser.add_argument("-o", "--output", default="output.txt", help="Output file")

args = parser.parse_args()
print(f"Processing {args.filename}")
if args.verbose:
    print("Verbose mode enabled")
```

### Subprocess (Running Shell Commands)
```python
import subprocess

# Run command and capture output
result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
print(result.stdout)
print(result.returncode)

# Run with shell
result = subprocess.run("echo Hello", shell=True, capture_output=True, text=True)

# Check if command succeeded
try:
    subprocess.run(["ls", "nonexistent"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed with exit code {e.returncode}")
```

---

## Best Practices

### Code Style (PEP 8)
```python
# Good naming conventions
user_name = "john"          # Variables: lowercase with underscores
USER_CONSTANT = 100         # Constants: uppercase with underscores

class MyClass:              # Classes: PascalCase
    pass

def my_function():          # Functions: lowercase with underscores
    pass

# Proper spacing
x = 1 + 2                   # Space around operators
my_list = [1, 2, 3]         # Space after commas
my_function(arg1, arg2)     # Space after commas in function calls

# Line length: Max 79 characters
# Use line continuation for long lines
total = (first_variable + second_variable +
         third_variable + fourth_variable)
```

### Documentation
```python
def calculate_area(radius):
    """
    Calculate the area of a circle.
    
    Args:
        radius (float): The radius of the circle
    
    Returns:
        float: The area of the circle
    
    Raises:
        ValueError: If radius is negative
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return 3.14159 * radius ** 2
```

### List Comprehensions vs. Loops
```python
# Instead of:
squares = []
for x in range(10):
    squares.append(x**2)

# Use:
squares = [x**2 for x in range(10)]

# Conditional comprehension
evens = [x for x in range(10) if x % 2 == 0]
```

### Context Managers
```python
# Always use 'with' for file operations
with open("file.txt", "r") as file:
    content = file.read()
# File is automatically closed

# Create custom context manager
class MyContext:
    def __enter__(self):
        print("Entering context")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")

with MyContext() as ctx:
    print("Inside context")
```

### Type Hints (Python 3.5+)
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add_numbers(a: int, b: int) -> int:
    return a + b

from typing import List, Dict, Optional

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def find_user(user_id: int) -> Optional[str]:
    # Returns string or None
    return None
```

### Virtual Environments
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install packages
pip install requests pandas

# Save dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

---

## Practical Examples

### Script 1: Log File Parser
```python
#!/usr/bin/env python3
"""
Parse log files and extract error messages
"""
import re
from collections import Counter

def parse_log_file(filename):
    error_pattern = r'ERROR: (.+)'
    errors = []
    
    with open(filename, 'r') as file:
        for line in file:
            match = re.search(error_pattern, line)
            if match:
                errors.append(match.group(1))
    
    return errors

def main():
    errors = parse_log_file('application.log')
    error_counts = Counter(errors)
    
    print("Top 5 errors:")
    for error, count in error_counts.most_common(5):
        print(f"{count}: {error}")

if __name__ == "__main__":
    main()
```

### Script 2: System Monitoring
```python
#!/usr/bin/env python3
"""
Monitor system resources
"""
import psutil
import time

def monitor_system(duration=60, interval=5):
    """Monitor CPU, memory, and disk usage"""
    end_time = time.time() + duration
    
    while time.time() < end_time:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        print(f"\n--- System Status ---")
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Memory Usage: {memory.percent}%")
        print(f"Disk Usage: {disk.percent}%")
        
        time.sleep(interval)

if __name__ == "__main__":
    monitor_system(duration=30, interval=5)
```

### Script 3: File Backup Utility
```python
#!/usr/bin/env python3
"""
Backup files to a destination directory
"""
import os
import shutil
from datetime import datetime

def backup_files(source_dir, backup_dir):
    """Create timestamped backup of directory"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(backup_dir, backup_name)
    
    try:
        shutil.copytree(source_dir, backup_path)
        print(f"Backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

def cleanup_old_backups(backup_dir, keep_count=5):
    """Keep only the most recent backups"""
    backups = sorted([
        d for d in os.listdir(backup_dir)
        if d.startswith("backup_")
    ])
    
    if len(backups) > keep_count:
        for old_backup in backups[:-keep_count]:
            old_path = os.path.join(backup_dir, old_backup)
            shutil.rmtree(old_path)
            print(f"Removed old backup: {old_backup}")

if __name__ == "__main__":
    source = "/path/to/source"
    destination = "/path/to/backups"
    
    backup_files(source, destination)
    cleanup_old_backups(destination, keep_count=5)
```

### Script 4: API Client
```python
#!/usr/bin/env python3
"""
Simple REST API client
"""
import requests
import json

class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.headers = {}
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

# Usage
if __name__ == "__main__":
    client = APIClient("https://api.example.com", api_key="your_key")
    
    try:
        users = client.get("users", params={"limit": 10})
        print(json.dumps(users, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
```

---

## Conclusion

This guide covers the fundamentals of Python scripting with practical examples. Python's simplicity and powerful libraries make it an excellent choice for automation, DevOps tasks, and general-purpose programming.

### Next Steps:
- Practice writing scripts for daily tasks
- Explore frameworks like Flask/Django for web development
- Learn data science libraries (pandas, numpy, matplotlib)
- Study advanced topics (decorators, generators, async/await)
- Contribute to open-source Python projects

### Resources:
- Official Python Documentation: https://docs.python.org/
- Python Package Index (PyPI): https://pypi.org/
- Real Python: https://realpython.com/
- Python.org Tutorial: https://docs.python.org/3/tutorial/
