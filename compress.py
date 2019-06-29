from config import Configs
import turicreate as tc
from tqdm import tqdm
import numpy as np
import os
import pickle
import argparse

from utils.annotations import compress_annotations
from utils.image import compress_img, compile_video
from utils.mask import compress_masks


parser = argparse.ArgumentParser(description='This compresses an SFrame in Turicreate format.')
parser.add_argument('-s', help='The SFrame directory.', required=True)
parser.add_argument('-o', help='The output directory.', required=True)
args = vars(parser.parse_args())

sframes = [file for file in os.listdir(args['s']) if file.endswith(".sframe")]
pbar = tqdm(sframes)
for sframe in pbar:
	pbar.set_description("Loading in {0}".format(sframe))
	# LOAD IN 
	sf = tc.load_sframe(os.path.join(args['s'], sframe))
	parent_dir = os.path.join(args['o'], Configs.SFRAME.replace('.sframe', '.tejas'))
	os.makedirs(parent_dir)

	# COMPRESS MASKS
	pbar.set_description("Packing masks")
	mask_subdir = os.path.join(parent_dir, Configs.MASKS_COL)
	os.makedirs(mask_subdir)
	mask_col = sf['stateMasks']
	for idx in range(len(mask_col)):
		masks = mask_col[idx]
		s, p, i = compress_masks(masks)
		np.savez_compressed(os.path.join(mask_subdir, '{0}.npz'.format(idx)), s, p, i)

	# COMPRESS IMAGES
	pbar.set_description("Packing images")
	img_subdir = os.path.join(parent_dir, Configs.IMAGE_COL)
	os.makedirs(img_subdir)
	compile_video([img.pixel_data for img in sf[Configs.IMAGE_COL]], target=os.path.join(img_subdir, 'frames.mp4'))

	# COMPRESS ANNOTATIONS
	pbar.set_description("Packing annotations")
	ann_subdir = os.path.join(parent_dir, Configs.ANNOTATIONS_COL)
	os.makedirs(ann_subdir)
	ann_col = sf['annotations']
	compressed, labels = compress_annotations(ann_col)
	np.savez_compressed(os.path.join(ann_subdir, 'annotations.npz'), compressed)
	with open(os.path.join(ann_subdir, 'labels.pickle'), 'wb') as handle:
	    pickle.dump(labels, handle, protocol=pickle.HIGHEST_PROTOCOL)

