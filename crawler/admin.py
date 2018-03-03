from django.contrib import admin
from .models import *


class PsTbAdmin(admin.ModelAdmin):
    list_display = ('ps_id', 'st_id', 'ps_title', 'ps_content',
                    'ps_date', 'ps_view_count', 'ps_symph', 'ps_registered_time')


class CoTbAdmin(admin.ModelAdmin):
    list_display = ('co_id', 'ps_id', 'co_content', 'co_date', 'co_registered_time')


class StInfoTbAdmin(admin.ModelAdmin):
    list_display = ('st_id', 'st_name', 'st_url')


admin.site.register(PsTb, PsTbAdmin)
admin.site.register(CoTb, CoTbAdmin)
admin.site.register(StInfoTb, StInfoTbAdmin)
