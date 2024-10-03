from flask import Flask, redirect, url_for, request, render_template
import weebscraping
import os
import sys

if getattr(sys, 'frozen', False):
     app = Flask(__name__,template_folder = os.path.join(sys._MEIPASS,"template"))
else:
     app = Flask(__name__,template_folder= os.path.join(os.getcwd(),"template"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/part_code', methods=['GET'])
def part_code():
    if request.method == 'GET':
        if(request.args.get('search2') == None):
                return render_template('index.html')
        elif(request.args.get('search2') == ''):
            return "<html><body> <h1>Invalid search</h1></body></html>"
        else:
            part_code = request.args.get('search2')
            price, product, address, min_index = weebscraping.main(part_code)
            return render_template('part_code.html',
                                    part_code = part_code, product = product, price = price, address = address, len = len(product), min_index =  min_index)
 
 
# Start with flask web app with debug as
# True only if this is the starting page
if(__name__ == "__main__"):
    app.run(debug=True, port=8076)