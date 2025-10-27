from pydantic import BaseModel, Field


class ReplayListParams(BaseModel):
    page_size: int = Field(
        default=1000,
        ge=1,
        le=1000,
        description="Number of replay IDs to return per page",
    )
    after: str | None = Field(
        default=None,
        description="Replay ID to start after (cursor for pagination)",
    )


class ReplayPagination(BaseModel):
    page_size: int = Field(description="Number of items per page")
    next_cursor: str | None = Field(
        description="Replay ID to use for next page (null if no more pages)"
    )
    has_more: bool = Field(description="Whether more results are available")


class ReplayListResponse(BaseModel):
    data: list[str] = Field(description="List of replay IDs")
    pagination: ReplayPagination = Field(description="Pagination information")
