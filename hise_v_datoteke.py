import re
import csv

vzorec_oglasa = re.compile(
    r"<div class=.oglas_container oglasbold oglasi.*?"
    r'</a>\s*</div>\s*<div class="clearer"></div>\s*</div>',
    flags=re.DOTALL
)

vzorec_hise = re.compile(
    r"title=.(?P<id>\d{7}).*?"
    r"<span class=.title.>(?P<kraj>.*?)</span>.*?"
    r"Leto: <strong>(?P<leto>\d*)</strong>.*?"
    r"<div class=.kratek. itemprop=.description.>(?P<opis>.*?)</div>.*?"
    r"<span class=.agencija.>(?P<agencija>.*?)</span>.*?"
    r"<meta itemprop=.price. content=.(?P<cena>\d*).*?",
    flags=re.DOTALL
    )

vzorec_nadstropja= re.compile(
    r"<span class=.atribut.>Nadstropje: <strong>(?P<nadstropja>.*?)</strong>.*?" 
    )

vzorec_povrsina_zemljisca = re.compile(
    r"Zemljišče: <strong>(?P<povrsina_zemljisca>\d*) m2</strong>.*?"
)

vzorec_povrsina_hise = re.compile(
    r"<span class=.velikost. lang=.sl.>(?P<povrsina_hise>\d*).*? m2"
)


def izloci_iz_oglasa(oglas):
    hisa = vzorec_hise.search(oglas).groupdict() 
    hisa['id'] = int(hisa['id'])
    hisa['leto'] = int(hisa['leto'])
    hisa['cena'] = int(hisa['cena'])
    hisa['opis'] = hisa['opis'].strip()
    
    nadstropja = vzorec_nadstropja.search(oglas)
    if "K" in str(nadstropja):
        hisa['nadstropja'] = str(nadstropja['nadstropja'])
        hisa["ima_klet"] = True
    elif nadstropja:
        hisa['nadstropja'] = str(nadstropja['nadstropja'])
        hisa["ima_klet"] = False
    else:
        hisa['nadstropja'] = None
        hisa["ima_klet"] = None
    
    povrsina_hise = vzorec_povrsina_hise.search(oglas)
    if povrsina_hise:
        hisa['povrsina_hise'] = int(povrsina_hise['povrsina_hise'].replace(".",""))
    else:
        hisa['povrsina_hise'] = None
    
    povrsina_zemljisca = vzorec_povrsina_zemljisca.search(oglas)
    if povrsina_zemljisca:
        hisa['povrsina_zemljisca'] = int(povrsina_zemljisca['povrsina_zemljisca'].replace(".",""))
    else:
        hisa['povrsina_zemljisca'] = None
    return hisa



def ime_datoteke_slovenija(st_strani):
    return f"hise\hise-slovenija-{st_strani}.html"

def ime_datoteke_hrvaska(st_strani):
    return f"hise\hise-hrvaska-{st_strani}.html"

hise = []

st = 0
for st_strani in range(1, 105):
    with open(ime_datoteke_slovenija(st_strani), encoding="utf-8") as dat:
        vsebina = dat.read()
    for zadetek in re.finditer(vzorec_oglasa, vsebina):
        hisa = izloci_iz_oglasa(zadetek.group(0))
        hisa["drzava"] = "Slovenija"
        hise.append(hisa)
        st += 1

for st_strani in range(1, 54):
    with open(ime_datoteke_hrvaska(st_strani), encoding="utf-8") as dat:
        vsebina = dat.read()
    for zadetek in re.finditer(vzorec_oglasa, vsebina):
        hisa = izloci_iz_oglasa(zadetek.group(0))
        hisa["drzava"] = "Hrvaska"
        hise.append(hisa)
        st += 1

print(st) 


with open("hise.csv", "w", encoding="utf-8") as dat:
    writer = csv.DictWriter(dat, [
        "id",
        "kraj",
        "leto",
        "cena",
        "agencija",
        "opis",
        "nadstropja",
        "povrsina_zemljisca",
        "povrsina_hise",
        "ima_klet",
        "drzava"
    ])
    writer.writeheader()
    writer.writerows(hise)
