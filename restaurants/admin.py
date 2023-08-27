from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models.Restaurant import Restaurant


@admin.register(Restaurant)
class RestaurantAdminModel(LeafletGeoAdmin):
    list_display = (
        'address',
    )
