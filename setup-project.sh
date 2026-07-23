#!/bin/bash

# setup-project.sh <project_name> [subdomain_prefix] [domain] [entry_point]
# Example: ./setup-project.sh pastebucket
# This script automates the deployment of "weirdo projects" on a shared VPS.

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <project_name> [subdomain_prefix] [domain] [entry_point]"
    exit 1
fi

PROJECT_NAME=$1
SUBDOMAIN_PREFIX=${2:-"."}
DOMAIN=${3:-"nicholaseasler.com"}
ENTRY_POINT=${4:-"main.py"}

if [ "$SUBDOMAIN_PREFIX" == "." ]; then
    SUBDOMAIN_PREFIX=$PROJECT_NAME
fi

# Use SUDO_USER if available to get the original user account
USER=${SUDO_USER:-$(whoami)}
HOME_DIR=$(getent passwd "$USER" | cut -d: -f6)
FULL_DOMAIN="${SUBDOMAIN_PREFIX}.${DOMAIN}"

echo "🚀 Setting up project: $PROJECT_NAME for $FULL_DOMAIN"

# 1. Determine Port
SERVICE_FILE="/etc/systemd/system/${PROJECT_NAME}.service"
if [ -f "$SERVICE_FILE" ]; then
    PORT=$(grep "Environment=PORT=" "$SERVICE_FILE" | grep -oP '(?<=PORT=)\d+')
    echo "ℹ️ Project already exists, keeping port: $PORT"
else
    # Find used ports in our services to assign a new one
    USED_PORTS=$(grep -rh "Environment=PORT=" /etc/systemd/system/ | grep -oP '(?<=PORT=)\d+' 2>/dev/null)
    if [ -z "$USED_PORTS" ]; then
        PORT=3000
    else
        MAX_PORT=$(echo "$USED_PORTS" | sort -rn | head -n 1)
        PORT=$((MAX_PORT + 1))
    fi
    echo "✅ Assigned new port: $PORT"
fi

# 2. Setup Virtual Environment
cd "$HOME_DIR/$PROJECT_NAME" || { echo "❌ Directory $HOME_DIR/$PROJECT_NAME not found"; exit 1; }
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

echo "📥 Installing dependencies..."
.venv/bin/pip install -r requirements.txt

# 3. Create/Update Systemd Service
echo "⚙️ Configuring systemd service..."
cat <<EOF | sudo tee $SERVICE_FILE > /dev/null
[Unit]
Description=${PROJECT_NAME} - Shared Host App
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=$HOME_DIR/$PROJECT_NAME
ExecStart=$HOME_DIR/$PROJECT_NAME/.venv/bin/python $ENTRY_POINT
Restart=always
Environment=PORT=$PORT

[Install]
WantedBy=multi-user.target
EOF

# 4. Create/Update Nginx Config
echo "🌐 Configuring Nginx..."
NGINX_CONF="/etc/nginx/sites-available/${PROJECT_NAME}"
cat <<EOF | sudo tee $NGINX_CONF > /dev/null
server {
    listen 80;
    server_name $FULL_DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 5. Enable and Restart
echo "🔄 Reloading and starting services..."
sudo systemctl daemon-reload
sudo systemctl enable --now "$PROJECT_NAME"
sudo systemctl restart "$PROJECT_NAME"

sudo ln -sf "$NGINX_CONF" "/etc/nginx/sites-enabled/"
if sudo nginx -t; then
    sudo systemctl reload nginx
else
    echo "❌ Nginx configuration test failed!"
    exit 1
fi

# 6. SSL with Certbot
echo "🔒 Enabling SSL with Certbot..."
# We use --non-interactive. If this is the first time, you might need to run it manually once to set an email.
sudo certbot --nginx -d "$FULL_DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email

echo "✨ Success! Your project is live at: https://$FULL_DOMAIN"
