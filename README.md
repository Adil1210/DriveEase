# Nano (Backend part)

## Overview

Briefly describe your backend application, its purpose, and any key features.

## Prerequisites

Make sure you have the following installed:

- Python (version x.x.x)
- Any other dependencies...

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/pinkishsabito/nano_back.git
    cd nano_back
    ```
    
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
    
3. Activate the virtual environment:
   * On Windows:
   ```bash
   .\venv\Scripts\activate
   ```
       
   * On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
    
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Configure your application by updating the `config.py` file with the necessary settings.

## Running the Application
```bash
uvicorn main:app --reload
```

Your app will be accessible at `http://localhost:8000`.
