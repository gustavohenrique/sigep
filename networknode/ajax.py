# -*- coding: utf-8 -*-
from sigep.networknode.models import *
from sigep.ajaxtools.pagination import *

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils import simplejson


@login_required
def datagridx(request):
  if request.method == 'POST':
    """
    Retorna valores necessarios para construcao do datagrid em javascript.
    """

    page = int(request.POST.get('page'))
    search_text = request.POST.get('search_text')
    search_text = search_text.strip()

    fields = ['ip','mac','plan.plan','blocked','allowed']

    # se houver algum texto no campo de busca, realiza uma consulta no campo name
    if search_text != '' and search_text != 'Busca' and len(search_text) > 0:
      n = NetworkNode.objects.filter(ip__icontains=search_text)
    else:
      n = NetworkNode.objects.all()  # lista todos objetos a serem paginados

    return pagination(n, fields, page)

@login_required
def deletex(request):
  """
  Deleta um ponto de rede e retorna o status da operacao.
  """

  if request.method == 'POST':
    try:
      id = int(request.POST.get('id'))
      n = NetworkNode.objects.get(pk=id).delete()
      list = ["ok",]
    except:
      list = ["error",]

    json = simplejson.dumps(list)
    return HttpResponse(json,mimetype="application/json")

