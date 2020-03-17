
import graphene

from django_graphql_jwt_flow.schema import Login


class Query(graphene.ObjectType):
    ping = graphene.String(default_value="pong")


class Mutation(graphene.ObjectType):
    login = Login.Field()


# noinspection PyTypeChecker
schema = graphene.Schema(query=Query, mutation=Mutation)