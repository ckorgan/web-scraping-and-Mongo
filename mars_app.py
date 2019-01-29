from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from scrape_mars import scrape
from flask_bootstrap import Bootstrap

app= Flask(__name__)
Bootstrap(app)


mongoClient = MongoClient()
db = mongoClient['mars_dict']
mars_dict = {}
mars_dict_id = 0

@app.route('/scrape', methods = ['GET'])
def scrape_mars_data():
    global mars_dict_id
    mars_dict = scrape()

    mars_dict_id = db.posts.insert_one(mars_dict).inserted_id
    return redirect('/')

@app.route('/',methods = ['GET'])
def get_mars_data():
    global mars_dict_id
    mars_dict = db.posts.find_one({"_id": mars_dict_id })

    if not mars_dict:
        mars_dict = scrape()
        mars_dict_id = db.posts.insert_one(mars_dict).inserted_id

    return render_template('index.html',mars_dict=mars_dict)

if __name__ == '__main__':
    app.run(debug=True)
