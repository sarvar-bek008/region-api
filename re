services:
  - type: web
    name: freefire-region
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt && playwright install chromium"
    startCommand: "python app.py"
