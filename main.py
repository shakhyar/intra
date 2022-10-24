import os
from datetime import timedelta
import secrets


import pandas as pd
from flask import Flask, render_template, request, url_for, redirect, session, send_file

from users import User
from config import *


app = Flask(__name__)
app.secret_key = "........"
app.permanent_session_lifetime = timedelta(minutes=10)

users = User()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if 'user' in session:
		return redirect(url_for('dashboard'))

	else:
		if request.method == 'POST':
			session.permanent = True
			name = request.form['name']
			std = request.form['std']
			school = request.form['school']
			email = request.form['email']
			password = request.form['password']
			ph1 = request.form['ph1']
			ph2 = request.form['ph2']
			prc = request.form['prc']
			prp = request.form['prp']
			exp = request.form['exp']
			fp = request.form['fp']
			notes = request.form['notes']
			paid=0
			secret = secrets.token_urlsafe(4)

			users.data_entry(name,std,school,email,password,ph1,ph2,prc,prp,exp,fp,notes, paid, secret)

			session['user'] = name

			return redirect(url_for('dashboard'))


		else:
			return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in session:
		return redirect(url_for('dashboard'))

	else:
		if request.method == 'POST':
			ph1 = request.form['ph1']
			password = request.form['password']

			try:
				actual = users.validate(ph1)
				if actual[1]==password:
					session.permanent = True
					session["user"] = actual[0]
					return redirect(url_for('dashboard'))
				else:
					return render_template('login.html', msg="Wrong Credentials")

			except TypeError:
				return f"incorrect username"				

		else:
			return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if 'user' in session:
		session.pop('user')
		return redirect(url_for('login'))

	else:
		return redirect(url_for('login'))


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
	if 'admin' in session:
		return redirect(url_for('admin'))

	else:
		if request.method=='POST':
			usr = request.form['username']
			passw = request.form['password']

			if passw==pw_admin and usr=='shakhyar' or usr=='parikhit' or usr=='murtaza' or usr=='iku':
				session['admin'] = 'usr'
				return redirect(url_for('admin'))

			else:
				return render_template('admin_login.html', msg='Wrong password')

		else:
			return render_template('admin_login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if 'admin' in session:
		if request.method == "POST":
			action = request.form['btn']
			flag = action[:action.index(':')]

			if flag == "reject":
				secret = action[action.index(':')+1:]
				print(secret)
				users.delete_entry(secret)
				return redirect(url_for('admin'))
			
			elif flag == "paid":
				# extracts the information of the given pid, redirects to profit page, and returns to dashboard
				secret = action[action.index(':')+1:]
				users.update_entry(secret)
				print(secret)
				return redirect(url_for('admin'))
			

		else:
			all_list = users.read_all()
			return render_template('admin.html', l=all_list)
	else:
		return redirect(url_for('admin_login'))


@app.route('/payments', methods=['GET', 'POST'])
def payments():
	if 'admin' in session:
		if request.method == "POST":
			action = request.form['btn']
			flag = action[:action.index(':')]

			if flag == "paid":
				secret = action[action.index(':')+1:]
				print(secret)
				users.update_entry(secret)
				return redirect(url_for('payments'))
			else:
				return redirect(url_for('payments'))
		else:
			all_list = users.read_all()
			return render_template('payments.html', l=all_list)

	else:
		return redirect(url_for('admin_login'))

@app.route('/download')
def download():
	if 'admin' in session:
		try:
			os.remove(csv_path)
		except Exception as e:
			print(e)
		l = users.read_all()
		df = pd.DataFrame((l), columns =['Name','Standard','School','Email','Password','ph1','ph2','prc','prp','exp','fp','notes','paid','secret'])
		df.drop(['password'], axis=1)

		
		df.to_csv(csv_path)


		print(df.head)
		return send_file(csv_path, as_attachment=True)
	else:
		return redirect(url_for('admin_login'))

@app.route('/dashboard')
def dashboard():
	if 'user' in session:
		l = users.read(session['user'])
		return render_template('dashboard.html', name=l[0], token=l[1])
	else:
		return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(debug=True)