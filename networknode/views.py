# -*- coding: utf-8 -*-
from sigep.client.models import Client
from sigep.networknode.models import *
from sigep.networknode.forms import *

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def list(request):
  """
  Listar os pontos de rede do cliente selecionado
  Exibe a tela contendo um datagrid com todos os pontos de rede
  do cliente e um form para novo cadastro.
  """

  if request.method == 'GET':
    try:
      client_id = int(request.GET.get('id'))
      client_name = Client.objects.get(pk=client_id).name.upper()
    except:
      client_id = 0
      client_name = '[CLIENTE NÃO ENCONTRADO]'

    try:
      n = NetworkNode.objects.filter(client=client_id)
      nform = NetworkNodeForm(instance=n)
    except:
      nform = NetworkNodeForm()

    return render_to_response('networknode/n_list.html', {'form':nform, 'client':client_name, 'client_id':client_id})

  else:
    return HttpResponse('raise Http404')


@login_required
def add(request):
  """
  Cadastrar ponto de rede.
  """

  if request.method == 'POST':
    client_name = request.POST.get('client_name')
    client_id = request.POST.get('client')
    n = NetworkNodeForm(request.POST)
    if n.is_valid():
      n.save()
      return HttpResponseRedirect('/networknode/list/?id=%s' % client_id)
    else:
      return render_to_response('networknode/n_list.html', {'form':n, 'status':'error', 'client_id':client_id})

  else:
    raise Http404


@login_required
def edit(request):
  """
  Editar Cliente.
  Obtem dados do cliente e exibe a tela contendo o form para alteracao de dados.
  """

  if request.method == 'POST':
    try:
      # tenta converter id para um numero inteiro
      id = int(request.POST.get('id'))
    except:
      id= 0

    n = get_object_or_404(NetworkNode, pk=id)
    client_name = n.client.name
    client_id = n.client.id
    # cria o form
    nform = NetworkNodeForm(instance=n)
    dic = {
      'form':nform,
      'option':'update',
      'client':client_name,
      'client_id':client_id,
      'id':id
    }
    return render_to_response('networknode/n_form_edit.html', dic)

  else:
    raise Http404


@login_required
def update(request):
  """
  Atualizar cliente.
  Atualiza os dados do cliente selecionado.
  """

  if request.method == 'POST':

    try:
      id = int(request.POST.get('id'))
    except:
      id = 0

    n = get_object_or_404(NetworkNode, pk=id)
    client_name = n.client.name
    client_id = n.client.id
    nform = NetworkNodeForm(request.POST, instance=n)

    if nform.is_valid():
      # verifica se o ip ja estah em uso por outro ponto de rede
      nform.save()
      return HttpResponseRedirect('/networknode/list/?id=%s' % client_id)
    else:
      dic = {
        'form':nform,
        'option':'update',
        'client':client_name,
        'client_id':client_id,
        'id':id
      }
      return render_to_response('networknode/n_form_edit.html', dic)

  else:
    raise Http404
