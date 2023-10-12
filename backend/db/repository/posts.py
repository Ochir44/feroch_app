from db.models.posts import Post
from schemas.posts import PostCreate
from sqlalchemy.orm import Session


async def create_new_post(post: PostCreate, db: Session, owner_id: int):
    """Database write new data in Post model and return result"""

    post_object = Post(**post.dict(), owner_id=owner_id)
    db.add(post_object)
    db.commit()
    db.refresh(post_object)
    return post_object
