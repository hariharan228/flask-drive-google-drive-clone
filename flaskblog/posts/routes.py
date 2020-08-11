from flaskblog.users.utils import save_file
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm,EditForm,SearchForm
from flask import send_file,request


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.files.data:
            post = Post(author=current_user,files = save_file(form.files.data))
            db.session.add(post)
            db.session.commit()
            flash('Your have uploaded a new file', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(form.files.data)
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your File has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/post/<int:post_id>/download")
@login_required
def download_file(post_id):
    post = Post.query.filter_by(id=post_id).first()
    filename = post.files
    return send_file(filename,as_attachment=True)


    

@posts.route("/edit/<int:post_id>", methods=['GET', 'POST'])
@login_required
def edit(post_id):
    form = EditForm()
    post = Post.query.filter_by(id=post_id).first()
    if form.validate_on_submit():
        post.files = form.name.data
        db.session.commit()
        flash('Your filename has been updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.name.data =  post.files
        
    return render_template('edit.html', title='Edit file name',
                            form=form)

@posts.route("/search",methods=['GET','POST'])
@login_required
def search_post():
    form = SearchForm()
    if form.validate_on_submit():
        filename = form.filename.data
        isFile = Post.query.filter_by(user_id=current_user.id,files=filename).first()
        return render_template('result.html',isFile=isFile)
    return render_template('search_post.html',form=form)
    
    
