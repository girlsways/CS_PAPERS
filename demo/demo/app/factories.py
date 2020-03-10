from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from django_graphql_jwt_flow.models import JwtRefreshToken
from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    password = Faker("password", length=20)
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    em