This repository contains all the files for our SURA project on formal verfication of neural networks.
We used MNIST dataset of hand-written images for experimenting. 
We used Z3 and gurobi solvers for encoding the neural network and the properties. Through various experiments gurobi performed better than Z3 
solving larger encodings in less time.

##Main project files:
**gurobi_.py** - This file contains the general encoding for a neural network and uses the inbuilt max function in gurobi to encode the RELU constraing.
**robustness.py** - This file contains the modified encoding of the neural network and the encoding for its robustness property. A neural network is said to be robust if on slight perturbation in the input the output remains same. For this we used the condition that if the sum of the absolute difference
between the pixel values of the two input images is less than some given valu delta then the network is said to be robust.
**brightness.py** - This just like robustness is another property which states that slightly increasing the brightness of the image (by increasing all
the pixel values by a fixed small number) the answer remains same.
