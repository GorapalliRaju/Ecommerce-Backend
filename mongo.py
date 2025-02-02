from flask_pymongo import PyMongo
from flask import current_app

def init_db(app):
    app.config["MONGO_URI"] = "mongodb+srv://gorapalliraju2004:Raju2004@cluster0.vfs2b.mongodb.net/Ecommerce?retryWrites=true&w=majority&appName=Cluster0"
    mongo = PyMongo(app)
    return mongo