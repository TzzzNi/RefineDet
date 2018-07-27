# generate results
python test/refinedet_demo.py --model_id 0 --save_fig --img_list /home/nt/PycharmProjects/transdata/test_data.txt
python test/refinedet_demo.py --model_id 1 --save_fig --img_list /home/nt/PycharmProjects/transdata/test_data.txt
python test/refinedet_demo.py --model_id 2 --save_fig --img_list /home/nt/PycharmProjects/transdata/test_data.txt
python test/refinedet_demo.py --model_id 3 --save_fig --img_list /home/nt/PycharmProjects/transdata/test_data.txt
python test/refinedet_demo.py --model_id 4 --save_fig --img_list /home/nt/PycharmProjects/transdata/test_data.txt
python test/refinedet_demo.py --model_id 5 --save_fig --img_list /home/nt/PycharmProjects/transdata/test_data.txt
python test/refinedet_demo.py --model_id 6 --save_fig --img_list /home/nt/PycharmProjects/transdata/test_data.txt
# plot the compare pictures

/home/nt/PycharmProjects/venv/bin/python3.5 /home/nt/PycharmProjects/transdata/plot_result_refineDet.py



