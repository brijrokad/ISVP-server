import lstm
import time
import matplotlib.pyplot as plt
import run
from keras.models import model_from_json

	#run.main()
def test():
	X_train, y_train, X_test, y_test = lstm.load_data('lux500.csv', 50,True)

	json_file = open("model.json")
	loaded_model = json_file.read()
	json_file.close()

	model = model_from_json(loaded_model)
	model.load_weights("model.h5")

	pred = lstm.predict_sequences_multiple(model, X_test, 50, 50)
	return run.plot_results_multiple(pred, y_test, 50)