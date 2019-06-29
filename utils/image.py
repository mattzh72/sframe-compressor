import numpy as np
import cv2
import turicreate as tc
from tqdm import tqdm

def read_video(video_path, rgb=True):
	video = cv2.VideoCapture(video_path)
	ret, frame = video.read()

	count = 0
	frames = []

	while ret:
		if rgb:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frames.append(get_tc_img(frame))
		ret, frame = video.read()
		count += 1

	return frames

def compile_video(frames, rgb=True, fps=30, target='frames.mp4'):
	assert len(frames) > 0, 'Frames list is empty.'

	height, width, layers = frames[0].shape
	codec = cv2.VideoWriter_fourcc(*'mp4v')
	video = cv2.VideoWriter(target, codec, fps, (width,height))
	
	for frame in frames:
		if rgb:
			frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

		video.write(frame)

	cv2.destroyAllWindows()
	video.release()

def compress_img(img, quality=80):
	return cv2.imencode('.jpg', img.pixel_data, [int(cv2.IMWRITE_JPEG_QUALITY), quality])[1]

def decompress_img(compressed):
	return cv2.imdecode(compressed, 1)

def get_tc_img(img):
	assert (isinstance(img, np.ndarray)), 'Image is not of type numpy.ndarray.'

	RAW_FORMAT = 2
	return tc.Image(_image_data=img.tobytes(), 
		_width=img.shape[1], 
		_height=img.shape[0], 
		_channels=img.shape[2], 
		_format_enum=RAW_FORMAT, 
		_image_data_size=img.size)
