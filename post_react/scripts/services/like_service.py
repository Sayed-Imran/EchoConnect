from fastapi import status, APIRouter, HTTPException
from scripts.core.handlers.posts_handler import PostsHandler
from scripts.constants.api_endpoints import APIEndpoints

like_router = APIRouter(prefix=APIEndpoints.api)


@like_router.get(APIEndpoints.like+"/{post_id}", status_code=status.HTTP_200_OK)
def like_dislike_post(post_id: str, user_id: str):
    try:
        post_handler = PostsHandler()
        return post_handler.post_like_dislike(post_id=post_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.args
        ) from e
