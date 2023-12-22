from typing import Optional

from pydantic import BaseModel, Field, RootModel


class Comment(BaseModel):
    line_start: int = Field(
        ..., description="The line number of the content at which the comment starts"
    )
    line_end: Optional[int] = Field(
        default=None,
        description="The line number of the content at which the comment ends, in case of a multiline comment",
    )
    content: str = Field(
        ...,
        description="The comment or suggestion you want to give for this or these lines",
    )


# Provide a pydantic type that acts as a list
class Comments(RootModel):
    root: list[Comment]
