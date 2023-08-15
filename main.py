from flask import Flask , render_template, request, session, redirect, send_file  
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from io import BytesIO
from werkzeug.utils import secure_filename


# Open Config.json file with read mode
with open('templates\config.json','r') as c:
    params = json.load(c)["params"]
local_server = True

app = Flask(__name__) #creating the Flask class object   

#Set Secret Key
app.secret_key ='supersecret-key'

# DB Connection

if(local_server):
    # configure the SQL database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']

else:
    # configure the SQL database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']

# create the extension
db = SQLAlchemy()

# initialize the app with the extension
db.init_app(app)


class Trainers(db.Model):
    # id, name, department, introduction, picture, facebook, twitter, linkedin, instagram, date
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    department = db.Column(db.String, nullable=True)
    introduction = db.Column(db.String, nullable=True)
    picture = db.Column(db.LargeBinary, nullable=True)  # Using LargeBinary for BLOB
    facebook = db.Column(db.String, nullable=True)
    twitter = db.Column(db.String, nullable=True)
    linkedin = db.Column(db.String, nullable=True)
    instagram = db.Column(db.String, nullable=True)
    date = db.Column(db.String, nullable=True)

# Image Upload and Fetch

@app.route('/trainer/<int:trainer_id>')
def show_trainer(trainer_id):
    trainer = Trainers.query.get(trainer_id)
    if trainer:
        return render_template('trainer.html', trainer=trainer)
    return "Trainer not found"

@app.route('/image/<int:trainer_id>')
def get_trainer_image(trainer_id):
    trainer = Trainers.query.get(trainer_id)
    if trainer and trainer.picture:
        return send_file(BytesIO(trainer.picture), mimetype='image/jpeg')
    return "Image not found"

# Pages Slug and functions

@app.route('/') #decorator drfines the   
def home():  

    return render_template('index.html', params=params) 

@app.route('/about') #decorator drfines the   
def about():  

    return render_template('about.html', params=params) 

@app.route('/courses') #decorator drfines the   
def courses():  

    return render_template('courses.html', params=params) 

@app.route('/course-details') #decorator drfines the   
def courses_detais():  

    return render_template('course-details.html', params=params)

@app.route('/trainers', methods = ['GET']) #decorator drfines the   
def trainers():  
    try:
        trainer = Trainers.query.all()
        print(trainer)
        return render_template('trainers.html', params=params, trainer=trainer)
    except Exception as e:
        # Print the error for debugging purposes
        print(f"Error fetching resume data: {e}")
        return render_template('trainers.html', params=params, trainer = [])

@app.route('/events') #decorator drfines the   
def events():  

    return render_template('events.html', params=params)

@app.route('/pricing') #decorator drfines the   
def pricing():  

    return render_template('pricing.html', params=params)

@app.route('/contact') #decorator drfines the   
def contact():  

    return render_template('contact.html', params=params)

@app.route('/login') #decorator drfines the   
def login():  

    return render_template('login.html', params=params) 

@app.route('/dashboard', methods=['GET','POST']) #decorator drfines the   
def dashboard():  
    #if user already in session
    if ('email' in session and session['email'] == params['admin_email']):
        trainer = Trainers.query.all()
        return render_template('dashboard.html', params=params, trainer=trainer) 
    
    #if user login and go to admin dashboard
    if request.method=='POST':
        #Redirect to Admin Panel
        useremail = request.form.get('email')
        userpassword = request.form.get('password')
        if(useremail == params['admin_email'] and userpassword == params['admin_pass']):
            #set the session variable
            session['email'] = useremail
            trainer = Trainers.query.all()
            return render_template('dashboard.html', params=params, trainer=trainer) 

    else:
        return render_template('login.html', params=params) 


@app.route('/add',methods=['GET','POST']) #decorator drfines the   
def add_edit(): 
    #if user already in session
    if ('email' in session and session['email'] == params['admin_email']):
        if request.method == 'POST':
                 # id, name, department, introduction, picture, facebook, twitter, linkedin, instagram, date
            name = request.form.get('name')
            department = request.form.get('department')
            introduction = request.form.get('introduce')
            # picture = request.form.get('picture')
            picture = request.files.get('picture')  # Get the uploaded file

            if picture:
                # Securely save the uploaded image
                picture_data = picture.read()

            facebook = request.form.get('facebook')
            twitter = request.form.get('twitter')
            linkedin = request.form.get('linkedin')
            instagram = request.form.get('instagram')
            date = datetime.now()
            data = Trainers(name=name, department=department, introduction=introduction,picture=picture_data, facebook=facebook, twitter=twitter, linkedin=linkedin, instagram=instagram, date=date)
            db.session.add(data)
            db.session.commit()


    return render_template('add-data.html', params=params) 

@app.route('/edit/<string:id>', methods= ['GET','POST']) #decorator drfines the   
def edit(id):  
     #if user already in session
    if ('email' in session and session['email'] == params['admin_email']):
        if request.method == 'POST':
            # id, name, department, introduction, picture, facebook, twitter, linkedin, instagram, date
            name = request.form.get('name')
            department = request.form.get('department')
            introduction = request.form.get('introduce')
            # picture = request.form.get('picture')
            picture = request.files.get('picture')  # Get the uploaded file

            if picture:
                # Securely save the uploaded image
                filename = secure_filename(picture.filename)
                picture_data = picture.read()

            
            facebook = request.form.get('facebook')
            twitter = request.form.get('twitter')
            linkedin = request.form.get('linkedin')
            instagram = request.form.get('instagram')
            date = datetime.now()

            # edit  data
            data = Trainers.query.filter_by(id=id).first()
            data.name = name
            data.department = department
            data.introduction = introduction
            data.picture = picture_data
            data.facebook = facebook
            data.twitter = twitter
            data.linkedin = linkedin
            data.instagram = instagram
            data.date = date
            db.session.commit()

            return redirect('/edit/' +str(id))


    update = Trainers.query.filter_by(id=id).first()
    return render_template('edit.html', params=params, update=update)

@app.route('/delete/<string:id>', methods= ['GET','POST']) #decorator drfines the   
def delete(id):  
     #if user already in session
    if ('email' in session and session['email'] == params['admin_email']):
        data = Trainers.query.filter_by(id=id).first()
        db.session.delete(data)
        db.session.commit()
    return redirect('/dashboard') 


@app.route('/logout') #decorator drfines the   
def logout():  
    session.pop('email')
    return redirect('/') 

if __name__ =='__main__':  
    app.run(debug = True)  