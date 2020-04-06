from flask import Flask, request,render_template,abort
import json
app = Flask(__name__)

def smallest_free_id(l):
    """
    :param l: list of dictionaries that have key "id".
    :return:  smallest positive integer that is not value of "id" in any dictionary."""
    new_id = 0
    new_id_free = False
    while not new_id_free:
        new_id_free = True
        for d in l:
            if new_id == d["id"]:
                new_id_free = False
                new_id += 1
                break
    return new_id

@app.route('/')
def test_page():
    """:return: html page with forms to test functionalities of the API."""
    return render_template('gui.html', methods=['GET', 'POST'])

@app.route('/json')
def all_categories():
    """:return: json array of all categories"""
    if len(request.values)==0:
        d = []
        for kategory in json.loads(open("databaas.json").read()):
            d.append({"name": kategory["name"],"id": kategory["id"]})
        return app.response_class(response=json.dumps(d), mimetype='application/json')
    abort(400)

@app.route('/json/<category_id>', methods=['GET', 'POST'])
def categorie(category_id):
    """
    *adds new category to database.
    *edits category.
    *deletes category.
    :param category_id: id of category. if category_id is "new", then new category is added.
    :return:json array all product in category ,id of added category ,message about that removal of category was successful,message about that editing of category was successful,or http status code(404 if there is no categoie with given id and 400 if request is otherwise faulty.).
    """
    if len(request.values)==0:#return all products in category.
        categories = json.load(open('databaas.json','r+'))
        try:
            category_id = int(category_id)
        except ValueError:
            abort(400)#id of category is not integer
        for categorie in categories:
            if categorie["id"]==category_id:
                d=[]
                for product in categorie["products"]:
                    d.append({"name": product["name"],"id":product["id"]})
                return app.response_class(response=json.dumps(d), mimetype='application/json')
        abort(404)#there is no category with given id in database
    elif category_id=="new" and "name" in request.values and len(request.values)==1:#add newcategory
        f = open('databaas.json', 'r+')
        categories = json.load(f)
        f.seek(0)#Resets file position to the beginning.
        new_id=smallest_free_id(categories)
        categories.append({"name":request.values.get("name"),"products":[],"id":new_id})
        json.dump(categories, f, indent=4)
        f.truncate()#remove remaining part
        return app.response_class(response=json.dumps({"id": new_id}), mimetype='application/json',status=201)
    elif "name" in request.values and len(request.values)==1:#edit or delete category
        categories=json.load(open('databaas.json','r+'))
        try:
            category_id = int(category_id)
        except ValueError:
            abort(400)  # id of category is not integer
        f = open('databaas.json', 'r+')
        for i in range(len(categories)):
            if categories[i]["id"] == category_id:
                if request.values.get("name"):#edit category name
                    categories[i]["name"]=request.values.get("name")
                    return_message ="category name has been changed"
                else:#delete category
                    categories.pop(i)
                    return_message="category deleted"
                json.dump(categories, f, indent=4)
                f.truncate()#remove remaining part
                return return_message
    else:
        abort(400)#invalid request

@app.route('/json/<category_id>/<product_id>', methods=['GET', 'POST'])
def hello_world(category_id,product_id):
    """
    *adds new product to database.
    *edits product
    *deletes product
    :param category_id: id of category.
    :param product_id:  id of product. If product_id is "new", then new product is added to database.
    :return:id of added product, json array of all products, message about that editing product was sucessful, message about taht deleting prodct was successful or html status code(404 if there is no categoie with given id and 400 if request is otherwise faulty.)
    """
    f = open('databaas.json', 'r+')
    categories = json.load(f)
    f.seek(0)#resets file position to the beginning.
    if product_id=="new" and "name" in request.values and len(request.values)==1:#adds new product.
        try:
            category_id=int(category_id)
        except ValueError:
            abort(400)#category id is not an integer
        for category_index_in_database in range(len(categories)):
            if categories[category_index_in_database]["id"] == category_id:
                new_id = smallest_free_id(categories[category_index_in_database]["products"])
                categories[category_index_in_database]["products"].append({"name": request.values.get("name"),"id":new_id})
                json.dump(categories, f, indent=4)
                f.truncate()  # remove remaining part
                return app.response_class(response=json.dumps({"id": new_id}),mimetype='application/json',status=201)
        abort(404)
    elif "name" in request.values and len(request.values)==1:#edit or delete product.
        try:
            category_id = int(category_id)
            product_id = int(product_id)
        except ValueError:
            abort(400)# id of category or product is not an integer.
        for category_index_in_database in range(len(categories)):
            if categories[category_index_in_database]["id"] == category_id:
                for product_index_in_database in range(len(categories[category_index_in_database]["products"])):
                    if categories[category_index_in_database]["products"][product_index_in_database]["id"] == product_id:
                        if request.values.get("name"):#edit product name
                            categories[category_index_in_database]["products"][product_index_in_database]["name"]=request.values.get("name")
                            return_message="product edited"
                        else:#delete product.
                            categories[category_index_in_database]["products"].pop(product_index_in_database)
                            return_message="product deleted"
                        json.dump(categories, f, indent=4)
                        f.truncate()  # remove remaining part
                        return return_message
        abort(404)
    else:
        abort(400)

if __name__=='__main__':
    app.run(debug=True)