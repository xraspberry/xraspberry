from xraspberry.rasplife.utils import generate_timestamp
from xraspberry.rasplife.handlers.base import route, BaseHandler, current_auth, admin_auth, user_auth, MESSAGES, user_visit_auth
from xraspberry.rasplife.models.post import Post
from xraspberry.rasplife.db import db_session


@route(r'/posts')
class PostsHandler(BaseHandler):
    @current_auth
    def get(self, *args, **kwargs):
        try:
            page = int(self.get_argument("page", 1))
            size = int(self.get_argument("size", 20))
        except ValueError as e:
            self.error(MESSAGES[400], status_code=400)

        offset = (page - 1) * size
        total, items = Post.get_posts(limit=size, offset=offset, is_admin=self.is_admin())

        ret = {
            "total": total,
            "items": items,
            "page": page,
            "size": size
        }

        self.data(ret)


@route(r'/posts/user/(\d+)')
class UserPostHandler(BaseHandler):
    """
    获取某个用户下的博文列表，可以将user_id作为/posts接口的查询参数
    但是为了更好的权限控制：普通用户不能查看已经删除用户的博文列表
    所以单独做一个接口
    """
    @user_visit_auth
    @current_auth
    def get(self, user_id, *args, **kwargs):
        try:
            page = int(self.get_argument("page", 1))
            size = int(self.get_argument("size", 20))
        except ValueError as e:
            self.error(MESSAGES[400], status_code=400)

        offset = (page - 1) * size
        total, items = Post.get_posts_by_user(user_id, limit=size, offset=offset, is_admin=self.is_admin())

        ret = {
            "total": total,
            "items": items,
            "page": page,
            "size": size
        }

        self.data(ret)


@route(r'/posts/(\d+)')
class PostHandler(BaseHandler):
    @current_auth
    def get(self, post_id, *args, **kwargs):
        post = Post.find_post_by_id(post_id)
        if not user_visit_auth.visit_auth_check(self, post.user.id):
            return self.error(MESSAGES[403], status_code=403)
        if not post:
            return self.error(MESSAGES[404], status_code=404)
        db_session.execute("UPDATE post SET read_count = read_count + 1 WHERE id = :post_id;", {"post_id": post_id})
        return self.data(post.to_dict())

    @current_auth
    def put(self, post_id, *args, **kwargs):
        post = Post.find_post_by_id(post_id)
        if post.user.id != self.current_user.id:
            return self.error(MESSAGES[403], status_code=403)
        if not post:
            return self.error(MESSAGES[404], status_code=404)
        data = self.get_json_body()
        post.title = data.get("title", "")
        post.content = data.get("content", "")
        post.update_count += 1
        db_session.add(post)
        db_session.commit()
        return self.data(post.to_dict())

    @admin_auth
    def delete(self, post_id, *args, **kwargs):
        post = Post.find_post_by_id(post_id)
        if not post:
            return self.error(MESSAGES[404], status_code=404)
        post.deleted_at = generate_timestamp()
        db_session.add(post)
        db_session.commit()
        return self.data(post.to_dict())
