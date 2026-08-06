# Setup (current version -- no Google Drive, no Cowork task)

This version writes the briefing itself, inside the GitHub Actions job, by
calling the Anthropic API directly. Nothing depends on your laptop or on
Claude's scheduler being available -- everything runs on GitHub's servers.

Do these steps once, in order.

## 1. The repo itself

Already done if you're reading this in it. Structure needed:

```
news-podcast/
├── .github/workflows/briefing.yml
├── scripts/
│   ├── generate_episode.py
│   └── briefing_prompt.txt
├── docs/                <- created automatically by the script
├── requirements.txt
├── .gitignore
└── SETUP.md
```

## 2. Turn on GitHub Pages (skip if already done)

- **Settings -> Pages**
- Source: **Deploy from a branch**, branch `main`, folder `/docs` -> Save
- Confirm the URL shown matches `SITE_URL` near the top of
  `scripts/generate_episode.py`

## 3. Add the cover art (skip if already done)

- Square JPG, 1400x1400 to 3000x3000px, under ~500KB
- Upload to the repo at exactly `docs/artwork.jpg`

## 4. Set up Google Cloud for the voice (skip if already done)

- console.cloud.google.com -> new project -> enable the **Text-to-Speech
  API**
- **IAM & Admin -> Service Accounts -> Create Service Account** -> open it
  -> **Keys -> Add Key -> JSON** -- downloads a file, keep it private
- That file's entire contents become the `GOOGLE_SERVICE_ACCOUNT_JSON`
  secret in step 6

## 5. Get an Anthropic API key (new)

- Go to **console.anthropic.com -> API Keys -> Create Key**
- This requires billing on file -- pay-as-you-go, separate from any Claude
  subscription. This workload runs on Haiku 4.5 (not Sonnet), one briefing
  a day, capped at 8 searches -- check the Anthropic Console after a week
  or two for an actual cost baseline rather than trusting an estimate here.
  Worth setting a spending limit in the console as a safety net, same idea
  as the earlier TTS budget alert

## 6. Add secrets to GitHub

**Settings -> Secrets and variables -> Actions.** You should end up with
exactly two:

- `ANTHROPIC_API_KEY` -- the key from step 5
- `GOOGLE_SERVICE_ACCOUNT_JSON` -- the full JSON file contents from step 4

If `GOOGLE_DRIVE_FOLDER_ID` exists from an earlier version, delete it --
unused now.

## 7. Retire the Claude scheduled task (new)

If you set up a Cowork scheduled task earlier for this, turn it off or
delete it. It's no longer part of the pipeline -- the GitHub Action writes
the briefing itself now.

## 8. Test by hand before trusting the schedule

- **Actions** tab -> "Generate daily briefing episode" -> **Run workflow**
- This run will take noticeably longer than before -- it's now doing the
  research and writing, not just reading a pre-written Doc. A few minutes
  is normal
- Check the Actions log for errors, and check `docs/episodes/` for a new
  dated `.mp3` afterward
- Open `docs/feed.xml` directly and confirm the episode looks right --
  real title, today's date, a reasonable file size

## 9. Subscribe (skip if already done)

Apple Podcasts -> Library -> ••• -> Follow a Show by URL -> paste your
feed URL (`SITE_URL` + `/feed.xml`)

## 10. The real test

Don't touch anything tomorrow morning. No manual runs, no scheduled
Claude task to worry about anymore -- just the cron trigger in
`briefing.yml` firing on GitHub's own servers. Check Apple Podcasts later
in the day.
