# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson


def pagination(object_list, fields, page):
  """
  Paginacao ajax.
  Retorna um dicionario contendo os registros de determinada pagina. No lado client
  uma funcao em javascript cria um datagrid contendo os dados retornados.
  @object_list Queryset de objetos a serem exibidos
  @fields Campos que serao exibidos de cada registro
  @page Pagina que sera exibida
  Ex.: object_list = City.objects.all(), fields = ['city','state'], page = 1
  Exibira a primeira pagina de cidades cadastradas, mostando apenas os campos city e state.
  """
  
  # numero de resultados por pagina
  show_per_page = 5
  # adiciona o campo id a lista de campos
  fields.insert(0,'id')
  
  paginator = Paginator(object_list,show_per_page)
  try:
    listing = paginator.page(page)
  except (EmptyPage, InvalidPage):
    listing = paginator.page(paginator.num_pages)
  
  li1 = []  # ['1','rio']
  li2 = []  # [['1','rio'], ['2','sao paulo'], {'previous_page_number:0','next_page_number':2}]
  
  for obj in listing.object_list:
    for f in fields:
      li1.append(eval('obj.'+f))
    li2.append(li1)
    li1 = []
  
  data = [{
    'previous_page_number': listing.previous_page_number(),
    'next_page_number': listing.next_page_number(),
    'current_page': listing.number,
    'num_pages': paginator.num_pages,
    'total_result': object_list.count(),
    'listing': list(li2)
  }]
  
  json = simplejson.dumps(data)
  return HttpResponse(json,mimetype="application/json")
  
  # fields = ['name','mobile','birth']
  # retorna: [{"listing": [[1, "Gustavo Henrique", "", "(22) 9216-8396", "08/01/1984"]], "current_page": 1, "num_pages": 1, "previous_page_number": 0, "next_page_number": 2}]
  


