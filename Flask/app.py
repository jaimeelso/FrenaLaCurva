from flask import Flask,render_template

from flask_bootstrap import Bootstrap
app = Flask(__name__)

Bootstrap(app)

@app.route('/',methods=['GET', 'POST'])
def index():    
    return render_template("index.html")




if __name__ == '__main__':    

    app.run(host="10.10.200.1", port=5000,debug=True)
    
