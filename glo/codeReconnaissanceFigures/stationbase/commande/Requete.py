import json


data = {
   'commande' : 'avance',
   'value' : 10,
}

# Writing JSON data
with open('data.json', 'w') as f:
    json.dump(data, f)