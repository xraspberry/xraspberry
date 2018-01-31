from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.types import String, Integer
from sqlalchemy.orm import relationship

from xraspberry.rasplife.db import BaseModel, db_session
from xraspberry.rasplife.utils import generate_timestamp


class Post(BaseModel):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String)
    content = Column(String)
    post_type = Column(Integer, default=0)
    update_count = Column(Integer, default=1)
    read_count = Column(Integer, default=0)
    created_at = Column(Integer, default=generate_timestamp)
    updated_at = Column(Integer, default=generate_timestamp, onupdate=generate_timestamp)
    deleted_at = Column(Integer, default=0)

    user = relationship("User", back_populates="posts", lazy="subquery")

    POST = 0
    MICRO_BLOG = 1
    DIARY = 2

    @classmethod
    def get_posts_by_user(cls, current_user, user_id, limit=20, offset=0, post_type=0):
        if not current_user.is_admin():
            cond = (cls.deleted_at == 0) & (cls.post_type == post_type) & (cls.user_id == user_id)
        else:
            cond = (cls.post_type == post_type) & (cls.user_id == user_id)
        total = db_session.query(func.count(cls.id)).filter(cond).scalar()
        items = db_session.query(cls).filter(cond).order_by(cls.id).offset(offset).limit(limit).all()
        return total, items

    @classmethod
    def get_posts(cls, user, limit=20, offset=0, post_type=0):
        if not user.is_admin():
            cond = (cls.deleted_at == 0) & (cls.post_type == post_type)
        else:
            cond = cls.post_type == post_type
        if post_type == cls.DIARY:
            cond &= (cls.user_id == user.id)
        total = db_session.query(func.count(cls.id)).filter(cond).scalar()
        items = db_session.query(cls).filter(cond).order_by(cls.id).offset(offset).limit(limit).all()
        return total, items

    @classmethod
    def find_post_by_id(cls, post_id):
        return db_session.query(cls).filter(cls.id == post_id).first()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "update_count": self.update_count,
            "read_count": self.read_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "username": self.user.username
        }
