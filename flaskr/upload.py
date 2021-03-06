import os
import json
from datetime import datetime
import sqlite3
from flask import (
    Blueprint, g, redirect, render_template, request, url_for, send_file, jsonify, current_app
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/image/<filename>', methods=("GET",))
def image(filename):
    filepath = os.path.join(current_app.instance_path, 'pic/' + filename)
    return send_file(filepath)

@bp.route('/uploadmarkdown', methods=("POST",))
@login_required
def uploadMarkDown():
    db = get_db()
    data = request.get_data()
    jsonData = json.loads(data)
    
    title = jsonData['title']
    body = jsonData['body']
    
    db.execute(
        'INSERT INTO post (title,author_id, body) VALUES (?,?,?)',
        (title, g.user['id'], body)
    )

    post_id = db.execute('SELECT id FROM post WHERE author_id=? ORDER BY created DESC', (g.user['id'],)).fetchone()['id']
    tags = jsonData['tags']
    tagIds = []
    for tagname in tags:
        tagIds.append( db.execute('SELECT id FROM tagList WHERE tagname=?', (tagname,)).fetchone()['id'] )
    for tagId in tagIds:
        db.execute(
            'INSERT INTO tags (post_id, tagid) VALUES (?, ?)',
            (post_id, tagId)
        ) 

    db.commit()

    return redirect('/')

@bp.route('/', methods=("POST",))
@login_required
def upload():
    file=request.files.get('editormd-image-file')
    if not file:
        res={
            'success':0,
            'message':'上传失败'
        }
    else:
        ex=os.path.splitext(file.filename)[1]
        filename=datetime.now().strftime('%Y%m%d%H%M%S')+ex
        bodypic_path='instance/pic/' + filename
        file.save(bodypic_path)
        res={
            'success':1,
            'message':'上传成功',
            'url':url_for('upload.image', filename=filename)
        }
    return jsonify(res)

@bp.route('/alterMarkdown/<int:blog_id>', methods=('POST',))
@login_required
def alterMarkdown(blog_id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM post WHERE id=?',
        (blog_id,)
    ).fetchone()
    if not post:
        abort(403)
    data = request.get_data()
    jsonData = json.loads(data)

    title = jsonData['title']
    body = jsonData['body']

    db.execute(
        'UPDATE post SET title=?, body=? WHERE id=?',
        (title, body, blog_id)
    )
    db.commit()
