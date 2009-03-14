# -*- coding: utf-8 -*-
from sigep.client.models import *
from sigep.ajaxtools.pagination import pagination

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils import simplejson


def comboajax(request, modelo, foreignkey, fieldkey):
  """
  Preenche o combobox (<select>) de destino de acordo com o item selecionado
  no combobox de origem.
  @modelo Model o qual se deseja obter o resultado
  @foreignkey Chave estrangeira do model
  @fiedlkey Campo cujo valor sera exibido no combobox de destino
  Ex.: modelo Street, foreignkey bairro, fieldkey rua, retornara todas as ruas do
  model Street referente a chave estrangeira.
  """
  
  if request.method == 'POST':
    try:
      id = int(request.POST.get('id'))
    except:
      id = 0
      
    try:
      object_list = eval(modelo+'.objects.filter('+foreignkey+'=id)')
      if object_list.count() > 0:
        json = serializers.serialize("json",object_list)
      else:
        object_list = [{"pk":"0","fields":{fieldkey:"Nenhum registro"}}]
        json = simplejson.dumps(object_list)
    except:
      object_list = [{"pk":"0","fields":{fieldkey:"Problemas na busca"}}]
      json = simplejson.dumps(object_list)
    
    return HttpResponse(json,mimetype="application/json")
  else:
    raise Http404

@login_required
def datagridx(request):
  if request.method == 'POST':
    """
    Retorna valores necessarios para construcao do datagrid em javascript.
    """
    
    page = int(request.POST.get('page'))
    search_text = request.POST.get('search_text')
    search_text = search_text.strip()
    
    fields = ['name','phone1','mobile','street.neighborhood.neighborhood']
    
    # se houver algum texto no campo de busca, realiza uma consulta no campo name
    if search_text != '' and search_text != 'Busca' and len(search_text) > 0:
      c = Client.objects.filter(name__icontains=search_text)
    else:
      c = Client.objects.all()  # lista todos objetos a serem paginados
      
    return pagination(c, fields, page)

@login_required
def deletex(request):
  """
  Deleta um cliente e retorna o status da operacao.
  """
  
  if request.method == 'POST':
    try:
      id = int(request.POST.get('id'))
      c = Client.objects.get(pk=id).delete()
      list = ["ok",]
    except:
      list = ["error",]
      
    json = simplejson.dumps(list)
    return HttpResponse(json,mimetype="application/json")
    
