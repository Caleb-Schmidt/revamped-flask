from app import db, login
from flask_login import UserMixin #### THIS IS ONLY FOR THE USER MODEL!!!!
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)
    token = db.Column(db.String, unique=True, index=True)
    token_exp = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)
    # current_user.followed.all() #all the people current user is following
    # current_user.followers.all() # all the people following the current user

    ##################################################
    ############## Methods for Token auth ############
    ##################################################    
    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        # If their is a token and it is valid we willtreturn the token
        if self.token and self.token_exp > current_time+timedelta(seconds=60):
            return self.token
        # There was no token or It was expired, so make a new token
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=60)
    
    @staticmethod
    def check_token(token):
        # u=User.query.filter(User.token == token).first()
        u = User.query.filter_by(token = token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u



    #########################################
    ############# End Methods for tokens ####
    #########################################

    # Should return a unique identifing string
    def __repr__(self):
        return f'<User: {self.email} | {self.id} >'

    # Human Readable repr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'
    
    # salt and hash our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    # save the user to the db
    def save(self):
        db.session.add(self) # add the user to out session
        db.session.commit() # saves the session to the database

    def to_dict(self):
        return {
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'created_on' :self.created_on,
            'icon':self.icon,
            'token':self.token,
            'is_admin':self.is_admin
        }

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']

    def get_icon_url(self):
        return f"https://avatars.dicebear.com/api/adventurer/{self.icon}.svg"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post: {self.id} | {self.body[:15]}>'

    def edit(self, new_body):
        self.body=new_body

    def to_dict(self):
        return{
            'id':self.id,
            'body':self.body,
            'created_on':self.created_on,
            'date_modified':self.date_modified,
            'user_id':self.user_id,
        }

    # save the post to the db
    def save(self):
        db.session.add(self) # add the post to out session
        db.session.commit() # saves the session to the database
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()