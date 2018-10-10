from flask import Flask, redirect, url_for, request, render_template
import sendgrid
import os
from sendgrid.helpers.mail import *

app = Flask(__name__) 
  
@app.route('/success/<code>') 
def success(code): 
   return 'Mail Sent!: %s' % code
@app.route('/failure/<code>')
def failure(code):
	return 'Problem Sending Mail!: %s' % code

@app.route('/')
def loadForm():
	return render_template('index.html')
  
@app.route('/send',methods = ['POST', 'GET']) 
def sendMail():
	sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
	sender = request.form['sender']
	from_email = Email(sender)

	receipent = request.form['receipent']
	to_email = Email(receipent)
	
	subject = request.form['subject']

	contentToSend = request.form['content']
	content = Content("text/plain", contentToSend)

	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	print(response.status_code)
	print(response.body)
	print(response.headers)

	if response.status_code == 202:
		return redirect(url_for('success', code = str(response.status_code)))
	else:
		return redirect(url_for('failure',code = str(response.status_code)))

       
  
if __name__ == '__main__': 
   app.run(debug = True) 