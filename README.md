# Smart Notes by Adithya Srivatsa

A Flask-based web application that leverages Google's Gemini AI to help users create, manage, and learn from their notes. The application automatically generates quizzes and summaries from note content, making it an ideal tool for learning and revision.

## Features

- ✍️ Create and store notes with titles and content
- 🤖 AI-powered quiz generation using Google's Gemini AI
- 📝 Intelligent note summarization
- 🎯 Interactive quiz interface with reveal-able answers
- 💫 Modern, responsive user interface
- 🚀 Real-time AI processing

## Prerequisites

Before you begin, ensure you have:

1. Python 3.10 or higher installed
2. A Google Cloud account with Gemini API access
3. Your Gemini API key

## Setup and Installation

1. Create a Python virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your Gemini API key:
   - Open `app/app.py`
   - Replace the API key with your own:
     ```python
     genai.configure(api_key="your-api-key-here")
     ```
   - Or set it as an environment variable:
     ```bash
     set GEMINI_API_KEY=your-api-key-here  # Windows
     export GEMINI_API_KEY=your-api-key-here  # Unix/MacOS
     ```

5. Run the application:
```bash
python app/app.py
```

6. Open your browser and navigate to `http://127.0.0.1:5000`

## Technologies Used

- Backend:
  - Flask 3.0.0 - Web framework
  - SQLAlchemy 3.1.1 - Database ORM
  - Google Generative AI - Gemini model for AI features
  - NLTK - Natural Language Processing
  
- Frontend:
  - HTML5 and CSS3
  - Bootstrap - Responsive design
  - JavaScript - Interactive features

## Project Structure

```
.
├── app/
│   ├── app.py           # Main application file
│   ├── static/         
│   │   ├── script.js    # Frontend JavaScript
│   │   └── style.css    # Custom styles
│   └── templates/
│       └── index.html   # Main template
├── instance/
│   └── notes.db        # SQLite database
└── requirements.txt     # Python dependencies
```

## Usage Guide

1. **Creating Notes**
   - Click "Add Note" at the top of the page
   - Enter a title and your note content
   - Click "Save Note" to store it

2. **Generating Quizzes**
   - Find your note in the list
   - Click "Generate Quiz"
   - Wait for the AI to create questions
   - Use "Reveal Answer" buttons to check your knowledge
   - The questions are contextual and test understanding

3. **Getting Summaries**
   - Locate the note you want to summarize
   - Click "Summarize"
   - The AI will generate a concise summary
   - Summaries focus on key points and main ideas

## Deployment

### Development Environment
For local development, the built-in Flask server is sufficient:
```bash
python app/app.py
```

### Production Deployment
For production deployment, follow these steps:

1. **Server Setup**
   - Install Gunicorn/uWSGI as WSGI server
   - Set up Nginx as reverse proxy
   - Configure SSL/TLS certificates

2. **Environment Configuration**
   ```bash
   export FLASK_ENV=production
   export GEMINI_API_KEY=your-api-key
   ```

3. **Database Configuration**
   - Consider using PostgreSQL for production
   - Update SQLAlchemy configuration
   - Set up regular backups

4. **Gunicorn Deployment Example**
   ```bash
   gunicorn -w 4 -b 127.0.0.1:8000 app:app
   ```

5. **Nginx Configuration Example**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Security Considerations

1. **API Security**
   - Keep API keys secure
   - Use environment variables
   - Implement rate limiting

2. **Data Protection**
   - Regular database backups
   - Input sanitization
   - XSS protection

3. **User Security**
   - Consider adding authentication
   - Implement CSRF protection
   - Use HTTPS in production