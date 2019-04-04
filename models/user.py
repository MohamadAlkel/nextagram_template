from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
import re

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=True)
    email = pw.CharField(unique=True, null=True)
    password = pw.CharField(unique=False, null=True) 

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        check_email = re.search("^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[A-Za-z]+$", self.email)
        check_password = re.search("(?=.{8,})", self.password)

        # email_v = User.get_or_none( == self.email)
        {duplicate_username and self.errors.append("username is not unique")}
        {duplicate_email and not duplicate_email.id == self.id and self.errors.append("email is not unique")}
        {not check_email and self.errors.append("email is not real")}
        {not check_password and self.errors.append("password should be more than 6 ")}
        
        
        # if duplicate_username :
        #     self.errors.append("username is not unique")
        # elif  not check_email :  
        #     self.errors.append("email is not unique")
