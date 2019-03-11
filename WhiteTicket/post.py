import re
import urllib
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request
import reverse_geocoder as rg 
from werkzeug import secure_filename
import cv2
import sys
import pytesseract
app = Flask(__name__)

@app.route('/')
def location():
   return render_template('geolocation.html')
   
@app.route('/login',methods=['POST','GET'])
def login():
	lat=request.form['lat']
	lon=request.form['lon']
	coordinates =(lat,lon) 
	result = rg.search(coordinates)
	return render_template('index.html',lat=result)

@app.route('/signup')
def signup():
	return render_template('signup.html')
	
@app.route('/loginp')
def loginp():
	return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)
	  
@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_fil():
   if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
		config = ('-l eng --oem 1 --psm 3')
		im = cv2.imread(f.filename, cv2.IMREAD_COLOR)
		text = pytesseract.image_to_string(im, config=config)
		F = open("testfile.txt","w") 
		F.write(text)
		return 'file uploaded successfully '+f.filename

if __name__ == '__main__':
   app.run(debug = True)