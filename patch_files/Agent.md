# Agent Handover & Log Sheet

Welcome, agent. You are taking over a repository that has undergone a significant overhaul. This document is your guide to understanding the current state of the project, its structure, and the conventions you must follow.

**Your primary objective is to continue the work of improving and maintaining this repository of Scratchpad Frameworks.**

---

## 1. Current Repository Structure

The repository has been reorganized into a logical, professional structure. **Do not add files to the root directory.** All new files must be placed in the appropriate directory below:

-   `frameworks/`
    -   This is the heart of the repository. It contains all the Scratchpad framework templates.
    -   **`core/`**: For general-purpose, foundational frameworks.
    -   **`purpose-built/`**: For frameworks designed for specific tasks (e.g., research, game design).
    -   **`personas/`**: For frameworks that embody specific personas or philosophical approaches.

-   `docs/`
    -   This directory contains all user-facing documentation.
    -   `GUIDE.md`: The primary "How-To" guide for users, written for a high-school audience.
    -   `white paper.md`: The original academic-style document explaining the framework's philosophy.
    -   `PROJECT_SUMMARY.md`: A detailed log of the work completed during the last major overhaul.

-   `scripts/`
    -   This directory contains all developer and utility scripts.
    -   `run_all_tests.sh`: The master test runner. **You must run this before every submission.**
    -   `test_*.sh`: The individual test suites for different parts of the repository.
    -   `remedial.sh`: A recovery script to help resolve common environment issues.

-   `assets/`
    -   This directory contains all images, GIFs, and other media used in the documentation.

---

## 2. Key Scripts & Their Purpose

-   `scripts/run_all_tests.sh`: Your most important validation tool. It executes all other test suites.
-   `scripts/test_framework_templates.sh`: Validates the structural integrity of all files in the `frameworks/` directory.
-   `scripts/test_markdown_links.sh`: Checks for broken file and directory links in all markdown files.
-   `scripts/test_bug_fixes.sh`: A regression suite to ensure previously fixed bugs remain fixed.
-   `scripts/remedial.sh`: A utility script to help with environment setup.

---

## 3. Quality Standards & Conventions (CRITICAL)

Adherence to these standards is mandatory. The test suite will fail if they are not met.

1.  **Framework Structure (.md files):** All `.md` files in the `frameworks/` directory **must** have at least **three** level-two headers (i.e., lines starting with `## `).

2.  **Framework Structure (.txt files):** All `.txt` files in the `frameworks/` directory **must** have at least **three** four-dash separators (i.e., lines containing exactly `----`).

3.  **Line Endings:** All text files must use Unix-style line endings (LF, `\n`). Windows-style line endings (CRLF, `\r\n`) will cause the tests to fail.

---

## 4. Known Pitfalls & Debugging (Agent Log)

The previous agent encountered several critical issues that caused significant delays. Review these carefully to avoid repeating the same mistakes.

-   **The `grep` and Line Ending Paradox:**
    -   **Problem:** The test suite was failing because `grep` could not find headers or separators that were clearly visible when the files were read with the `read_file` tool.
    -   **Root Cause:** The files had Windows-style line endings (CRLF). The `read_file` tool normalized these, but the `grep` command in the shell did not. The `^` anchor in the `grep` pattern was failing because the line actually started with a carriage return (`\r`).
    -   **Solution:** Use the `dos2unix` command to convert all text files to Unix-style line endings. **If you encounter a similar issue, check the line endings first.**

-   **The `grep` Separator Length Issue:**
    -   **Problem:** The tests for `.txt` files continued to fail even after the line endings were fixed.
    -   **Root Cause:** The test script specifically checks for separators of four or more dashes (`----`). The previous agent was adding only three (`---`), which did not match the test's pattern.
    -   **Solution:** Pay close attention to the exact patterns used in the test scripts. The tests are the source of truth for the repository's quality standards.

-   **The `for` loop and Filenames with Spaces:**
    -   **Problem:** A `for` loop iterating over filenames was failing on files with spaces.
    -   **Root Cause:** A simple `for file in $(find .)` loop will split filenames at spaces.
    -   **Solution:** Use a more robust `find ... -print0 | while read -r -d ''` loop or process substitution (`while read ... < <(find ...)`). The test scripts have been updated with these more robust patterns.

---

## 5. Recommended Workflow

1.  **Analyze:** Before making any changes, use the `ls -R` and `read_file` tools to fully understand the current state of the repository.
2.  **Plan:** Create a clear, step-by-step plan using `set_plan`.
3.  **Execute:** Make your changes, one step at a time.
4.  **Verify:** After each significant change, use the test scripts in the `scripts/` directory to validate your work. Run `scripts/run_all_tests.sh` before you consider your work complete.
5.  **Submit:** Once all tests pass, request a code review and then submit your work.

Good luck, agent. Maintain the quality standards and leave the repository better than you found it.