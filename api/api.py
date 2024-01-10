from flask import Flask
from flask_cors import CORS
import sim
import pickle

file = open("../model/model.pkl", "rb")
MODEL = pickle.load(file)

app = Flask(__name__)
CORS(app)

@app.get("/sim")
def index():
    match = sim.Match(MODEL)
    match.sim()

    return match.json()



if __name__ == "__main__":
    app.run(debug=True)