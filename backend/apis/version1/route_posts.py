from typing import List

from apis.version1.route_login import get_current_user_from_token
from core.helpers import handle_file_upload
from db.models.posts import Post
from db.models.users import Users
from db.repository.posts import create_new_post
from db.repository.request_posts import delete_post_by_id
from db.repository.request_posts import list_posts
from db.repository.request_posts import retreive_post
from db.repository.request_posts import search_post
from db.repository.request_posts import update_post_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import status
from fastapi import UploadFile
from schemas.posts import PostCreate
from schemas.posts import ShowPost
from schemas.posts import UpdatePost
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/create-post/", response_model=ShowPost)
async def create_post(
    title: str = Form(...),
    text: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user_from_token),
):
    """This function will check the received
    data using a schema named PostCreate
    """

    posts = UpdatePost(title=title, text=text)
    if image:
        posts.image = await handle_file_upload(image)  # Media file Processing
    elif not image:
        posts.image = ""
    return await create_new_post(db=db, owner_id=current_user.id, post=posts)


@router.get("/get/{id}", response_model=ShowPost)
async def read_post(id: int, db: Session = Depends(get_db)):
    """This function returns data about a post by its ID"""

    post = await retreive_post(id=id, db=db)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with this id {id} does not exist",
        )
    return post


@router.get("/all-posts/", response_model=List[ShowPost])
async def read_posts(db: Session = Depends(get_db)):
    """This funtion returns list posts"""

    posts = await list_posts(db=db)
    return posts


@router.post("/update-post/{id}")
async def update_post(
    id: int,
    title: str = Form(None),
    text: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user_from_token),
):
    """This function will check the received
    data using a schema named UpdatePost and return updated post
    """

    post = await retreive_post(id=id, db=db)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )
    print(post.owner_id, current_user.id, current_user.is_superuser)

    # Only users who have created a post or are superusers can updating a job post.
    if post.owner_id == current_user.id or current_user.is_superuser:
        post_update = UpdatePost(title=title, text=text)
        if not title:
            post_update.title = Post.title
        if not text:
            post_update.text = Post.text
        if not image:
            post_update.image = Post.image
        elif image:
            post_update.image = await handle_file_upload(image)  # Media file Processing
        message = await update_post_by_id(
            id=id, post=post_update, db=db, owner_id=current_user.id
        )
        return {"detail": "Successfully updated data."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )


@router.delete("/delete/{id}")
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user_from_token),
):
    """This function delete a post"""

    post = await retreive_post(id=id, db=db)
    if not post:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )
    print(post.owner_id, current_user.id, current_user.is_superuser)

    # Only users who have created a post or are superusers can delete a job post.
    if post.owner_id == current_user.id or current_user.is_superuser:
        await delete_post_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )


@router.get("/autocomplete")
async def autocomplete(term: str | None = None, db: Session = Depends(get_db)):
    """This function responsible for autocomplete in search field"""

    posts = await search_post(term, db=db)
    post_titles = []
    for post in posts:
        post_titles.append(post.title)
    return post_titles
