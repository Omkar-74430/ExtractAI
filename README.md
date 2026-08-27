
# ExtractAI – AI Search Engine

An intelligent, site-grounded search engine designed to extract knowledge from open internet data and internal documents. ExtractAI enables intelligent question-answering and knowledge retrieval, helping businesses significantly reduce the manual effort required in data analysis and research.

## 🚀 Key Features

*   **Intelligent Question-Answering:** Uses Agentic AI to process and answer queries based on retrieved data.
*   **Web Grounding & Scraping:** Dynamically fetches and parses relevant information from the web using search APIs and web scrapers.
*   **Knowledge Retrieval:** Ideal for extracting actionable insights from both open internet sources and internal business documents.
*   **Local LLM Integration:** Privacy-focused AI processing utilizing Ollama.

## 🛠️ Tech Stack

*   **Language:** Python
*   **Web Scraping & Search:** BeautifulSoup, DuckDuckGo Search API
*   **AI / LLM:** Agentic AI, Ollama (Local LLM)
*   **Database:** MongoDB
*   **Web Framework:** (via `app.py`, `templates/`, `static/`)

## 📂 Project Structure

```text
ExtractAI/
├── static/css/          # Stylesheets for the web interface
├── templates/           # HTML templates for the frontend
├── .google-cookie       # Search/scraping auth configurations
├── app.py               # Main application entry point (Flask/FastAPI)
├── requirements.txt     # Python dependencies
├── web_scraper.py       # Core scraping and data extraction logic
└── SECURITY.md          # Security policies

```

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.8+
* [MongoDB](https://www.mongodb.com/) installed and running locally or via Atlas.
* [Ollama](https://ollama.ai/) installed and running with your preferred model (e.g., `llama3`).

### 1. Clone the repository

```bash
git clone [https://github.com/Omkar-74430/ExtractAI.git](https://github.com/Omkar-74430/ExtractAI.git)
cd ExtractAI

```

### 2. Set up a virtual environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```

### 3. Install dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Environment Variables

Ensure your MongoDB connection string and any necessary API keys are configured (you can create a `.env` file if integrated into `app.py`).

### 5. Run the application

```bash
python app.py

```

*The application will start, and you can access the web interface via your local host (typically `http://localhost:5000` or `http://127.0.0.1:8000`).*

## 🏢 Industry Use Case

ExtractAI is built to help organizations seamlessly interact with their data. By automating the extraction of insights from complex internal documents and web resources, it cuts down hours of manual research, empowering teams to make faster, data-driven decisions.

## 🔗 Links

* **Project Demo/Post:** [LinkedIn Overview](https://www.linkedin.com/posts/omkar-khurd-98a631166_ai-knowledgeextraction-websearchai-activity-7317620356758786049-6kDI?utm_source=share&utm_medium=member_android&rcm=ACoAACeapzoBhhO6NRkNkiq2KQ2_R6cKjtFA3eI)



```
