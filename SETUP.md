# One-time setup

Do these once, in order. After that, the whole pipeline runs itself every
weekday morning -- nothing left to click.

## 1. Create the GitHub repo

Create a new repo and add these files to it, keeping the folder structure
as-is (`.github/workflows/briefing.yml` has to stay at that exact path for
GitHub to recognize it). Public is simplest and fully free; private also
works, it just uses a small slice of your free Actions minutes.

## 2. Turn on GitHub Pages

- In the repo: **Settings -> Pages**
- Under "Build and deployment," set Source to **Deploy from a branch**,
  branch `main`, folder `/docs`
- Save. GitHub gives you a URL like
  `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME` -- note it down
- Open `scripts/generate_episode.py` and paste that URL into `SITE_URL`
  near the top of the file

## 3. Set up Google Cloud (for the voice)

- Go to console.cloud.google.com and create a new project (any name)
- Search for "Text-to-Speech API" and enable it
- You'll be asked to enable billing -- go ahead. This pipeline uses well
  under 1% of the free monthly allowance. As a safety net, go to
  **Billing -> Budgets & alerts** and set a $1 budget alert
- Go to **IAM & Admin -> Service Accounts -> Create Service Account**
  (any name is fine)
- Open the new service account -> **Keys -> Add Key -> JSON**. This
  downloads a JSON file -- keep it private, never commit it to the repo
  (the included `.gitignore` helps guard against that)

## 4. Create the Google Doc Claude will write to

- Create a new blank Google Doc, name it anything (e.g. "Daily Briefing
  Draft")
- Open the JSON file from step 3 and find the `client_email` field --
  it looks like `something@your-project.iam.gserviceaccount.com`
- Share the Doc with that email address, same as sharing with a person,
  giving it Viewer access
- Copy the Doc's ID out of its URL:
  `docs.google.com/document/d/THIS-PART-HERE/edit`

## 5. Add secrets to GitHub

In the repo: **Settings -> Secrets and variables -> Actions -> New
repository secret**. Add two:

- `GOOGLE_SERVICE_ACCOUNT_JSON` -- paste the entire contents of the JSON
  file from step 3
- `GOOGLE_DOC_ID` -- paste the Doc ID from step 4

## 6. Set up the Claude scheduled task

- In claude.ai, open this Project and create a Scheduled Task (weekday
  mornings, ahead of the 6:52am Actions trigger -- e.g. 6:30am)
- Add one instruction to the prompt: after writing the briefing, save the
  full text into the Google Doc from step 4, overwriting whatever was
  there before, using your Google Drive connector

## 7. Test it by hand before trusting the schedule

- In the repo's **Actions** tab, find "Generate daily briefing episode"
  and click **Run workflow** to fire it manually -- don't wait for the
  cron trigger
- Check the `docs/` folder afterward for a new `.mp3` file and an updated
  `feed.xml`
- If it fails, the Actions log will show exactly which step broke --
  most first-run issues are a typo in one of the two secrets

## 8. Subscribe in Apple Podcasts

- Open Apple Podcasts -> **Library** -> **•••** -> **Follow a Show by
  URL**
- Paste `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/feed.xml`
- Done. From here, everything just happens on its own every weekday
  morning.
