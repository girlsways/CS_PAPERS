from graphql.error.base import GraphQLError as BaseGraphQLError


class GraphQLError(BaseGraphQLError):
    __slots__