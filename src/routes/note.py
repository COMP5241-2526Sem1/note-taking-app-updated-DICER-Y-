from flask import Blueprint, jsonify, request
from src.models.note import Note, db
from src.models.llm import translate as llm_translate

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        
        note = Note(title=data['title'], content=data['content'])
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        db.session.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])


@note_bp.route('/translate', methods=['POST'])
def translate_note():
    """Translate a note's title and/or content using the LLM helper.

    Request JSON:
      { "note_id": optional int, "title": str, "content": str, "target_language": str, "save": optional bool }

    Response JSON:
      { "translated_title": str, "translated_content": str, "saved": bool }
    """
    try:
        data = request.json or {}
        target = data.get('target_language')
        if not target:
            return jsonify({'error': 'target_language is required'}), 400

        title = data.get('title', '')
        content = data.get('content', '')
        note_id = data.get('note_id')
        save = bool(data.get('save', False))

        translated_title = llm_translate(title, target) if title else ''
        translated_content = llm_translate(content, target) if content else ''

        if save and note_id:
            note = Note.query.get(note_id)
            if note:
                note.title = translated_title or note.title
                note.content = translated_content or note.content
                db.session.commit()
                return jsonify({'translated_title': note.title, 'translated_content': note.content, 'saved': True})

        return jsonify({'translated_title': translated_title, 'translated_content': translated_content, 'saved': False})
    except Exception as e:
        try:
            db.session.rollback()
        except Exception:
            pass
        return jsonify({'error': str(e)}), 500

