from django.contrib import admin
from .models import *


class CoNmTbAdmin(admin.ModelAdmin):
    list_display = ('conm_id', 'conm_name', 'conm_registered_time')


class CoDicTbAdmin(admin.ModelAdmin):
    list_display = ('codic_id', 'conm_id', 'codic_nickname', 'codic_registered_time')


class PdTbAdmin(admin.ModelAdmin):
    list_display = ('pd_id', 'pd_start', 'pd_minutes', 'pd_registered_time')


class MtScTbAdmin(admin.ModelAdmin):
    list_display = ('mtsc_id', 'pd_id', 'conm_id', 'mtsc_score', 'mtsc_mention', 'mtsc_registered_time')


admin.site.register(CoNmTb, CoNmTbAdmin)
admin.site.register(CoDicTb, CoDicTbAdmin)
admin.site.register(PdTb, PdTbAdmin)
admin.site.register(MtScTb, MtScTbAdmin)
