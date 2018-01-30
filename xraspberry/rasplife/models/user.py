from sqlalchemy import Column
from sqlalchemy.types import String, Integer, DateTime, ARRAY
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from xraspberry.rasplife.db import BaseModel, db_session
from xraspberry.rasplife.utils import generate_timestamp


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    nickname = Column(String)
    sex = Column(Integer)
    birth = Column(DateTime)
    birth_place = Column(String)
    phone = Column(ARRAY(String))
    email = Column(ARRAY(String))
    password_hash = Column(String)
    role = Column(Integer)
    created_at = Column(Integer, default=generate_timestamp)
    updated_at = Column(Integer, default=generate_timestamp, onupdate=generate_timestamp)
    deleted_at = Column(Integer, default=0)

    posts = relationship("Post", back_populates="user", lazy="select")
    todos = relationship("Todo", back_populates="user", lazy="select")

    # role
    ROLE = {
        3: "older",
        2: "current",
        1: "admin"
    }
    ADMIN = 1
    CURRENT = 2
    OLDER = 3

    # sex
    MALE = 0
    FEMALE = 1

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_id(cls, user_id):
        return db_session.query(cls).filter_by(id=user_id).first()

    @classmethod
    def find_by_name(cls, username):
        return db_session.query(cls).filter_by(username=username).first()

    @classmethod
    def get_users(cls, limit=20, offset=0):
        return db_session.query(cls).offset(offset).order_by(cls.id).limit(limit).all()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "birth": self.birth.strftime("%Y-%m-%d %H:%M:%S"),
            "birth_place": self.birth_place,
            "sex": "male" if self.sex == self.MALE else "female",
            "phone": self.phone,
            "email": self.email,
            "role": self.ROLE[self.role],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at
        }

    @classmethod
    def delete_user(cls, user_id):
        """
        删除一个用户需要删除其 posts, todos, todo_items
        都是软删除，即将deleted_at置为当前时间戳
        :param user_id:
        :return:
        """
        pass

