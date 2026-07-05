# User Story Quality AI Agent

User Story Quality AI Agent je jednostavan AI agent razvijen u Python programskom jeziku korišćenjem LangChain framework-a i lokalnog LLM modela preko Ollama platforme.

Agent analizira kvalitet user stories iz backlog-a, identifikuje probleme i rizike, daje preporuke za poboljšanje i generiše predlog acceptance criteria i test scenarija. Cilj agenta je da pomogne Product Owner-u, Project Manager-u i QA timu da pre početka implementacije prepoznaju nejasne ili nedovoljno definisane zahteve.



## Problem koji agent rešava

U softverskim projektima često se dešava da user stories nisu dovoljno jasno napisane. Takvi zahtevi mogu dovesti do:

- pogrešnog razumevanja funkcionalnosti,
- loše implementacije,
- dodatnih izmena tokom razvoja,
- problema u testiranju,
- kašnjenja u projektu.

Product Owner ili Project Manager obično ručno proverava user stories, dopunjava opise i priprema kriterijume prihvatanja. QA inženjer zatim na osnovu tih zahteva priprema test scenarije.

Ovaj agent automatizuje deo tog procesa tako što učitava user stories iz CSV fajla ili direktno sa JIRA Cloud platforme, analizira njihov kvalitet i generiše strukturisan PDF izveštaj.



## Kome je agent namenjen

Agent je namenjen sledećim korisnicima:

- Product Owner-u, za proveru kvaliteta user stories;
- Project Manager-u, za identifikaciju rizika u backlog-u;
- QA inženjeru, za pripremu osnovnih test scenarija;
- razvojnom timu, za bolje razumevanje zahteva pre implementacije.



## Funkcionalnosti

Agent omogućava:

- učitavanje user stories iz CSV fajla;
- direktno učitavanje Story issue-a sa JIRA Cloud platforme;
- korišćenje JQL upita za filtriranje JIRA podataka;
- konverziju JIRA ADF description formata u običan tekst;
- proveru da li user story ima naslov, opis, prioritet i status;
- proveru da li opis prati standardni user story format;
- ocenjivanje kvaliteta svakog zahteva;
- identifikaciju problematičnih i kritičnih zahteva;
- generisanje preporuka za poboljšanje;
- generisanje acceptance criteria pomoću LLM modela;
- generisanje test scenarija pomoću LLM modela;
- čuvanje finalnog izveštaja u PDF fajl.



## Izvori podataka

Agent podržava dva izvora podataka:

1. CSV fajl;
2. direktno učitavanje Story issue-a sa JIRA Cloud platforme.

### CSV izvor

Podrazumevani ulazni podaci nalaze se u fajlu:

`data/user_stories.csv`

CSV fajl mora imati sledeće kolone:

```text
id,title,description,priority,status
```

```primer
id,title,description,priority,status
US-1,Login korisnika,Kao korisnik želim da se prijavim pomoću email-a i lozinke da bih pristupio svom nalogu,High,To Do
US-2,Registracija korisnika,Kao novi korisnik želim da napravim nalog da bih mogao da koristim aplikaciju,High,To Do
US-3,Plaćanje karticom,Kao kupac želim da platim karticom,High,In Progress
US-4,Admin panel,Admin panel za upravljanje korisnicima,Medium,To Do
US-5,Notifikacije,,Low,To Do
```

CSV Režim se pokreće komandom: python main.py
ili konkretnim CSV fajlom: python main.py data/test_cases/test_1_mixed_backlog.csv

## Jira Cloud izvor

Agent može direktno da učita Story issue-e sa JIRA Cloud platforme preko REST API-ja.

JIRA režim pokreće se komandom: python main.py --jira

U JIRA režimu agent:

- autentifikuje se pomoću JIRA email adrese i API tokena;
- koristi JQL upit za preuzimanje Story issue-a;
- preuzima summary, description, priority i status vrednosti;
- konvertuje JIRA ADF description strukturu u običan tekst;
- mapira JIRA podatke na internu strukturu koju koristi analyzer;
- analizira kvalitet user stories;
- koristi LLM za generisanje acceptance criteria i test scenarija;
- generiše strukturisan PDF izveštaj.

JIRA i CSV izvori vraćaju podatke u istom internom formatu, tako da ostatak workflow-a koristi iste module za analizu, AI generisanje i PDF izlaz.

## Izlaz sistema

Agent generiše strukturisan PDF izveštaj koji sadrži:

1. pregled kvaliteta backlog-a;
2. identifikovane probleme i rizike;
3. preporuke za poboljšanje;
4. predlog acceptance criteria;
5. predlog test scenarija.

Generisani izveštaji čuvaju se u `output/` folderu.
Primer dela izlaza:


## 1. Pregled kvaliteta backlog-a

- Ukupan broj analiziranih user stories: 5
- Broj dobrih user stories: 2
- Broj user stories koje zahtevaju doradu: 2
- Broj kritičnih user stories: 1
- Prosečna ocena kvaliteta: 72.0/100


## Workflow agenta

Agent radi kroz šest glavnih koraka:

### 1. Učitavanje podataka

Agent podržava dva izvora podataka.

Modul `data_loader.py` učitava user stories iz CSV fajla i proverava da li postoje sve potrebne kolone.

Modul `jira_loader.py` povezuje se sa JIRA Cloud REST API-jem, koristi JQL za preuzimanje Story issue-a i mapira dobijene podatke na internu strukturu aplikacije.

Ako CSV fajl ne postoji, nema potrebne kolone ili JIRA API zahtev nije uspešan, aplikacija prikazuje odgovarajuću poruku o grešci.

### 2. Analiza user stories

Modul `story_analyzer.py` analizira svaki zahtev i proverava:

- da li postoji naslov;
- da li postoji opis;
- da li opis ima dovoljno informacija;
- da li opis prati user story format;
- da li postoji prioritet;
- da li postoji status;
- da li visokoprioritetni zahtev ima probleme.

Na osnovu toga svaki user story dobija ocenu kvaliteta od 0 do 100 i kategoriju:

- `Good`
- `Needs improvement`
- `Critical`

### 3. Generisanje AI dela izveštaja

Modul `ai_agent.py` koristi LangChain i LLM model za generisanje acceptance criteria i test scenarija.

Agent koristi hibridni pristup:

- Python deo generiše tačne brojeve, probleme i preporuke;
- LLM deo generiše acceptance criteria i test scenarije.

Ovim se smanjuje mogućnost da model pogreši u osnovnim podacima kao što su broj analiziranih zahteva ili kategorije kvaliteta.

### 4. Generisanje strukturisanog izveštaja

Nakon analize i LLM generisanja, sistem formira kompletan tekstualni izveštaj sa pet sekcija:

1. pregled kvaliteta backlog-a;
2. identifikovani problemi i rizici;
3. preporuke za poboljšanje;
4. predlog acceptance criteria;
5. predlog test scenarija.

### 5. Generisanje PDF dokumenta

Modul `pdf_generator.py` koristi ReportLab biblioteku za generisanje PDF dokumenta.

PDF generator podržava:

- naslove i podnaslove;
- bullet liste;
- srpska latinična slova;
- numeraciju stranica;
- automatsko kreiranje output foldera.

### 6. Čuvanje rezultata

Fajl `main.py` povezuje sve module i upravlja kompletnim workflow-om.

Za CSV ulaz generiše se PDF sa nazivom koji odgovara nazivu ulaznog fajla.

Za JIRA režim generiše se:

`output/jira_backlog_report.pdf`


## Zašto agent nije običan chatbot

Ovaj agent nije običan chatbot zato što ne vodi slobodan razgovor sa korisnikom, već ima jasno definisan zadatak i strukturisan workflow.

Razlika:

| Chatbot | User Story Quality AI Agent |
|---|---|
| Odgovara na slobodna pitanja | Izvršava konkretan proces analize |
| Nema obavezan format ulaza | Koristi CSV ili podatke direktno sa JIRA Cloud platforme |
| Odgovor može biti bilo kog oblika | Izlaz je strukturisan PDF izveštaj |
| Nema fiksne korake obrade | Ima workflow: učitavanje, analiza, AI generisanje, čuvanje |
| Može odgovoriti bez podataka | Radi na osnovu konkretnih user stories |


## Tehnologije

Projekat koristi:

- Python 3.10+
- LangChain
- Ollama
- Qwen2.5 ili Llama 3.2 lokalni LLM model
- pandas
- python-dotenv
- requests
- ReportLab
- JIRA Cloud REST API
- JQL
- GitHub

## Struktura projekta

user-story-ai-agent/
│
├── main.py
├── data_loader.py
├── jira_loader.py
├── story_analyzer.py
├── ai_agent.py
├── pdf_generator.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── TEST_REPORT.md
├── SRS_doc.docx
│
├── data/
│   ├── user_stories.csv
│   └── test_cases/
│       ├── test_1_mixed_backlog.csv
│       ├── test_2_good_backlog.csv
│       └── test_3_critical_backlog.csv
│
└── output/
    ├── user_stories_report.pdf
    ├── test_1_mixed_backlog_report.pdf
    ├── test_2_good_backlog_report.pdf
    ├── test_3_critical_backlog_report.pdf
    └── jira_backlog_report.pdf

Opis glavnih fajlova:

- `main.py` — ulazna tačka aplikacije;
- `pdf_generator.py` — generiše pdf izveštaj;
- `data_loader.py` — modul za učitavanje CSV podataka;
- `story_analyzer.py` — modul za analizu i scoring user stories;
- `ai_agent.py` — modul za rad sa LangChain-om i LLM modelom;
- `data/user_stories.csv` — ulazni podaci;
- `output/user_story_report.pdf` — generisani izveštaj;
- `.env` — lokalna konfiguracija modela i API ključeva;
- `.env.example` — primer konfiguracionog fajla;
- `requirements.txt` — lista potrebnih Python biblioteka.
- `jira_loader.py` — modul za povezivanje sa JIRA Cloud REST API-jem, JQL pretragu, ADF preprocessing i mapiranje JIRA issue-a;


## Instalacija

### 1. Kloniranje ili preuzimanje projekta

Preuzeti projekat i otvoriti root folder projekta u VS Code-u.

Primer: cd C:\Users\aleks\OneDrive\Desktop\ai_agent

### 2. Kreiranje virtualnog okruženja

python -m venv venv

Ako komanda `python` ne radi, može se koristiti: py -m venv venv


### 3. Aktivacija virtualnog okruženja

U PowerShell terminalu:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

Nakon aktivacije treba da se pojavi oznaka `(venv)` u terminalu.

### 4. Instalacija biblioteka

pip install -r requirements.txt


## requirements.txt

Fajl `requirements.txt` treba da sadrži:

pandas>=2.0.0
python-dotenv>=1.0.1
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-ollama>=0.2.0
reportlab
requests>=2.31.0

## Podešavanje Ollama modela

Projekat koristi lokalni LLM model preko Ollama platforme.

Potrebno je instalirati Ollama i skinuti model.

Primer za Qwen model:

    ollama pull qwen2.5:7b

Ukoliko računar ne može da pokrene veći model, može se koristiti manji:

    ollama pull qwen2.5:3b

Može se koristiti i Llama model:

    ollama pull llama3.2


Provera instaliranih modela:

ollama list



## Podešavanje .env fajla

U root folderu projekta potrebno je napraviti `.env` fajl.

Primer za Ollama:

LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:7b


Ako se koristi manji model:

LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:3b


OpenAI API ključ nije potreban ako se koristi Ollama lokalni model.

Projekat podržava i OpenAI model, ali je za to potreban OpenAI API ključ i aktivan API billing:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Za direktnu JIRA integraciju potrebno je dodati:

```env
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token
JIRA_PROJECT_KEY=USQA
```

## .env.example

Fajl `.env.example` treba da sadrži:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:7b

# OPENAI_API_KEY=your_openai_api_key_here
# OPENAI_MODEL=gpt-4o-mini

JIRA_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=
JIRA_PROJECT_KEY=USQA
```

## .gitignore

Fajl `.gitignore` treba da sadrži:

```gitignore
.env
venv/
__pycache__/
*.pyc
output/
```

`.env` fajl se ne postavlja na GitHub jer može sadržati API ključeve i osetljive podatke.



## Pokretanje aplikacije

Agent podržava CSV i JIRA režim rada.

### Pokretanje sa podrazumevanim CSV fajlom

```powershell
python main.py
```

### Pokretanje sa konkretnim CSV fajlom

```powershell
python main.py data/test_cases/test_1_mixed_backlog.csv
```

### Pokretanje sa direktnim Jira izvorom

```powershell
python main.py --jira
```

U JIRA režimu agent direktno učitava Story issue-e iz JIRA projekta definisanog kroz JIRA_PROJECT_KEY vrednost u .env fajlu.

Nakon obrade generiše se: output/jira_backlog_report.pdf

## Primer pokretanja

Primer ispisa u terminalu:

```text
Ucitavanje user stories...

Ucitano je 5 user stories.

Analiza user stories...

=== REZIME ANALIZE ===
Ukupno user stories: 5
Dobri zahtevi: 2
Potrebna dorada: 2
Kriticni zahtevi: 1
Prosecna ocena kvaliteta: 72.0/100

Generisanje AI izvestaja...

Izvestaj je sacuvan u fajl: output/user_story_report.pdf
```



## Error handling

Aplikacija obrađuje sledeće greške:

- nepostojeći CSV fajl;
- nedostajuće kolone u CSV fajlu;
- nepoznat LLM provider;
- nedostajući OpenAI API ključ ako se koristi OpenAI;
- greške prilikom generisanja acceptance criteria;
- greške prilikom generisanja test scenarija.
- nedostajuće JIRA konfiguracione vrednosti;
- neuspešna JIRA autentifikacija;
- nedovoljne dozvole za pristup JIRA projektu;
- timeout JIRA API zahteva;
- greške prilikom povezivanja sa JIRA Cloud platformom;
- neočekivani JIRA API status kodovi.


Ukoliko LLM ne uspe da generiše jedan deo izveštaja, aplikacija ne prekida ceo program, već prikazuje poruku o grešci za taj deo.



## Testiranje

Agent je testiran na različitim primerima user stories:

### Test 1 — Mešani backlog

Ulaz sadrži kombinaciju dobrih i problematičnih user stories.

Očekivani rezultat:

- agent prepoznaje dobre zahteve;
- agent označava prekratke ili nepotpune opise;
- agent generiše preporuke, acceptance criteria i test scenarije.

### Test 2 — Kvalitetan backlog

Ulaz sadrži user stories koje imaju jasan opis, prioritet i status.

Očekivani rezultat:

- većina zahteva dobija kategoriju `Good`;
- agent ne prijavljuje kritične rizike;
- izveštaj potvrđuje da backlog ima dobar kvalitet.

### Test 3 — Kritičan backlog

Ulaz sadrži više zahteva bez opisa ili sa vrlo kratkim opisima.

Očekivani rezultat:

- agent identifikuje više kritičnih ili problematičnih zahteva;
- agent upozorava da visokoprioritetni nejasni zahtevi predstavljaju rizik;
- agent predlaže dopunu user stories pre implementacije.


### Test 4 — Direktna JIRA integracija

Agent je testiran direktnim učitavanjem pet Story issue-a sa JIRA Cloud platforme.

Komanda:

```powershell
python main.py --jira
```

Rezultat:

- učitano je 5 user stories direktno sa JIRA platforme;
- 2 zahteva su ocenjena kao Good;
- 2 zahteva zahtevaju doradu;
- 1 zahtev je ocenjen kao Critical;
- prosečna ocena kvaliteta iznosi 72.0/100;
- generisan je output/jira_backlog_report.pdf.

Ovaj test potvrđuje kompletan workflow:

JIRA Cloud → REST API → JQL → ADF preprocessing → analiza → LLM → PDF.

## Ograničenja

- Agent trenutno samo čita Story issue-e sa JIRA platforme i ne menja ih automatski.
- JIRA integracija zahteva ispravnu lokalnu konfiguraciju i API token.
- Kvalitet AI generisanog teksta zavisi od izabranog LLM modela.
- Lokalni modeli ponekad mogu generisati gramatički slabiji tekst.
- Agent ne menja user stories automatski, već daje preporuke za njihovo poboljšanje.
- Ako user story nema opis, agent ne može pouzdano generisati konkretne acceptance criteria i test scenarije.

---

## Mogućnosti za unapređenje

Moguća unapređenja projekta:

- upload CSV fajla kroz web interfejs;
- čuvanje istorije analiza;
- automatsko dodavanje komentara u JIRA taskove;
- preciznije ocenjivanje user stories na osnovu INVEST kriterijuma;
- podrška za više jezika;
- bolji post-processing AI generisanog teksta.
- automatsko ažuriranje JIRA Story issue-a na osnovu preporuka agenta;
- automatsko dodavanje acceptance criteria u JIRA;
- automatsko dodavanje komentara sa rezultatima analize;
- periodično analiziranje JIRA backlog-a;

## Zaključak

User Story Quality AI Agent predstavlja jednostavan AI alat za podršku Product Owner-u, Project Manager-u i QA timu.

Agent ima jasno definisan ulaz, više koraka obrade, determinističku analizu, LLM komponentu i strukturisan izlaz. Njegova glavna vrednost je u tome što pomaže timu da ranije prepozna loše definisane zahteve, smanji rizik pogrešne implementacije i brže pripremi acceptance criteria i test scenarije.


## JIRA i GitHub integracija

Razvoj projekta je organizovan kroz JIRA projekat sa key-em `USQA`.

Projekat je povezan sa GitHub repozitorijumom, a primer povezivanja prikazan je kroz branch i commit koji sadrže JIRA key.

Primer:

- Branch: `USQA-23-add-jira-github-commit-example`
- Commit: `USQA-23 add Jira GitHub integration example`

Na ovaj način JIRA može da prikaže GitHub aktivnost povezanu sa konkretnim taskom.


## Dodatni AI alat

Tokom razvoja projekta korišćen je ChatGPT kao dodatni AI alat za pomoć pri analizi arhitekture rešenja, unapređenju promptova, rešavanju tehničkih problema i pripremi projektne dokumentacije.

ChatGPT nije deo runtime workflow-a aplikacije. Sam agent koristi LangChain i lokalni LLM model preko Ollama platforme.