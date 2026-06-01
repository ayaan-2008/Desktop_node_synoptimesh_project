# SynoptiMesh Desktop Node

An AI-powered desktop automation assistant built with Python.

SynoptiMesh combines desktop control, AI interaction, Gmail automation, OCR, voice output, and application launching into a single command-driven assistant.

## Features

### Desktop Automation

* Open desktop applications
* Launch Chrome, VS Code, Spotify, Discord, Notepad, Paint, Calculator, and more
* Open Windows Settings and File Explorer
* Execute system actions

### AI Assistant

* Powered by Groq API
* Maintains short conversation history
* Uses Llama models for intelligent responses
* Supports desktop-oriented assistance and commands

### Gmail Integration

* Send emails through the Gmail API
* OAuth2 authentication
* Secure token-based access
* Automatic token reuse after first login

### OCR & Computer Vision

* Screenshot analysis
* Optical Character Recognition (OCR)
* OpenCV integration
* Tesseract OCR support

### Voice Features

* Text-to-Speech responses
* Voice feedback through Windows speech engine

### Smart Command Suggestions

* Fuzzy command matching using RapidFuzz
* Typo-tolerant command recognition
* Intelligent command suggestions

---

## Technologies Used

* Python
* Groq API
* OpenCV
* RapidFuzz
* PyAutoGUI
* PyTTSX3
* Tesseract OCR
* Gmail API
* Google OAuth2

---

## Project Structure

```text
desktop-node/
│
├── ai_engine.py          # AI interaction engine
├── desktop_node.py       # Main desktop automation logic
├── email_feature.py      # Gmail integration
├── search_engine.py      # Command matching and suggestions
├── deskmain.py           # Program entry point
│
├── .env                  # Environment variables (not committed)
├── credentials.json      # Google OAuth credentials (not committed)
├── token.json            # Generated Gmail token (not committed)
│
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd desktop-node
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install groq
pip install pyautogui
pip install opencv-python
pip install rapidfuzz
pip install pywin32
pip install pytesseract
pip install pyttsx3
pip install python-dotenv

pip install google-auth
pip install google-auth-oauthlib
pip install google-auth-httplib2
pip install google-api-python-client
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit this file to GitHub.

---

## Gmail Setup

1. Create a project in Google Cloud Console.
2. Enable Gmail API.
3. Create OAuth2 Desktop Application credentials.
4. Download the credentials file.
5. Rename it to:

```text
credentials.json
```

6. Place it in the project folder.

On first use, a browser window will open for Google authentication.

A `token.json` file will be generated automatically and reused for future sessions.

---

## Running the Assistant

```bash
python deskmain.py
```

---

## Example Commands

```text
open chrome
open vscode
open spotify
open notepad

search google
search youtube

take screenshot

ask ai
chat ai

send email
```

---

## Security Notes

Do NOT upload:

```text
.env
credentials.json
token.json
.venv/
__pycache__/
```

These files contain credentials, authentication tokens, or machine-specific data.

---

## Future Goals

* Voice command support
* Mobile node integration
* IoT device control
* Local AI model support
* Multi-device synchronization
* Advanced automation workflows

---

## Author

Abdul Ayaan

Built as part of the SynoptiMesh ecosystem for AI-powered desktop automation.
