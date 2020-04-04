from flask import Flask

from flask_bootstrap import Bootstrap
app = Flask(__name__)

Bootstrap(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'





if __name__ == '__main__':    

    app.run(host="10.10.200.1", port=5000,debug=True)
    
