To run our program, make sure your file structure is:

ConjureDetectorFinal.py
/model
/train
  /malware
  /benignware
/test
  /malware
  /benignware


Where "/" connotes a directory and model is the model folder provided


command to train program: python3 ConjureDetectorFinal.py –train
command to test program: python3 ConjureDetectorFinal.py --test
