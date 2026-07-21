# Pastebucket

Pastebucket is a minimalist, real-time collaborative text editor. It allows users to share and edit text instantly without the need for accounts or logins.

## Features

- **Instant Sessions**: Navigate to the root URL to be redirected to a new, randomly generated session ID (e.g., `shiny-fox-123`).
- **Real-time Collaboration**: Multiple users can edit the same "bucket" simultaneously with changes synchronized instantly via WebSockets.
- **No Authentication**: No login or registration required. Just share the URL to collaborate.
- **Clean UI**: A focused, full-screen interface for distraction-free writing and sharing.

## How it Works

Pastebucket uses **FastAPI** on the backend and **WebSockets** for real-time communication. Text content is stored in-memory, making it extremely fast but temporary (content is cleared if the server restarts).

## Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pastebucket
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the server using `uvicorn` (defaults to port 3000):

```bash
python main.py
```

Alternatively, you can still use `uvicorn` directly:

```bash
uvicorn main:app --port 3000 --reload
```

Once the server is running, open your browser and navigate to:
[http://127.0.0.1:3000](http://127.0.0.1:3000)

## The "Weirdo Project" Shared Host Workflow (Pull-Based)

This setup allows you to host multiple projects on a single VPS without opening SSH (Port 22) to the world. Instead of GitHub "pushing" to your server, your server "pulls" from GitHub using a Webhook or a Cron job.

### 1. One-Time Server Setup
Run these once on your server:
```bash
# Install core dependencies
sudo apt update && sudo apt install nginx python3-venv certbot python3-certbot-nginx ufw -y

# Setup Firewall (Only Web ports need to be open)
sudo ufw allow 'Nginx Full' # Ports 80 & 443
sudo ufw --force enable

# Optional: Close SSH to everyone but you
# sudo ufw allow from YOUR_IP_ADDRESS to any port 22
```

### 2. Adding a New Project

#### A. DNS & Nginx
1.  **DNS**: Create a **CNAME** for your subdomain.
2.  **Nginx**: Use `nginx.conf.template` to create `/etc/nginx/sites-available/pastebucket`.
3.  **SSL**: Run `sudo certbot --nginx -d pastebucket.nicholaseasler.com`.

#### B. Systemd Service
1.  Copy `pastebucket.service` to `/etc/systemd/system/`.
2.  Update paths and set a unique `Environment=PORT=3000`.
3.  Start it: `sudo systemctl enable --now pastebucket`.

#### C. Auto-Deploy (The "Pull" Method)
Instead of GitHub Actions, we use a simple Cron job or a Webhook listener on the server to pull changes.

**Option 1: The Simple Cron (Recommended for "Weirdo Projects")**
Run `crontab -e` and add this line to check for updates every 5 minutes:
```bash
*/5 * * * * cd ~/pastebucket && git pull origin main && sudo systemctl restart pastebucket
```

**Option 2: The Webhook**
If you want instant deploys, you can use a minimalist webhook listener (like `adnanh/webhook`) that triggers the `deploy.sh` script whenever GitHub sends a POST request.

> **Tip**: When starting a new project, just copy this repo, change the service/directory names in the files, and you're live in minutes.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Real-time**: WebSockets
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
