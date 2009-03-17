# -*- coding: utf-8 -*-
from sigep.networknode.models import NetworkNode, Plan, AccessPoint, Router

from django.forms.models import ModelForm, ModelChoiceField
from django.forms.util import ValidationError
from django.forms.fields import IntegerField, IPAddressField, BooleanField
from django.forms.widgets import CheckboxInput, HiddenInput
from django.conf import settings

class NetworkNodeForm(ModelForm):

  def getNextIP():
    """
    Retorna o proximo IP disponivel num intervalo entre o minimo IP e o maximo IP
    definidos no arquivo de configuracao.
    Se NETMASK = 24, incrementa apenas o ultimo octeto do IP. NETMASK = 16, trabalha
    sobre os dois ultimos octetos.

    Exemplo:

      MIN_IP = 10.0.0.2
      MAX_IP = 10.0.3.100

      NETMASK = 24, IP fica entre 10.0.0.2 e 10.0.0.100
      NETMASK = 16, IP fica entre 10.0.0.2 e 10.0.3.100, sendo que nas
      faixas 10.0.0.0,  10.0.1.0 e 10.0.2.0 o ultimo octeto vai ate 254.
    """

    n = NetworkNode.objects.all()

    # Se nao houver nenhum IP cadastrado, retorna o minimo ip definido na configuracao
    if n.count() == 0:
      return settings.MIN_IP
    else:
      ip_list = []
      for obj in n:
        ip_list.append(obj.ip)

      min_ip = settings.MIN_IP.split('.')
      max_ip = settings.MAX_IP.split('.')
      last_ip = max(tuple(ip_list)).split('.')

      if settings.NETMASK == 24:
        # Compara apenas o ultimo octeto
        if (int(last_ip[3]) >= int(min_ip[3])) and (int(last_ip[3]) < int(max_ip[3])):
          last_ip[3] = int(last_ip[3]) + 1
        else:
          last_ip = min_ip

      else:
        if settings.NETMASK == 16:
          # se o 3o octeto for maior ou igual ao do ip maximo possivel
          if (int(last_ip[2]) >= int(max_ip[2])):
            # ... entao o 4o octeto deve ter o valor maximo = ao 4o octeto do maximo ip
            if (int(last_ip[3]) >= int(min_ip[3])) and (int(last_ip[3]) < int(max_ip[3])):
              last_ip[3] = int(last_ip[3]) + 1
            else:
              last_ip[3] = max_ip[3]

          # se o 3o octeto estiver entre a faixa
          else:
            if (int(last_ip[2]) >= int(min_ip[2])) and (int(last_ip[2]) < int(max_ip[2])):
              if (int(last_ip[3]) < 254):
                last_ip[3] = int(last_ip[3]) + 1
              else:
                last_ip[3] = max_ip[3]
                last_ip[2] = int(last_ip[2]) + 1

      return "%s.%s.%s.%s" % (last_ip[0],last_ip[1],last_ip[2],last_ip[3])

  '''def clean(self):
    """Para amarrar o MAC ao IP, é necessario um MAC válido"""
    isbound = self.cleaned_data['isbound']
    mac = self.cleaned_data['mac']
    if isbound == 'Y':
      if len(mac.strip()) > 0:
        return isbound
      else:
        raise ValidationError(u'MAC invalido')
    else:
      return isbound'''

  id = IntegerField(required=False,widget=HiddenInput())
  ip = IPAddressField(required=True,initial=getNextIP(),label='IP',max_length=15,help_text='Endereço IP classe A. Ex.: 10.0.0.2')
  plan = ModelChoiceField(label='Plano',queryset=Plan.objects.all(),help_text='Plano de Acesso',empty_label=None)
  accesspoint = ModelChoiceField(label='AP/Switch',queryset=AccessPoint.objects.all(),help_text='Access Point ou Switch o qual está conectado',empty_label=None)
  router = ModelChoiceField(label='Rota',queryset=Router.objects.all(),help_text='Servidor atuando como roteador e proxy',empty_label=None)

  class Meta:
    model = NetworkNode
