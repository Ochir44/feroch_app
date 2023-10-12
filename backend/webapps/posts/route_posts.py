from apis.version1.route_login import get_current_user_from_token
from core.helpers import handle_file_upload
from db.models.posts import Post
from db.models.users import Users
from db.repository.posts import create_new_post
from db.repository.request_posts import list_posts
from db.repository.request_posts import retreive_post
from db.repository.request_posts import search_post
from db.repository.request_posts import update_post_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from schemas.posts import PostCreate
from schemas.posts import UpdatePost
from sqlalchemy.orm import Session
from webapps.posts.forms import PostCreateForm
from webapps.posts.forms import PostUpdateForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    """This function will show
    all posts on home page
    """

    posts = await list_posts(db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "posts": posts, "msg": msg}
    )


@router.get("/details/{id}")
async def post_detail(id: int, request: Request, db: Session = Depends(get_db)):
    """This function displays detailed
    information about a single post
    """

    post = await retreive_post(id=id, db=db)
    return templates.TemplateResponse(
        "posts/detail.html", {"request": request, "post": post}
    )


@router.get("/create-post/")
def create_post(request: Request, db: Session = Depends(get_db)):
    """Returns an empty create_post form"""

    return templates.TemplateResponse("posts/create_post.html", {"request": request})


@router.post("/create-post/")
async def create_post(request: Request, db: Session = Depends(get_db)):
    """This function will provide the user with opportunity to fill out a create post form and
    send a publication request that will contain the data entered by users."""

    form = PostCreateForm(request)
    await form.load_data()
    if await form.is_valid():

        try:
            token = request.cookies.get("access_token")
            # Scheme will hold "Bearer" and param will hold actual token value
            scheme, param = get_authorization_scheme_param(token)

            # Getting the current user
            current_user: User = await get_current_user_from_token(token=param, db=db)

            # create a post
            post = PostCreate(title=form.title, text=form.text, image=form.image)
            post = await create_new_post(post=post, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/details/{post.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            """In case of an error, we update form.erorrs"""

            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("posts/create_post.html", form.__dict__)

    return templates.TemplateResponse("posts/create_post.html", form.__dict__)


@router.get("/delete-post/")
async def show_posts_to_delete(request: Request, db: Session = Depends(get_db)):
    """This function will display our template with all the tasks in our database,
    and we will delete the tasks by calling our API using the fetch api in Javascript."""

    posts = await list_posts(db=db)
    return templates.TemplateResponse(
        "posts/show_posts_to_delete.html", {"request": request, "posts": posts}
    )


@router.get("/update-post/{id}")
async def update_post(id: int, request: Request, db: Session = Depends(get_db)):
    post = await retreive_post(id=id, db=db)
    if not post:
        return templates.TemplateResponse(
            "posts/not_found_post.html", {"request": request}
        )
    return templates.TemplateResponse(
        "posts/update_post.html", {"request": request, "post": post}
    )


@router.post("/update-post/{id}")
async def update_post(id: int, request: Request, db: Session = Depends(get_db)):
    post = await retreive_post(id=id, db=db)
    form = PostUpdateForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            token = request.cookies.get("access_token")
            _, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = await get_current_user_from_token(token=param, db=db)
            if post.owner_id == current_user.id or current_user.is_superuser:
                updated_post = UpdatePost(
                    title=form.title, text=form.text, image=form.image
                )
                if not form.image:
                    updated_post.image = Post.image
                updated_post = await update_post_by_id(
                    id=id, post=updated_post, db=db, owner_id=current_user.id
                )
                return responses.RedirectResponse(
                    f"/details/{post.id}", status_code=status.HTTP_302_FOUND
                )
            form.__dict__.get("errors").append("You are not permitted!!!!")
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse(
                "posts/update_post.html",
                {"request": request, "post": post, "errors": form.errors},
            )
    return templates.TemplateResponse(
        "posts/update_post.html",
        {"request": request, "post": post, "errors": form.errors},
    )


@router.get("/search/")
async def search(
    request: Request, db: Session = Depends(get_db), query: str | None = None
):
    """This function returns the search result using funtction search_post"""
    posts = await search_post(query, db=db)
    return templates.TemplateResponse(
        "search/search.html", {"request": request, "posts": posts}
    )
