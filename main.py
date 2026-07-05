import os
import sys

from data_loader import load_user_stories
from jira_loader import load_user_stories_from_jira
from story_analyzer import (
    analyze_all_stories,
    generate_analysis_summary,
)
from ai_agent import generate_user_story_report
from pdf_generator import generate_pdf


def main():
    # Provera izvora podataka
    use_jira = "--jira" in sys.argv[1:]

    # Određivanje CSV fajla ako se ne koristi JIRA
    if use_jira:
        file_path = None
    else:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
        else:
            file_path = "data/user_stories.csv"

    try:
        # ==================================================
        # 1. UČITAVANJE PODATAKA
        # ==================================================

        if use_jira:
            print(
                "Ucitavanje user stories direktno sa "
                "JIRA platforme...\n"
            )

            stories = load_user_stories_from_jira()

        else:
            print(
                f"Ucitavanje user stories iz fajla: "
                f"{file_path}\n"
            )

            stories = load_user_stories(file_path)

        print(
            f"Ucitano je {len(stories)} user stories.\n"
        )

        if len(stories) == 0:
            print(
                "Nije pronadjena nijedna user story "
                "za analizu."
            )
            return

        # ==================================================
        # 2. ANALIZA USER STORIES
        # ==================================================

        print("Analiza user stories...\n")

        analysis_results = analyze_all_stories(
            stories
        )

        summary = generate_analysis_summary(
            analysis_results
        )

        # ==================================================
        # 3. ISPIS REZIMEA
        # ==================================================

        print("=== REZIME ANALIZE ===")

        print(
            f"Ukupno user stories: "
            f"{summary['total']}"
        )

        print(
            f"Dobri zahtevi: "
            f"{summary['good']}"
        )

        print(
            f"Potrebna dorada: "
            f"{summary['needs_improvement']}"
        )

        print(
            f"Kriticni zahtevi: "
            f"{summary['critical']}"
        )

        print(
            f"Prosecna ocena kvaliteta: "
            f"{summary['average_score']}/100"
        )

        print()

        # ==================================================
        # 4. AI GENERISANJE
        # ==================================================

        print("Generisanje AI izvestaja...\n")

        report = generate_user_story_report(
            summary,
            analysis_results,
        )

        print(report)

        # ==================================================
        # 5. ODREĐIVANJE OUTPUT FAJLA
        # ==================================================

        os.makedirs(
            "output",
            exist_ok=True,
        )

        if use_jira:
            input_file_name = "jira_backlog"
        else:
            input_file_name = os.path.splitext(
                os.path.basename(file_path)
            )[0]

        output_path = (
            f"output/"
            f"{input_file_name}_report.pdf"
        )

        # ==================================================
        # 6. GENERISANJE PDF-A
        # ==================================================

        print("\nGenerisanje PDF dokumenta...")

        generate_pdf(
            report,
            output_path,
        )

        print(
            f"\nPDF izvestaj je sacuvan u fajl: "
            f"{output_path}"
        )

    except FileNotFoundError as error:
        print(
            f"Greska: {error}"
        )

    except ValueError as error:
        print(
            f"Greska u podacima: {error}"
        )

    except RuntimeError as error:
        print(
            f"Greska pri radu aplikacije: {error}"
        )

    except Exception as error:
        print(
            f"Neocekivana greska: {error}"
        )


if __name__ == "__main__":
    main()