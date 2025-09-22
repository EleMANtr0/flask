from app import app, db
from app.models import User, Post
import sqlalchemy as sa

@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "db": db, "User": User, "Post": Post}
