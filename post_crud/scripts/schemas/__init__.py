from typing import Optional, List
from pydantic import BaseModel, Extra


class PostSchema(BaseModel, extra=Extra.ignore):
    caption: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
