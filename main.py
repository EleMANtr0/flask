from app import app, db
from app.models import User, Post
import sqlalchemy as sa
import os


@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "db": db, "User": User, "Post": Post}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))