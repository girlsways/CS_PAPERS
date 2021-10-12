from graphql.error.base import GraphQLError as BaseGraphQLError


class GraphQLError(BaseGraphQLError):
    __slots__ = BaseGraphQLError.__slots__ + ("status_code",)

    def __init__(
        self,
        message,  # type: str
        status_code=0,  # type: int
        **kwargs,
    ):
        # type: (...) -> None
        super().__in