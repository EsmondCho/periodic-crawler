from django.db import models
from django.utils import timezone


# Coin Name Table
class CoNmTb(models.Model):
    conm_id =  models.AutoField(db_column='CONM_ID', primary_key=True)
    conm_symbol = models.CharField(db_column='CONM_SYMBOL', max_length=10)
    conm_registered_time = models.DateTimeField(db_column='CONM_REGISTERED_TIME', default=timezone.localtime)


# Coin Dictionary Table
class CoDicTb(models.Model):
    codic_id =  models.AutoField(db_column='CODIC_ID', primary_key=True)
    conm_id = models.ForeignKey('CoNmTb', db_column='CONM_ID')
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
    conm_id = models.ForeignKey('CoNmTb', db_column='COMN_ID')
    mtsc_score = models.IntegerField(db_column='MTSC_SCORE')
    mtsc_mention = models.IntegerField(db_column='MTSC_MENTION')
    mtsc_registered_time = models.DateTimeField(db_column='MTSC_REGISTERED_TIME', default=timezone.localtime)

    class Meta:
        unique_together = (('pd_id', 'mtsc_score'),)
