
from django.urls import path
from graphene_django.views import GraphQLView #View for the user interface
from app.schema import schema #Schema we want to query

urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),

]
