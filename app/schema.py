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
    

class AuthorMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, name):
        author = Author(name=name)
        author.save()

        return AuthorMutation(author=author)
    
class UpdateAuthorMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()

    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, id, name):
        author = Author.objects.get(id=id)
        author.name = name
        author.save()

        return UpdateAuthorMutation(author=author)

class DeleteAuthorMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, id):
        author = Author.objects.get(id=id)
        author.delete()

        return

class Mutation(graphene.ObjectType):
    create_author = AuthorMutation.Field()
    update_author = UpdateAuthorMutation.Field()
    delete_author = DeleteAuthorMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)