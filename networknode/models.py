# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings

from sigep.client.models import Client


class Plan(models.Model):
  plan = models.CharField(max_length=200,verbose_name=_('Plano'),unique=True)
  desc = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Descrição'))
  downstream_min = models.PositiveSmallIntegerField("Down Min.",max_length=4)
  downstream_max = models.PositiveSmallIntegerField("Down Max.",max_length=4)
  upstream_min = models.PositiveSmallIntegerField("UP Min.",max_length=4)
  upstream_max = models.PositiveSmallIntegerField("UP Max.",max_length=4)
  price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True,verbose_name=_(u'Preço'))

  def __unicode__(self):
    return self.plan

  class Meta:
    ordering = ('plan',)
    verbose_name = 'Plano de Acesso'
    verbose_name_plural = 'Planos de Acesso'
    db_table = 'plan'


class AccessPoint(models.Model):
  accesspoint = models.CharField(max_length=10,verbose_name=_(u'Access Point'))
  ip = models.IPAddressField(blank=True,null=True,unique=True,verbose_name='IP')
  netmask = models.IPAddressField(verbose_name=_(u'Máscara'),blank=True,null=True)
  location = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Localização'))

  def __unicode__(self):
    return self.accesspoint

  class Meta:
    ordering = ('accesspoint','ip')
    verbose_name = 'Access Point'
    verbose_name_plural = 'Access Point'
    db_table = 'accesspoint'


class Server(models.Model):
  
  servername = models.CharField(max_length=100,unique=True)
  ip = models.IPAddressField(unique=True)
  default = models.CharField(max_length=1,choices=settings.BOOLEAN_CHOICES,default='N')
  desc = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Descrição'))
  
  class Meta:
    abstract = True


class Proxy(Server):
  
  def __unicode__(self):
    return self.servername

  class Meta:
    ordering = ('servername','ip')
    db_table = 'proxy'


class Router(Server):
  mark = models.PositiveSmallIntegerField(max_length=2,verbose_name=_(u'Marcação'))
  iface = models.CharField(max_length=4,verbose_name='Interface')
  
  def __unicode__(self):
    return self.servername

  class Meta:
    ordering = ('iface','mark')
    db_table = 'router'


class Hardware(models.Model):
  hardware = models.CharField(max_length=100,unique=True)

  def __unicode__(self):
    return self.hardware

  class Meta:
    ordering = ('hardware',)
    db_table = 'hardware'


class NetworkNode(models.Model):
  client = models.ForeignKey(Client,verbose_name=_(u'Cliente'))
  plan = models.ForeignKey(Plan,verbose_name=_(u'Plano'))
  accesspoint = models.ForeignKey(AccessPoint,verbose_name=_(u'AP/Switch'))
  proxy = models.ForeignKey(Proxy,blank=True,null=True)
  router = models.ForeignKey(Router,blank=True,null=True,verbose_name=_(u'Roteador'))
  hardware = models.ForeignKey(Hardware,verbose_name=_(u'Equipamento'),blank=True,null=True)
  ip = models.IPAddressField('IP',db_index=True)
  mac = models.CharField('MAC',max_length=17,blank=True,null=True,db_index=True)
  desc = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Descrição'))
  blocked = models.BooleanField(verbose_name=_(u'Bloqueado'),default=False,db_index=True)
  allowed = models.BooleanField(verbose_name=_(u'Liberado sem MAC'),default=True,db_index=True)

  def __unicode__(self):
    return self.ip

  class Meta:
    ordering = ('client','ip','accesspoint')
    verbose_name = 'Ponto de Rede'
    verbose_name_plural = 'Pontos de Rede'
    db_table = 'networknode'


