# -*- coding: utf-8 -*-
from sigep.networknode.models import *
from sigep.ajaxtools.pagination import *

from django.db.models import Q

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils import simplejson


@login_required
def datagridx(request):
  """
  Exibe os pontos de rede.
  """

  if request.method == 'POST':
    """Retorna valores necessarios para construcao do datagrid em javascript."""

    page = int(request.POST.get('page'))
    id_client = int(request.POST.get('obj_id'))
    search_text = request.POST.get('search_text')
    search_text = search_text.strip()

    fields = ['ip','mac','plan.plan','accesspoint.accesspoint','router.hostname','useproxy','isblocked','isbound']

    # se houver algum texto no campo de busca, realiza uma consulta nos campos ip e mac
    if search_text != '' and search_text != 'Busca' and len(search_text) > 0:
      n = NetworkNode.objects.filter(Q(client=id_client)& Q(ip__icontains=search_text)|Q(mac__icontains=search_text))
    else:
      n = NetworkNode.objects.filter(client=id_client)  # lista todos objetos a serem paginados

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


@login_required
def unblock(request):
  """
  Bloqueia/Desbloqueia um ponto de rede
  """

  if request.method == 'POST':
    try:
      id = int(request.POST.get('id'))
      n = NetworkNode.objects.get(pk=id)
      # Se estiver bloqueado, desbloqueia e vice-versa
      if n.isblocked == 'Y':
        n.isblocked = 'N'
      else:
        n.isblocked = 'Y'
      n.save()

      list = ["ok",]
    except:
      list = ["error",]

    json = simplejson.dumps(list)
    return HttpResponse(json,mimetype="application/json")


@login_required
def unbound(request):
  """
  Amarra/Libera MAC ao endereco IP
  """

  if request.method == 'POST':
    try:
      id = int(request.POST.get('id'))
      n = NetworkNode.objects.get(pk=id)
      # Se estiver bloqueado, desbloqueia e vice-versa
      if n.isbound == 'Y':
        n.isbound = 'N'
      else:
        if len(n.mac) > 0:
          n.isbound = 'Y'
        else:
          n.isbound = 'N'

      n.save()

      list = ["ok",]
    except:
      list = ["error",]

    json = simplejson.dumps(list)
    return HttpResponse(json,mimetype="application/json")


@login_required
def useproxy(request):
  """
  Habilita/Desabilita o uso do proxy transparente.
  """

  if request.method == 'POST':
    try:
      id = int(request.POST.get('id'))
      n = NetworkNode.objects.get(pk=id)
      # Se estiver bloqueado, desbloqueia e vice-versa
      if n.useproxy == 'Y':
        n.useproxy = 'N'
      else:
        n.useproxy = 'Y'

      n.save()

      list = ["ok",]
    except:
      list = ["error",]

    json = simplejson.dumps(list)
    return HttpResponse(json,mimetype="application/json")
