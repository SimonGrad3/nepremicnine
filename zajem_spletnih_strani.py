import os
import requests
import sys
import re

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





for n in range(1,105):
    url = f"https://www.nepremicnine.net/oglasi-prodaja/slovenija/hisa/{n}/"
    ime_datoteke = f"hise\hise-slovenija-{n}.html"
    shrani_spletno_stran(url, ime_datoteke)
    vsebina = vsebina_datoteke(ime_datoteke)

for n in range(1,54):
    url = f"https://www.nepremicnine.net/oglasi-prodaja/hrvaska/hisa/{n}/"
    ime_datoteke = f"hise\hise-hrvaska-{n}.html"
    shrani_spletno_stran(url, ime_datoteke)
    vsebina = vsebina_datoteke(ime_datoteke)