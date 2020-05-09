from math import *

from flask import  (
    Flask,
    render_template,
    request,
    g,
    session,
    redirect,
    url_for
)
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import pymongo 
from pymongo import MongoClient 



### Tạo APP
app = Flask(__name__)
app.secret_key = "nguyenhuurong"

### LIÊN KẾT TỚI DB MONGO
MONGO_URI = 'mongodb://rong:rong123456@ds121222.mlab.com:21222/heroku_x24xm6q2?retryWrites=false'
cluster = MongoClient(MONGO_URI)

db =  cluster.heroku_x24xm6q2  # cluster["heroku_phqfm0rw"]


### CODE Flask - Python Web

@app.route('/')
def  index():
    return render_template("login.html")


@app.route('/home')
def  home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def  login():

    if session.get('logged_in_flag'):
        if session['logged_in_flag']:
            return redirect(url_for('home'))

    query_parameters = request.args
    vusername = query_parameters.get("username")
    vpassword = query_parameters.get("password")

    collection = db.account
    ### ch-eck Account / Tài khoản USER
    results = collection.find({"_id":vusername, "password": vpassword}) 


    if  results.count() == 1:
        session['logged_in_flag'] = True
        return render_template("home.html")
    else:
        session['logged_in_flag'] = False
        return render_template("login.html", mesg = "")

@app.route('/orderInDay', methods=['GET', 'POST'])
def  orderInDay():
    query_parameters = request.args
    vdate = query_parameters.get("date")

    collection = db.orders
    ### ch-eck Account / Tài khoản USER
    results = collection.find({"date":vdate}) 


    if  results.count() !=0:
        return render_template("orders.html", orderList = results)
    else:
        return render_template("orderInDay.html")

@app.route('/logout', methods=['GET', 'POST'])
def  logout():
    session['logged_in_flag'] = False
    return render_template("login.html", mesg = "")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    collectionProfile = db.profile 
    lprofile = collectionProfile.find()
    return render_template("profile.html", profileList = lprofile)

@app.route('/products', methods=['GET', 'POST'])
def products():
    collection = db.products 
    lprofile = collection.find()
    return render_template("products.html", productList = lprofile)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    collection = db.orders 
    lorder = collection.find()
    return render_template("orders.html", orderList = lorder)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if ("username" in request.args and "fullname" in request.args  and "password" in request.args):
        signId = request.args.get("username")
        signFullname = request.args.get("fullname")
        signPassword = request.args.get("password")
        newUser = {"_id" : signId,"FullName" : signFullname, "password" : signPassword}
        collectionU = db.account 
        collectionU.insert_one(newUser)
    return render_template("signUp.html")

@app.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    collection = db.products 
    lpro = collection.find()	
    if ("productId" in request.args and "product" in request.args  and "priceOfeach" in request.args):
        pId = request.args.get("productId")
        pName = request.args.get("product")
        pPrice = request.args.get("priceOfeach")
        newProduct = {"productId" : pId,"product" : pName, "priceOfeach" : pPrice}
        collectionP = db.products 
        collectionP.insert_one(newProduct)
    return render_template("addProduct.html", productList = lpro)

@app.route('/addOrder', methods=['GET', 'POST'])
def addOrder():
    collection = db.orders 
    lorder = collection.find()	
    if ("orderId" in request.args and "product" in request.args  and "quantity" in request.args	
    	and "date" in request.args and "shop" in request.args and "price" in request.args):
        oId = request.args.get("orderId")
        oName = request.args.get("product")
        oQuantity = request.args.get("quantity")
        oDate = request.args.get("date")
        oShop = request.args.get("shop")
        oPrice = request.args.get("price")
        newOrder = {    "orderId": oId , "product": oName, "quantity": oQuantity,
                          "date": oDate, "shop": oShop, "price": oPrice}
        collectionO = db.orders 
        collectionO.insert_one(newOrder)
    return render_template("addOrder.html", orderList = lorder)

@app.route('/addProfile', methods=['GET', 'POST'])
def addProfile():
    collection = db.profile 
    lprofile = collection.find()	
    if ("staffName" in request.args and "shop" in request.args  and "dayWork" in request.args
    	and "time" in request.args):
        staffName = request.args.get("staffName")
        shop = request.args.get("shop")
        dayWork = request.args.get("dayWork")
        time = request.args.get("time")
        newProduct = {"staffName" : staffName,"shop" : shop, "dayWork" : dayWork, "time" : time}
        collectionP = db.profile 
        collectionP.insert_one(newProduct)
    return render_template("addProfile.html", profileList = lprofile)

@app.route('/reportInDay', methods=['GET', 'POST'])
def  reportInDay():
        return render_template("reportInDay.html")
