from callcenter.models import *
import re

def initDataBase():
    NumbersLocation.objects.all().delete() #On vide l'ancienne db
    data = open('callcenter/locationNumbers.tsv', 'r')
    for line in data:
        values = re.split(r'\t+', line)
        print values
        entry = NumbersLocation(code=values[0], pays=values[1], zone=values[2], indicatif=values[3], location_lat=values[5], location_long=values[6])
        entry.save()
    data.close()
