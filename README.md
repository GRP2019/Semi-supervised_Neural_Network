# Semi-supervised_Neural_Network

pytorch version of code for paper: Semi-Supervised Learning with Ladder Networks

forked from https://github.com/jibancanyang/Semi-supervised_Neural_Network

experiments on coil20, hela10 and pollen7

----------------------------------------------------------------------------------------

A semi-supervised neural network which is based on the paper **Semi-Supervised Learning with Ladder Networks** by Pytorch.
The sturctrue of this deep neural network combines supervised learning with unsupervised learning, and it is trained to simultaneously minimize the sum of supervised and unsupervised cost functions by backpropagation.In fact, the unsupervised learing complement supervised learing mission to get a better result.

The structure of this model:

<img src="./utils/pictures/ladder_net.png" width = "650" height = "400" alt="ladder" />

This code uses the MLP network, and CNN or ResNet is also ok theoretically.

### The result in MNIST of just use 100 labelled data and 49900 unlabelled data

Accuracy: 98.75%

The parameter:
```shell
* Batch size: 100
* Learning rate: 0.02
* Aim epochs: 100
* Random seed: 42
* Noise std 0.3
* CUDA: True
* Unsupervised cost lambda: [0.5, 0.5, 0.5, 0.5, 0.5, 50.0, 20000.0]
* Encoder size: [1000, 800, 600, 400, 200, 10]
* encoder_train_bn_scaling: [True, True, True, True, True, True]
```
#### Training
I use segmentation leraing rate, which is divided by 2 at 25%, divided by 10 at 50% and 75%.

### Run and change labelled data
```shell
python3 ladder.py #run
python3 utils/mnist_data.py --num_labelled 100 #change labelled data
```

### About GPU
If your Pytorch can get GPU, this model will firstly use GPU, or use the CPU.
In my machine the GPU(GTX 1080ti) version cost about 121 s/epoch, but the CPU version cost about 200 s/epoch.
```python
torch.cuda.is_available() 
```
# Semi-supervised_Neural_Network
