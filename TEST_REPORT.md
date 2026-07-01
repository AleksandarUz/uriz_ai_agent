# TEST_REPORT.md

# Test izveštaj — User Story Quality AI Agent

Ovaj dokument predstavlja validaciju AI agenta nad tri različita primera ulaznih podataka. Cilj testiranja je da se proveri da li agent pravilno učitava CSV fajl, analizira kvalitet user stories, identifikuje probleme i rizike, generiše strukturisan Markdown izveštaj i čuva rezultat u `output/` folder.

Agent je testiran na sledećim scenarijima:

1. Mešani backlog
2. Kvalitetan backlog
3. Kritičan backlog

---

## Test 1 — Mešani backlog

### Ulazni fajl

```text
data/test_cases/test_1_mixed_backlog.csv
```

### Opis scenarija

Ovaj test predstavlja realan backlog u kome postoje i dobro napisani zahtevi i zahtevi koji zahtevaju doradu.

Ulaz sadrži 5 user stories:

- 2 user stories su dobro napisane;
- 2 user stories zahtevaju doradu;
- 1 user story je kritična.

### Komanda za pokretanje

```powershell
python main.py data/test_cases/test_1_mixed_backlog.csv
```

### Dobijeni rezime

```text
Ukupno user stories: 5
Dobri zahtevi: 2
Potrebna dorada: 2
Kriticni zahtevi: 1
Prosecna ocena kvaliteta: 72.0/100
```

### Generisani izveštaj

Izveštaj je sačuvan u fajl:

```text
output/test_1_mixed_backlog_report.md
```

### Validacija rezultata

Agent je ispravno prepoznao da postoje dve kvalitetne user stories i tri problematične user stories.

Kao problematični zahtevi označeni su:

- `US-3 - Plaćanje karticom`, zato što je opis prekratak i nije napisan u standardnom user story formatu;
- `US-4 - Admin panel`, zato što opis nije dovoljno precizan;
- `US-5 - Notifikacije`, zato što nema opis.

Zaključak: rezultat je ispravan i koristan jer agent razlikuje dobre i loše zahteve i daje preporuke za njihovu doradu.

---

## Test 2 — Kvalitetan backlog

### Ulazni fajl

```text
data/test_cases/test_2_good_backlog.csv
```

### Opis scenarija

Ovaj test predstavlja kvalitetan backlog u kome su svi zahtevi napisani u user story formatu i imaju jasnu ulogu, funkcionalnost i vrednost za korisnika.

### Komanda za pokretanje

```powershell
python main.py data/test_cases/test_2_good_backlog.csv
```

### Dobijeni rezime

```text
Ukupno user stories: 5
Dobri zahtevi: 5
Potrebna dorada: 0
Kriticni zahtevi: 0
Prosecna ocena kvaliteta: 100.0/100
```

### Generisani izveštaj

Izveštaj je sačuvan u fajl:

```text
output/test_2_good_backlog_report.md
```

### Validacija rezultata

Agent je ispravno prepoznao da su svi zahtevi dobrog kvaliteta.

U izveštaju je navedeno:

- da nema značajnih problema;
- da nema posebnih preporuka za poboljšanje;
- da nema potrebe za dodatnim acceptance criteria i test scenarijima za problematične zahteve.

Zaključak: rezultat je ispravan jer agent ne izmišlja rizike kada su ulazni podaci kvalitetni.

---

## Test 3 — Kritičan backlog

### Ulazni fajl

```text
data/test_cases/test_3_critical_backlog.csv
```

### Opis scenarija

Ovaj test predstavlja loše definisan backlog u kome većina zahteva ima veoma kratak opis ili nema opis. Više zahteva ima visok prioritet, što povećava rizik za projekat.

### Komanda za pokretanje

```powershell
python main.py data/test_cases/test_3_critical_backlog.csv
```

### Dobijeni rezime

```text
Ukupno user stories: 5
Dobri zahtevi: 0
Potrebna dorada: 3
Kriticni zahtevi: 2
Prosecna ocena kvaliteta: 49.0/100
```

### Generisani izveštaj

Izveštaj je sačuvan u fajl:

```text
output/test_3_critical_backlog_report.md
```

### Validacija rezultata

Agent je ispravno prepoznao da backlog ima ozbiljne probleme.

Kao problematični ili kritični zahtevi označeni su:

- `US-1 - Login sistem`, zato što je opis prekratak i zahtev je visokog prioriteta;
- `US-2 - Plaćanje`, zato što nema opis i ima visok prioritet;
- `US-3 - Admin panel`, zato što je opis prekratak i zahtev je visokog prioriteta;
- `US-4 - Izveštaji`, zato što je opis prekratak i nije u standardnom user story formatu;
- `US-5 - Notifikacije`, zato što nema opis i ima visok prioritet.

Zaključak: rezultat je ispravan jer agent pravilno eskalira nejasne zahteve, posebno one sa visokim prioritetom.

---

## Zbirni zaključak testiranja

Sva tri testa potvrđuju da agent pravilno obrađuje različite tipove backlog-a:

| Test | Tip backlog-a | Rezultat |
|---|---|---|
| Test 1 | Mešani backlog | Agent razlikuje dobre i problematične zahteve |
| Test 2 | Kvalitetan backlog | Agent ne prijavljuje lažne rizike |
| Test 3 | Kritičan backlog | Agent pravilno označava nejasne i rizične zahteve |

Deterministički deo sistema uspešno i dosledno računa:

- ukupan broj user stories;
- broj dobrih zahteva;
- broj zahteva koji zahtevaju doradu;
- broj kritičnih zahteva;
- prosečnu ocenu kvaliteta;
- listu problema i preporuka.

LLM deo sistema generiše acceptance criteria i test scenarije za problematične zahteve. Kvalitet ovog dela zavisi od lokalnog modela koji se koristi preko Ollama platforme.

---

## Uočena ograničenja tokom testiranja

Tokom testiranja primećeno je da lokalni LLM model ponekad može generisati gramatički slabije formulacije ili predloge koji nisu potpuno precizni.

Zbog toga je u aplikaciji primenjen hibridni pristup:

- tačni brojevi, kategorije, problemi i preporuke generišu se deterministički kroz Python logiku;
- LLM se koristi za pomoćne tekstualne delove, kao što su acceptance criteria i test scenariji;
- ako user story nema opis, agent ne izmišlja detaljne testove, već vraća preporuku da se opis prvo dopuni.

Ovo ograničenje je prihvatljivo za MVP verziju agenta i predstavlja prostor za buduće unapređenje kroz korišćenje jačeg modela, preciznijeg prompta ili direktne integracije sa JIRA podacima.

---

## Zaključak

Testiranje pokazuje da User Story Quality AI Agent ispunjava osnovnu namenu projekta. Agent nije običan chatbot, već sistem sa definisanim ulazom, višekoračnom obradom i strukturisanim izlazom.

Agent može pomoći Product Owner-u, Project Manager-u i QA timu da ranije prepoznaju loše definisane zahteve, smanje rizik pogrešnog razumevanja i pripreme kvalitetnije acceptance criteria i test scenarije.
