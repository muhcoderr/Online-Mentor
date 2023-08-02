from flask import Flask , render_template
import json
  
# Open Config.json file with read mode
with open('templates\config.json','r') as c:
    params = json.load(c)["params"]
local_server = True

app = Flask(__name__) #creating the Flask class object   

# DB Connection

if(local_server):
    # configure the SQL database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']

else:
    # configure the SQL database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']

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

@app.route('/trainers') #decorator drfines the   
def trainers():  

    return render_template('trainers.html', params=params)

@app.route('/events') #decorator drfines the   
def events():  

    return render_template('events.html', params=params)

@app.route('/pricing') #decorator drfines the   
def pricing():  

    return render_template('pricing.html', params=params)

@app.route('/contact') #decorator drfines the   
def contact():  

    return render_template('contact.html', params=params)

if __name__ =='__main__':  
    app.run(debug = True)  