'''
In this example, we will load a RefineDet model and use it to detect objects.
'''

import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io

# Make sure that caffe is on the python path:
caffe_root = './'
os.chdir(caffe_root)
sys.path.insert(0, os.path.join(caffe_root, 'python'))
import caffe

from google.protobuf import text_format
from caffe.proto import caffe_pb2


def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames


def ShowResults(img, img_name, results, labelmap, threshold=0.6, save_fig=False):
    plt.clf()
    plt.imshow(img)
    plt.axis('off')
    ax = plt.gca()

    num_classes = len(labelmap.item) - 1
    colors = plt.cm.hsv(np.linspace(0, 1, num_classes)).tolist()

    for i in range(0, results.shape[0]):
        score = results[i, -2]
        if threshold and score < threshold:
            continue

        label = int(results[i, -1])
        name = get_labelname(labelmap, label)[0]
        color = colors[label % num_classes]

        xmin = int(round(results[i, 0]))
        ymin = int(round(results[i, 1]))
        xmax = int(round(results[i, 2]))
        ymax = int(round(results[i, 3]))
        coords = (xmin, ymin), xmax - xmin, ymax - ymin
        # print("xmin,ymin:" +str(xmin)+","+str(ymin)+"\t\txmax,ymax:" +str(xmax)+","+str(ymax))
        ax.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
        display_text = '%s: %.2f' % (name, score)
        #ax.text(xmin, ymin, display_text, bbox={'facecolor':color, 'alpha':0.5})
    if save_fig:
        plt.savefig(img_name[:-4] + '.jpg', bbox_inches="tight")
        print('Saved: ' + img_name[:-4] + '.jpg')
    #plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_id', type=int, default=-1)
    parser.add_argument('--save_fig', action='store_true')
    parser.add_argument('--threshold', type=float, default=0.2)
    parser.add_argument('--model_id', type=int, default=0)
    parser.add_argument('--img_list', type=str, default="")
    args = parser.parse_args()

    # load model
    defs = [['data/VOC0712/labelmap_voc.prototxt',
             'models/VGGNet/VOC0712/refinedet_vgg16_512x512/deploy.prototxt',
             'models/VGGNet/VOC0712/refinedet_vgg16_512x512/VOC0712_refinedet_vgg16_512x512_final.caffemodel'],
            ['data/VOC0712/labelmap_voc.prototxt',
             'models/VGGNet/VOC0712/refinedet_vgg16_512x512_ft/deploy.prototxt',
             'models/VGGNet/VOC0712/refinedet_vgg16_512x512_ft/VOC0712_refinedet_vgg16_512x512_ft_final.caffemodel'],
            ['data/VOC0712/labelmap_voc.prototxt',
             'models/VGGNet/VOC0712/refinedet_vgg16_512x512_coco/deploy.prototxt',
             'models/VGGNet/VOC0712/refinedet_vgg16_512x512_coco/coco_refinedet_vgg16_512x512.caffemodel'],
            ['data/VOC0712Plus/labelmap_voc.prototxt',
             'models/VGGNet/VOC0712Plus/refinedet_vgg16_512x512/deploy.prototxt',
             'models/VGGNet/VOC0712Plus/refinedet_vgg16_512x512/VOC0712Plus_refinedet_vgg16_512x512_final.caffemodel'],
            ['data/VOC0712Plus/labelmap_voc.prototxt',
             'models/VGGNet/VOC0712Plus/refinedet_vgg16_512x512_ft/deploy.prototxt',
             'models/VGGNet/VOC0712Plus/refinedet_vgg16_512x512_ft/VOC0712Plus_refinedet_vgg16_512x512_ft_final.caffemodel'],
            ['data/coco/labelmap_coco.prototxt',
             'models/VGGNet/coco/refinedet_vgg16_512x512/deploy.prototxt',
             'models/VGGNet/coco/refinedet_vgg16_512x512/coco_refinedet_vgg16_512x512_final.caffemodel'],
            ['data/coco/labelmap_coco.prototxt',
             'models/VGGNet/coco/refinedet_resnet101_512x512/deploy.prototxt',
             'models/VGGNet/coco/refinedet_resnet101_512x512/coco_refinedet_resnet101_512x512_final.caffemodel']]
    model_info = defs[args.model_id]
    # gpu preparation
    if args.gpu_id >= 0:
        caffe.set_device(args.gpu_id)
        caffe.set_mode_gpu()

    # load labelmap
    labelmap_file = model_info[0]
    file = open(labelmap_file, 'r')
    labelmap = caffe_pb2.LabelMap()
    text_format.Merge(str(file.read()), labelmap)

    model_def = model_info[1]
    model_weights = model_info[2]
    net = caffe.Net(model_def, model_weights, caffe.TEST)

    # image preprocessing
    if '320' in model_def:
        img_resize = 320
    else:
        img_resize = 512
    net.blobs['data'].reshape(1, 3, img_resize, img_resize)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', np.array([104, 117, 123]))  # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2, 1, 0))  # the reference model has channels in BGR order instead of RGB

    # im_names = os.listdir('examples/images')
    # im_names = ['000456.jpg', '000542.jpg', '001150.jpg', '001763.jpg', '004545.jpg']
    with open(args.img_list, 'r') as list_f:
        lines = list_f.readlines()
        for n, line in enumerate(lines):
            s = model_def.split('/')
            save_dir = 'results/'+s[-3]+'/'+s[-2]+'_'+str(args.threshold)+'/'
            img_name = save_dir+line.split('/')[-1]     # save to right dictory
            img_name = img_name[:-1]
            print(str(n) + ' in ' + str(len(lines)) + ", " + img_name)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            image_file = line
            image_file = image_file[:-1]
            image = caffe.io.load_image(image_file)
            transformed_image = transformer.preprocess('data', image)
            net.blobs['data'].data[...] = transformed_image

            detections = net.forward()['detection_out']
            det_label = detections[0, 0, :, 1]
            det_conf = detections[0, 0, :, 2]
            det_xmin = detections[0, 0, :, 3] * image.shape[1]
            det_ymin = detections[0, 0, :, 4] * image.shape[0]
            det_xmax = detections[0, 0, :, 5] * image.shape[1]
            det_ymax = detections[0, 0, :, 6] * image.shape[0]
            result = np.column_stack([det_xmin, det_ymin, det_xmax, det_ymax, det_conf, det_label])

            # show result
            ShowResults(image, img_name, result, labelmap, args.threshold, save_fig=args.save_fig)
            #exit()
