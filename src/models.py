from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='author')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='user_to')
    following = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='user_from')

class Follower(Base):
    __tablename__ = 'follower'
    
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    
    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='following')
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Media(Base):
    __tablename__ = 'media'
    
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_types'), nullable=False)
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    
    post = relationship('Post', back_populates='media')
