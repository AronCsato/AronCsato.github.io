from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route('/search/<part_code>')
def search(part_code):
    return "Part code %s" %part_code

@app.route('/index', methods=['POST', 'GET'])
def get_code():
    if request.method == 'POST':
        user = request.form['search2']
        return redirect(url_for('search', part_code=user))
    else:
        user = request.args.get('search2')
        return redirect(url_for('search', part_code=user))
 
if __name__ == '__main__':
    app.run(debug=True)