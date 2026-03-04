# Optimization for Machine Learning

## Gradient descent
Gradient descent minimizes a differentiable objective by moving parameters in the direction of negative gradient.
In batch gradient descent, each step uses the full training set.
Stochastic gradient descent updates parameters using a single example or mini-batch and often converges faster per wall-clock time.

## Learning rate
The learning rate controls step size.
If it is too large, optimization may diverge or oscillate.
If it is too small, convergence may be very slow.

## Regularization
L2 regularization adds a penalty on large weights and can reduce overfitting.
