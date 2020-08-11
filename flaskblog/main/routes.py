from flask import render_template, request, Blueprint
from flaskblog.models import Post,User
from flask_login import current_user, login_required
from sqlalchemy import and_

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/main.home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.author==current_user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=9)
    file_ext = "pdf"
    search = "%{}%".format(file_ext)
    pdf_count = Post.query.filter((Post.files.like(search))&(Post.author==current_user)).count()
    file_ext = "txt"
    search = "%{}%".format(file_ext)
    txt_count = Post.query.filter((Post.files.like(search))&(Post.author==current_user)).count()
    last_uploaded =  Post.query.order_by(Post.date_posted.desc()).first()
    return render_template('home.html',title="home", posts=posts,pdf_count=pdf_count,txt_count=txt_count,last_uploaded=last_uploaded)


@main.route("/about")
def about():
    return render_template('about.html', title='About')