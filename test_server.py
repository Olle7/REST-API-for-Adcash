import unittest,requests
class Test_server(unittest.TestCase):
    def test_01testpage(self):
        url = "http://127.0.0.1:5000/"
        response_decoded_json = requests.get(url, data={"name": "unittest_product"}, headers={"Content-type": "application/x-www-form-urlencoded"})
        assert(response_decoded_json.status_code==200)
        assert(response_decoded_json.text==open("templates/gui.html").read())
    def test_02invalid_request_to_all_categories_page(self):
        url = "http://127.0.0.1:5000/json"
        response_decoded_json = requests.get(url, data={"name": "unittest_invalid_request"}, headers={"Content-type": "application/x-www-form-urlencoded"})
        assert(response_decoded_json.status_code==400)
    def test_03add_new_category(self):#adds new category, which name is "C1"
        url = "http://127.0.0.1:5000/json/new"
        response_decoded_json = requests.get(url, data={"name":"C1"}, headers={"Content-type": "application/x-www-form-urlencoded"})
        assert(response_decoded_json.status_code==201)
        assert("id" in response_decoded_json.json())#must return id of newly added category in json format.
    def test_04all_categories_page(self):#checks whether category with name "C1" is in database.
        url = "http://127.0.0.1:5000/json"
        response_decoded_json = requests.get(url, data={}, headers={"Content-type": "application/x-www-form-urlencoded"})
        assert(response_decoded_json.status_code==200)
        for catergory in response_decoded_json.json():
            if catergory["name"]=="C1":
                return
        raise Exception
    def test_05get_products_in_category(self):#checks that there are no products in category "C1"
        url = "http://127.0.0.1:5000/json"
        response_decoded_json = requests.get(url, data={},headers={"Content-type": "application/x-www-form-urlencoded"})
        assert (response_decoded_json.status_code == 200)
        kategooriad = response_decoded_json.json()
        for i in range(len(kategooriad)):
            if kategooriad[i]["name"]=="C1":
                products_in_category=requests.get("http://127.0.0.1:5000/json/"+str(i), data={},headers={"Content-type": "application/x-www-form-urlencoded"})
        assert (products_in_category.json()==[])

    def test_06delete_category(self):#deletes category "C1"
        url = "http://127.0.0.1:5000/json"
        response_decoded_json = requests.get(url, data={},headers={"Content-type": "application/x-www-form-urlencoded"})
        assert (response_decoded_json.status_code == 200)
        element_C1_olemas=False
        kategooriad=response_decoded_json.json()
        for i in range(len(kategooriad)):
            if kategooriad[i]["name"] == "C1":
                element_C1_olemas=True
                delete_message=requests.get("http://127.0.0.1:5000/json/"+str(i), data={"name":""},headers={"Content-type": "application/x-www-form-urlencoded"})#deletes category "C1"
        assert(delete_message.text=="category deleted")
        assert(element_C1_olemas)
        kategooriad =requests.get(url, data={},headers={"Content-type": "application/x-www-form-urlencoded"}).json()
        for i in range(len(kategooriad)):
            if kategooriad[i]["name"] == "C1":
                raise Exception

if __name__ == "__main__":
    unittest.main()