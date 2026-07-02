# User Story Quality AI Agent

User Story Quality AI Agent je jednostavan AI agent razvijen u Python programskom jeziku korišćenjem LangChain framework-a i lokalnog LLM modela preko Ollama platforme.

Agent analizira kvalitet user stories iz backlog-a, identifikuje probleme i rizike, daje preporuke za poboljšanje i generiše predlog acceptance criteria i test scenarija. Cilj agenta je da pomogne Product Owner-u, Project Manager-u i QA timu da pre početka implementacije prepoznaju nejasne ili nedovoljno definisane zahteve.

---

## Problem koji agent rešava

U softverskim projektima često se dešava da user stories nisu dovoljno jasno napisane. Takvi zahtevi mogu dovesti do:

- pogrešnog razumevanja funkcionalnosti,
- loše implementacije,
- dodatnih izmena tokom razvoja,
- problema u testiranju,
- kašnjenja u projektu.

Product Owner ili Project Manager obično ručno proverava user stories, dopunjava opise i priprema kriterijume prihvatanja. QA inženjer zatim na osnovu tih zahteva priprema test scenarije.

Ovaj agent automatizuje deo tog procesa tako što učitava user stories iz CSV fajla, analizira njihov kvalitet i generiše strukturisan izveštaj.

---

## Kome je agent namenjen

Agent je namenjen sledećim korisnicima:

- Product Owner-u, za proveru kvaliteta user stories;
- Project Manager-u, za identifikaciju rizika u backlog-u;
- QA inženjeru, za pripremu osnovnih test scenarija;
- razvojnom timu, za bolje razumevanje zahteva pre implementacije.

---

## Funkcionalnosti

Agent omogućava:

- učitavanje user stories iz CSV fajla;
- proveru da li user story ima naslov, opis, prioritet i status;
- proveru da li opis prati standardni user story format;
- ocenjivanje kvaliteta svakog zahteva;
- identifikaciju problematičnih i kritičnih zahteva;
- generisanje preporuka za poboljšanje;
- generisanje acceptance criteria pomoću LLM modela;
- generisanje test scenarija pomoću LLM modela;
- čuvanje finalnog izveštaja u Markdown fajl.

---

## Ulazni podaci

Ulazni podaci se nalaze u fajlu:

```text
data/user_stories.csv
```

CSV fajl mora imati sledeće kolone:

```csv
id,title,description,priority,status
```

Primer ulaza:

```csv
id,title,description,priority,status
US-1,Login korisnika,Kao korisnik želim da se prijavim pomoću email-a i lozinke da bih pristupio svom nalogu,High,To Do
US-2,Registracija korisnika,Kao novi korisnik želim da napravim nalog da bih mogao da koristim aplikaciju,High,To Do
US-3,Plaćanje karticom,Kao kupac želim da platim karticom,High,In Progress
US-4,Admin panel,Admin panel za upravljanje korisnicima,Medium,To Do
US-5,Notifikacije,,Low,To Do
```

---

## Izlazni podaci

Agent generiše Markdown izveštaj i čuva ga u fajl:

```text
output/user_story_report.md
```

Izveštaj sadrži sledeće sekcije:

1. Pregled kvaliteta backlog-a
2. Identifikovani problemi i rizici
3. Preporuke za poboljšanje
4. Predlog acceptance criteria
5. Predlog test scenarija

Primer dela izlaza:

```markdown
## 1. Pregled kvaliteta backlog-a

- Ukupan broj analiziranih user stories: 5
- Broj dobrih user stories: 2
- Broj user stories koje zahtevaju doradu: 2
- Broj kritičnih user stories: 1
- Prosečna ocena kvaliteta: 72.0/100
```

---

## Workflow agenta

Agent radi kroz četiri glavna koraka:

### 1. Učitavanje podataka

Modul `data_loader.py` učitava user stories iz CSV fajla i proverava da li postoje sve potrebne kolone.

Ako CSV fajl ne postoji ili nema potrebne kolone, aplikacija prikazuje poruku o grešci.

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

### 4. Čuvanje izveštaja

Fajl `main.py` povezuje sve module, pokreće ceo workflow i čuva rezultat u `output/user_story_report.md`.

---

## Zašto agent nije običan chatbot

Ovaj agent nije običan chatbot zato što ne vodi slobodan razgovor sa korisnikom, već ima jasno definisan zadatak i strukturisan workflow.

Razlika:

| Chatbot | User Story Quality AI Agent |
|---|---|
| Odgovara na slobodna pitanja | Izvršava konkretan proces analize |
| Nema obavezan format ulaza | Koristi strukturisan CSV fajl |
| Odgovor može biti bilo kog oblika | Izlaz je strukturisan Markdown izveštaj |
| Nema fiksne korake obrade | Ima workflow: učitavanje, analiza, AI generisanje, čuvanje |
| Može odgovoriti bez podataka | Radi na osnovu konkretnih user stories |

---

## Tehnologije

Projekat koristi:

- Python 3.10+
- LangChain
- Ollama
- Qwen2.5 ili Llama 3.2 lokalni LLM model
- pandas
- python-dotenv

---

## Struktura projekta

```text
user-story-ai-agent/
│
├── main.py
├── data_loader.py
├── story_analyzer.py
├── ai_agent.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── user_stories.csv
│
└── output/
    └── user_story_report.md
```

Opis glavnih fajlova:

- `main.py` — ulazna tačka aplikacije;
- `data_loader.py` — modul za učitavanje CSV podataka;
- `story_analyzer.py` — modul za analizu i scoring user stories;
- `ai_agent.py` — modul za rad sa LangChain-om i LLM modelom;
- `data/user_stories.csv` — ulazni podaci;
- `output/user_story_report.md` — generisani izveštaj;
- `.env` — lokalna konfiguracija modela i API ključeva;
- `.env.example` — primer konfiguracionog fajla;
- `requirements.txt` — lista potrebnih Python biblioteka.

---

## Instalacija

### 1. Kloniranje ili preuzimanje projekta

Preuzeti projekat i otvoriti root folder projekta u VS Code-u.

Primer:

```powershell
cd C:\Users\aleks\OneDrive\Desktop\ai_agent
```

### 2. Kreiranje virtualnog okruženja

```powershell
python -m venv venv
```

Ako komanda `python` ne radi, može se koristiti:

```powershell
py -m venv venv
```

### 3. Aktivacija virtualnog okruženja

U PowerShell terminalu:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Nakon aktivacije treba da se pojavi oznaka `(venv)` u terminalu.

### 4. Instalacija biblioteka

```powershell
pip install -r requirements.txt
```

---

## requirements.txt

Fajl `requirements.txt` treba da sadrži:

```txt
pandas>=2.0.0
python-dotenv>=1.0.1
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-ollama>=0.2.0
```

---

## Podešavanje Ollama modela

Projekat koristi lokalni LLM model preko Ollama platforme.

Potrebno je instalirati Ollama i skinuti model.

Primer za Qwen model:

```powershell
ollama pull qwen2.5:7b
```

Ukoliko računar ne može da pokrene veći model, može se koristiti manji:

```powershell
ollama pull qwen2.5:3b
```

Može se koristiti i Llama model:

```powershell
ollama pull llama3.2
```

Provera instaliranih modela:

```powershell
ollama list
```

---

## Podešavanje .env fajla

U root folderu projekta potrebno je napraviti `.env` fajl.

Primer za Ollama:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:7b
```

Ako se koristi manji model:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:3b
```

OpenAI API ključ nije potreban ako se koristi Ollama lokalni model.

Projekat podržava i OpenAI model, ali je za to potreban OpenAI API ključ i aktivan API billing:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

---

## .env.example

Fajl `.env.example` treba da sadrži:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:7b

# OPENAI_API_KEY=your_openai_api_key_here
# OPENAI_MODEL=gpt-4o-mini
```

---

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

---

## Pokretanje aplikacije

Kada je virtualno okruženje aktivirano i biblioteke instalirane, aplikacija se pokreće komandom:

```powershell
python main.py
```

Nakon pokretanja, agent će:

1. učitati user stories iz `data/user_stories.csv`;
2. analizirati njihov kvalitet;
3. prikazati rezime analize u terminalu;
4. generisati AI izveštaj;
5. sačuvati izveštaj u `output/user_story_report.md`.

---

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

Izvestaj je sacuvan u fajl: output/user_story_report.md
```

---

## Error handling

Aplikacija obrađuje sledeće greške:

- nepostojeći CSV fajl;
- nedostajuće kolone u CSV fajlu;
- nepoznat LLM provider;
- nedostajući OpenAI API ključ ako se koristi OpenAI;
- greške prilikom generisanja acceptance criteria;
- greške prilikom generisanja test scenarija.

Ukoliko LLM ne uspe da generiše jedan deo izveštaja, aplikacija ne prekida ceo program, već prikazuje poruku o grešci za taj deo.

---

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

---

## Ograničenja

- Agent trenutno ne povlači podatke direktno iz JIRA API-ja, već koristi CSV fajl kao simulaciju JIRA export-a.
- Kvalitet AI generisanog teksta zavisi od izabranog LLM modela.
- Lokalni modeli ponekad mogu generisati gramatički slabiji tekst.
- Agent ne menja user stories automatski, već daje preporuke za njihovo poboljšanje.
- Ako user story nema opis, agent ne može pouzdano generisati konkretne acceptance criteria i test scenarije.

---

## Mogućnosti za unapređenje

Moguća unapređenja projekta:

- direktna integracija sa JIRA API-jem;
- upload CSV fajla kroz web interfejs;
- čuvanje istorije analiza;
- automatsko dodavanje komentara u JIRA taskove;
- export izveštaja u PDF format;
- preciznije ocenjivanje user stories na osnovu INVEST kriterijuma;
- podrška za više jezika;
- bolji post-processing AI generisanog teksta.

---

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