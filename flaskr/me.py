import sqlite3
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('me', __name__, url_prefix='/me')

@bp.route('/', methods=("GET",))
@login_required
def index():
    db = get_db()
    posts = db.execute(
        'SELECT * FROM post WHERE author_id=?',
        (g.user['id'],)
    ).fetchall()
    return render_template('me/index.html', posts=posts)





