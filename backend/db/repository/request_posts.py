from db.models.posts import Post
from schemas.posts import PostCreate
from schemas.posts import UpdatePost
from sqlalchemy.orm import Session


async def retreive_post(id: int, db: Session):
    """The database will find the post and return the result."""

    item = db.query(Post).filter(Post.id == id).first()
    return item


async def list_posts(db: Session):
    """The database will find all existing posts and return the result."""

    posts = db.query(Post).filter(Post.is_active == True).all()
    return posts


async def update_post_by_id(id: int, post: UpdatePost, db: Session, owner_id: int):
    """Database write updated data in Post model and return result"""

    existing_post = db.query(Post).filter(Post.id == id)
    if not existing_post.first():
        return 0
    post.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_post.update(post.__dict__)
    db.commit()
    return 1


async def delete_post_by_id(id: int, db: Session, owner_id):
    """Database delete post by post id"""
    existing_post = db.query(Post).filter(Post.id == id)
    if not existing_post.first():
        return 0
    existing_post.delete(synchronize_session=False)
    db.commit()
    return 1


async def search_post(query: str, db: Session):
    """Database will find the data of a certain post by their content."""

    posts = db.query(Post).filter(Post.title.contains(query))
    return posts
