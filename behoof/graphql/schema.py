import graphene

from restaurants.schema.queries.RestaurantQuery import RestaurantQuery


class Query(RestaurantQuery):
    pass


schema = graphene.Schema(query=Query)
