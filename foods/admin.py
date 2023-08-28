from django.contrib import admin

from .models.Category import Category
from .models.Food import Food


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'is_published',
    )
    list_filter = (
        'is_published',
    )


@admin.register(Food)
class FoodModelAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'price', 'is_published',
    )
    list_filter = (
        'category', 'is_published',
    )
