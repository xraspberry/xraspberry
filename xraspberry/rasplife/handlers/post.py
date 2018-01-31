from xraspberry.rasplife.utils import generate_timestamp
from xraspberry.rasplife.handlers.base import route, BaseHandler, current_auth, admin_auth, MESSAGES, user_visit_auth
from xraspberry.rasplife.models.post import Post
from xraspberry.rasplife.db import db_session


@route(r'/posts')
class PostsHandler(BaseHandler):
    @current_auth
    def post(self, *args, **kwargs):
        data = self.get_json_body()
        title = data.get("title")
        content = data.get("content")
        post_type = data.get("post_type", Post.POST)
        if not title or not content:
            return self.error(MESSAGES[400], status_code=400)
        post = Post()
        post.user_id = self.current_user.id
        post.title = title
        post.content = content
        post.post_type = post_type
        db_session.add(post)
        db_session.commit()
        return self.data(post.to_dict())

    @current_auth
    def get(self, *args, **kwargs):
        try:
            page = int(self.get_argument("page", 1))
            size = int(self.get_argument("size", 20))
            post_type = int(self.get_argument("post_type", Post.POST))
        except ValueError as e:
            self.error(MESSAGES[400], status_code=400)

        offset = (page - 1) * size
        total, items = Post.get_posts(limit=size, offset=offset, user=self.current_user, post_type=post_type)

        ret = {
            "total": total,
            "items": [item.to_dict() for item in items],
            "page": page,
            "size": size
        }

        self.data(ret)


@route(r'/posts/(\d+)')
class PostHandler(BaseHandler):
    @current_auth
    def get(self, post_id, *args, **kwargs):
        post = Post.find_post_by_id(post_id)
        if post.deleted_at != 0 and not self.is_admin():
            return self.error(MESSAGES[403], status_code=403)
        if not user_visit_auth.visit_auth_check(self, post.user.id):
            return self.error(MESSAGES[403], status_code=403)
        if not post:
            return self.error(MESSAGES[404], status_code=404)
        if post.post_type == Post.DIARY and post.user_id != self.current_user.id:
            return self.error(MESSAGES[403], status_code=403)
        db_session.execute("UPDATE post SET read_count = read_count + 1 WHERE id = :post_id;", {"post_id": post_id})
        db_session.commit()
        return self.data(post.to_dict())

    @current_auth
    def put(self, post_id, *args, **kwargs):
        post = Post.find_post_by_id(post_id)
        if not post:
            return self.error(MESSAGES[404], status_code=404)
        if post.user.id != self.current_user.id:
            return self.error(MESSAGES[403], status_code=403)
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
