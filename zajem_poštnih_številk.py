import os
import requests
import sys
import re
import csv

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print(f'Shranjujem {url} ...', end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')

def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()



crke = ['a', 'b', 'c', "c1", 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', "s1", 't', 'u', 'v', 'z', "z1"]

for crka in crke:
    url = f"https://www.postnestevilke.com/postne-stevilke-{crka}.php"
    ime_datoteke = f"postne\postne_stevilke-{crka}.html"
    shrani_spletno_stran(url, ime_datoteke)
    vsebina = vsebina_datoteke(ime_datoteke)


vzorec = re.compile(
    r"<strong>(?P<kraj>.*)</strong> (?P<postna_stevilka>\d{4})<br/>"
) 

postne_stevilke = []

for crka in crke:
    with open(f"postne\postne_stevilke-{crka}.html", encoding="utf-8") as dat:
        vsebina = dat.read()
    for zadetek in re.finditer(vzorec, vsebina):
        postna = zadetek.groupdict()
        postne_stevilke.append(postna)
        

with open("postne.csv", "w", encoding="utf-8") as dat:
    writer = csv.DictWriter(dat, [
        "kraj",
        "postna_stevilka"
    ])
    writer.writeheader()
    writer.writerows(postne_stevilke)







