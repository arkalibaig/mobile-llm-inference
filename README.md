# Pocket Llama 3.2 (1B)

A mobile-responsive web interface that turns your local machine into a private AI cloud. Chat with Meta's Llama 3.2 or any model you like from any device on your local network — no internet required.

## How It Works

1. **Backend:** Ollama runs the Llama 3.2 1B model and exposes it via a local API.
2. **Middleware:** A Streamlit Python app manages chat history and communicates with Ollama.
3. **Frontend:** Any mobile browser connects to the Streamlit server over Wi-Fi.

## Setup Instructions

### 1. Install Dependencies

* **Ollama:** Download from [ollama.com](https://ollama.com)
* **Python 3.9+:** Make sure it's installed and available in your PATH

### 2. Configure & Run Ollama

Set the host environment variable so Ollama accepts connections from other devices on your network:

```bash
export OLLAMA_HOST=0.0.0.0
ollama serve
```

In a second terminal, pull the model:

```bash
ollama pull llama3.2:1b
```

### 3. Set Up the Web UI

```bash
# Clone the repo
git clone https://github.com/arkalibaig/llama3.2-1b-home-server.git
cd llama3.2-1b-home-server

# Install dependencies
pip install -r requirements.txt

# Run the app (broadcast to network)
streamlit run app.py --server.address 0.0.0.0
```

### 4. Access from Your Phone

1. Connect your phone to the same Wi-Fi as your laptop.
2. Find your laptop's local IP — on Linux run `hostname -I`.
3. Open your phone's browser and navigate to `http://YOUR_LOCAL_IP:8501`.
