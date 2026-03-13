from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
GENERATED_DIR = BASE_DIR / "static" / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_HASHTAGS = [
    "#CyberSecurity",
    "#InfoSec",
    "#Ransomware",
    "#ThreatDetection",
    "#BusinessContinuity",
    "#MSSP",
    "#CyberAwareness",
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "newsletter"


def fetch_trending_hashtags(topic: str, max_tags: int = 12) -> list[str]:
    keywords = [w for w in re.split(r"\W+", topic.lower()) if len(w) > 2][:3]
    seeded = []
    for key in keywords:
        seeded.extend(
            [
                f"#{key.title()}",
                f"#{key.title()}Security",
                f"#{key.title()}Awareness",
            ]
        )

    trends_tags = []
    try:
        response = requests.get(
            "https://trends.google.com/trending/rss?geo=US",
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
        titles = re.findall(r"<title>(.*?)</title>", response.text)
        for title in titles[2:15]:
            words = [w for w in re.split(r"\W+", title) if len(w) > 3]
            if not words:
                continue
            tag = "#" + "".join(word.title() for word in words[:2])
            if tag.lower().startswith("#googletrends"):
                continue
            trends_tags.append(tag)
    except Exception:
        pass

    merged = []
    for tag in seeded + DEFAULT_HASHTAGS + trends_tags:
        if tag not in merged:
            merged.append(tag)
    return merged[:max_tags]


def generate_newsletter(topic: str, incident: str, takeaway: str, joke: str, include_comics: bool) -> dict:
    date_label = datetime.now().strftime("%B %d, %Y")
    intro = (
        f"Aloha,\n\n"
        f"This week in Deepwatch Insights, we are focusing on **{topic}**."
        " Cyber incidents move fast, but preparation moves faster when leadership has a clear plan."
    )

    body = (
        f"\n\n{incident.strip()}\n\n"
        "The pattern is always the same: attackers rely on delay, confusion, and weak controls. "
        "Your advantage is to reduce response time and remove easy attack paths before they are exploited."
        f"\n\n**Key Takeaway:** {takeaway.strip()}"
        "\n\nIf your team wants help pressure-testing your defenses before an incident,"
        " call Cypac at 808-861-9595 option 2."
    )

    funnies_text = f"Friday Funnies: {joke.strip()}"
    comics_note = (
        "Friday Funnies Comics: [Insert licensed/original comic here.]"
        if include_comics
        else ""
    )

    return {
        "title": f"Weekly Deepwatch Newsletter — {date_label}",
        "email": intro + body + "\n\nThe Cypac Team\nStan & Howard\nCypac",
        "funnies_text": funnies_text,
        "funnies_comics": comics_note,
        "blog_body": intro + body + "\n\n" + funnies_text,
    }


def create_social_posts(summary: str, hashtags: list[str], wix_url: str) -> dict[str, str]:
    tags = " ".join(hashtags)
    return {
        "LinkedIn": f"{summary}\n\nRead more: {wix_url}\n\n{tags}",
        "Instagram": f"{summary}\n\nLink in bio / {wix_url}\n\n{tags}",
        "Facebook": f"{summary}\n\nRead here: {wix_url}\n\n{tags}",
        "X": f"{summary}\n\n{wix_url}\n\n{tags}",
    }


def generate_image(topic: str) -> str | None:
    prompt = (
        f"Professional cybersecurity newsletter hero image about {topic}, "
        "cinematic blue lighting, SOC monitors, subtle Hawaiian business setting, "
        "clean corporate style, high detail"
    )
    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1600&height=900&nologo=true"
    filename = f"{slugify(topic)}-{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    outfile = GENERATED_DIR / filename

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        outfile.write_bytes(response.content)
        return f"generated/{filename}"
    except Exception:
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        topic = request.form.get("topic", "Cyber resilience")
        incident = request.form.get("incident", "")
        takeaway = request.form.get("takeaway", "Enable MFA, verify requests, and test backups monthly.")
        joke = request.form.get("joke", "Our firewall loves leftovers... it blocks all unknown turkey traffic.")
        include_comics = bool(request.form.get("include_comics"))
        wix_url = request.form.get("wix_url", "https://www.cypac.com/blog/deepwatch")

        newsletter = generate_newsletter(topic, incident, takeaway, joke, include_comics)
        hashtags = fetch_trending_hashtags(topic)
        summary = f"This week's Deepwatch Insight: {topic}. Practical lessons for business leaders to reduce cyber risk."
        socials = create_social_posts(summary, hashtags, wix_url)
        image_path = generate_image(topic)

        result = {
            "newsletter": newsletter,
            "hashtags": hashtags,
            "socials": socials,
            "wix_url": wix_url,
            "image_path": image_path,
            "csg_humor": newsletter["funnies_comics"] or "[No comic selected this week]",
            "csg_insight": newsletter["email"],
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
