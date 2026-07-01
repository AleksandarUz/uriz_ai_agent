import os
import json
import re
from typing import Any

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


load_dotenv()


ACCEPTANCE_CRITERIA_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Ti si AI asistent za Product Owner-a.

Piši isključivo na srpskom jeziku, latinicom.
Nemoj koristiti engleske reči kao "system", već piši "sistem".
Nemoj koristiti hrvatske ili slovenačke izraze.
Ne smeš da menjaš temu user story-ja.
Ne smeš da izmišljaš funkcionalnosti koje nemaju veze sa naslovom i opisom.

Vrati samo 3 bullet stavke.
Svaka stavka mora početi sa:
- AC1:
- AC2:
- AC3:
""",
        ),
        (
            "user",
            """
Napiši 3 acceptance criteria za sledeću user story.

ID: {story_id}
Naslov: {title}
Opis: {description}
Prioritet: {priority}
Status: {status}
Problemi: {issues}

Acceptance criteria moraju biti konkretni i direktno povezani sa ovom user story.
""",
        ),
    ]
)


TEST_SCENARIOS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Ti si AI asistent za QA testera.

Piši isključivo na srpskom jeziku, latinicom.
Nemoj koristiti engleske reči kao "system", već piši "sistem".
Nemoj koristiti hrvatske ili slovenačke izraze.
Ne smeš da menjaš temu user story-ja.
Ne smeš da pišeš testove za drugu funkcionalnost.

Vrati samo 3 bullet stavke.
Svaka stavka mora početi sa:
- Test 1:
- Test 2:
- Test 3:
""",
        ),
        (
            "user",
            """
Napiši 3 osnovna test scenarija za sledeću user story.

ID: {story_id}
Naslov: {title}
Opis: {description}
Prioritet: {priority}
Status: {status}
Problemi: {issues}

Test scenariji moraju biti jasni, praktični i direktno povezani sa ovom user story.
""",
        ),
    ]
)


def get_llm_model():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":
        model_name = os.getenv("OLLAMA_MODEL", "llama3.2")

        return ChatOllama(
            model=model_name,
            temperature=0.2
        )

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY nije postavljen. Dodaj ga u .env ili koristi LLM_PROVIDER=ollama."
            )

        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        return ChatOpenAI(
            model=model_name,
            temperature=0.2
        )

    raise RuntimeError(
        f"Nepoznat LLM_PROVIDER: {provider}. Dozvoljeno je: ollama ili openai."
    )

def clean_llm_text(text: str) -> str:
    replacements = {
        "unio": "uneo",
        "netočne": "neispravne",
        "prihvaća": "prihvata",
        "sistema treba": "sistem treba",
        "sistema proverava": "sistem proverava",
        "sistema ne može": "sistem ne može",
        "kartičke informacije": "podatke kartice",
        "uključujuće": "uključujući",
        "uspešnoj plaćanju": "uspešnom plaćanju",
        "odmogući": "onemogući",
        "prikaze": "prikaže",
        "obrisuje": "obriše",
        "odmahnije": "odbije",
        "odmahnje": "odbije",
        "brise": "briše",
        "dodaje u bazu": "doda u bazu",
        "sa unosa podataka": "unosom podataka",
        "preko dozvoljenog granica": "preko dozvoljene granice",
    }

    cleaned_text = text

    for old, new in replacements.items():
        cleaned_text = cleaned_text.replace(old, new)

    return cleaned_text


def is_bad_llm_output(text: str, expected_prefix: str) -> bool:
    forbidden_patterns = [
        r"[\u4e00-\u9fff]",  # kineski znakovi
        r"[\u0400-\u04FF]",  # ćirilica/ruski tekst
    ]

    for pattern in forbidden_patterns:
        if re.search(pattern, text):
            return True

    if text.count(expected_prefix) > 1:
        return True

    if len(text) > 1200:
        return True

    return False


def fallback_acceptance_criteria(story: dict) -> str:
    title = story["title"].lower()

    if "plać" in title or "plac" in title:
        return (
            "- AC1: Kupac može da izabere plaćanje karticom tokom procesa kupovine.\n"
            "- AC2: Sistem proverava da li su podaci kartice ispravno uneti.\n"
            "- AC3: Sistem prikazuje poruku o uspešnom ili neuspešnom plaćanju."
        )

    if "admin" in title:
        return (
            "- AC1: Administrator može da pristupi admin panelu.\n"
            "- AC2: Administrator može da pregleda listu korisnika.\n"
            "- AC3: Administrator može da dodaje, menja ili briše korisnike."
        )

    if "login" in title or "prijav" in title:
        return (
            "- AC1: Korisnik može da unese korisničko ime ili email i lozinku.\n"
            "- AC2: Sistem proverava tačnost unetih podataka.\n"
            "- AC3: Sistem prikazuje grešku ako su podaci neispravni."
        )

    if "izvešt" in title or "izvest" in title:
        return (
            "- AC1: Korisnik može da izabere tip izveštaja.\n"
            "- AC2: Sistem generiše izveštaj na osnovu dostupnih podataka.\n"
            "- AC3: Korisnik može da pregleda generisani izveštaj."
        )

    return (
        "- AC1: User story mora imati jasno definisanu ulogu korisnika.\n"
        "- AC2: User story mora imati jasno definisanu funkcionalnost.\n"
        "- AC3: User story mora imati jasno definisanu vrednost za korisnika."
    )


def fallback_test_scenarios(story: dict) -> str:
    title = story["title"].lower()

    if "plać" in title or "plac" in title:
        return (
            "- Test 1: Proveriti uspešno plaćanje sa ispravnim podacima kartice.\n"
            "- Test 2: Proveriti odbijanje plaćanja sa neispravnim podacima kartice.\n"
            "- Test 3: Proveriti prikaz poruke o grešci kada plaćanje nije uspešno."
        )

    if "admin" in title:
        return (
            "- Test 1: Proveriti da administrator može da pristupi admin panelu.\n"
            "- Test 2: Proveriti da administrator može da pregleda korisnike.\n"
            "- Test 3: Proveriti da administrator može da doda, izmeni ili obriše korisnika."
        )

    if "login" in title or "prijav" in title:
        return (
            "- Test 1: Proveriti uspešnu prijavu sa ispravnim podacima.\n"
            "- Test 2: Proveriti neuspešnu prijavu sa pogrešnom lozinkom.\n"
            "- Test 3: Proveriti validaciju kada su polja za prijavu prazna."
        )

    if "izvešt" in title or "izvest" in title:
        return (
            "- Test 1: Proveriti uspešno generisanje izveštaja.\n"
            "- Test 2: Proveriti generisanje izveštaja za različite periode.\n"
            "- Test 3: Proveriti poruku o grešci ako nema podataka za izveštaj."
        )

    return (
        "- Test 1: Proveriti da user story ima jasan opis.\n"
        "- Test 2: Proveriti da opis sadrži ulogu, funkcionalnost i vrednost.\n"
        "- Test 3: Nakon dopune opisa, pripremiti konkretne funkcionalne testove."
    )

def get_problematic_stories(
    analysis_results: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    return [
        story for story in analysis_results
        if story.get("issues")
    ]


def build_deterministic_report_part(
    summary: dict[str, Any],
    analysis_results: list[dict[str, Any]]
) -> str:
    lines = []

    lines.append("# User Story Quality Report")
    lines.append("")
    lines.append("## 1. Pregled kvaliteta backlog-a")
    lines.append("")
    lines.append(f"- Ukupan broj analiziranih user stories: **{summary['total']}**")
    lines.append(f"- Broj dobrih user stories: **{summary['good']}**")
    lines.append(f"- Broj user stories koje zahtevaju doradu: **{summary['needs_improvement']}**")
    lines.append(f"- Broj kritičnih user stories: **{summary['critical']}**")
    lines.append(f"- Prosečna ocena kvaliteta: **{summary['average_score']}/100**")
    lines.append("")

    lines.append("## 2. Identifikovani problemi i rizici")
    lines.append("")

    problematic_stories = get_problematic_stories(analysis_results)

    if not problematic_stories:
        lines.append("Nisu identifikovani značajni problemi u analiziranim user stories.")
    else:
        for story in problematic_stories:
            lines.append(f"### {story['id']} - {story['title']}")
            lines.append(f"- Kategorija kvaliteta: **{story['quality']}**")
            lines.append(f"- Prioritet: **{story['priority']}**")
            lines.append(f"- Status: **{story['status']}**")
            lines.append("- Problemi:")

            for issue in story["issues"]:
                lines.append(f"  - {issue}")

            lines.append("")

    lines.append("## 3. Preporuke za poboljšanje")
    lines.append("")

    if not problematic_stories:
        lines.append("Nema posebnih preporuka jer su svi user stories dobrog kvaliteta.")
    else:
        for story in problematic_stories:
            lines.append(f"### {story['id']} - {story['title']}")

            for recommendation in story["recommendations"]:
                lines.append(f"- {recommendation}")

            lines.append("")

    return "\n".join(lines)


def generate_acceptance_criteria_for_story(
    llm,
    story: dict[str, Any]
) -> str:
    description = story.get("description", "").strip()

    if not description:
        return (
            "- AC1: Nije moguće pouzdano definisati acceptance criteria jer user story nema opis.\n"
            "- AC2: Product Owner treba prvo da dopuni opis user story-ja.\n"
            "- AC3: Nakon dopune opisa moguće je definisati jasne kriterijume prihvatanja."
        )

    chain = ACCEPTANCE_CRITERIA_PROMPT | llm | StrOutputParser()

    result = chain.invoke(
    {
        "story_id": story["id"],
        "title": story["title"],
        "description": story["description"],
        "priority": story["priority"],
        "status": story["status"],
        "issues": json.dumps(story["issues"], ensure_ascii=False),
    }
    )
    cleaned_result = clean_llm_text(result)

    if is_bad_llm_output(cleaned_result, "- AC1:"): 
        return fallback_acceptance_criteria(story)

    return cleaned_result





def generate_test_scenarios_for_story(
    llm,
    story: dict[str, Any]
) -> str:
    description = story.get("description", "").strip()

    if not description:
        return (
            "- Test 1: Proveriti da user story sadrži jasan opis pre početka testiranja.\n"
            "- Test 2: Proveriti da opis sadrži ulogu korisnika, funkcionalnost i očekivanu vrednost.\n"
            "- Test 3: Nakon dopune opisa, pripremiti konkretne funkcionalne testove."
        )

    chain = TEST_SCENARIOS_PROMPT | llm | StrOutputParser()

    result = chain.invoke(
    {
        "story_id": story["id"],
        "title": story["title"],
        "description": story["description"],
        "priority": story["priority"],
        "status": story["status"],
        "issues": json.dumps(story["issues"], ensure_ascii=False),
    })
    cleaned_result = clean_llm_text(result)

    if is_bad_llm_output(cleaned_result, "- Test 1:"):
        return fallback_test_scenarios(story)

    return cleaned_result



def generate_ai_sections(
    analysis_results: list[dict[str, Any]]
) -> str:
    problematic_stories = get_problematic_stories(analysis_results)

    if not problematic_stories:
        return (
            "## 4. Predlog acceptance criteria\n\n"
            "Nema problematičnih user stories za koje je potrebno generisati dodatne acceptance criteria.\n\n"
            "## 5. Predlog test scenarija\n\n"
            "Nema problematičnih user stories za koje je potrebno generisati dodatne test scenarije.\n"
        )

    llm = get_llm_model()

    lines = []

    lines.append("## 4. Predlog acceptance criteria")
    lines.append("")

    for story in problematic_stories:
        lines.append(f"### {story['id']} - {story['title']}")

        try:
            acceptance_criteria = generate_acceptance_criteria_for_story(llm, story)
            lines.append(acceptance_criteria)
        except Exception as error:
            lines.append(f"- Greška pri generisanju acceptance criteria: {error}")

        lines.append("")

    lines.append("## 5. Predlog test scenarija")
    lines.append("")

    for story in problematic_stories:
        lines.append(f"### {story['id']} - {story['title']}")

        try:
            test_scenarios = generate_test_scenarios_for_story(llm, story)
            lines.append(test_scenarios)
        except Exception as error:
            lines.append(f"- Greška pri generisanju test scenarija: {error}")

        lines.append("")

    return "\n".join(lines)


def generate_user_story_report(
    summary: dict[str, Any],
    analysis_results: list[dict[str, Any]]
) -> str:
    deterministic_part = build_deterministic_report_part(summary, analysis_results)
    ai_part = generate_ai_sections(analysis_results)

    return deterministic_part + "\n\n" + ai_part