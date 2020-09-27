
from flask import render_template,url_for,flash,redirect,request,abort,Blueprint
from flask_project_1 import db,bcrypt
from flask_project_1.users.form import RegistrationForm,LoginForm,UpdateAccountForm,ResetPasswordForm,RequestResetForm
from flask_project_1.models import User,Post
from datetime import datetime
from flask_login import login_user,current_user,logout_user,login_required
from flask_project_1.users.utils import save_picture,send_reset_email


users=Blueprint('users',__name__)
"""AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME=os.environ.get('AWS_STORAGE_BUCKET_NAME')
s3 = boto3.client(
        "s3",
        aws_access_key_id=S3_KEY,
        aws_secret_access_key=S3_SECRET
    )"""

"""def upload_file_to_s3(file, bucket_name, acl="public-read"):

   

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)"""

@users.route('/register',methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.hello'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hash_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully!','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title="Register",form=form)
@users.route('/login',methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.hello'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            
            return redirect(url_for('main.hello'))
        else:
            flash('Login Unsuccessfull.Please check your email and password','danger')


    return render_template('login.html',title="Login",form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.hello'))

@users.route('/account',methods=["GET","POST"])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        #file.filename = secure_filename(file.filename)
        #output        = upload_file_to_s3(form.picture, AWS_STORAGE_BUCKET_NAME)
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("your Account has been updated","success")
        return redirect(url_for('users.account'))

    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename="Anon/"+current_user.image_file)
    return render_template('account.html',title="Account",image_file=image_file,form=form)

@users.route('/user/<string:username>')
def user_posts(username):
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
    .order_by(Post.date_posted.desc())\
    .paginate(page=page,per_page=5)
    return render_template('user_post.html',user=user,posts=posts)



@users.route('/reset_password',methods=["GET","POST"])

def reset_request(): 
    if current_user.is_authenticated:
            return redirect(url_for('main.hello'))  
    form=RequestResetForm() 
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to your given mail id,Please reset your password")
    return render_template('resetrequest.html',title="Reset password",form=form)



@users.route('/reset_password/<token>',methods=["GET","POST"])

def reset_token(token): 
    if current_user.is_authenticated:
            return redirect(url_for('main.hello'))
    user=User.verify_reset_token(token)
    if user is None:
        flash("Token maybe invalid or expired",'warning')
        return redirect(url_for('users.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hash_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user.password=hash_password
        db.session.commit()
        flash('Your password has been updated successfully!','success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title="Reset password",form=form)