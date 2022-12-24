from typing import Optional, List
from pydantic import BaseModel

class PostSchema(BaseModel):
    caption: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]