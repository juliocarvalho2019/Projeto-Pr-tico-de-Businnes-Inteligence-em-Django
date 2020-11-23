from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Dados(models.Model):
    cpf = models.CharField(primary_key=False ,max_length=255, blank=True, null=True)
    etnia = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    escola_origem = models.CharField(max_length=255, blank=True, null=True)
    renda_familiar = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    matr_situacao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dados'

    @staticmethod
    def get_vestibular(q=None):
        
        if q:
            if q =='1':
                return Dados.objects.values('etnia').annotate(Sum('etnia'))
            elif q == '2':
                return Dados.objects.values('sexo').annotate(Sum('sexo'))
            elif q == '3':
                return Dados.objects.values('escola_origem').annotate(Sum('escola_origem'))
            elif q == '4':
                return Dados.objects.values('renda_familiar').annotate(Sum('renda_familiar'))
            elif q == '5':
                return Dados.objects.values('cidade').annotate(Sum('cidade'))
            elif q == '6':
                return Dados.objects.values('estado').annotate(Sum('estado'))
            elif q == '7':
                return Dados.objects.values('data_nascimento').annotate(Sum('data_nascimento'))
            elif q == '8':
                return Dados.objects.values("matr_situacao").annotate(Sum('matr_situacao'))
    
    @staticmethod
    def get_dados(q=None):
        
        if q:
            if q =='1':
                return Dados.objects.values('etnia')
            elif q == '2':
                return Dados.objects.values('sexo')
            elif q == '3':
                return Dados.objects.values('escola_origem')
            elif q == '4':
                return Dados.objects.values('renda_familiar')
            elif q == '5':
                return Dados.objects.values('cidade')
            elif q == '6':
                return Dados.objects.values('estado')
            elif q == '7':
                return Dados.objects.values('data_nascimento')
            elif q == '8':
                return Dados.objects.values("matr_situacao")
