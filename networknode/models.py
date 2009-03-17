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
  hostname = models.CharField(max_length=100,unique=True,verbose_name="Hostname")
  ip = models.IPAddressField(unique=True,verbose_name="IP")
  ilan = models.CharField(max_length=4,verbose_name='Interface')
  desc = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Descrição'))

  class Meta:
    abstract = True


class Router(Server):
  mark = models.PositiveSmallIntegerField(max_length=2,verbose_name=_(u'Marcação'))
  isproxy = models.BooleanField(default=True,verbose_name='Proxy?')

  def __unicode__(self):
    return self.hostname

  class Meta:
    ordering = ('ilan','mark')
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
  plan = models.ForeignKey(Plan,verbose_name=_(u'Plano'),help_text='Plano de Acesso contendo downstream e upstream')
  accesspoint = models.ForeignKey(AccessPoint,blank=True,null=True,verbose_name=_(u'AP/Switch'),help_text='Access Point ou Switch o qual está conectado')
  router = models.ForeignKey(Router,verbose_name=_(u'Rota'),help_text='Servidor atuando como roteador e proxy')
  hardware = models.ForeignKey(Hardware,verbose_name=_(u'Equipamento'),blank=True,null=True,help_text='Tipo de equipamento')
  ip = models.IPAddressField('IP',db_index=True,help_text='Endereço IP classe A. Ex.: 10.0.0.2')
  mac = models.CharField('MAC',max_length=17,blank=True,null=True,db_index=True,help_text='Endereço físico no formato XX:XX:XX:XX:XX:XX')
  desc = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Descrição'),help_text='Breve descrição')
  useproxy = models.CharField(max_length=1,choices=settings.BOOLEAN_CHOICES,default='Y',verbose_name='Usa Proxy',help_text='Define se vai utilizar o proxy transparente')
  isblocked = models.CharField(max_length=1,choices=settings.BOOLEAN_CHOICES,default='N',verbose_name=_(u'Bloqueado'),db_index=True,help_text='Bloqueia o acesso à internet')
  isbound = models.CharField(max_length=1,choices=settings.BOOLEAN_CHOICES,default='N',verbose_name=_(u'Amarrado'),db_index=True,help_text='Se o IP não estiver amarrado ao MAC, qualquer placa de rede poderá utiliza-lo')

  def __unicode__(self):
    return self.ip

  class Meta:
    ordering = ('client','ip','accesspoint')
    verbose_name = 'Ponto de Rede'
    verbose_name_plural = 'Pontos de Rede'
    db_table = 'networknode'

  def save(self):
    try:
      """O mesmo IP pode estar cadastrado mais de uma vez desde que seja
      para o mesmo cliente. Isso acontence quando se deseja utiliza-lo
      em com MACs diferentes"""

      nodes = NetworkNode.objects.filter(ip=self.ip)
      inuse = False
      for n in nodes:
        if n.client.id != self.client.id:
          inuse = True

      if inuse == False:
        super(NetworkNode, self).save()
    except:
      super(NetworkNode, self).save()
