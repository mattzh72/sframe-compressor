import numpy as np

def compress_annotations(annotations):
	labels = []
	compressed = []

	for annotation in annotations:
		compressed_annotation = []
		for mark in annotation:
			compressed_mark = []
			if mark['label'] not in labels:
				labels.append(mark['label'])

			compressed_annotation.append(np.array([mark['coordinates']['x'],
				mark['coordinates']['width'],
				mark['coordinates']['y'],
				mark['coordinates']['height'],
				labels.index(mark['label']),
				mark['objectID']], dtype=np.uint16))

		compressed.append(compressed_annotation)

	return np.array(compressed, dtype=np.uint16), labels

def decompress_annotations(compressed, labels):
	decompressed = []

	for annotation in tqdm(compressed, desc='Unpacking annotations'):
		decompressed_annotation = []
		for mark in annotation:
			decompressed_annotation.append({'coordinates': 
				{'x': mark[0], 'width': mark[1], 'y': mark[2], 'height': mark[3]}, 
				'label': labels[mark[4]], 
				'objectID': str(mark[5])})

		decompressed.append(decompressed_annotation)

	return decompressed








