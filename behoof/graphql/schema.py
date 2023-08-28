import graphene

from foods.schema.queries.CategoryQuery import CategoryQuery
from foods.schema.queries.FoodQuery import FoodQuery
from restaurants.schema.queries.RestaurantQuery import RestaurantQuery


class Query(CategoryQuery, FoodQuery, RestaurantQuery):
    pass


schema = graphene.Schema(query=Query)
