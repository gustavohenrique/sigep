# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django.forms import forms
from django.forms.fields import CharField, DateField, IntegerField
from django.forms.widgets import DateTimeInput, HiddenInput
from django.contrib.localflavor.br.forms import BRStateSelect

from sigep.client.models import *

class CityForm(ModelForm):
  state = CharField(label="UF",widget=BRStateSelect(),initial='RJ')
  
  class Meta:
    model = City
    

class ClientForm(ModelForm):

  # campo hidden contendo o id do cliente.
  # usado pelo metodo update para saber o id do objeto a ser atualizado.
  id = IntegerField(required=False,widget=HiddenInput())
  
  # campo data usando jquery calendar para aceitar apenas data no formato especificado
  birth = DateField(label=u'Data Nascimento',required=False,widget=DateTimeInput(format='%d/%m/%Y'))
  
  def formfill(self, client=None):
    """
    Obtem os dados do cliente que serao exibidos nos campos do form.
    Se nenhum objeto cliente for recebido como argumento, seleciona a primeira
    cidade de todas cadastradas e a partir dela os respectivos bairros, e a
    ruas referentes ao primeiro bairro de todos os cadastrados.
    
    Senão, vai obter todos os bairros e a respectiva cidade do primeiro bairro,
    a partir da rua associada ao objeto.
    
    Retorna uma lista de tuplas contendo os dados do cliente, bairros e cidades.
    """
    
    # cria uma lista vazia que vai conter tuplas com os dados a serem inseridos no form
    listing = []
    
    if client is None:
      # queryset contendo todas as cidades cadastradas
      city_list = City.objects.all()
      # obtem o primeiro registro de todas as cidades cadastradas
      city = city_list.values_list()[:1]
      # obtem apenas o id da primeira cidade
      id_city = 0
      for ci in city: id_city = ci[0]
      # obtem todos os bairros cadastrados relacionados a cidade
      neighborhood_list = Neighborhood.objects.filter(city=id_city)
      # obtem o primeiro registro de todos os bairros cadastrados
      neighborhood = neighborhood_list.values_list()[:1]
      # obtem apenas o id do primeiro bairro
      id_neighborhood = 0
      for n in neighborhood: id_neighborhood = n[0]
      # obtem todas as ruas cadastradas de acordo com o bairro
      street_list = Street.objects.filter(neighborhood=id_neighborhood)
      
    else:
      # todas as cidades cadastradas
      city_list = City.objects.all()
      # rua do cliente
      s = client.street.id
      # bairro a partir da rua obtida
      n = client.street.neighborhood.id
      # cidade o qual o bairro pertence
      ci = client.street.neighborhood.city.id
      # bairros relacionados a cidade
      neighborhood_list = Neighborhood.objects.filter(city=ci)
      # ruas relacionadas ao bairro
      street_list = Street.objects.filter(neighborhood=n)
      listing = [
        ('id_street',s),
        ('id_neighborhood',n),
        ('id_city',ci)
      ]
    
    # adiciona dados na lista  
    listing += [
      ('form',self),
      ('city_list',city_list),
      ('neighborhood_list',neighborhood_list),
      ('street_list',street_list),
    ]
    
    return listing
  
    
  class Meta:
    model = Client

    
