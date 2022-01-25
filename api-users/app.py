from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from flask_pymongo import ObjectId


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}, r"/users/*":{"origins":"*"}, r"/user/*":{"origins": "*"}})

def get_db():
    client = MongoClient(host='dbmongo',
                         port=27017, 
                         username='root', 
                         password='pass',
                         authSource="admin")

    db = client["pymongodb"]

    return db

db = get_db()


@app.route("/users", methods=["POST"])
def create_user():
    try:
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]

        if username and email and password:
            hash_pass = generate_password_hash(password)

            _id = db.users.insert_one({
                "username": username,
                "email": email,
                "password": hash_pass
            })
    
            return jsonify({"Message": f"User created with id: {str(_id.inserted_id)}"}), 201
            
        else:
            return jsonify({"Message": "Error create user. Check the data"}), 400

    except:
        return jsonify({"Message": "Error internal server"}), 500
    

@app.route("/users/")
def get_users():
    users = []
    try:
        data_users = db.users.find()

        for data_user in data_users:
            users.append(
                {
                    "id": str(data_user["_id"]),
                    "username": data_user["username"],
                    "email": data_user["email"]
                }
            )
        
        response = jsonify(users)
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response, 200
    
    except:
        response = jsonify({"Message": "Error internal server"})
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response, 500


@app.route("/users/<id>/")
def get_user(id):
    try:
        user = db.users.find_one({"_id": ObjectId(id)})
        
        return jsonify({
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }), 200

    except:
        return jsonify({"Message": "Error internal server"}), 500


@app.route("/user/update/<id>", methods=["POST"])
def update_user(id):
    try:
        username = request.json["username"]
        email = request.json["email"]

        if username and email:

            db.users.update_one(
                {"_id": ObjectId(id)},
                {"$set": {
                    "username": username,
                    "email": email
                }}
            )

            return jsonify({"Message": f"User updated with id: {id}"}), 201

        else:
            return jsonify({"Message": "Error update user. Check the data"}), 400

    except:
        return jsonify({"Message": "Error internal server"}), 500


@app.route("/user/delete/<id>/", methods=["POST"])
def delete_user(id):
    try:
        db.users.delete_one({"_id": ObjectId(id)})
        return jsonify({"Message": f"User with id: {id}. Deleted successfully"})
    
    except:
        return jsonify({"Message": "Error internal server"}), 500



if __name__ == "__main__":
    app.run(debug=True)