import numpy as np

def compress_masks(masks, target=-1):
	shapes = []
	points = []
	inners = []

	for mask in masks:
		shape, (y1, x1), (y2, x2) = mask.shape, find_mask_top_left(mask, target), find_mask_bottom_right(mask, target)
		shapes.append(np.array(list(shape), dtype=np.int16))
		points.append(np.array([y1, x1], dtype=np.int16))
		inners.append(mask[y1:y2, x1:x2])

	return np.array(shapes, dtype=np.int16), np.array(points, dtype=np.int16), np.array(inners, dtype=np.float16)

def decompress_masks(shapes, points, inners, pad_val=-1):
	decompressed = []

	for shape, point, inner in zip(shapes, points, inners):
		y1, x1 = point[0], point[1]
		mask = np.full(tuple(shape), pad_val, dtype=np.float64)
		mask[y1:y1+len(inner), x1:x1+len(inner[0])] = inner
		decompressed.append(mask)

	return np.array(decompressed, dtype=np.float64)

def pad_all(arr):
	r, c = 0, 0

	for el in arr:
		if el.shape[0] > r:
			r = el.shape[0]
		if el.shape[1] > c:
			c = el.shape[1]

	new_arr = []
	for el in arr:
		result = np.full((r, c), -1, dtype=np.float16)
		result[:el.shape[0],:el.shape[1]] = el
		new_arr.append(result)

	return np.array(new_arr, dtype=np.float16)

def find_mask_top_left(mask, target=-1):
	for y in range(len(mask)):
		if np.sum(mask[y]) != target * len(mask[y]):
			for x in range(len(mask[y])):
				if mask[y][x] != target:
					return (y, x)

	return None

def find_mask_bottom_right(mask, target=-1):
	for y in range(len(mask)-1, -1, -1):
		if np.sum(mask[y]) != target * len(mask[y]):
			for x in range(len(mask[y])-1, -1, -1):
				if mask[y][x] != target:
					return (y + 1, x + 1)

	return None

