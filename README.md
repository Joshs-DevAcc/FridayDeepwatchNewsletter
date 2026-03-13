# Friday Deepwatch Newsletter Automation App

A lightweight Flask app that helps you generate a weekly Friday content pack:

- Newsletter draft in your preferred tone
- Blog-ready post (automatically excludes comics text)
- Current/trending hashtag suggestions
- Platform-specific social post drafts (LinkedIn, Instagram, Facebook, X)
- CSG/Circle.so split content (IT Humor + Deepwatch Insights)
- AI-generated hero image using Pollinations

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

---

## Suggested weekly workflow (Friday)

1. **Seed content in app**
   - Paste your weekly incident story/content from Elastic Email.
   - Add takeaway + Friday Funnies text.

2. **Generate Friday pack**
   - Click **Generate Friday Pack**.
   - Review newsletter, hashtags, image, social drafts.

3. **Publish blog (Cypac.com)**
   - Use **Blog Draft (No Comics)** output.
   - Upload generated image as thumbnail.
   - Publish and copy the Wix/blog URL.

4. **Publish social posts**
   - Use generated per-platform copy + hashtags + image + blog link.
   - Post to LinkedIn, Instagram, Facebook, X.

5. **Publish to CSG (circle.so)**
   - Put comic in IT Humor.
   - Put full Deepwatch content in Deepwatch Insights.

---

## Recommended tools stack

- **Content source**: Elastic Email
- **Automation/orchestration**: Zapier or Make
- **Scheduling**: Buffer / Hootsuite (optional)
- **Blog + URL**: Wix
- **Community posting**: Circle.so
- **Optional upgrades**:
  - OpenAI/Claude API for more tailored copy generation
  - Canva API for brand-perfect image templates
  - Google Sheets/Airtable for approval workflow + archive

## Practical automation architecture

- Trigger: Every Friday 8:00 AM (Zapier/Make scheduler)
- Pull source: Elastic Email campaign content or inbox parser
- Call this app (or a future API endpoint) to generate newsletter/social packs
- Human approval step in Slack/Email
- Push approved outputs to:
  - Wix draft post
  - Buffer queue for social channels
  - Circle.so posts

