# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _


class ClientGroup(models.Model):
  clientgroup = models.CharField(max_length=100,unique=True,verbose_name=_(u'Grupo'))
  desc = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Descrição'))
  
  def __unicode__(self):
    return self.clientgroup
  
  class Meta:
    ordering = ('clientgroup',)
    verbose_name = 'Grupo de Cliente'


class City(models.Model):
  city = models.CharField(max_length=100,verbose_name=_(u'Cidade'),unique=True)
  state = models.CharField(max_length=2,verbose_name=_(u'State'))
  
  def __unicode__(self):
    return "%s/%s" % (self.city, self.state)
    
  class Meta:
    ordering = ('city','state')
    verbose_name = 'Cidade'
  
  
class Neighborhood(models.Model):
  city = models.ForeignKey(City,verbose_name=_(u'Cidade'))
  neighborhood = models.CharField(max_length=100,verbose_name=_(u'Bairro'))
  
  def __unicode__(self):
    return self.neighborhood
  
  class Meta:
    ordering = ('neighborhood','city')
    verbose_name = 'Bairro'


class Street(models.Model):
  neighborhood = models.ForeignKey(Neighborhood,verbose_name=_(u'Bairro'))
  street = models.CharField(max_length=100,verbose_name=_(u'Logradouro'))
  
  def __unicode__(self):
    return self.street
  
  class Meta:
    ordering = ('street','neighborhood')
    verbose_name = 'Logradouro'
 

class Client(models.Model):
  TYPE_CHOICES = (
    ('I',_(u'Pessoa Física')),  # Individual
    ('L',_(u'Pessoa Jurídica')) # Legal
  )
  clientgroup = models.ForeignKey(ClientGroup,verbose_name=_(u'Grupo'))
  street = models.ForeignKey(Street,verbose_name=_(u'Endereço'))
  name = models.CharField(max_length=250,verbose_name=_(u'Nome'),unique=True)
  nickname = models.CharField(max_length=250,null=True,blank=True,verbose_name=_(u'Apelido'))
  ssn = models.CharField(max_length=20,verbose_name=_(u'CPF/CNPJ'),unique=True)
  ic = models.CharField(max_length=10,blank=True,null=True,verbose_name=_(u'RG/IE'))
  ic_agency = models.CharField(max_length=10,blank=True,null=True,verbose_name=_(u'Orgão RG'))
  type = models.CharField(max_length=250,choices=TYPE_CHOICES,default='I',verbose_name=_(u'Tipo'))
  birth = models.DateField(blank=True,null=True,verbose_name=_(u'Data de Nascimento'))
  register = models.DateTimeField(auto_now_add=True,blank=True,null=True,max_length=250,verbose_name=_(u'Data do Cadastro'))
  phone1 = models.CharField(max_length=14,blank=True,null=True,verbose_name=_(u'Telefone1'))
  phone2 = models.CharField(max_length=14,blank=True,null=True,verbose_name=_(u'Telefone2'))
  mobile = models.CharField(max_length=14,blank=True,null=True,verbose_name=_(u'Celular'))
  fax = models.CharField(max_length=14,blank=True,null=True,verbose_name=_(u'Fax'))
  email = models.EmailField(max_length=250,blank=True,null=True,verbose_name=_(u'E-mail'))
  site = models.URLField(max_length=250,blank=True,null=True,verbose_name=_(u'Site'))
  number = models.CharField(max_length=20,blank=True,null=True,verbose_name=_(u'Número'))
  reference = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Referência'))
  zipcode = models.PositiveIntegerField(max_length=8,blank=True,null=True,verbose_name=_(u'CEP'))
  
  def __unicode__(self):
    return self.name
    
  class Meta:
    ordering = ('name','-register')
    verbose_name = 'Cliente'
 

class AccessPoint(models.Model):
  accesspoint = models.CharField(max_length=10,verbose_name=_(u'CPF/CNPJ'))
  ip = models.IPAddressField(blank=True,null=True,unique=True)
  netmask = models.IPAddressField(verbose_name=_(u'Máscara'),blank=True,null=True)
  location = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Localização'))
  
  def __unicode__(self):
    return self.accesspoint
  
  class Meta:
    ordering = ('accesspoint','ip')
    verbose_name = 'Access Point'
    verbose_name_plural = 'Access Point'


class Proxy(models.Model):
  proxy = models.CharField(max_length=100,unique=True)
  desc = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Descrição'))
  ip = models.IPAddressField(unique=True)
  netmask = models.IPAddressField(verbose_name=_(u'Máscara'))
  
  def __unicode__(self):
    return self.proxy
  
  class Meta:
    ordering = ('proxy','ip')


class Plan(models.Model):
  plan = models.CharField(max_length=200,verbose_name=_('Plano'),unique=True)
  desc = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Descrição'))
  downstream = models.PositiveSmallIntegerField(max_length=4)
  upstream = models.PositiveSmallIntegerField(max_length=4)
  price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True,verbose_name=_(u'Preço'))
  
  def __unicode__(self):
    return self.plan

  class Meta:
    ordering = ('plan',)
    verbose_name = 'Plano de Acesso'
    verbose_name_plural = 'Planos de Acesso'

class Hardware(models.Model):
  hardware = models.CharField(max_length=100,unique=True)

  def __unicode__(self):
    return self.hardware
  
  class Meta:
    ordering = ('hardware',)


class NetworkNode(models.Model):
  client = models.ForeignKey(Client,verbose_name=_(u'Cliente'))
  plan = models.ForeignKey(Plan,verbose_name=_(u'Plano de Acesso'))
  accesspoint = models.ForeignKey(AccessPoint)
  hardware = models.ForeignKey(Hardware)
  ip = models.IPAddressField(db_index=True)
  mac = models.CharField(max_length=17,blank=True,null=True,unique=True,db_index=True)
  desc = models.CharField(max_length=250,blank=True,null=True,verbose_name=_(u'Descrição'))
  blocked = models.BooleanField(verbose_name=_(u'Bloqueado'),default=False,db_index=True)
  allowed = models.BooleanField(verbose_name=_(u'Liberado sem MAC'),default=True,db_index=True)
  
  def __unicode__(self):
    return self.ip
  
  class Meta:
    ordering = ('client','ip','accesspoint')
    verbose_name = 'Ponto de Rede'
    verbose_name_plural = 'Pontos de Rede'

#from django.contrib import databrowse
#databrowse.site.register(Client)

  