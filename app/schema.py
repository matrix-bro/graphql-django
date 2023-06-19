import graphene
from graphene_django import DjangoObjectType

from app.models import Author

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        field = ("id", "name")

class Query(graphene.ObjectType):
    list_author = graphene.List(AuthorType)

    def resolve_list_author(root, info):
        return Author.objects.all()

schema = graphene.Schema(query=Query)