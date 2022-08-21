from multiprocessing.spawn import import_main_path
import requests
import pprint
import json
import csv

from requests.models import default_hooks
try:
     import xmlrpclib
except ImportError:
     import xmlrpc.client as xmlrpclib

client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
# get a list of package names
# packages = client.list_packages()
# GNN Package list
packages=['torch','DGL','graphnet','Spektral','Tensorflow','Keras','Sonnet','MXNet','JAX','PyTorch-Lightning','Flax','Scikeras','Skorch','Haiku','Jraph']
x=0
y=0
for i in packages:
     q = requests.get(f'https://pypi.python.org/pypi/{i}/json')
     try:
          jsonData = q.json()
          # print(jsonData)
          info = jsonData['info'] 
          last_serial = jsonData['last_serial']
          releases = jsonData['releases']
          url = jsonData['urls']
          vulnarebility = jsonData['vulnerabilities']

          with open("GNN.csv","a", newline='') as file:
               csv_file = csv.writer(file)
               csv_file.writerow([info,last_serial,releases,url,vulnarebility])
          x+=1
     except:
          y+=1
          print(i)
     print(x,y)

print("Done")