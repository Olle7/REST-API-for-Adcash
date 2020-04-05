from flask import Flask, request, redirect, Response,render_template
app = Flask(__name__)



kategooriad=[["C1",["i1","i2","i3"]],["C2",["i21","i22","i23"]],["C3",["i31","i32","i33"]],["C4",["i41","i42","i43"]]]


@app.route('/', methods=['GET', 'POST'])
def pealeht():
    global kategooriad
    html='<!DOCTYPE html>\n<html>   <head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}</style></head>  \n<body>\n<h2>\nAll products:\n</h2>\n<table style="border: 1px solid black;">'
    html+="<tr><th>category</th> <th>product</th></tr>"
    for kategooria in kategooriad:
        for toode in kategooria[1]:
            html+="<tr>"
            html+="<td>"+toode+"</td>"
            html+="<td>"+kategooria[0]+"</td>"
            html+="</tr>"
    return html+"</table></body>\n</html>"


@app.route('/category', methods=['GET', 'POST'])
def kõik_kategooriad():
    global kategooriad
    html='<!DOCTYPE html>\n<html>   <head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}</style></head>  \n<body>\n<h2>\nCategories:\n</h2>\n<table style="border: 1px solid black;">'
    html+="<tr><th>category</th></tr>"
    for kategooria in kategooriad:
        html+="<tr>"
        html+="<td>"+kategooria[0]+"</td>"
        html+="</tr>"
    return html+"</table></body>\n</html>"

if __name__ == "__main__":
    print("app.run has closed.",app.run(debug=True,port=5000,host='0.0.0.0'))