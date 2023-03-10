import json
from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, status, UploadFile, File, Form
from scripts.core.handlers.posts_handler import PostsHandler
from scripts.constants.api_endpoints import APIEndpoints
from scripts.schemas import PostSchema
from scripts.errors import UserException

posts_router = APIRouter(prefix=APIEndpoints.api)


@posts_router.get(APIEndpoints.get_posts, status_code=status.HTTP_200_OK)
def get_all_posts():
    try:
        posts_handler = PostsHandler()
        return posts_handler.get_all_posts()
    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.args,
        ) from e


@posts_router.get(APIEndpoints.get_post+"/{post_id}", status_code=status.HTTP_200_OK)
def get_post_by_id(post_id: str):
    try:
        posts_handler = PostsHandler()
        return posts_handler.get_post_by_id(post_id=post_id)
    except Exception as e:
        print(e.args)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e.args) from e


@posts_router.post(APIEndpoints.create_post, status_code=status.HTTP_201_CREATED)
async def create_post(file: Optional[UploadFile] = File(None), post: str = Form(default="")):
    try:
        if not post and not file:
            raise UserException("Please provide a post or a file.") 
        post = PostSchema(**(json.loads(post) if post else {})).dict()
        posts_handler = PostsHandler()
        return await posts_handler.create_post(file=file, post=post)
        
    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.args) from e


@posts_router.put(APIEndpoints.update_post+"/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: str, post: PostSchema):
    try:
        posts_handler = PostsHandler()
        return posts_handler.update_post(post_id=post_id, post=post.dict())
    except Exception as e:
        print(e.args)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e.args) from e


@posts_router.delete(APIEndpoints.delete_post+"/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: str):
    try:
        posts_handler = PostsHandler()
        return posts_handler.delete_post(post_id=post_id)
    except Exception as e:
        print(e.args)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e.args) from e
