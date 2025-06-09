Product Requirements Document (PRD) — Fathom → Markdown Scraper
1 — Objective
Headless-Python script that logs into Fathom with the user's Google credentials (no 2-factor), crawls every meeting transcript, and exports each to an Obsidian-ready Markdown file. Runs automatically once per day at ~21:00 local but can be launched manually.

2 — Background & Constraints
No public Fathom API, so browser automation is required.

Google login without 2FA (username + password only).

Credentials kept in a local .env; code structured so a secrets vault can be swapped in later.

Polite scraping: small randomized waits, respect page-size defaults.

Attachments/video download out of scope.

3 — Requirements
ID	Requirement
R-1 Auth	Use Playwright in headless mode to perform Google OAuth; cache session cookies locally to avoid re-login.
R-2 Discovery	**DECOUPLED DISCOVERY**: A dedicated process (`--discover`) hits the `/calls/previous` API endpoint, handling pagination to fetch all meeting records. It adds any new meeting URLs to a central list (`meeting_urls.md`).
R-3 Data fields	Extract: meeting title (if any), ISO-8601 start datetime, duration, participant names, full transcript.
R-4 Fallback Name	If "other person" name is missing, inject placeholder {{UNKNOWN_PARTICIPANT}} so it's easy to global-replace later.
R-5 Deduplication	**STATEFUL SCRAPING**: A separate process (`--scrape`) reads from `meeting_urls.md`. It maintains a list of already processed URLs (`processed_urls.json`) to prevent re-scraping and ensure fault tolerance.
R-6 Backfill	On first run (when `meeting_urls.md` doesn't exist), the `--discover` command will populate it with all historical meetings.
R-7 Export	Write files to ${OUTPUT_DIR} with filename template: YYYY-MM-DD-<other>-<slug-title>.md.
R-8 Front-matter	YAML block:
yaml<br>---<br>title: "{{title}}"<br>date: "{{start_iso}}"<br>duration: "{{HH:MM:SS}}"<br>participants:<br> - {{name1}}<br> - {{name2}}<br>source: "{{share_url}}"<br>---<br>
R-9 Scheduling	Provide separate CLI flags: `--discover` and `--scrape`. The README will recommend a two-step cron job: first discover, then scrape.
R-10 Logging	Append to fathom_scraper.log; rotate at 1 MB (keep last 3).
R-11 Resilience	Retry any nav/network step up to 3× with exponential back-off (1 s, 2 s, 4 s); the scraping process will skip any meeting that fails after retries and continue with the next.
R-12 Dependencies	playwright>=1.44,<1.45, python-dotenv, pyyaml, beautifulsoup4, rich. Pin minor versions.
R-13 Config	.env keys: GOOGLE_EMAIL, GOOGLE_PASSWORD, OUTPUT_DIR (default ./fathom_notes), HEADLESS=true.
R-14 Structure	Code modules: auth.py, scrape.py, export.py, cli.py. Clear seams for future extensions (alerts, new storage back-end).
R-15 Master List	A human-readable file, `meeting_urls.md`, will serve as the master list of all meeting URLs to be processed, allowing for manual inspection and management.

4 — Non-Goals
Downloading video/audio.

Pushing notes directly into Obsidian vault.

Alerting/monitoring (add later).

5 — Success Metrics
Fresh setup in ≤ 5 minutes (venv + pip install).

First run completes in < 10 minutes for full account history (assumes ≤ 5 years, ≤ 2 000 meetings).

Daily delta runs complete in < 2 minutes for ≤ 100 new meetings.

No duplicate Markdown files across consecutive runs.

6 — Future Enhancements
Slack/email alerts on error.

Swap credential storage to AWS/GCP secrets manager.

Replace scraping with Fathom API when available.

