from django.contrib.auth import get_user_model
from factory import django, Faker, PostGenerationMethodCall


class UserFactory(django.DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")
    password = PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
