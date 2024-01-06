import sim
import pickle

file = open("model.pkl", "rb")
model = pickle.load(file)

innings = sim.Innings(model)
innings.sim()