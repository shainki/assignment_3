from flask import Flask, Response, request, jsonify, render_template
import json
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask_cors import CORS

app=Flask(__name__)

# Bootstrap(app)
CORS(app)

app.config["MONGO_DBNAME"] = "familytree"
app.config["MONGO_URI"] = "mongodb://localhost:27017/familytree"
mongo = PyMongo(app)

person=mongo.db.person
relation=mongo.db.relation

Details=[]
Detail_relation=[]
#---------------------------------------------Create Person Details------------------------------------#
@app.route("/",methods=["POST"])
def create_person():
    try:
        new_person={"firstname":request.form["firstname"],
                    "lastname":request.form["lastname"],
                    "phone":request.form["phone"],
                    "email":request.form["email"],
                    "address":request.form["address"],
                    "DOB":request.form["DOB"]
                    }

        dataset=person.insert_one(new_person)
        Details.append(dataset)
        return Response(
            response=json.dumps(
                {
                    'message': "Created user successfully",
                    "id": f"{dataset.inserted_id}"
                }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ep:
        return Response(
            response=json.dumps(
                {
                    'message': "Failed !!!!",
                }
            ),
            status=500,
            mimetype="application/json"
        )

#----------------------------------------Create Relations -----------------------------------------#
@app.route("/relation",methods=["POST"])
def create_relation():
    try:
        if person.find_one({"firstname":request.form["firstname"],"lastname":request.form["lastname"]}) \
                and person.find_one({"firstname":request.form["rfname"],"lastname":request.form["rlname"]}):
            print("This is indide if")
            new_relation={"firstname":request.form["firstname"],
                        "lastname":request.form["lastname"],
                        "relation":request.form["relation"],
                        "relation_to_fname":request.form["rfname"],
                        "relation_to_lname":request.form["rlname"],
                        }

            Relationship=relation.insert_one(new_relation)
            Detail_relation.append(Relationship)
            return Response(
                response=json.dumps(
                    {
                        'message': "Created user successfully",
                        "id": f"{Relationship.inserted_id}"
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        else:
            print("This is outside if")

    except Exception as ep:
        print(ep,"This is exception handled")


@app.route("/list",methods=["GET"])
def show_details():
    print(" I AM INSIDE")
    try:
        Data = list(relation.find({"firstname":request.args.get("firstname"),"lastname":request.args.get("lastname")}))
        for user in Data:
            user["_id"] = str(user["_id"])
            return Response(
                response=json.dumps(Data),
                status=200,
                mimetype="application/json",
            )




   # If you want to use it in frontend uncomment it out
        # valid_data = {"response":json.dumps(Data)}
        # return render_template("index.html", valid_data=valid_data)


    except Exception as ep:
        print("This is the exception handled as ",ep)


#---------------------------Person Update and Delete ----------------------------------------------#

@app.route("/person/<id>", methods=["PUT","DELETE"])
def ud_person(id):
    if request.method=="PUT":
        print("Inserted inside")
        person_update = person.update_one(
            {'_id': ObjectId(id)},
            {"$set": {"firstname":request.form["firstname"],
                        "lastname":request.form["lastname"],
                        "phone":request.form["phone"],
                        "email":request.form["email"],
                        "address":request.form["address"]
                      }
             },
        )
        if person_update.modified_count == 1:
            return Response(
                response=json.dumps(
                    {
                        'message': "User Updated !",

                    }
                ),
                status=200,
                mimetype="application/json",
            )
        else:
            return Response(
                response=json.dumps(
                    {
                        'message': "Update failed !",

                    }
                ),
                status=200,
                mimetype="application/json",
            )
    elif request.method=="DELETE":
        person.delete_one({'_id': ObjectId(id)})
        return Response(
            response=json.dumps(
                {
                    'message': "Deleted !",

                }
            ),
            status=200,
            mimetype="application/json",
        )
#--------------------------------------Relation Update and Delete ------------------------------------#

@app.route("/relation/<id>", methods=["PUT","DELETE"])
def ud_relation(id):
    if request.method=="PUT":
        relation_update = relation.update_one(
            {'_id': ObjectId(id)},
            {"$set": {"firstname":request.form["firstname"],
                        "lastname":request.form["lastname"],
                        "relation":request.form["relation"],
                        "relation_to_fname":request.form["rfname"],
                        "relation_to_lname":request.form["rlname"],
                      }
             },
        )
        print("This is the upate staus",relation_update)
        if relation_update.modified_count == 1:
            return Response(
                response=json.dumps(
                    {
                        'message': "User Updated !",

                    }
                ),
                status=200,
                mimetype="application/json",
            )
        else:
            return Response(
                response=json.dumps(
                    {
                        'message': "Update failed !",

                    }
                ),
                status=200,
                mimetype="application/json",
            )
    elif request.method=="DELETE":
        relation.delete_one({'_id': ObjectId(id)})
        return Response(
            response=json.dumps(
                {
                    'message': "Deleted !",

                }
            ),
            status=200,
            mimetype="application/json",
        )


#------------------------------------------------------#--------------------------------------------------#

if __name__=="__main__":
    app.run()




