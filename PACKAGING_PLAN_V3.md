# Fathom Scraper - Hardened Packaging Plan (v3)

**Version:** 3.0
**Status:** Not Started

This document is the final, comprehensive source of truth for packaging the Fathom Scraper. It incorporates expert feedback and critical user experience (UX) enhancements to ensure the final installers are robust, secure, communicative, and professional.

**Core Strategy:** The strategy is to create **platform-native installers** that configure a self-contained, controlled environment. The key is to work *with* platform security and user expectations, providing constant feedback throughout the installation and first-run process.

---

## Progress Tracker

### Phase 0: Pre-Packaging Code Hardening
*Goal: To make the application code itself portable, secure, and verifiably correct before packaging.*

- [ ] **Step 0.1: Fully Isolate Application State**
    - **Action:** Modify the code to use the `platformdirs` library for all dynamic files (`meetings_master_list.json`, logs, etc.).
    - **Hardening 1a (Critical): Isolate Playwright's Browser Cache.**
        - **Action:** Set the `PLAYWRIGHT_BROWSERS_PATH` environment variable to a `browsers` subdirectory within the `platformdirs` data directory.
    - **Hardening 1b (Critical): Secure Credentials with OS Keychain.**
        - **Action:** Replace the clear-text `.env` file with the `keyring` library. Update all credential handling logic to use `keyring`.

- [ ] **Step 0.2: Implement Robust & Communicative First Run**
    - **Action:** Create a first-run wizard for setting credentials. Add a "Change Credentials" option to the main menu.
    - **Hardening 2a (Critical): Add Rich Status Indicators.**
        - **Action:** Within the Python code, wrap long-running operations (especially the initial Playwright browser download) with `rich.status`. This provides a visual spinner and prevents the user from seeing a "frozen" terminal.
    - **Hardening 2b (macOS): Post-Install Wizard Launch.**
        - **Action:** The macOS installer's post-install script will immediately launch the app for the first time to ensure credential-writing happens outside the app's quarantine sandbox.
    - **Hardening 2c (Critical): Add a Regression Test Suite.**
        - **Action:** Create a `tests/` directory with a `pytest` and `pytest-playwright` test suite to run against a dummy local server. This suite **must pass** before building any release.

---

### Phase 1: Professional Project Structuring
*Goal: To organize the project into a standard, reproducible format that build tools can rely on.*

- [ ] **Step 1.1: Adopt a Standard `src` Layout and `pyproject.toml`**
    - **Action:** Move all Python source files into a `src/fathom_scraper/` directory. Create a `pyproject.toml` file.
    - **Hardening 1a (Critical): Pin All Dependencies.**
        - **Action:** In `pyproject.toml`, pin the exact versions of *all* application and build-time dependencies to ensure reproducible builds.
    - **Hardening 1b: Use a Modern Build Backend.**
        - **Action:** Specify `hatchling` as the `build-backend` in `pyproject.toml`.
    - **Hardening 1c: Configure Pytest.**
        - **Action:** Add a `[tool.pytest.ini_options]` section to `pyproject.toml` to configure test paths.

---

### Phase 2: Building a Self-Contained, Offline-Ready Distribution
*Goal: To prepare the application for an offline installation, preventing failures due to network issues.*

- [ ] **Step 2.1: Bundle Playwright Browsers Offline**
    - **Action:** Before building, run `playwright install --with-deps --target ./build_assets/browsers` to download browsers. This `browsers` folder will be shipped inside the installer.

- [ ] **Step 2.2: Bundle a Python Runtime**
    - **Action:** Bundle a specific, embeddable Python version (for Windows) or relocatable framework build (for macOS) inside the installers.

- [ ] **Step 2.3: Build a Python Wheel**
    - **Action:** Run `python -m build` to create a `.whl` file from the source code.

---

### Phase 3: Creating Professional, Signed, and Communicative Installers
*Goal: To create trustworthy, user-friendly installers that provide constant feedback.*

- [ ] **Step 3.1: Create Windows Installer (Inno Setup)**
    - **Action:** Write an Inno Setup script (`.iss`) to build the `.exe` installer.
    - **Hardening 3a (Critical): Informative Installer UI.**
        - **Action:** The installer UI must display descriptive status text during each stage (e.g., "Installing Python runtime...", "Configuring browser environment...").
        - **Action:** The final page must include a "Launch Fathom Scraper" checkbox.
    - **Hardening 3b (Critical): Code Signing.**
        - **Action:** The installer `.exe` and any bundled `.dll` files **must be code-signed** with a valid Authenticode certificate.
    - **Hardening 3c (Critical): Per-User Installs & No UAC.**
        - **Action:** Configure the installer for `PrivilegesRequired=lowest` to default to a per-user installation and avoid UAC prompts.

- [ ] **Step 3.2: Create macOS Installer (`.pkg`)**
    - **Action:** Write shell scripts using `pkgbuild` and `productbuild` to create a native `.pkg` installer.
    - **Hardening 3d (Critical): Visible Post-Install Script.**
        - **Action:** The post-install script must not be silent. It must `echo` clear status messages to the installer's log window.
    - **Hardening 3e (Critical): Notarization.**
        - **Action:** The final `.pkg` file **must be notarized** by Apple using `notarytool`.
    - **Hardening 3f (Critical): Create an `.app` Bundle.**
        - **Action:** Create a minimal `FathomScraper.app` bundle containing a launcher stub for a native, double-clickable experience.
    - **Hardening 3g: Sign Post-Install Scripts.**
        - **Action:** The post-install script itself must be signed as part of the package.

---

### Phase 4: Rigorous, Automated Verification
*Goal: To prove that the installers and the application work flawlessly on clean systems.*

- [ ] **Step 4.1: Automate Clean-VM Testing via CI**
    - **Action:** Set up a CI workflow (e.g., GitHub Actions) to build the installers and test them on fresh `windows-latest` and `macos-latest` VMs. The CI will run the `pytest` suite on the installed application.

- [ ] **Step 4.2: Add Uninstallation and Disk Space Tests**
    - **Action:** The CI workflow must also test the uninstaller and log the final installation's disk space usage.

---

### Cross-Cutting Enhancements
*Goal: To add professional touches that improve maintainability and user trust.*

- [ ] **Step 5.1: Implement Versioning and Telemetry**
    - **Action:** Add a `__version__` string and a `--version` flag.
    - **Action:** Use `rich.traceback.install()` to write detailed crash logs to a file in the user's data directory.

- [ ] **Step 5.2: Add Self-Update and Documentation**
    - **Action:** Add a "Check for updates" menu item that queries the GitHub Releases API.
    - **Action:** Create `INSTALL.md` with OS support, disk space needs, and SHA256 checksums for releases. 