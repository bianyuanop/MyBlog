import sqlite3
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/', methods=("GET",))
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=("GET",))
@login_required
def create():
    db = get_db()
    readCount = db.execute('SELECT readcount FROM read WHERE userid=?', (g.user['id'],)).fetchone()
    error = None
    if not readCount:
        error = "You have to read up to 5 and you have read 0 article"
    else:
        readCount = readCount['readcount']
        if readCount < 5:
            error = "You have to read up to 5 and now you have read %d" % readCount
    if error:
        flash(error)
        return redirect('/')

    tags = db.execute('SELECT tagname FROM tagList').fetchall()
    tagNames = [tag['tagname'] for tag in tags] 
    return render_template('blog/edit.html', tags=tagNames) 

@bp.route('/viewBlog/<int:blog_id>', methods=("GET",))
def viewBlog(blog_id):
    db = get_db()
    if g.user:
        userid = g.user['id']
        readCount = db.execute('SELECT * FROM read WHERE userid=?', (userid,)).fetchone()
        with open("instance/log.txt", 'w') as f:
            f.write(str(readCount))
        if readCount is None:
            db.execute(
                'INSERT INTO read (userid, readcount) VALUES(?, ?)',
                (userid, 1)
            )
        else:
            readCount = readCount['readcount']
            readCount += 1
            db.execute(
                'UPDATE read SET readcount=? WHERE userid=?',
                (readCount, userid)
            )

    tagNames = []
    tagIds = db.execute(
        'SELECT tagid FROM tags WHERE post_id=?',
        (blog_id,)
    ).fetchall()
    tagIds = [tag['tagid'] for tag in tagIds]
    for tagId in tagIds:
        tagNames.append( db.execute('SELECT tagname FROM tagList WHERE id=?', (tagId,)).fetchone()['tagname'] )


    post = db.execute(
        'SELECT * FROM post WHERE id=?',
        (blog_id,)
    ).fetchone()
    if not post:
        abort(404)
    db.commit()
    return render_template('blog/view.html', post=post, tags=tagNames)

@bp.route('/edit/<int:blog_id>', methods=('GET',))
@login_required
def alter(blog_id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM post WHERE id=?',
        (blog_id,)
    ).fetchone()
    if g.user['id'] != post['author_id']:
        abort(403)
    return render_template('blog/alter.html', post=post)

@bp.route('/delete/<int:blog_id>', methods=('POST',))
@login_required
def delete(blog_id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM post WHERE id=?',
        (blog_id,)
    ).fetchone()
    if not post:
        abort(403)
    db.execute(
        'DELETE FROM post WHERE id=?',
        (blog_id,)
    )
    db.commit()
    return redirect(url_for('blog.index'))
