from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.types import String, Integer, Date
from sqlalchemy.orm import relationship

from xraspberry.rasplife.db import BaseModel, db_session
from xraspberry.rasplife.utils import generate_timestamp


class Todo(BaseModel):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(Date)
    created_at = Column(Integer, default=generate_timestamp)
    updated_at = Column(Integer, default=generate_timestamp, onupdate=generate_timestamp)
    deleted_at = Column(Integer, default=0)

    user = relationship("User", back_populates="todos", lazy="select")
    todo_items = relationship("TodoItem", back_populates="todo", lazy="select")

    @classmethod
    def get_todo_by_user(cls, user_id, limit=20, offset=0, is_admin=False):
        if not is_admin:
            cond = (cls.deleted_at == 0) & (cls.user_id == user_id)
        else:
            cond = cls.user_id == user_id
        total = db_session.query(func.count(cls.id)).filter(cond).scalar()
        items = db_session.query(cls).filter(cond).order_by(cls.date).offset(offset).limit(limit).all()
        items = [item.to_dict() for item in items]
        # 非管理员无法查看到已经删除的todo_item子项
        if not is_admin:
            for todo in items:
                todo['todo_items'] = [todo_item for todo_item in todo['todo_items'] if todo_item.deleted_at == 0]
        return total, items

    @classmethod
    def get_todo_by_id(cls, todo_id):
        return db_session.query(cls).filter(cls.id == todo_id).first()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "date": self.date.strftime("%Y%m%d"),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "todo_items": [todo_item.to_dict() for todo_item in self.todo_items]
        }


class TodoItem(BaseModel):
    __tablename__ = 'todo_item'

    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer, ForeignKey("todo.id"))
    content = Column(String)
    status = Column(Integer, default=0)
    created_at = Column(Integer, default=generate_timestamp)
    updated_at = Column(Integer, default=generate_timestamp, onupdate=generate_timestamp)
    deleted_at = Column(Integer, default=0)

    todo = relationship("Todo", back_populates="todo_items", lazy="select")

    STATUS_CREATED = 0
    STATUS_FINISHED = 1

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    @classmethod
    def get_todo_item_by_id(cls, todo_item_id):
        return db_session.query(cls).filter(cls.id == todo_item_id).first()
