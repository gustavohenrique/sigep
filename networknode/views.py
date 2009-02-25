# -*- coding: utf-8 -*-
from sigep.client.models import Client
from sigep.networknode.models import *
from sigep.networknode.forms import *

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def list(request):
  """
  Listar os pontos de rede do cliente selecionado
  Exibe a tela contendo um datagrid com todos os pontos de rede
  do cliente e um form para cadastrar um novo.
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
  '''
  if request.method == 'POST':
    try:
      # tenta converter id para um numero inteiro
      id = int(request.POST.get('id'))
    except:
      id= 0

    client = get_object_or_404(Client, pk=id)
    #client.birth = client.birth.strftime("%d-%m-%Y")
    # cria o form
    c = ClientForm(instance=client)
    #c.base_fields['birth'].input_formats = ('%d/%m/%Y',)
    # obtem dados do cliente e a lista de bairros e cidade de acordo com a rua
    listing = c.formfill(client)
    listing.append(('option','update'))
    return render_to_response('client/client_form_edit.html', dict(listing))

  else:
    raise Http404'''

@login_required
def update(request):
  """
  Atualizar cliente.
  Atualiza os dados do cliente selecionado.
  """
  '''
  if request.method == 'POST':
    # tenta converter id para um numero inteiro
    try:
      id = int(request.POST.get('id'))
    except:
      id = 0

    client = get_object_or_404(Client, pk=id)
    c = ClientForm(request.POST, instance=client)
    c.base_fields['birth'].input_formats = ('%d/%m/%Y',)
    # se todos os dados estão corretos, exibe a tela de clientes cadastrados
    if c.is_valid():
      c.save()
      return HttpResponseRedirect(reverse('client_list'))
    else:
      listing = c.formfill(client)
      listing.append(('status','error'))
      listing.append(('option','update'))
      return render_to_response('client/client_form_edit.html', dict(listing))

  else:
    raise Http404'''

