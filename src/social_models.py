from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    email = Column(String(120), nullable=False)
    password = Column(String(80), nullable=False)
    full_name = Column(String(120))
    bio = Column(String(250))
    website = Column(String(200))
    is_private = Column(Boolean, nullable=False, default=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    caption = Column(String(2200))
    location = Column(String(120))
    created_at = Column(DateTime)
    is_archived = Column(Boolean, nullable=False, default=False)
    user = relationship('User')


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    media_type = Column(String(20))
    url = Column(String(250))
    order = Column(Integer)
    post = relationship('Post')


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(String(500))
    created_at = Column(DateTime)
    parent_id = Column(Integer, ForeignKey('comment.id'))
    post = relationship('Post')
    user = relationship('User')
    parent = relationship('Comment', remote_side=[id])


class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    created_at = Column(DateTime)
    user = relationship('User')
    post = relationship('Post')


class Follow(Base):
    __tablename__ = 'follow'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime)
    is_accepted = Column(Boolean, nullable=False, default=True)
    follower = relationship('User', foreign_keys=[follower_id])
    followed = relationship('User', foreign_keys=[followed_id])


if __name__ == '__main__':
    render_er(Base, 'diagram_social.dot')
