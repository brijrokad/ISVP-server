import lstm
import time, json

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)


def plot_results_multiple(predicted_data, true_data, prediction_len):
    # fig = plt.figure(facecolor='white')
    # ax = fig.add_subplot(111)
    # ax.plot(true_data, label='True Data')
    # #Pad the list of predictions to shift it in the graph to it's correct start
    dict_ = {}
    for i, data in enumerate(predicted_data):
        padding = [0 for p in range(i * prediction_len)]
        dict_[i] = padding + data
    #     plt.plot(padding + data, label='Prediction')
    #     plt.legend()
    # plt.show()
    return json.dumps(str(dict_), ensure_ascii = False)

#Main Run Thread
def main():
	global_start_time = time.time()
	epochs  = 1
	seq_len = 50

	print('> Loading data... ')

	X_train, y_train, X_test, y_test = lstm.load_data('lux500.csv', seq_len, True)

	print('> Data Loaded. Compiling...')

	model = lstm.build_model([1, 50, 100, 1])

	model.fit(
	    X_train,
	    y_train,
	    batch_size=512,
	    nb_epoch=epochs,
	    validation_split=0.05)

	model_json = model.to_json()
	with open("model.json","w") as json_file:
		json_file.write(model_json)
	model.save_weights("model.h5")
	print('Model saved to disk')

	predictions = lstm.predict_sequences_multiple(model, X_test, seq_len, 50)
	#predicted = lstm.predict_sequence_full(model, X_test, seq_len)
	#predicted = lstm.predict_point_by_point(model, X_test)        
	print('Training duration (s) : ', time.time() - global_start_time)
	data = plot_results_multiple(predictions, y_test, 50)
	#print(data)
	return data
