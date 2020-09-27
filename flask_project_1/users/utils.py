import secrets 
import os     
from PIL import Image
from flask import current_app
from flask import url_for
from flask_mail import Message
from flask_project_1 import mail
import boto3



def save_picture(form_picture):
    AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME=os.environ.get('AWS_STORAGE_BUCKET_NAME')
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(current_app.root_path,'static/Anon',picture_fn)
    output_size=(125,125)
    i=Image.open(form_picture)
    
    i.thumbnail(output_size)
    i.save(picture_path)
    
    
    return picture_fn
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, click the below link:
{url_for('users.reset_token', token=token, _external=True)}
If you donot want to change or didnt make this request,kindly ignore the mail.
'''
    mail.send(msg)