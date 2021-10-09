from graphql.error.base import GraphQLError as BaseGraphQLError


class GraphQLError(BaseGraphQLError):
    __slots__ = BaseGraphQLError.__slots__ + ("status_code",)

    def __init__(
       