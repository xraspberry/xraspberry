from datetime import datetime
from xraspberry.rasplife.utils import generate_timestamp
from xraspberry.rasplife.handlers.base import route, BaseHandler, current_auth, admin_auth, MESSAGES
from xraspberry.rasplife.models.todo import Todo, TodoItem
from xraspberry.rasplife.db import db_session


@route(r'/todos')
class TodosHandler(BaseHandler):
    """
    对应某日期的todo
    """
    @current_auth
    def post(self, *args, **kwargs):
        data = self.get_json_body()
        date = data.get("date")
        if not date:
            return self.error(MESSAGES[400], status_code=400)
        todo = Todo()
        todo.user = self.current_user
        try:
            todo.date = datetime.strptime(date, "%Y%m%d").date()
        except ValueError as e:
            return self.error(MESSAGES[400], status_code=400)
        db_session.add(todo)
        db_session.commit()
        return self.data(todo.to_dict())

    @current_auth
    def get(self, *args, **kwargs):
        try:
            page = int(self.get_argument("page", 1))
            size = int(self.get_argument("size", 20))
        except ValueError as e:
            self.error(MESSAGES[400], status_code=400)

        offset = (page - 1) * size
        total, items = Todo.get_todo_by_user(self.current_user.id, limit=size, offset=offset, is_admin=self.is_admin())

        ret = {
            "total": total,
            "items": items,
            "page": page,
            "size": size
        }

        self.data(ret)


@route(r'/todos/(\d+)')
class TodoHandler(BaseHandler):
    """
    对某个日期的todo列表整个进行修改和删除

        put是新增一个todo条目
        delete是删除一整个日期的todo
    """
    @current_auth
    def put(self, todo_id, *args, **kwargs):
        todo = Todo.get_todo_by_id(todo_id)
        if not todo:
            return self.error(MESSAGES[404], status_code=404)
        if todo.user_id != self.current_user.id:
            return self.error(MESSAGES[403], status_code=403)
        content = self.get_json_body().get("content")
        if not content:
            return self.error(MESSAGES[400], status_code=400)
        todo_item = TodoItem(content=content)
        todo_item.todo = todo
        db_session.add(todo_item)
        db_session.commit()
        return self.data(todo.to_dict())

    @admin_auth
    def delete(self, todo_id, *args, **kwargs):
        todo = Todo.get_todo_by_id(todo_id)
        if not todo:
            return self.error(MESSAGES[404], status_code=404)
        todo.deleted_at = generate_timestamp()
        for todo_item in todo.todo_items:
            todo_item.deleted_at = generate_timestamp()
            db_session.add(todo_item)
        db_session.add(todo)
        db_session.commit()
        return self.data(todo.to_dict())


@route(r'/todo_items/(\d+)')
class TodoItemHandler(BaseHandler):
    """
    对某日期下的单个todo条目进行修改和删除
    """
    @current_auth
    def put(self, todo_item_id, *args, **kwargs):
        todo_item = TodoItem.get_todo_item_by_id(todo_item_id)
        if not todo_item:
            return self.error(MESSAGES[404], status_code=404)
        if self.current_user.id != todo_item.todo.user_id:
            return self.error(MESSAGES[403], status_code=403)
        data = self.get_json_body()
        status = data.get("status", 0)
        if status not in (TodoItem.STATUS_CREATED, TodoItem.STATUS_FINISHED):
            return self.error(MESSAGES[400], status_code=400)
        content = data.get("content")
        if not content:
            return self.error(MESSAGES[400], status_code=400)
        todo_item.status = status
        todo_item.content = content
        db_session.add(todo_item)
        db_session.commit()
        return self.data(todo_item.to_dict())

    @admin_auth
    def delete(self, todo_item_id, *args, **kwargs):
        todo_item = TodoItem.get_todo_item_by_id(todo_item_id)
        if not todo_item:
            return self.error(MESSAGES[404], status_code=404)
        todo_item.deleted_at = generate_timestamp()
        db_session.add(todo_item)
        db_session.commit()
        return self.data(todo_item.to_dict())
