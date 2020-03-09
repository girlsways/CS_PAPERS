from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from django_graphql_jwt_flow.models import JwtRefreshToken
from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = U