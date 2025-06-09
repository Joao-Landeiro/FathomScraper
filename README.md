# Fathom to Markdown Scraper

## 1. Project Overview

This is a headless Python script that automates backing up meeting transcripts from Fathom.video. It uses Playwright for browser automation, supports an interactive menu for ease of use, and includes command-line flags for automation (e.g., cron jobs).

**Current Status:** The application is stable and feature-complete. All core logic for authentication, discovery, and scraping is robust and optimized.

---

## 2. Core Architecture

The scraper is built on a modular, two-stage design to ensure resilience and efficiency.

#### Key Modules & Files:

*   **`cli_v2.py`**: The main entry point and orchestrator. It handles both interactive menu logic and command-line arguments.
*   **`auth_module/`**: Handles all authentication, including the session restoration "fast path."
*   **`scrape.py`**: Contains the `FathomScraper` class, responsible for all browser automation and data extraction.
*   **`export.py`**: Manages the creation of the final Markdown files with correct formatting and YAML frontmatter.
*   **`ui.py`**: A dedicated module using the `rich` library to render the interactive menu, progress bars, and all other user-facing elements.
*   **`env.env`**: Stores user credentials (email, password) and the output directory. Created on first run.
*   **`session.json`**: Caches browser session data (cookies, etc.) to enable fast, subsequent logins without re-entering credentials.
*   **`meetings_master_list.json`**: A master record of all meetings ever discovered. This is the source of truth for the scraping process.
*   **`processed_urls.json`**: A simple list of meeting URLs that have already been successfully scraped and exported, preventing duplicate work.

---

## 3. How to Use the Scraper

#### First-Time Setup

If no `env.env` file is present, the script automatically launches a setup wizard on first run.

1.  **Install Dependencies:**
    ```bash
    # Install Python packages
    pip install -r requirements.txt

    # Install Playwright's browser dependencies
    playwright install
    ```
2.  **Run the Script:**
    ```bash
    python3 cli_v2.py
    ```
    Follow the prompts to configure your credentials. The script will then proceed directly to the main menu.

#### Daily Use (Interactive Menu)

To use the dashboard-style interactive menu, run the script without any arguments:

```bash
python3 cli_v2.py
```

The menu provides a progress bar overview and guided access to all features.

#### Automation (Command-Line Mode)

For automation, use command-line flags to bypass the interactive menu.

1.  **Discover New Meetings:**
    ```bash
    # Efficiently finds any new meetings and adds them to the master list.
    python3 cli_v2.py --discover
    ```
2.  **Scrape New Transcripts:**
    ```bash
    # Scrapes all meetings from the master list that haven't been processed yet.
    python3 cli_v2.py --scrape

    # Scrape a maximum of 5 new meetings.
    python3 cli_v2.py --scrape --limit 5
    ```

---

## 4. Key Logic & State Summary

This section summarizes the "smart" parts of the script for quick context.

*   **Authentication ("Fast Path"):** On startup, the script attempts to restore a session from `session.json`. If successful, it bypasses the entire Google login flow, making startup almost instant. A fresh login is only performed if the session is invalid or doesn't exist.
*   **Optimized Discovery:** The `--discover` process is highly efficient. It first fetches only the most recent page of meetings from the Fathom API. If all meetings on that page are already in `meetings_master_list.json`, it assumes there are no new meetings and stops immediately, avoiding a slow, full history scan.
*   **Stateful Scraping:** The script uses `processed_urls.json` to keep track of what it has already scraped. This ensures that if the process is interrupted, it can be restarted without re-downloading or creating duplicate files.
*   **Dashboard UI:** The interactive menu reads from both the master list and the processed list to generate a real-time progress bar, giving a clear overview of the work completed and remaining.

---

## 5. Project Log

*A reverse-chronological log of major changes and decisions.*

*   **2024-06-18: Implemented Scraping Timestamp**
        *   **Action:** Added a `scrapingdate` field to the YAML frontmatter of exported files, which contains a precise, timezone-aware ISO 8601 timestamp.
        *   **Outcome:** Each file now has valuable metadata for auditing and tracking when it was scraped, distinguishing it from the meeting's original creation date.
*   **2024-06-14: UI & Progress Bar Overhaul**
        *   **Action:** Implemented a dashboard-style main menu featuring a progress bar that visualizes the scraping progress (`scraped` vs. `total`). Refactored the UI and CLI modules to support this, including fixing compatibility issues with the `rich` library version.
        *   **Outcome:** The application now provides a clear, at-a-glance overview of its state, significantly improving user experience.
*   **2024-06-13: Authentication & Session Restoration Overhaul**
        *   **Action:** Performed a major refactor of the `auth_module`. Fixed a persistent and tricky bug that prevented session reuse, forcing a fresh login on every run. The logic was hardened against race conditions, resource cleanup was corrected, and confusing logs were eliminated.
        *   **Outcome:** The "fast path" authentication now works reliably. The script successfully reuses valid sessions, making subsequent runs dramatically faster.
*   **2024-06-13: First-Run Experience & Discovery Optimization**
        *   **Action:** Streamlined the first-run setup to proceed directly to the main menu without requiring a manual restart. Optimized the `--discover` process to be much faster for daily runs by first checking only the most recent page of meetings.
        *   **Outcome:** The script is now more intuitive for new users and more efficient for daily, automated use.
*   **2024-06-12: Initial Stable `cli_v2.py` Architecture**
        *   **Action:** Created a new, stable `cli_v2.py` entry point and refactored the project into a modular, two-stage architecture (`discover` and `scrape`).
        *   **Outcome:** Resolved persistent logic errors and provided a robust, maintainable foundation for the application.
*   **2024-06-11: Core Scraping & Export Logic**
        *   **Action:** Implemented the core data extraction logic. Switched transcript fetching to a more reliable clipboard-based method and fixed character encoding issues in the Markdown export.
        *   **Outcome:** The script can now reliably extract and save full transcripts with correct frontmatter and character encoding.
*   **2024-06-10: API-Based Discovery**
        *   **Action:** Re-engineered the discovery process to use a Fathom API endpoint (`/calls/previous`) with cursor-based pagination.
        *   **Outcome:** Enabled the reliable and efficient discovery of the user's complete meeting history.