from typing import Generic, TypeVar, TypedDict

T = TypeVar("T")

class ApiResponse(TypedDict, Generic[T]):
    total: int
    data: T