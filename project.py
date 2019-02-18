from models import Base, User, Food, Variety, Characteristic
from flask import Flask, jsonify, request, redirect
from flask import url_for, flash, g, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

import json
import random
import string
import bleach

from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

auth = HTTPBasicAuth()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FoodVarieties.db'
db = SQLAlchemy(app)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
# Reusing an OAuth from a previous project for this course!
APPLICATION_NAME = 'Udacity Pale Kale'


@app.route('/clientOAuth')
def loginPage():
    return render_template('clientOAuth.html')


@app.route('/oauth/<provider>', methods=['POST'])
def loginUser(provider):
    # Get the auth code
    auth_code = json.loads(request.get_data())['auth_code']
    print "Acquired auth code %s" % auth_code
    if provider == 'google':
        # Get token from Google
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets('client_secrets.json',
                                                 scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            flow_error = 'Failed to upgrade the authorization code.'
            response = make_response(json.dumps(flow_error), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
               % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'

        # Verify that the access token is used for the intended user.
        gplus_id = credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            text = "Token's user ID doesn't match given user ID."
            response = make_response(json.dumps(text), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Verify that the access token is valid for this app.
        if result['issued_to'] != CLIENT_ID:
            text = "Token's client ID does not match app's."
            response = make_response(json.dumps(text), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        stored_credentials = login_session.get('access_token')
        stored_gplus_id = login_session.get('gplus_id')
        if stored_credentials is not None and gplus_id == stored_gplus_id:
            text = 'Current user is already connected.'
            response = make_response(json.dumps(text), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        print "Step 2 Complete! Access Token : %s " % credentials.access_token

        # Find User or make a new one

        # Get user info
        h = httplib2.Http()
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        login_session['username'] = data['name']
        login_session['email'] = data['email']
        login_session['provider'] = 'google'
        login_session['gplus_id'] = gplus_id
        login_session['access_token'] = access_token

        # see if user exists, if it doesn't make a new one
        user = db.session.query(User).filter_by(email=login_session['email'])
        user = user.first()
        if not user:
            user = User(username=login_session['username'],
                        email=login_session['email'])
            db.session.add(user)
            db.session.commit()

        user_id = user.id
        login_session['user_id'] = user_id

        return "Success"
    else:
        return 'Unrecoginized Provider'


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        text = 'Current user not connected.'
        response = make_response(json.dumps(text), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Revoke access token
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        text = 'Failed to revoke token for given user.'
        response = make_response(json.dumps(text, 400))
        response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showFoods'))
    else:
        flash("You are not logged in")
    return redirect(url_for('showFoods'))


def get_user():
    if 'email' in login_session:
        user = db.session.query(User).filter_by(email=login_session['email'])
        return user.one()
    else:
        return None


@app.context_processor
def inject_foods():
    # Make foods available for html templates
    return dict(foods=db.session.query(Food).all())


@app.context_processor
def inject_user():
    # Make needed user information available for html templates
    if 'email' in login_session:
        this_email = login_session['email']
        current_user = db.session.query(User).filter_by(email=this_email)
        id = current_user.first().id
    else:
        id = None
    return dict(username=login_session.get('username', None),
                current_user_id=id)


@app.route('/')
@app.route('/foods')
def showFoods():
    print(login_session)
    foods = db.session.query(Food).all()
    return render_template('food.html', foods=foods)


@app.route('/foods/JSON')
def showFoodsJSON():
    foods = db.session.query(Food).all()
    return jsonify(Foods=[f.serialize for f in foods])


@app.route('/foods/new', methods=['GET', 'POST'])
def newFood():
    current_user = get_user()
    if current_user is None:
        # Must be logged in to create a food
        return render_template('clientOAuth.html')
    if request.method == 'POST':
        newFood = Food(name=request.form['name'])

        # Only add a food if it is valid
        prospective_url = bleach.clean(request.form['picture'])
        url_resp = Food.verify_valid_pic(prospective_url)

        if url_resp is not None:
            newFood.picture = url_resp
        db.session.add(newFood)
        db.session.commit()
        new_food = newFood.id
        if request.form['redirect_choice'] == 'EditMenu':
            return redirect(url_for('foodVarieties', food_id=food.id))
        elif request.form['redirect_choice'] == 'ReturnDatabase':
            return redirect(url_for('showFoods'))
    else:
        return render_template('newFood.html')


@app.route('/foods/<int:food_id>/edit', methods=['GET', 'POST'])
def editFood(food_id):
    food = db.session.query(Food).filter_by(id=food_id).one()
    current_user = get_user()
    if food.protected:
        # Cannot edit a food that is protected
        return render_template('unauthorizedFood.html', food=food)
    if current_user is None:
        return render_template('clientOAuth.html')
    if request.method == 'POST':
        food.name = request.form['name']

        prospective_url = bleach.clean(request.form['picture'])
        url_resp = Food.verify_valid_pic(prospective_url)
        food.picture = url_resp

        db.session.add(food)
        db.session.commit()
        if request.form['redirect_choice'] == 'Varieties':
            return redirect(url_for('foodVarieties', food_id=food.id))
        elif request.form['redirect_choice'] == 'ReturnDatabase':
            return redirect(url_for('showFoods'))
    else:
        return render_template('editFood.html', food=food)


@app.route('/foods/<int:food_id>/delete', methods=['GET', 'POST'])
def deleteFood(food_id):
    food = db.session.query(Food).filter_by(id=food_id).one()
    current_user = get_user()
    if food.protected:
        # Cannot delete a food that is protected
        return render_template('unauthorizedFood.html', food=food)
    if current_user is None:
        return render_template('clientOAuth.html')
    if request.method == 'POST':
        db.session.delete(food)
        db.session.commit()
        return redirect(url_for('showFoods'))
    else:
        return render_template('deleteFood.html', food=food)


@app.route('/foods/<int:food_id>/')
def foodVarieties(food_id):
    # Get all varieties for this food
    food = db.session.query(Food).filter_by(id=food_id).one()
    varieties = db.session.query(Variety).filter_by(food_id=food.id).all()
    existingChars = db.session.query(Characteristic).all()

    return render_template('varieties.html',
                           food=food,
                           varieties=varieties,
                           chars=existingChars)


# Endpoint for API to look at varieties
@app.route('/foods/<int:food_id>/JSON')
def foodVarietiesJSON(food_id):
    food = db.session.query(Food).filter_by(id=food_id).one()
    varieties = db.session.query(Variety).filter_by(food_id=food.id)

    return jsonify(Varieties=[v.serialize for v in varieties])


@app.route('/foods/<int:food_id>/new', methods=['GET', 'POST'])
def newVariety(food_id):
    current_user = get_user()
    if current_user is None:
        return render_template('clientOAuth.html')
    food = db.session.query(Food).filter_by(id=food_id).one()
    if request.method == 'POST':
        newVar = Variety(name=request.form['name'],
                         description=request.form['description'],
                         user_id=current_user.id,
                         food_id=food_id)

        prospective_url = bleach.clean(request.form['picture'])
        url_resp = Variety.verify_valid_pic(prospective_url)
        if url_resp is not None:
            newVar.picture = url_resp
        all_chars = request.form.getlist('char')
        for c in all_chars:
            char = db.session.query(Characteristic).filter_by(char=c).one()
            newVar.characteristics.append(char)

        db.session.add(newVar)
        db.session.commit()
        flash("New variety created!")
        return redirect(url_for('foodVarieties', food_id=food.id))
    else:
        existingChars = db.session.query(Characteristic).all()
        return render_template('newVariety.html',
                               food=food,
                               chars=existingChars)


@app.route('/foods/<int:food_id>/<int:variety_id>/edit',
           methods=['GET', 'POST'])
def editVariety(food_id, variety_id):
    existingVar = db.session.query(Variety).filter_by(id=variety_id).one()
    food = db.session.query(Food).filter_by(id=food_id).one()
    current_user = get_user()
    if current_user is None or login_session['email'] != current_user.email:
        # Cannot edit another user's varieties
        return render_template('unauthorizedVariety.html',
                               food=food,
                               var=existingVar)

    if request.method == 'POST':
        # Do the edit
        existingVar.name = request.form['name']
        existingVar.description = request.form['description']

        # Only save the provided URL if it actually links to a picture
        prospective_url = bleach.clean(request.form['picture'])
        url_resp = Variety.verify_valid_pic(prospective_url)
        existingVar.picture = url_resp

        existingVar.characteristics = []
        for c in request.form.getlist('char'):
            char = db.session.query(Characteristic).filter_by(char=c).one()
            existingVar.characteristics.append(char)
        db.session.add(existingVar)
        db.session.commit()
        flash("Successfully edited menu item!")
        return redirect(url_for('foodVarieties', food_id=food_id))
    else:
        # Return the form
        existingChars = db.session.query(Characteristic).all()
        return render_template('editVariety.html',
                               food=food,
                               var=existingVar,
                               chars=existingChars)


@app.route('/foods/<int:food_id>/<int:variety_id>/delete',
           methods=['GET', 'POST'])
def deleteVariety(food_id, variety_id):
    # Find the variety we want
    existingVar = db.session.query(Variety).filter_by(id=variety_id).one()
    food = db.session.query(Food).filter_by(id=food_id).one()
    current_user = get_user()
    if current_user is None or login_session['email'] != current_user.email:
        return render_template('unauthorizedVariety.html',
                               food=food,
                               var=existingVar)

    if request.method == 'POST':
        # Delete it!
        db.session.delete(existingVar)
        db.session.commit()
        flash("Successfully deleted variety!")
        return redirect(url_for('foodVarieties', food_id=food_id))
    else:
        # Return the form
        return render_template('deleteVariety.html',
                               food=food,
                               var=existingVar)


if __name__ == '__main__':
    app.debug = True
    app.config['SECRET_KEY'] = ''.join(random.choice(
                                     string.ascii_uppercase + string.digits)
                                     for x in xrange(32))
    app.run(host='0.0.0.0', port=5000)
