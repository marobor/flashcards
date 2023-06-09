from . import db
import re
from time import time

from unidecode import unidecode

# from flask_security import UserMixin, RoleMixin

from sqlalchemy.sql import func

# from sqlalchemy import event


# Function that processes title of a post and returns a slug.
def slugify(post_title):
    pattern = r'[^\w+]'
    title = unidecode(post_title)
    return str.lower(re.sub(pattern, '-', title))


# Create table in database for storing posts
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    edited_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))