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

## Deployment (DIY VPS)

For a minimalist, reliable setup on any Linux VPS (DigitalOcean, Hetzner, etc.):

### 1. Server Setup
1. Clone the repo to your server: `git clone <your-repo-url> ~/pastebucket`
2. Create a virtual environment: `python3 -m venv ~/pastebucket/.venv`
3. Install the systemd service:
   - Edit `pastebucket.service` and replace `youruser` with your actual username.
   - Copy it: `sudo cp pastebucket.service /etc/systemd/system/`
   - Start it: `sudo systemctl enable --now pastebucket`

### 2. GitHub Actions (Auto-Deploy)
Add these **Secrets** to your GitHub repository (`Settings > Secrets and variables > Actions`):
- `SERVER_IP`: Your server's IP address.
- `SERVER_USER`: Your SSH username (e.g., `root` or `ubuntu`).
- `SSH_PRIVATE_KEY`: Your private SSH key (ensure the public key is in `~/.ssh/authorized_keys` on the server).

> **Note**: Your server user needs permission to run `sudo systemctl restart pastebucket` without a password, or you can remove `sudo` if running as root.

Now, every time you `git push`, GitHub will automatically update the code on your server and restart the service.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Real-time**: WebSockets
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
