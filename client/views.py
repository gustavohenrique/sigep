# -*- coding: utf-8 -*-
from sigep.client.forms import *
from sigep.ajaxtools.pagination import *

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


@login_required
def list(request):
  """
  Listar clientes.
  Exibe a tela contendo um datagrid com todos os clientes cadastrados e um
  form para cadastro de novo cliente.
  """
  
  clientform = ClientForm()
  list_clientdata = clientform.formfill()
  return render_to_response('client/client_list.html', dict(list_clientdata))

@login_required
def add(request):
  """
  Cadastrar cliente.
  Retorna a tela de cadastro informando o status (error ou ok).
  """
  
  if request.method == 'POST':
    status = 'error'
    c = ClientForm(request.POST)
    if c.is_valid():
      c.save()
      status = 'ok'

    listing = c.formfill()
    listing.append(('status',status))
    
    return render_to_response('client/client_list.html', dict(listing))
    
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
      
    client = get_object_or_404(Client, pk=id)
    # cria o form
    c = ClientForm(instance=client)
    # obtem dados do cliente e a lista de bairros e cidade de acordo com a rua
    listing = c.formfill(client)
    listing.append(('option','update'))
    return render_to_response('client/client_form_edit.html', dict(listing))

  else:
    raise Http404

@login_required
def update(request):
  """
  Atualizar cliente.
  Atualiza os dados do cliente selecionado.
  """
  
  if request.method == 'POST':
    # tenta converter id para um numero inteiro
    try:
      id = int(request.POST.get('id'))
    except:
      id = 0
      
    client = get_object_or_404(Client, pk=id)
    c = ClientForm(request.POST, instance=client)
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
    raise Http404

