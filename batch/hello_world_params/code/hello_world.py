import os
def hello(name: str):
    print("Hello {}!".format(name))

if __name__ == "__main__":
    name = os.environ.get("NAME", "Sir")
    hello(name)