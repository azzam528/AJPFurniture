from flask import Flask, render_template, request, jsonify,redirect
from pymongo import MongoClient

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app = Flask(__name__)


@app.route('/')
def home():
    ulasan = db.reviews.find()
    return render_template('home.html', ulasan=ulasan)

@app.route('/faq')
def faq():
   return render_template('faq.html')

@app.route('/contact')
def contact():
   return render_template('contact.html')

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/belanja/<nama>')
def belanja(nama):
   produk = db.produk.find_one({"nama": nama}, {'_id': False})
   return render_template('belanja.html', nama=nama, kategori=produk['kategori'])
  

@app.route('/produk/<keyword>')
def produk(keyword):
   produkresult = db.produk.find({},{'_id': False})
   produk = []
   for prod in produkresult:
      produk.append({
         "nama":prod['nama'],
         "kategori":prod['kategori'],
      })   
   return render_template('produk.html', keyword=keyword , produk=produk)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    if request.method == 'POST':
        nama_pengirim = request.form.get('nama_pengirim')  
        ulasan = request.form.get('Ulasan')  
        furniture = request.form.get('furniture')  
        db.reviews.insert_one({'nama_pengirim': nama_pengirim, 'ulasan': ulasan, 'furniture': furniture})
        return redirect('/')



if __name__ == '__main__':  
    app.run('0.0.0.0',port=5000,debug=True)