from datetime import datetime
from xraspberry.rasplife.utils import generate_timestamp
from xraspberry.rasplife.handlers.base import route, BaseHandler, current_auth, admin_auth, user_auth, MESSAGES
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
        total, items = Todo.get_todo_by_user(self.current_user.id, limit=size, offset=offset)

        ret = {
            "total": total,
            "items": [item.to_dict() for item in items],
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
        pass

    @admin_auth
    def delete(self, todo_id, *args, **kwargs):
        pass


@route(r'/todo_items/(\d+)')
class TodoItemHandler(BaseHandler):
    """
    对某日期下的单个todo条目进行修改和删除
    """
    @current_auth
    def put(self, todo_item_id, *args, **kwargs):
        pass

    @admin_auth
    def delete(self, todo_item_id, *args, **kwargs):
        pass
