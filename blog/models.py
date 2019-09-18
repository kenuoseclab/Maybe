from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from blog.extensions import db


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    blog_title = db.Column(db.String(64))
    blog_sub_title = db.Column(db.String(128))
    about = db.Column(db.Text)
    name = db.Column(db.String(32))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    articles = db.relationship('Article', backref='category')


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    can_comment = db.Column(db.Boolean, default=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', backref='article', cascade='all, delete-orphan')


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), nullable=False)
    body = db.Column(db.Text, nullable=False)
    reviewed = db.Column(db.Boolean, default=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    # replied = db.relationship(          # 被评论的评论
    #     'Comment', back_populates='replies', remote_side=[id])
    # replies = db.relationship(          # 评论的评论
    #     'Comment', back_populates='replied', cascade='all')

    replies = db.relationship(
        'Comment',
        backref=db.backref('replied', remote_side=[id]),
        cascade='all, delete-orphan')
