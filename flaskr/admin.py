import sys
import sqlite3
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, abort
)

from flaskr.auth import login_required
from flaskr.db import get_db

from . import db as dbClass

bp = Blueprint('admin', __name__, url_prefix='/admin')

def get_ipaddr():
    if request.access_route:
        return request.access_route[0]
    else:
        return request.remote_addr or '127.0.0.1'

@bp.route('/', methods=('GET','POST'))
def index():
    if request.method == 'POST':
        tagname = request.form['tag']
        try:
            dbClass.addTags(tagname)
            flash('Tag added')
        except:
            flash('Tag already in')
        return redirect(url_for('admin.index'))
    requestIp = get_ipaddr()
    print(requestIp, file=sys.stderr)
    if requestIp != '183.225.23.66':
        abort(403)
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template("admin/charge.html", posts=posts)
