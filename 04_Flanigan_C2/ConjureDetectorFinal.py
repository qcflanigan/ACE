import sklearn, os
import argparse
import binary2strings as b2s
from os import system
from sklearn.feature_extraction import FeatureHasher
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from scipy.sparse import csc_matrix

def parse_args(): # Add either "--train", "--test", or "--path" after "python3 finalMalwareCheck.py" for different functions
    parser = argparse.ArgumentParser(description="Description - Train and test a model for determining if a file is malicious")
    parser.add_argument("--train", 
                        help="train a new model and save weights",
                        action="store_true")
    parser.add_argument("--test",
                        help="load and test model",
                        action="store_true")
    
    parser.add_argument("--path",
                        help="default save/load path for model",
                        type=str,
                        default="model") 
    args = parser.parse_args()
    return args

def get_data(folderToSearch):
	if folderToSearch == "train":
		only_int = True
	else:
		only_int = False
	strings=[] # list of lists of readable strings from the files
	Y = [] # List to label a file either benign or malicious
	malwareFilenames=[]
	benignwareFilenames=[]
	#for every file found in the current directory's train/malware folder
	for filename in os.listdir(os.getcwd() + "/" + folderToSearch + "/malware"):
		malwareFilenames.append(filename)
	#for every file found in the current directory's train/benignware folder
	for filename in os.listdir(os.getcwd() + "/" + folderToSearch + "/benignware"):
		benignwareFilenames.append(filename)
	i = 0
	for filename in malwareFilenames:
		f = open("" + folderToSearch + "/malware/"+filename,"rb") # Read the file in bytes
		data = f.read()
		f.close() # Just good practice
		temp=[]
		for (string,type,span,is_interesting) in b2s.extract_all_strings(data, min_chars=4, only_interesting=only_int):
		    temp.append(string) # Add an interesting string to a list of interesting strings
		# List of lists to distinguish one file's bytes from another's
		strings.append(temp) # Add the interesting-string list to a list of lists
		Y.append(1) # Add 1 to the Y list (used as the result for modeling & predicting malware)

		# This just handles the loading bars
		system('clear')
		numDone = int((i/len(malwareFilenames))*100)
		numLeft = 100-numDone
		print("Fomatting Malware Test Files:\t\t" + str(i+1) + "/" + str(len(malwareFilenames)))
		print("<"+"="*numDone+"-"*numLeft+">")
		i += 1

	# ===Read in the benignware files===

	# This function iterates through all 600 benignware files and reads the bytes
	# from the files. It then uses the binary2strings library to translate 
	# these bytes into strings and select only the interesting ones. 

	# When it has found an interesting string it adds it to a list.
	# Once it has translated the whole file, it adds the string list to another
	# list
	i = 0
	for filename in benignwareFilenames:
		f = open("" + folderToSearch + "/benignware/"+filename,"rb") # Open the file in bytes mode
		data = f.read()
		f.close() # Just good practice
		temp=[]
		for (string,type,span,is_interesting) in b2s.extract_all_strings(data, min_chars=4, only_interesting=only_int):
		    temp.append(string) # Add an interesting string to a list of interesting strings

		# List of lists to distinguish one file's bytes from another's
		strings.append(temp) # Add the interesting string list to a list of lists
		Y.append(0) # Add 0 to the Y list (used as the result for modeling & predicting benignware)

		# This just handles the loading bars
		system('clear')
		numDone = int((i/len(benignwareFilenames))*100)
		numLeft = 100-numDone
		print("Fomatting Malware Test Files:\t\t" + str(len(malwareFilenames)) + "/" + str(len(malwareFilenames)))
		print("<"+"="*100+"-"*0+">")
		print("Fomatting Benignware Test Files:\t" + str(i+1) + "/" + str(len(benignwareFilenames)))
		print("<"+"="*numDone+"-"*numLeft+">")
		i += 1
	return strings, Y

# X - output of the feature hasher
# y - list of the results
def train(model, f2, y, path):
    print("===Training and saving model===")
    batch_size = 64
    epochs = 10

    X_train_temp, X_test_temp, y_train, y_test = train_test_split(f2, y, test_size=0.1)
    
    X_train = X_train_temp.toarray()
    X_test = X_test_temp.toarray()
    y_train = np.asarray(y_train)
    y_test = np.asarray(y_test)

    optimizer = keras.optimizers.Adam(learning_rate=0.001)

    model.compile(
        loss=keras.losses.BinaryCrossentropy(),
        optimizer=optimizer,
        metrics=["accuracy",keras.metrics.Precision(),keras.metrics.Recall()],
    )

    #Batch size describes how many files to go through before changing internal model weights/biases
    #Epoch is how many times the model will go through the data both forward and backwards (backpropogation)
    #Steps per epoch = how many batches to complete an epoch (10 batches per epoch)
    model.fit( #Start training the file then evaluate the final result
        X_train, y_train, validation_data=(X_test, y_test), batch_size=batch_size, epochs=epochs, steps_per_epoch=10
    )

    model.save(path)

def fast_evaluate(path, x_test, y_test): #Test the model and evaluate its performance
    model = tf.keras.models.load_model(path)
    model.evaluate(x_test, y_test)
    

def getPredictions(path, X, Y):
    model = tf.keras.models.load_model(path)
    predictions = model.predict(X)
    i=0
    for pred in predictions:
        roundedPred = round(pred[0])
        print(f"file {i}: true value: ", pred, f'prediction: {roundedPred}', "expected: ", Y[i])
        i+=1

def get_model(inputSize):
    model = keras.Sequential()
    # A 6-layer neural network using relu on every layer but the last 
    model.add(layers.Dense(2048, input_shape=(inputSize,), activation="relu"))
    #Relu used to rate feature as malicious from 0 - infinity
    model.add(layers.Dense(2048, activation="relu"))
    model.add(layers.Dense(1024, activation="relu")) #Start to reduce the number of nodes to 1
    model.add(layers.Dense(512, activation="relu"))
    model.add(layers.Dense(256, activation="relu"))
    
    # Sigmoid to force a 0 (benign) or 1 (malicious) from the model
    model.add(layers.Dense(1, activation="sigmoid"))

    return model

def main():
    args = parse_args()
    #Get the arguments from the command the user types into the terminal (python3 finalMalwareCheck.py <arg>)
    if not args.train and not args.test:
        print("Get --help")
        return # End the program, must put one of the three arguments listed at parse_args() declaration

    inputSize=6400 # Number of unique features to evaluate per file

    model = get_model(inputSize) # Create model and prepare it for training

    if args.train: #If told to train the model
        # The raw data with the labels received from a function
        strings, Y = get_data("train")

        # Create feature hasher that takes strings and finds 6400 unique features to analyze all the files with
        h = FeatureHasher(n_features=inputSize,input_type="string")  
        f2 = sklearn.preprocessing.normalize(h.fit_transform(strings)) # Make & normalise the feature hasher

        # take the model, the processed data, and the labels of the data to train the model
        train(model, f2, Y, args.path) 

    model = get_model(inputSize)

    if args.test: #If told to test the model
        # The raw data with the labels received from a function
        filename = "test1"
        strings, Y = get_data(filename)

        # Create feature hasher that takes strings and finds 6400 unique features to analyze all the files with
        h = FeatureHasher(n_features=inputSize,input_type="string")  
        f2 = sklearn.preprocessing.normalize(h.fit_transform(strings)) # Make & normalise the feature hasher

        X = f2.toarray()
        y = np.asarray(Y)
        print("===Evaluation===")
        fast_evaluate(args.path, X, y)
        getPredictions(args.path, X, y)

if __name__ == '__main__':
    # Clear the terminal for a cleaner output before running the program
    system('clear') 
    main()
