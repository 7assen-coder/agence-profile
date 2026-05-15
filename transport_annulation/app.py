from flask import Flask, render_template
from routes.annulation import annulation_bp

app = Flask(__name__)
app.register_blueprint(annulation_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)