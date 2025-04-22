# 🤖 AI Chat Bot

**AI Chat Bot** is a full-stack intelligent chatbot powered by **OpenAI GPT**, capable of answering questions based on the content of **web pages** using **RAG (Retrieval-Augmented Generation)**.

Built using:
- 🧠 **Flask (Python)** for backend and AI processing
- 💻 **React.js** for an interactive frontend
- 📚 **LangChain + ChromaDB** for vector search
- 🌐 **Web Page Scraping** for knowledge augmentation

---

## 🌟 Features

- Ask natural language questions
- Paste web page URLs as input
- Uses RAG to generate accurate answers based on the scraped page content
- Interactive, responsive UI built with React
- Handles OpenAI API errors (e.g., quota exceeded, invalid key)
- Secure key storage via `.env`

---

## 🔗 Web Page Support

You can paste a URL of a web page (e.g., blog, documentation, FAQ), and the system will:
1. **Scrape the page content**
2. **Chunk and embed the text**
3. **Store it in a vector database**
4. **Use it as context during chat**

This enables the chatbot to give answers grounded in **real-time online information**.

---

## 🔧 Tech Stack

| Layer     | Tool         |
|-----------|--------------|
| Frontend  | React.js     |
| Backend   | Flask        |
| AI Engine | OpenAI GPT   |
| RAG       | LangChain + ChromaDB |
| Data      | Web page content |

---

## 🚀 Getting Started

### 1. Clone the Project

```bash
git clone https://github.com/yourusername/ai-chat-bot.git
cd ai-chat-bot
```

### 2. Backend (Flask)

```bash
cd backend
python -m venv rag-env
source rag-env/bin/activate  # or rag-env\Scripts\activate (Windows)
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key
```

Run the server:

```bash
python run.py
```

### 3. Frontend (React)

```bash
cd ../frontend
npm install
npm start
```

---

## 📂 Folder Structure

```
ai-chat-bot/
├── backend/
│   ├── app/              # Flask API & RAG logic
│   │   ├── __init__.py
│   │   ├── rag_service.py  # Core RAG logic (web ingestion)
│   │   └── ...
│   └── .env
│
├── frontend/
│   ├── src/              # React components
│   ├── public/
│   └── ...
│
├── README.md
└── .gitignore

```

---

## 🔐 Environment Variables

Backend `.env` file (add to `.gitignore`):

```env
OPENAI_API_KEY=your-secret-key
```

---

## 📘 RAG Flow (Web Pages Only)

1. User pastes a URL
2. Page content is extracted
3. Text is chunked and embedded
4. Chunks are stored in ChromaDB
5. When a question is asked, top relevant chunks are retrieved and passed to GPT

---

## 🛡️ Security & Errors

- API key is stored securely via `.env`
- OpenAI quota errors are caught and logged
- Secrets are ignored via `.gitignore` and GitHub push protection

---

## 📄 License

MIT

---

## 🙋 Questions?

Feel free to open an issue or contact me on [GitHub](https://github.com/gangadhar341/ai-chat-bot/issues).

