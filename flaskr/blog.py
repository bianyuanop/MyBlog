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

@bp.route('/create', methods=("GET","POST",))
@login_required
def create():
    return render_template('blog/edit.html') 

@bp.route('/viewBlog/<int:blog_id>', methods=("GET",))
def viewBlog(blog_id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM post WHERE id=?',
        (blog_id,)
    ).fetchone()
    return render_template('blog/view.html', post=post)

