import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from app.models import Author, Book

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        field = ("id", "name")

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        field = ("id", "title", "author")

class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = ['name']
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    list_author = graphene.List(AuthorType)
    list_books = graphene.List(BookType)

    author = relay.Node.Field(AuthorNode)
    all_authors = DjangoFilterConnectionField(AuthorNode)

    def resolve_list_author(root, info):
        return Author.objects.all()
    
    def resolve_list_books(root, info):
        return Book.objects.all()



class AuthorMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, name):
        author = Author(name=name)
        author.save()

        return AuthorMutation(author=author)
    
class BookMutation(graphene.Mutation):
    class Arguments:
        author_id = graphene.ID()
        title = graphene.String()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, author_id, title):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            raise GraphQLError("Invalid Author ID")

        book = Book(title=title, author=author)
        book.save()

        return BookMutation(book=book)
    
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
    
    create_book = BookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)