import os
from sendgrid import SendGridAPIClient
from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from helpers.braintree import *
from braintree import client_token
from models.user import Donation
from flask_login  import current_user


payments_blueprint = Blueprint('payments',
                            __name__,
                            template_folder='templates')



@payments_blueprint.route("/don/<img_id>/<user_id>", methods=["GET"])
def client_token(img_id,user_id):
  client_token =  gateway.client_token.generate()
  return render_template('payments/new.html', client_token=client_token, img_id = img_id , user_id=user_id  )



@payments_blueprint.route("/client_token/<img_id>/<user_id>", methods=["POST"])
def create_purchase(img_id,user_id):
    img = img_id
    user = user_id
   
    nonce_from_the_client = request.form["payment_method_nonce"] 
    amount = request.form['amount']
    amount=amount
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
        "submit_for_settlement": True
        }
    })
    
    send_email(current_user.email, amount )
    d = Donation(amount=amount, user_img = img , user=user )
    d.save()
    return redirect(url_for('payments.client_token', img_id = img_id , user_id=user_id ))  




def send_email(email,value):
    message = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': email
                    }
                ],
                'subject': 'Sending with SendGrid is Fun'
            }
        ],
        'from': {
            'email': "arcmohammadalkl@gmail.com"
        },
        'content': [
            {
                'type': 'text/plain',
                'value': 'and easy to do anywhere, even with Python , Thanks for you help, you pay '+value
            }
        ]
    }
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)    

