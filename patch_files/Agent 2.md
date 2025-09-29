# Agent Instructions

Welcome, agent. This repository contains the Scratchpad Framework, a collection of advanced reasoning templates. Your primary goal is to assist users by performing tasks related to these frameworks, such as bug fixing, documentation, and feature implementation.

This repository has a specific, logical structure. Please adhere to it.

## Repository Structure

-   `frameworks/`: This is the most important directory. It contains all the Scratchpad framework templates, organized into subdirectories:
    -   `core/`: General-purpose, foundational frameworks.
    -   `purpose-built/`: Frameworks designed for specific tasks.
    -   `personas/`: Frameworks that embody specific personas.
-   `docs/`: Contains all user-facing documentation. The primary user guide is `docs/GUIDE.md`.
-   `scripts/`: Contains all developer and utility scripts. The test suite is located here and can be run with `scripts/run_all_tests.sh`.
-   `assets/`: Contains all images, GIFs, and other media.

## Core Directives

1.  **Respect the Structure**: Do not add files to the root directory. Place new frameworks, docs, scripts, or assets in their respective directories.
2.  **Maintain Quality**: All framework files must adhere to the structural standards validated by the test suite. `.md` files require at least three level-two headers (`##`), and `.txt` files require at least three four-dash separators (`----`).
3.  **Test Your Changes**: Before submitting any work, you MUST run the full test suite located at `scripts/run_all_tests.sh` to ensure you have not introduced any regressions.
4.  **Document Your Work**: If you add or significantly modify a script or framework, ensure it is properly documented, either within the file itself or in the `docs/` directory.

Adherence to these guidelines is critical for maintaining the integrity and usability of this repository.