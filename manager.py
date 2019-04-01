from app import app  # the former 'app' from 'app'director __init__.py
from flask_script import Manager

if __name__ == "__main__":
    app.run(host="localhost", port=8081)
