from config import Configs
import turicreate as tc
from tqdm import tqdm
import numpy as np
import os
import pickle
import argparse

from utils.annotations import decompress_annotations
from utils.image import decompress_img, get_tc_img, read_video
from utils.mask import decompress_masks

parser = argparse.ArgumentParser(description='This decompresses an .TEJAS into a SFrame.')
parser.add_argument('-t', help='The .TEJAS directory.', required=True)
parser.add_argument('-o', help='The output directory.', required=True)
args = vars(parser.parse_args())

tejases = [file for file in os.listdir(args['t']) if file.endswith(".tejas")]

pbar = tqdm(tejases)
for tejas in pbar:
	pbar.set_description("Loading in {0}".format(tejas))
	annotations_dir = os.path.join(args['t'], tejas, Configs.ANNOTATIONS_COL)
	masks_dir = os.path.join(args['t'], tejas, Configs.MASKS_COL)
	images_dir = os.path.join(args['t'], tejas, Configs.IMAGE_COL)


	# LOAD ANNOTATIONS
	pbar.set_description("Unpacking annotations")
	annotations_data, labels = None, None
	for file in os.listdir(annotations_dir):
		if file.endswith(".pickle"):
			with open(os.path.join(annotations_dir, file), 'rb') as handle:
				labels = pickle.load(handle)
		if file.endswith(".npz"):
			annotations_data = np.load(os.path.join(annotations_dir, file))['arr_0']

	annotations = decompress_annotations(annotations_data, labels)

	# LOAD MASKS
	pbar.set_description("Unpacking masks")
	masks = list(range(len(os.listdir(masks_dir))))
	for file in tqdm(os.listdir(masks_dir), desc='Unpacking masks'):
		if file.endswith(".npz"):
			masks_data = np.load(os.path.join(masks_dir, file))
			s, p, i = masks_data['arr_0'], masks_data['arr_1'], masks_data['arr_2']

			idx = int(file.split(".")[0])
			masks[idx] = decompress_masks(s, p, i)

	# LOAD IMAGES
	pbar.set_description("Unpacking images")
	images = read_video(os.path.join(images_dir, 'frames.mp4'))

	# WRITE TO SFRAME
	pbar.set_description("Writing to disk")
	sf = tc.SFrame({Configs.IMAGE_COL:images, Configs.ANNOTATIONS_COL:annotations, Configs.MASKS_COL:masks})
	sf.save(os.path.join(args['o'], '{0}.sframe'.format(tejas.split('.')[0])))









