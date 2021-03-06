from __future__ import print_function
import os
import urllib
import random
import numpy as np
import gzip
from collections import defaultdict
import pickle
import argparse
import urllib.request

from scipy import io
import random

def load_data(train_nums=20):
    # 862*32*32, 1*862
    n_class = 10
    all_data = io.loadmat("../data/hela_32_32.mat")
    all_fea  = all_data['fea']
    all_label= all_data['label']
    all_label  = np.transpose(all_label, (1, 0)) # 862*1
    all_fea  = np.expand_dims(all_fea, -1) # 862*32*32*1

    mnist_train_images = []
    mnist_train_labels = []
    mnist_test_images  = []
    mnist_test_labels  = []
    for n in range(1,n_class+1):
        y_ind = np.where(all_label==n)[0]
        random.shuffle(y_ind)
        mnist_train_images.extend(all_fea[y_ind[0:train_nums]])
        mnist_train_labels.extend(all_label[y_ind[0:train_nums]])

        mnist_test_images.extend(all_fea[y_ind[train_nums:]])
        mnist_test_labels.extend(all_label[y_ind[train_nums:]])
    
    mnist_train_images = np.array(mnist_train_images)
    mnist_train_labels = np.reshape(np.array(mnist_train_labels), (-1))
    mnist_test_images  = np.array(mnist_test_images)
    mnist_test_labels  = np.reshape(np.array(mnist_test_labels), (-1))

    print(np.shape(mnist_train_images), np.shape(mnist_train_labels))
    print(np.shape(mnist_test_images), np.shape(mnist_test_labels))
    
    return mnist_train_images, mnist_train_labels-1, mnist_test_images, mnist_test_labels-1

# load_data()

def shuffle_images_labels(images, labels):
    """shuffle the images """
    assert images.shape[0] == labels.shape[0]
    randomize = np.arange(images.shape[0])
    np.random.shuffle(randomize)
    return images[randomize], labels[randomize]


def dump_pickle(filepath, d):
    with open(filepath, "wb") as f:
        pickle.dump(d, f)


def main():
    # command line arguments
    parser = argparse.ArgumentParser(description="Parser for MNIST data generation")
    parser.add_argument("--num_labelled", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    n_labelled = args.num_labelled

    rand_seed = args.seed
    random.seed(rand_seed)
    np.random.seed(rand_seed)

    n_class = 10
    data_dir = "../data/hela-10-data/label"+str(int(n_labelled/n_class))+'_'+str(rand_seed)
    if not os.path.exists(data_dir):
        os.system("mkdir -p %s" %(data_dir) )
    if not os.path.exists(data_dir+'_mat'):
        os.system("mkdir -p %s" %(data_dir+'_mat') )
    

    # load coil20 dataset 
    mnist_train_images, mnist_train_labels, mnist_test_images, mnist_test_labels = load_data()

    train_data_shuffle = [(x, y) for x, y in zip(mnist_train_images, mnist_train_labels)]
    random.shuffle(train_data_shuffle)
    mnist_shuffled_train_images = np.array([x[0] for x in train_data_shuffle])
    mnist_shuffled_train_labels = np.array([x[1] for x in train_data_shuffle])

    train_size = n_class*20
    train_images = mnist_shuffled_train_images[:train_size].copy()
    train_labels = mnist_shuffled_train_labels[:train_size].copy()

    validation_images = mnist_shuffled_train_images[:train_size].copy()
    validation_labels = mnist_shuffled_train_labels[:train_size].copy()

    test_images = mnist_test_images
    test_labels = mnist_test_labels

    train_data_label_buckets = defaultdict(list)
    
    #split into different label class
    for image, label in zip(train_images, train_labels):
        train_data_label_buckets[label].append((image, label))

    num_labels = len(train_data_label_buckets)
    print(num_labels)

    train_labelled_data_images = []
    train_labelled_data_labels = []
    train_unlabelled_data_images = []
    train_unlabelled_data_labels = []
    train_unlabelled_data_labels_mat = []

    print(n_labelled)
    #uniform labeled data in different class
    for label, label_data in train_data_label_buckets.items():
        count = n_labelled / num_labels
        count = int(count)
        for v in label_data[:count]:
            train_labelled_data_images.append(v[0])
            train_labelled_data_labels.append(v[1])
        for v in label_data[count:]:
            train_unlabelled_data_images.append(v[0])
            # dummy label
            train_unlabelled_data_labels.append(-1)
            train_unlabelled_data_labels_mat.append(v[1])

    train_labelled_images = np.array(train_labelled_data_images)
    train_labelled_labels = np.array(train_labelled_data_labels)

    train_unlabelled_images = np.array(train_unlabelled_data_images)
    train_unlabelled_labels = np.array(train_unlabelled_data_labels)
    train_unlabelled_labels_mat = np.array(train_unlabelled_data_labels_mat)

    train_labelled_images = train_labelled_images[:, :, :, 0]
    train_unlabelled_images = train_unlabelled_images[:, :, :, 0]
    validation_images = validation_images[:, :, :, 0]
    test_images = test_images[:, :, :, 0]

    train_labelled_images, train_labelled_labels = shuffle_images_labels(train_labelled_images, train_labelled_labels)

    # normalizing, range[0, 1]
    train_labelled_images = np.multiply(train_labelled_images, 1./65535.)
    train_unlabelled_images = np.multiply(train_unlabelled_images, 1./65535.)
    validation_images = np.multiply(validation_images, 1./65535.)
    test_images = np.multiply(test_images, 1./65535,)

    print("=" * 50)
    print("train_labelled_images shape:", train_labelled_images.shape)
    print("train_labelled_labels shape:", train_labelled_labels.shape)
    print()
    print("train_unlabelled_images shape:", train_unlabelled_images.shape)
    print("train_unlabelled_labels shape:", train_unlabelled_labels.shape)
    print()
    print("validation_images shape:", validation_images.shape)
    print("validation_labels shape:", validation_labels.shape)
    print()
    print("test_images shape:", test_images.shape)
    print("test_labels shape:", test_labels.shape)
    print("=" * 50)

    print("Dumping pickles")

    dump_pickle(data_dir + "/train_labelled_images.p", train_labelled_images)
    dump_pickle(data_dir + "/train_labelled_labels.p", train_labelled_labels)
    dump_pickle(data_dir + "/train_unlabelled_images.p", train_unlabelled_images)
    dump_pickle(data_dir + "/train_unlabelled_labels.p", train_unlabelled_labels)
    dump_pickle(data_dir + "/validation_images.p", validation_images)
    dump_pickle(data_dir + "/validation_labels.p", validation_labels)
    dump_pickle(data_dir + "/test_images.p", test_images)
    dump_pickle(data_dir + "/test_labels.p", test_labels)

    # save to mat files    
    all_mat = {}
    all_mat['train_labelled_images'] = train_labelled_images
    all_mat['train_labelled_labels'] = train_labelled_labels
    all_mat['train_unlabelled_images'] = train_unlabelled_images
    all_mat['train_unlabelled_labels']  = train_unlabelled_labels_mat
    #all_mat['valid_images']  = valid_images
    #all_mat['valid_labels']  = valid_labels
    all_mat['test_images']  = test_images
    all_mat['test_labels']  = test_labels
    io.savemat(data_dir + "_mat/all_mat.mat", all_mat)


    print("hela dataset successfully created")


if __name__ == "__main__":
    main()
