cd /home/nt/Github/RefineDet
./build/tools/caffe train \
--solver="models/VGGNet/VOC0712Plus/refinedet_vgg16_512x512_ft/solver.prototxt" \
--weights="models/VGGNet/VOC0712/refinedet_vgg16_512x512_coco/coco_refinedet_vgg16_512x512.caffemodel" \
--gpu 0,1,2,3 2>&1 | tee jobs/VGGNet/VOC0712Plus/refinedet_vgg16_512x512_ft/VOC0712Plus_refinedet_vgg16_512x512_ft.log
