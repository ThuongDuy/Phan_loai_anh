from flask import Flask, render_template, request,jsonify
from flask_restful import Resource, Api
from predict import predict
from flask_cors import CORS
from pathlib import Path
app = Flask(__name__)
CORS(app)
api = Api(app)
@app.get("/")

def index_get():
    return render_template("base.html")

class Classification(Resource):
    def post(self):
        img_path=request.get_json().get("path")
        base_path = Path(__file__).parent
        path = (base_path / "../csdl_dpt/anh_test").resolve()
        print(str(path))
        img_path=str(path)+'\\'+img_path
        print(img_path)
        response=predict(img_path)
        message={"result":response}
        print(message)
        return jsonify(message)

api.add_resource(Classification, '/classification')

if __name__ == '__main__':
     app.run(debug=True)

   
