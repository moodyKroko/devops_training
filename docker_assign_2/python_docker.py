import os

name = os.environ.get("NAME", "Docker")
print(f"Hello, {name}!")