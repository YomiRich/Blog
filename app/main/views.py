from flask import render_template, request, redirect,url_for,abort
from . import main
from ..models import Post,User, Comment
from .forms import PostForm, UpdateProfile, CommentsForm
from flask_login import login_required, current_user
from .. import db,photos
import markdown2
from ..requests import get_quote 
from ..email import mail_message

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = "Blog Post"
    quote = get_quote()
    posts = Post.query.order_by(Post.posted.desc()).all()

    return render_template('index.html',title = title, posts=posts,quote=quote)


@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    new_post = None

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        
        new_post = Post( description = description, title = title, user = current_user)

        new_post.save_post()
        users = User.query.all()
        for user in users:
            mail_message("New post","email/new_post",user.email,user=users)

        return redirect(url_for('.index'))

    return render_template('new_post.html', post_form = form, new_post=new_post)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    posts = Post.query.filter_by(user_id = user.id)

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,posts=posts)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template('posts.html', posts=posts)

@main.route('/post/<int:id>')
def single_post(id):
    posts = Post.query.filter_by(id=id)
    comments = Comment.query.filter_by(post_id=id).all()
    print(posts)
    if posts is None:
        abort(404)
    # format_post = markdown2.markdown(posts.description,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('post.html',posts = posts,comments=comments)

@main.route('/post/<int:id>/delete',methods = ['GET','POST'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(id=id).all()
    if post is None:
        abort(404)
    for comment in comments:
        db.session.delete(comment)
        db.session.commit()
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('.posts',id=post.id))

    return render_template('posts.html',form =form)

@main.route("/post/new/comment/<int:id>",methods=["GET","POST"])
@login_required
def comment(id):
    
    post = Post.query.get(id)
    commentForm = CommentsForm()

    if id is None:
        abort(404)

    if commentForm.validate_on_submit():
        comments = commentForm.comment.data
        new_comment = Comment(comments = comments, post_id = id, user = current_user)

        new_comment.save_comment()
        return redirect(url_for('.comment',id=id))

    all_comments = Comment.query.filter_by(post_id=id).all()

    return render_template("comment.html",post = post, id=id,comment_form = commentForm, all_comments = all_comments)

@main.route('/post/<int:id>/edit',methods = ['GET','POST'])
@login_required
def update_post(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        abort(404)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post',id=post.id))

    return render_template('new_post.html',form =form)