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

## The "Weirdo Project" Shared Host Workflow (One-Command Setup)

This setup allows you to host multiple projects on a single VPS without opening SSH (Port 22) to the world. You manage projects manually via a single script that handles Nginx, Systemd, and SSL.

### 1. One-Time Server Setup
Run these once on your server:
```bash
# Install core dependencies
sudo apt update && sudo apt install nginx python3-venv certbot python3-certbot-nginx ufw -y

# Setup Firewall (Only Web ports need to be open)
sudo ufw allow 'Nginx Full' # Ports 80 & 443
sudo ufw --force enable
```

### 2. Adding a New Project
Follow these steps for every new "weirdo project" (like this one):

1.  **DNS**: Create an **A Record** pointing your subdomain (e.g., `pastebucket.nicholaseasler.com`) to your server's IP address. (Use a **CNAME** only if you are pointing to another domain name).
2.  **Clone**: On your server, clone the repository:
    ```bash
    git clone <your-repo-url> ~/pastebucket
    ```
3.  **Setup**: Run the setup script from the project folder:
    ```bash
    cd ~/pastebucket
    sudo ./setup-project.sh pastebucket .
    ```

    *Note: The script accepts optional arguments for domain and entry point:*
    `sudo ./setup-project.sh <project_name> <subdomain_prefix> [domain] [entry_point]`

### How the script works:
- **Auto-Port**: It automatically finds an available port (starting at 3000) so projects don't clash.
- **Nginx & SSL**: It generates the Nginx config and runs Certbot for HTTPS.
- **Systemd**: It creates a background service so your app stays running.
- **Updates**: To update the project, just `git pull` and run the script again.

> **Tip**: You can copy `setup-project.sh` to your home directory (`~/`) to use it as a master tool for all your one-off projects.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Real-time**: WebSockets
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
