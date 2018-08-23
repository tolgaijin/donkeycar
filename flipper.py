import cv2
import json
from pprint import pprint
import fnmatch

import time
import traceback
import os
import sys
import pandas as pd
import glob


def get_path(list, file_name):
	path = next((s for s in list if file_name in s), "NA")
	print(path)
	return path

def get_all_list(basedir, ext):
	all_list = glob.glob(basedir + "\**\*" +ext, recursive = True)
	return all_list

def list2df(list, col_name):
	newdf = pd.DataFrame(list)
	newdf.columns = [col_name]
	return newdf

def get_tub_name(path):
	a = path.split('\\')
	filter = fnmatch.filter(a,"tub*")
	idx = a.index(filter[0])
	tub_name = a[idx]
	return tub_name

def splitall(path):
	allparts = []
	while 1:
		parts = os.path.split(path)
		if parts[0] == path:  # sentinel for absolute paths
			allparts.insert(0, parts[0])
			break
		elif parts[1] == path: # sentinel for relative paths
			allparts.insert(0, parts[1])
			break
		else:
			path = parts[0]
			allparts.insert(0, parts[1])
	return allparts

def main():

	#get data
	imgs  = get_all_list(r"C:\Users\ermito1.HAGL\Downloads\data", "jpg")
	jsons = get_all_list(r"C:\Users\ermito1.HAGL\Downloads\data", "json")

	#image manipulation
	for file in imgs:
		s = "\\"
		dir, name = os.path.split(file)
		img = cv2.imread(file)
		#cropped_img = img[40:120, 0:160]
		vertical_img = cv2.flip( img, 1 )

		#saving in a new path with new name
		new_dir = s.join(splitall(dir)[0:len(splitall(dir))-1])
		new_path = new_dir+"\\"+get_tub_name(file)+str("_00")
		#new_name = os.path.splitext(name)[0] + '_cf'+".jpg"
		if not os.path.exists(new_path):
			os.makedirs(new_path)
		cv2.imwrite(new_path+"\\"+name, vertical_img)

	#json manipulation (angle)
	for file in jsons:
		dir, name = os.path.split(file)
		try:
			#reading and manipulating the existing json content
			with open(file) as f:
				data = json.load(f)
			data["user/angle"] = (-1) * data["user/angle"]
				#data["cam/image_array"] = os.path.splitext(data["cam/image_array"])[0] + "_cf" + os.path.splitext(data["cam/image_array"])[1]

			#saving the manipulated json
			new_dir = s.join(splitall(dir)[0:len(splitall(dir)) - 1])
			new_path = new_dir + "\\" + get_tub_name(file) + str("_00")
				#new_name = os.path.splitext(name)[0] + '_cf'+".json"
			if not os.path.exists(new_path):
				os.makedirs(new_path)
			with open(new_path+"\\"+name, "w") as outfile:
				json.dump(data, outfile)

		except KeyError as k:
			with open(file) as f:
				data = json.load(f)

			with open(new_path+"\\"+name, "w") as outfile:
				json.dump(data, outfile)

			continue


if __name__ == '__main__':
	try:
		start_time = time.time()
		print(time.asctime())
		main()
		print(time.asctime())
		print('Done.')
		print('TOTAL TIME IN MINUTES:', ((time.time() - start_time) / 60.0))
	#
		sys.exit(0)
	except KeyboardInterrupt as e:  # Ctrl-C
		raise e
	except SystemExit as e:  # sys.exit()
		raise e
	except Exception as e:
		print('ERROR, UNEXPECTED EXCEPTION')
		str(e)
		traceback.print_exc()
		os._exit(1)