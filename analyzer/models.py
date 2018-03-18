from django.db import models
from django.utils import timezone


# Coin Symbol Table
class CoSymTb(models.Model):
    cosm_id =  models.AutoField(db_column='COSM_ID', primary_key=True)
    cosm_symbol = models.CharField(db_column='COSM_SYMBOL', max_length=10)
    cosm_registered_time = models.DateTimeField(db_column='COSM_REGISTERED_TIME', default=timezone.localtime)


# Coin Dictionary Table
class CoDicTb(models.Model):
    codic_id =  models.AutoField(db_column='CODIC_ID', primary_key=True)
    cosm_id = models.ForeignKey('CoSymTb', db_column='COSM_ID')
    codic_nickname = models.CharField(db_column='CODIC_NICKNAME', max_length=40)
    codic_registered_time = models.DateTimeField(db_column='CODIC_REGISTERED_TIME', default=timezone.localtime)


# Period Table
class PdTb(models.Model):
    pd_id = models.AutoField(db_column='PD_ID', primary_key=True)
    pd_start = models.DateTimeField(db_column='PD_START')
    pd_minutes = models.IntegerField(db_column='PD_MINUTES')
    pd_registered_time = models.DateTimeField(db_column='PD_REGISTERED_TIME', default=timezone.localtime)

    @property
    def pd_end(self):
        return self.pd_start + self.pd_minutes


# Mention Score Table
class MtScTb(models.Model):
    mtsc_id =  models.AutoField(db_column='MTSC_ID', primary_key=True)
    pd_id = models.ForeignKey('PdTb', db_column='PD_ID')
    cosm_id = models.ForeignKey('CoSymTb', db_column='COSM_ID')
    mtsc_score = models.IntegerField(db_column='MTSC_SCORE')
    mtsc_mention = models.IntegerField(db_column='MTSC_MENTION')
    mtsc_registered_time = models.DateTimeField(db_column='MTSC_REGISTERED_TIME', default=timezone.localtime)

    class Meta:
        unique_together = (('pd_id', 'mtsc_score'),)
