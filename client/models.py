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
    db_table = 'clientgroup'


class City(models.Model):
  city = models.CharField(max_length=100,verbose_name=_(u'Cidade'),unique=True)
  state = models.CharField(max_length=2,verbose_name=_(u'State'))
  
  def __unicode__(self):
    return "%s/%s" % (self.city, self.state)
    
  class Meta:
    ordering = ('city','state')
    verbose_name = 'Cidade'
    db_table = 'city'
  
  
class Neighborhood(models.Model):
  city = models.ForeignKey(City,verbose_name=_(u'Cidade'))
  neighborhood = models.CharField(max_length=100,verbose_name=_(u'Bairro'))
  
  def __unicode__(self):
    return self.neighborhood
  
  class Meta:
    ordering = ('neighborhood','city')
    verbose_name = 'Bairro'
    db_table = 'neighborhood'


class Street(models.Model):
  neighborhood = models.ForeignKey(Neighborhood,verbose_name=_(u'Bairro'))
  street = models.CharField(max_length=100,verbose_name=_(u'Logradouro'))
  
  def __unicode__(self):
    return self.street
  
  class Meta:
    ordering = ('street','neighborhood')
    verbose_name = 'Logradouro'
    db_table = 'street'
 

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
    db_table = 'client'
 

  
