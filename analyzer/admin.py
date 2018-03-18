from django.contrib import admin
from .models import *


class CoSymTbAdmin(admin.ModelAdmin):
    list_display = ('cosm_id', 'cosm_symbol', 'cosm_registered_time')


class CoDicTbAdmin(admin.ModelAdmin):
    list_display = ('codic_id', 'cosm_id', 'codic_nickname', 'codic_registered_time')


class PdTbAdmin(admin.ModelAdmin):
    list_display = ('pd_id', 'pd_start', 'pd_minutes', 'pd_registered_time')


class MtScTbAdmin(admin.ModelAdmin):
    list_display = ('mtsc_id', 'pd_id', 'cosm_id', 'mtsc_score', 'mtsc_mention', 'mtsc_registered_time')


admin.site.register(CoSymTb, CoSymTbAdmin)
admin.site.register(CoDicTb, CoDicTbAdmin)
admin.site.register(PdTb, PdTbAdmin)
admin.site.register(MtScTb, MtScTbAdmin)
