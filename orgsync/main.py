"""`main` is the top level module for your Flask application."""
# Import the Flask Framework
from flask import Flask, flash, redirect, url_for, get_flashed_messages
app = Flask(__name__)
from flask import Blueprint, request, render_template
from google.appengine.api import urlfetch
import urllib2
from instagram.client import InstagramAPI
from instagram import client
import json
import requests
urlfetch.set_default_fetch_deadline(99999999999)

import re
from google.appengine.ext import db
from oauth2client.client import SignedJwtAssertionCredentials
import gspread
from apiclient.discovery import build
import flask
from apiclient.discovery import build
from oauth2client import file, client, tools
import httplib2
from apiclient import discovery
httplib2.Http(timeout=45) 
CLUBS_INFO_KEY = '1OZkgZ81cfNGKh-YqizzlZsGNgSdySsZzqRWx7zbEuf4'
CLUBS_GRANT_KEY = '1BCFVDoDiBetMqTqgdsXms7XA6DqTIIelLa1jvd4xx04'
CREDENTIALS_SOURCE = 'static/json/4.json'
SCOPE = 'https://spreadsheets.google.com/feeds'
KEY = 'koQxAU7LX2S23GDvEP_c4WAlsCi_z_UgIXU-iRSCAMk'

def get_clubs_info(): 
    json_key = json.load(open(CREDENTIALS_SOURCE))
    scope = [SCOPE]
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(CLUBS_INFO_KEY).sheet1

def get_club_information(club_name): 
    json_key = json.load(open(CREDENTIALS_SOURCE))
    scope = [SCOPE]
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open_by_key(CLUBS_GRANT_KEY).get_worksheet(2)



def get_grant_information(grant_data, clubs_info): 
    populate = {}
    for data in grant_data['responses']: 
        current_id = int(data['element']['id'])
        populate[data['element']['id']] = data['data']

    profile = []
        
    club = grant_data['on_behalf_of']['name']

    clubs = get_clubs_info()
    for i in range (2, 250): 
        if clubs.cell(i, 1).value == club: 
            profile = clubs.row_values(i)
            break

    return populate, profile

@app.route('/form_submission', methods=["POST"]) 
def api(): 
    populate = {}
    profile = {}
    pro = []
    clubs_info = get_clubs_info()
    submission_url = request.form["Clubs Grant URL"]
    submission_id = re.search("submissions/(\d+)", submission_url).groups()[0]
    params = {"key" : KEY}
    endpoint = 'https://sandbox.orgsync.com/api/v2/form_submissions/' + submission_id
    data = json.loads(requests.get(endpoint, params=params).content)
    populate, pro = get_grant_information(data, clubs_info)
    profile['name'] = pro[0] 
    profile['short_name'] = pro[1]
    profile['club_type'] = pro[2]
    profile['club_level'] = pro[4]
    profile['club_exec'] = pro[9]
    profile['club_members'] = pro[10]
    return render_template("grantsinfo.html", response=generate_response(data), populate=populate, profile=profile)


def generate_unused_responses(data): 
	data = {"Publication Design" : ""}
	return data

def generate_response(data): 
	response = {}
	for responses in data["responses"]:
		if not responses["data"] == "": 
			question_name = responses["element"]["name"]
			response[question_name] = responses["data"]
	return response

@app.route('/find_orgsync_account', methods=["POST"]) 
def udpate_membership(): 
	response = {} 
	data = {"account_found":"false"}
	params = {"key" : KEY}
	endpoint = ""
	if "student_number" or "email" or "name" in request.form: 
		if "name" in request.form: 
			name = request.form["name"] 
			endpoint = 'https://sandbox.orgsync.com/api/v2/accounts'
		if "student_number" in request.form: 
			print "hey"
			student_number = request.form["student_number"] 
			endpoint = 'https://sandbox.orgsync.com/api/v2/accounts/custom_profile/' + student_number + '/'
		elif "email" in request.form: 
			email = request.form["email"] 
			endpoint = 'https://sandbox.orgsync.com/api/v2/accounts/email/' + email + '/'
        if requests.get(endpoint, params=params): 
			data = json.loads(requests.get(endpoint, params=params).content)
			print data['username']
			response['membership'] = []
			account_id = data['id']
			data['account_found'] = "true"
	return render_template("accounts.html", response=data)
	
@app.route('/update', methods=["POST"]) 
def update(): 
	account_id = request.form['account_id'] 
	endpoint = "https://sandbox.orgsync.com/api/v2/groups/402309/accounts/add/"
	params = {"key" : KEY, "ids" : account_id}
	r = requests.post(endpoint, params=params)
	return render_template("submission.html") 

@app.route('/') 
def index(): 
	#endpoint = "https://sandbox.orgsync.com/api/v2/accounts"
	#params = {"key" : KEY}
	#data = json.loads(requests.get(endpoint, params=params).content)
	return render_template("submission.html")

@app.route('/home') 
def home(): 
    return render_template("home.html")

@app.route('/president') 
def hoe(): 
    return render_template("president.html")



