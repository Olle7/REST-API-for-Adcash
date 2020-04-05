from flask import Flask, request, redirect, Response,render_template,jsonify,abort
import json
app=Flask(__name__)




@app.route('/categories', methods=['GET', 'POST'])
def categories():
    print()
    """
    :param id of category.
    :param: name of category.
    :return: if there are no arguments in reauest jsonarray of all categories. If there is category id r name in request arguments, then returns list of all products in this category.
    If there is no category with given name or id, then returned html statuscode is 404. If id is not integer, then returned html statuscode is 400"""
    categories = json.loads(open("databaas.json").read())
    if len(request.args)==1:
        if "id" in request.args:
            try:
                request_category_id = int(request.args["id"])
            except ValueError:
                print("Client request not filled because id is not an integer.")
                abort(400)
            if request_category_id>=len(categories):
                print("Client request not filled because there is no category which id is " + request.args["id"])
                abort(404)
            else:
                return app.response_class(response=json.dumps(categories[request_category_id]["products"]),mimetype='application/json')
        elif "name" in request.args:
            for kategory in categories:
                if str(kategory["name"])==request.args["name"]:
                    return app.response_class(response=json.dumps(kategory["products"]), mimetype='application/json')
            print("Client request not filled because there is no category which name is "+request.args["name"])
            abort(404)
    elif not request.args:
        d=[]
        for kategory in categories:
            d.append({"name":kategory["name"]})
        return app.response_class(response=json.dumps(d),mimetype='application/json')
    else:
        abort(400)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """
creates new gategory, which name is specified in reguest.
    :return: text, about that new category has been added.
    """
    if len(request.args)==1 and "name" in request.args:
        f=open('databaas.json', 'r+')
        categories = json.load(f)
        f.seek(0)#Should reset file position to the beginning.
        categories.append({"name":request.args["name"],"products":[]}) # <--- add `id` value.
        json.dump(categories,f,indent=4)
        f.truncate()     # remove remaining part
        return app.response_class(response=json.dumps({"id":len(categories)-1}),mimetype='application/json')
    else:
        abort(400)

@app.route('/categories/edit', methods=['GET', 'POST'])
def edit_category_name():
    """edits gategory, which name or id is specified in reguest from database.
    :return: text, about that category has been deleted."""
    if len(request.args)==2 and "id" in request.args and "new_name" in request.args:
        try:
            try:
                request_id = int(request.args["id"])
            except ValueError:
                print("Client request not filled because, id in request was not integer.")
                abort(400)
            databaas = open('databaas.json', 'r+')
            categories = json.load(databaas)
            databaas.seek(0)  # Should reset file position to the beginning.
            categories[request_id]["name"]=request.args["new_name"] # remove category, which id is request id
            json.dump(categories, databaas, indent=4)
            databaas.truncate()  # remove remaining part
            return "Sucessfuly edited."
        except Exception:
            print("Client request not filled, because there is no category which id is " + request.args["id"])
            abort(404)

@app.route('/categories/delete', methods=['GET', 'POST'])
def delete_category():
    """deletes gategory, which name or id is specified in reguest from database.
    :return: text, about that category has been deleted."""
    if len(request.args) == 1:
        if "id" in request.args:
            try:
                request_id = int(request.args["id"])
                databaas=open('databaas.json', 'r+')
                categories=json.load(databaas)
                databaas.seek(0)  # Should reset file position to the beginning.
                categories.pop(request_id)#remove category, which id is request id
                json.dump(categories, databaas, indent=4)
                databaas.truncate()  # remove remaining part
                return "Sucessfuly deleted from database."
            except ValueError:
                print("Client request not filled because, id in request was not integer.")
                abort(400)
            except Exception:
                print("Client request not filled because there is no category which id is " + request.args["id"])
                abort(404)
        elif "name" in request.args:
            try:
                databaas=open('databaas.json', 'r+')
                categories=json.load(databaas)
                databaas.seek(0)  # Should reset file position to the beginning.
                for i in range(len(categories)):
                    if categories[i]["name"]==request.args["name"]:
                        categories.pop(i)#remove category, which id is request id
                        break
                json.dump(categories, databaas, indent=4)
                databaas.truncate()  # remove remaining part
                return "Sucessfully deleted from database."
            except ValueError:
                print("Client request not filled because, id in request was not integer.")
                abort(400)
            except Exception:
                print("Client request not filled because there is no category which name is " + request.args["id"])
                abort(404)
        #        if str(kategoorija["name"]) == request.args["name"]:
        #            return "Sucessfuly deleted from database."
        #    print("Client request not filled because there is no category which name is " + request.args["name"])
        #    abort(404)
    else:
        abort(400)

@app.route('/categories/products', methods=['GET', 'POST'])
def get_all_products_in_category():
    """
    :return: json array, that contains all products in given array, or html error code if id was out of range.
    """
    if len(request.args)==1 and "id" in request.args:
        categories=json.load(open('databaas.json', 'r+'))
        try:
            request_id = int(request.args["id"])
            if request_id>=len(categories):
                abort(404)
        except ValueError:
            abort(400)
        products_in_category=categories[request_id]["products"]
        print(products_in_category)
        d = []
        for product in products_in_category:
            d.append({"name": product["name"]})
        return app.response_class(response=json.dumps(d), mimetype='application/json')
    else:
        abort(400)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    """creates new product, which name and category is specified in reguest.
    :return: http status(error) code or id of new element.If there is no categori with given id http statuscode is 404. is request is othewise invalid, then retuned statuscode is 400"""
    if len(request.args)==2 and "name" in request.args and "category_id" in request.args:
        f=open('databaas.json', 'r+')
        categories = json.load(f)
        try:
            request_id = int(request.args["category_id"])
            if request_id>=len(categories):
                abort(404)
        except ValueError:
            abort(400)
        f.seek(0)  # Should reset file position to the beginning.
        categories[request_id]["products"].append({"name":request.args["name"]})
        json.dump(categories, f, indent=4)
        f.truncate()  # remove remaining part
        return app.response_class(response=json.dumps({"id":len(categories[request_id]["products"])-1}), mimetype='application/json')
    else:
        abort(400)

@app.route('/products/edit', methods=['GET', 'POST'])
def edit_product():
    """edits product, which name and category is specified in reguest, name.
    :param category_id id of category to which product, that you want to dit belongs.
    :param product_id id of product you want to edit.
    :param new_name new name of product aka name of product after editing
    :return: http status(error) code or id of new element.If there is no categori with given id http statuscode is 404. is request is othewise invalid, then retuned statuscode is 404"""
    if len(request.args)==3 and "category_id" in request.args and "product_id" in request.args and "new_name" in request.args:
        f=open('databaas.json', 'r+')
        categories=json.load(f)
        try:
            category_id = int(request.args["category_id"])
            product_id = int(request.args["product_id"])
            if category_id>=len(categories) or product_id>=len(categories[category_id]):
                abort(404)
        except ValueError:
            abort(400)
        f.seek(0)  # Should reset file position to the beginning.
        categories[category_id]["products"][product_id]["name"]=request.args["new_name"]
        json.dump(categories, f, indent=4)
        f.truncate()  # remove remaining part
        return "product has been sucessfuly edited."
    else:
        abort(400)

@app.route('/products/delete', methods=['GET', 'POST'])
def delete_product():
    """edits product, which name and category is specified in reguest, name.
    :param category_id id of category to which product, that you want to delete belongs.
    :param product_id id of product you want to delete.
    :return: http status(error) code or id of new element.If there is no categori with given id http statuscode is 404. is request is othewise invalid, then retuned statuscode is 404"""
    if len(request.args)==2 and "category_id" in request.args and "product_id" in request.args:
        f=open('databaas.json', 'r+')
        categories=json.load(f)
        try:
            category_id = int(request.args["category_id"])
            product_id = int(request.args["product_id"])
            if category_id>=len(categories) or product_id>=len(categories[category_id]):
                abort(404)
        except ValueError:
            abort(400)
        f.seek(0)  # Should reset file position to the beginning.
        categories[category_id]["products"].pop(product_id)
        json.dump(categories, f, indent=4)
        f.truncate()  # remove remaining part
        return "product has been sucessfuly deleted."
    else:
        abort(400)

if __name__ == "__main__":
    print("app.run has closed.",app.run(debug=True,port=5000,host='0.0.0.0'))