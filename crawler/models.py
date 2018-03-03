from django.db import models
from django.utils import timezone


# Post Table
class PsTb(models.Model):
    ps_id = models.AutoField(db_column='PF_ID', primary_key=True)
    st_id = models.ForeignKey('StInfoTb', db_column='ST_ID')
    ps_title = models.CharField(db_column='PS_TITLE', max_length=100)
    ps_content = models.TextField(db_column='PS_CONTENT')
    ps_date = models.DateTimeField(db_column='PS_DATE',)
    ps_view_count = models.IntegerField(db_column='PS_VIEW_COUNT', default=0)
    ps_symph = models.IntegerField(db_column='PS_SYMPH', default=0)
    ps_registered_time = models.DateTimeField(db_column='PS_REGISTERED_TIME', default=timezone.localtime)

    class Meta:
        ordering = ['-ps_date']


# Comment Table
class CoTb(models.Model):
    co_id = models.AutoField(db_column='CO_ID', primary_key=True)
    ps_id = models.ForeignKey('PsTb', db_column='PS_ID')
    co_content = models.TextField(db_column='CO_CONTENT')
    co_date = models.DateTimeField(db_column='CO_DATE')
    co_registered_time = models.DateTimeField(db_column='CO_REGISTERED_TIME', default=timezone.localtime)

    class Meta:
        ordering = ['-co_date']


# Site Information Table
class StInfoTb(models.Model):
    st_id = models.AutoField(db_column='ST_ID', primary_key=True)
    st_name = models.CharField(db_column='ST_NM', max_length=10)
    st_url = models.CharField(db_column='ST_URL', max_length=50)
