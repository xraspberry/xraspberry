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
    update_count = Column(Integer, default=1)
    read_count = Column(Integer, default=0)
    created_at = Column(Integer, default=generate_timestamp)
    updated_at = Column(Integer, default=generate_timestamp, onupdate=generate_timestamp)
    deleted_at = Column(Integer, default=0)

    user = relationship("User", back_populates="posts", lazy="subquery")

    @classmethod
    def get_posts_by_user(cls, user_id, limit=20, offset=0, is_admin=False):
        if not is_admin:
            # 非管理员只能查看未删除的数据
            cond = (cls.deleted_at == 0) & (cls.user_id == user_id)
        else:
            cond = cls.user_id == user_id
        total = db_session.query(func.count(cls.id)).filter(cond).scalar()
        items = db_session.query(cls).filter(cond).order_by(cls.id).offset(offset).limit(limit).all()
        return total, items

    @classmethod
    def get_posts(cls, limit=20, offset=0, is_admin=False):
        if not is_admin:
            cond = cls.deleted_at == 0
        else:
            cond = True
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
