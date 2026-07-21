#!/bin/bash
# Webhook listener for auto-deployments
# This is a minimalist replacement for GitHub Actions push-based deployment.

# 1. Configuration
PROJECT_DIR="/home/youruser/pastebucket"
SECRET="your_webhook_secret" # Optional: add a secret check if you want
PORT=3000

# 2. Update code
cd $PROJECT_DIR
git pull origin main

# 3. Update environment
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt

# 4. Restart service
sudo systemctl restart pastebucket
