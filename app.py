# Run this program to create a simple web application.
# This will only be accessible by devices connected same network as your device.

from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
