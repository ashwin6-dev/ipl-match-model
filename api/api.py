from flask import Flask
import sim
import pickle

file = open("model.pkl", "rb")
MODEL = pickle.load(file)

app = Flask(__name__)

@app.get("/sim")
def index():
    match = sim.Match(MODEL)
    match.sim()

    return match.json()



if __name__ == "__main__":
    app.run(debug=True)