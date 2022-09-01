https://www.kaggle.com/code/lakhindr/small-efficient-neural-network-for-mnist -> "small" and 98%+ accuracy
https://mlfromscratch.com/neural-network-tutorial/#/ -> MNIST NN from scratch using NumPy


Mnist image = (28 x 28) -> 784 px


Implementation in SnarkyJS:
https://makalfo.medium.com/snarkynet-mnist-handwritten-digits-in-a-zkapp-on-mina-protocol-d85f8847aded

784 nodes -> 128 nodes (RelU) -> 10 nodes (Softmax)

~ 2 million arithmetic ops (excluding activation func)?
\* cost of single arithmetic op?
\* cost of activation func?

