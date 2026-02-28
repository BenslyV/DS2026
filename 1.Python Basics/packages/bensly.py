def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def is_even(num):
    """Check if a number is even."""
    return num % 2 == 0


def reverse_string(text):
    """Return the reversed string."""
    return text[::-1]


def calculate_average(numbers):
    """Return the average of a list of numbers."""
    return sum(numbers) / len(numbers) if numbers else 0