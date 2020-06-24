from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

class CentroidTracker():
	def __init__(self, maxDisappeared=5):
		self.nextObjectID = 0
		self.objects = OrderedDict()
		self.disappeared = OrderedDict()

		self.maxDisappeared = maxDisappeared

	def register(self, centroid):

		self.objects[self.nextObjectID] = centroid
		self.disappeared[self.nextObjectID] = 0
		self.nextObjectID += 1
		# print("new objects registering")

	def deregister(self, objectID):
		print("deregistering")
		del self.objects[objectID]
		del self.disappeared[objectID]

	def update(self, rects):

		if len(rects) == 0:
			temp_dict = {}
			temp_dict = self.disappeared.copy()
			print("self disappeared",self.disappeared.keys())
			for objectID in temp_dict.keys():
				temp_dict[objectID] += 1

				if temp_dict[objectID] > self.maxDisappeared:
					print("object id dereg", objectID)
					self.deregister(objectID)
				print("failind",objectID)
			print("printing objects after loop",self.objects)
			return self.objects

		# initialize an array of input centroids for the current frame
		inputCentroids = np.zeros((len(rects), 2), dtype="int")
		# print("centroids",inputCentroids)
		# loop over the bounding box rectangles
		for (i, (startX, startY, endX, endY)) in enumerate(rects):
			# use the bounding box coordinates to derive the centroid
			cX = int((startX + endX) / 2.0)
			cY = int((startY + endY) / 2.0)
			inputCentroids[i] = (cX, cY)

		if len(self.objects) == 0:     ## at the starting time or when we have no data
			print("creating the starting object")
			for i in range(0, len(inputCentroids)):
				self.register(inputCentroids[i])

		else:
			# grab the set of object IDs and corresponding centroids
			objectIDs = list(self.objects.keys())
			objectCentroids = list(self.objects.values())

			D = dist.cdist(np.array(objectCentroids), inputCentroids)
			rows = D.argmin(axis=1)
			d_list = list(D)

			for i in range(0,len(list(rows))):
				temp = list(rows)
				index = temp[i]
				# print("row",i,index,d_list[i][index])
				objectID = objectIDs[i]
				# print(index,inputCentroids[index])
				if(d_list[i][index]<30):
					print("tracking the old ones")
					self.objects[objectID] = inputCentroids[index]
					self.disappeared[objectID] = 0
				else:
					print("registering new ones")
					self.disappeared[objectID] += 1
					if(self.disappeared[objectID]>self.maxDisappeared):
						self.deregister(objectID)
					self.register(inputCentroids[index])

		return self.objects
