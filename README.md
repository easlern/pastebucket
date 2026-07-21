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

## Tech Stack

- **Backend**: FastAPI (Python)
- **Real-time**: WebSockets
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
