import os
import sys

from data_loader import load_user_stories
from story_analyzer import analyze_all_stories, generate_analysis_summary
from ai_agent import generate_user_story_report


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "data/user_stories.csv"

    try:
        print(f"Ucitavanje user stories iz fajla: {file_path}\n")

        stories = load_user_stories(file_path)

        print(f"Ucitano je {len(stories)} user stories.\n")

        print("Analiza user stories...\n")

        analysis_results = analyze_all_stories(stories)
        summary = generate_analysis_summary(analysis_results)

        print("=== REZIME ANALIZE ===")
        print(f"Ukupno user stories: {summary['total']}")
        print(f"Dobri zahtevi: {summary['good']}")
        print(f"Potrebna dorada: {summary['needs_improvement']}")
        print(f"Kriticni zahtevi: {summary['critical']}")
        print(f"Prosecna ocena kvaliteta: {summary['average_score']}/100")
        print()

        print("Generisanje AI izvestaja...\n")

        report = generate_user_story_report(summary, analysis_results)

        print(report)

        os.makedirs("output", exist_ok=True)

        input_file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = f"output/{input_file_name}_report.md"

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(report)

        print(f"\nIzvestaj je sacuvan u fajl: {output_path}")

    except FileNotFoundError as error:
        print(f"Greska: {error}")

    except ValueError as error:
        print(f"Greska u podacima: {error}")

    except RuntimeError as error:
        print(f"Greska pri radu AI agenta: {error}")

    except Exception as error:
        print(f"Neocekivana greska: {error}")


if __name__ == "__main__":
    main()