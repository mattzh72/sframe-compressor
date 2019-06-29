import turicreate as tc
import numpy as np
import matplotlib.pyplot as plt


def array_equals_2D(a1, a2):
	if a1.shape != a2.shape:
		return False

	result = True
	for row in range(len(a1)):
		for col in range(len(a1[row])):
			result = result and a1[row][col] == a2[row][col]

			if not result:
				print(row, col)
				print(a1[row][col], a2[row][col])

				return result

	return result

sf1 = tc.load_sframe('sample.sframe')
sf2 = tc.load_sframe('new.sframe')

plt.imshow(sf1[34]['image'].pixel_data)
plt.show()
plt.imshow(sf2[34]['image'].pixel_data)
plt.show()
plt.close()
# print(sf1[34]['image'].pixel_data)
# print("LOOOOOL")
# print(sf2[34]['image'].pixel_data)

