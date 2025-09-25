from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import google.generativeai as genai
import json
import asyncio
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Gemini API
genai.configure(api_key="your api key here")
model = genai.GenerativeModel('gemini-2.5-flash')
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Gemini API
GOOGLE_API_KEY = ""
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

def generate_summary(text):
    prompt = f"""
    Please provide a concise and informative summary of the following text. 
    Focus on the main ideas and key points. Keep the summary clear and well-structured.
    
    Text to summarize:
    {text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None

def generate_quiz_content(text):
    prompt = f"""
    Please create 5 engaging quiz questions based on the following text. 
    For each question:
    1. Focus on testing understanding of key concepts
    2. Create fill-in-the-blank style questions
    3. Include the answer and the relevant context
    
    Format the output as a JSON array with 'question', 'answer', and 'context' fields.
    
    Text to analyze:
    {text}
    """
    
    try:
        response = model.generate_content(prompt)
        quiz_data = json.loads(response.text)
        return quiz_data
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        return []

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.title}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    notes = Note.query.order_by(Note.date_created.desc()).all()
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    new_note = Note(title=title, content=content)
    
    try:
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Note added successfully'})
    except:
        return jsonify({'success': False, 'message': 'Error adding note'})

@app.route('/generate_quiz/<int:note_id>')
def generate_quiz(note_id):
    note = Note.query.get_or_404(note_id)
    
    try:
        prompt = f"""
        Create 5 engaging quiz questions based on this text. For each question:
        1. Focus on key concepts and important details
        2. Create fill-in-the-blank style questions that test understanding
        3. Make sure the questions are challenging but clear
        4. Use proper context to help understand the question
        5. Include both the answer and the relevant context
        
        Format each question as a JSON object with:
        - "question": The fill-in-the-blank question
        - "answer": The correct word or phrase
        - "context": The full sentence or passage for context
        
        Return an array of these question objects.
        
        Text to analyze:
        {note.content}
        """
        
        response = model.generate_content(prompt)
        try:
            # Try to parse the response as JSON
            quiz_data = json.loads(response.text)
            return jsonify(quiz_data)
        except json.JSONDecodeError:
            # If JSON parsing fails, extract questions manually
            quiz_questions = []
            text = response.text
            
            # Simple parsing of the response text to extract questions
            lines = text.split('\n')
            current_question = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith('"question":') or line.startswith('question:'):
                    if current_question:
                        quiz_questions.append(current_question)
                        current_question = {}
                    current_question['question'] = line.split(':', 1)[1].strip().strip('"').strip()
                elif line.startswith('"answer":') or line.startswith('answer:'):
                    current_question['answer'] = line.split(':', 1)[1].strip().strip('"').strip()
                elif line.startswith('"context":') or line.startswith('context:'):
                    current_question['context'] = line.split(':', 1)[1].strip().strip('"').strip()
            
            if current_question:
                quiz_questions.append(current_question)
            
            return jsonify(quiz_questions)
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/summarize/<int:note_id>')
def summarize_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    try:
        prompt = f"""
        Provide a concise and informative summary of the following text.
        Focus on the main ideas and key points. Keep the summary clear and well-structured.
        Highlight the most important concepts and their relationships.
        Make sure the summary flows naturally and reads well.
        
        Text to summarize:
        {note.content}
        """
        
        response = model.generate_content(prompt)
        if response and response.text:
            return jsonify({
                'success': True,
                'summary': response.text.strip()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to generate summary'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)