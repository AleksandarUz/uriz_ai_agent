from typing import Any


def has_user_story_format(description: str) -> bool:
    description_lower = description.lower()

    has_role = "kao" in description_lower
    has_goal = "želim" in description_lower or "zelim" in description_lower
    has_value = "da bih" in description_lower

    return has_role and has_goal and has_value


def analyze_story(story: dict[str, Any]) -> dict[str, Any]:
    issues = []
    recommendations = []
    score = 100

    story_id = story.get("id", "")
    title = story.get("title", "")
    description = story.get("description", "")
    priority = story.get("priority", "")
    status = story.get("status", "")

    if not title:
        issues.append("User story nema naslov.")
        recommendations.append("Dodati kratak i jasan naslov.")
        score -= 20

    if not description:
        issues.append("User story nema opis.")
        recommendations.append(
            "Dodati opis u formatu: Kao [uloga], želim [funkcionalnost], da bih [vrednost]."
        )
        score -= 40
    else:
        if len(description.split()) < 8:
            issues.append("Opis user story-ja je prekratak.")
            recommendations.append("Proširiti opis tako da bude jasnije šta korisnik želi.")
            score -= 20

        if not has_user_story_format(description):
            issues.append("Opis nije napisan u standardnom user story formatu.")
            recommendations.append(
                "Preformulisati opis u formatu: Kao [uloga], želim [funkcionalnost], da bih [vrednost]."
            )
            score -= 25

    if not priority:
        issues.append("Prioritet nije definisan.")
        recommendations.append("Dodati prioritet: High, Medium ili Low.")
        score -= 10

    if not status:
        issues.append("Status nije definisan.")
        recommendations.append("Dodati status: To Do, In Progress ili Done.")
        score -= 10

    if priority.lower() == "high" and issues:
        issues.append("Visok prioritet sa nedovoljno jasnim zahtevom predstavlja rizik za projekat.")
        recommendations.append(
            "Ovaj zahtev treba dodatno razraditi pre početka implementacije."
        )
        score -= 10

    if score < 0:
        score = 0

    if score >= 80:
        quality = "Good"
    elif score >= 50:
        quality = "Needs improvement"
    else:
        quality = "Critical"

    return {
        "id": story_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": status,
        "score": score,
        "quality": quality,
        "issues": issues,
        "recommendations": recommendations,
    }


def analyze_all_stories(stories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results = []

    for story in stories:
        analyzed_story = analyze_story(story)
        results.append(analyzed_story)

    return results


def generate_analysis_summary(analysis_results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(analysis_results)

    good = len([story for story in analysis_results if story["quality"] == "Good"])
    needs_improvement = len(
        [story for story in analysis_results if story["quality"] == "Needs improvement"]
    )
    critical = len([story for story in analysis_results if story["quality"] == "Critical"])

    average_score = 0

    if total > 0:
        total_score = sum(story["score"] for story in analysis_results)
        average_score = round(total_score / total, 1)

    return {
        "total": total,
        "good": good,
        "needs_improvement": needs_improvement,
        "critical": critical,
        "average_score": average_score,
    }