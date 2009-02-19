import unittest
from django.test.client import Client

from sigep.client.models import City
from sigep.client.forms import CityForm
from sigep.ajaxtools.pagination import *


class AjaxTest(unittest.TestCase):
  
  def setUP(self):
    self.client = Client()
  
  def datagridx(self):
    c = Client()
    print c.get('/client/ajax/datagridx/', {'page':1,'fields':['id','city'] })
    #c.get('/client/ajax/datagridx/next/')
    
  def addx(self):
    c = Client()
    f = CityForm()
    print c.post('/client/ajax/addx/', f)
    
  def pag(self):
    data_dict = {
      'object_list': City.objects.all(),
      'fields': ['id','city'],
      'page': 1,
      'show_per_page': 5,
    }
    print pagination(data_dict)
    
