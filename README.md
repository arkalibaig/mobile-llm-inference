#  Pocket Llama 3.2 (1B)

A mobile-responsive web interface that turns your local machine into a private AI cloud. This app allows you to chat with Meta's Llama 3.2 model from any device on your local network.

##  How it Works
1. **Backend:** Ollama runs the Llama 3.2 1B model and serves it via an API.
2. **Middleware:** A Streamlit Python app handles chat history and communicates with Ollama.
3. **Frontend:** Any mobile browser connects to the Streamlit port (8501) over Wi-Fi.



##  Setup Instructions (For any PC)

### 1. Install the "Heavy Shit"
* **Ollama:** Download from [ollama.com](https://ollama.com).
* **Python:** Ensure Python 3.9+ is installed.

### 2. Configure & Run Ollama
Open your terminal and set the network environment variable so the server accepts outside connections:
```bash
export OLLAMA_HOST=0.0.0.0
ollama serve```

**In a second terminal, pull the model:**
```bash
ollama pull llama3.2:1b
```
### 3. Setup the Web UI
```bash
# Clone the repo
git clone [https://github.com/arkalibaig/llama3.2-1b-home-server.git](https://github.com/arkalibaig/llama3.2-1b-home-server.git)
cd llama3.2-1b-home-server

# Install Python dependencies
pip install -r requirements.txt

#run the app (broadcast to network)
streamlit run app.py --server.address 0.0.0.0
```
### Accessing from your Phone
1. Connect your phone to the same Wi-Fi as your laptop.

2. Find your laptop's local IP (Linux: hostname -I).

3. Open your phone's browser and go to http://YOUR_LOCAL_IP:8501.
