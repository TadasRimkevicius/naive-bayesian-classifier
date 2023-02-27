Tadas Rimkevicius's Naive Bayesian Classifier, Last Updated 02/24/2023

SUMMARY
	This classifier is a tool used to demonstrate simple bayesian reasoning for use in rudamentary
	machine learning. The program takes in training data, trains itself, then classifies any further
	attributes as accurately as is possible given the Naive Bayes Classifier method of classifying data.

	As a python program, no compilation is needed. Double clicking the program will run it in command prompt.

MENU
	Starting the program, you are presented with a simple command-line interface to interact with the program:
		
		Choose your desired option:
                1. Train
                2. Classify
                3. Test Accuracy
                4. Quit
                Enter your choice:
	
	TRAINING
		Prerequisites: none

		To train the model, two files are needed: a 'meta' file and a 'training' file.
		The meta file must have the following format:

			attribute1:value1,value2,...,valuen
			attribute2:value1.value2,...,valuen
					.
					.
					.
			class:classification1,classification2,...,classification3

		Note: make sure that there is a blank line at the end of each file passed through.
		Also make sure that the last entry is always the classification.
		Other than that, the program is designed to work with as many elements as you wish,
		though keep in mind that each added attribute without sufficient data points
		decreases the overall accuracy of the model.

		The training file will have n number of entries, where each entry follows
		the following format:
			
			attribute1Val,attribute2Val,...,attributenVal,classificationVal
		
		Make sure that the training data has a classification label, as the program depends on it
		for its internal learning algorithm.

		Selecting the Train option in the menu while already having a trained model will retrain it with new data.

		There is no way to train the model from multiple files. All training is done from the single training file.

	CLASSIFYING
		Prerequisites: Must have trained the model beforehand

		After training the model, it is possible to classify a series of test data. The format of
		the pre-classified file follows the same format as the training file in the section before,
		including a predicted classification. The program will ignore this and classify the rest of
		the data set, and output it in the same format as the training/test programs

	TESTING
		Prerequisites: Must have trained the model beforehand

		After training the model, it is also possible to test for the accuracy of the model. The format
		of the test file is the same as the training file format, except the classification label will
		now be compared to the predicted label, and output an accuracy percentage to console.
	
CONTACT
	For any queries, please contact me (Tadas Rimkevicius) at
		trimkev@ilstu.edu or rimkeviciust@gmail.com

NOTICE
	While not under any official copyright, this program and its spaghetti implementation are the
	intellectual works of Tadas Rimkevicius.
