# -*- coding: utf-8 -*-
from sigep.networknode.models import NetworkNode

from django.forms.models import ModelForm
from django.forms.fields import IntegerField, IPAddressField
from django.forms.widgets import HiddenInput
from django.conf import settings

class NetworkNodeForm(ModelForm):
  def getLastIPClassA():
    n = NetworkNode.objects.all()

    if n.count() == 0:
      return settings.INITIAL_IP
    else:
      ip_list = []
      for obj in n:
        ip_array = obj.ip.split('.')
        ip_list.append(ip_array[0]+ip_array[1]+ip_array[2]+ip_array[3])

      last_ip = int(max(tuple(ip_list)))
      return last_ip + 1

  id = IntegerField(required=False,widget=HiddenInput())
  ip = IPAddressField(required=True,initial=getLastIPClassA(),label="IP")

  class Meta:
    model = NetworkNode


