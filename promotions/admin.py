from django.contrib import admin

from .models.Promotion import Promotion


@admin.register(Promotion)
class PromotionModelAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'start_time', 'end_time',
    )
