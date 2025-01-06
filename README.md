# Automated Grading Tools for Web Development Projects

This repository contains two Python scripts designed to assist Teaching Assistants (TAs) in automating grading tasks for Web Development classes. The tools streamline processes like opening HTML files for manual review and managing Flask-based projects, including dependency installation and virtual environment setup.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
   - [Script 1: TA_Assistant.py](#script-1-ta_assistantpy)
   - [Script 2: TA_Assistant_server.py](#script-2-ta_assistant_serverpy)
5. [Environment Variables](#environment-variables)


---

## Overview

### Script 1: TA_Assistant.py
- Opens all `.html` files in a specified directory using the default web browser.
- Allows manual grading by presenting one file at a time.

### Script 2: TA_Assistant_server.py
- Automates the setup and management of Python projects, focusing on Flask apps.
- Key features:
  - Sets up a virtual environment.
  - Installs dependencies from `requirements.txt`.
  - Runs Flask apps.
  - Provides guidance on unclear README instructions using OpenAI.

---

## Prerequisites

- Python 3.7+
- `pip` (Python package manager)
- A web browser installed (for HTML previews)
- OpenAI API key (for the guidance feature in `TA_Assistant_server.py`)

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/automated-grading-tools.git
   cd automated-grading-tools
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Script 1: TA_Assistant.py

**Description:**
Opens all `.html` files in a directory for manual grading, pausing after each file until the user is ready to proceed.

**Steps:**
1. Run the script:
   ```bash
   python3 TA_Assistant.py
   ```
2. When prompted, enter the directory path containing your `.html` files.
3. The script will open each file in your default web browser.
4. Review the HTML file and press Enter to close it and proceed to the next file.

### Script 2: TA_Assistant_server.py

**Description:**
Handles virtual environment creation, dependency installation, and running Flask apps in a specified project directory. It can also provide additional guidance on README instructions via the OpenAI API.

**Steps:**
1. Ensure you have a `.env` file in the same directory as this script, containing your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```
2. Run the script:
   ```bash
   python3 TA_Assistant_server.py
   ```
3. Follow the interactive prompts:
   - Enter the project directory where the Flask app is located.
4. The script will:
   - Create and activate a virtual environment (if one doesn’t already exist).
   - Install dependencies from `requirements.txt` (if found in the project).
   - Search for a README file (`.txt` or `.md`) and provide guidance using the OpenAI API.
   - Identify and run Flask files in the project directory.
   - Press Enter to stop each Flask app before moving to the next.

---

## Environment Variables

To enable the OpenAI guidance feature, create a `.env` file in the root of this repository with the following content:
