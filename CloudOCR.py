#!/usr/bin/python
# coding: utf-8

from wand.image import Image
import io
import sys
import argparse
import time
import os
import shutil
import subprocess
from google.cloud import vision

class CloudOCR(object):
	def __init__(self, ocr_language, pdf_input, img_dir, imageformat, img_prefix):
		print('0. starting work on "%s"' % pdf_input)
		self.ocr_language = ocr_language
		self.pdf_input = pdf_input
		self.img_dir = img_dir
		self.img_prefix = img_prefix
		self.imageformat = imageformat

	def pdfimages(self):
		print('1. pdfimages')
		if os.path.isdir(args.img_dir) is True:
			# return
			print('rmdir "%s"' % args.img_dir)
			shutil.rmtree(self.img_dir)
		os.mkdir(self.img_dir)
		comando = "pdfimages -png %s %s/%s" % (self.pdf_input, self.img_dir, self.img_prefix)
		cmd_start = time.time()
		process = subprocess.Popen(comando, shell=True, cwd="./")
		process.wait()
		cmd_elaboration = time.time() - cmd_start
		if process is not None:
			print('completed in %s sec.' % cmd_elaboration)

	def convert(self):
		print('2. convert')
		files = os.listdir(self.img_dir)
		print("pages: %s" % len(files))
		for file in files:
			f_output = file.replace("ppm", self.imageformat)
			self.worker_convert((self.img_dir+file), (self.img_dir+f_output))

	def worker_convert(self, f_input, f_output):
		source = Image(filename=f_input)
		destination = source.convert(self.imageformat)
		destination.save(filename=f_output)
		os.remove(f_input)
		print('%s => %s' % (f_input, f_output))

	def list(self, folder=None):
		if folder is None:
			folder = self.img_dir
		print('listdir')
		files = os.listdir(folder)
		print("#: %s list: %s" % (len(files), files))

	def visionapi(self):
		print('3. visionapi')
		vision_client = vision.Client()

		files = os.listdir(self.img_dir)
		txt = ""
		for file in files:
			txt += self.worker_visionapi(vision_client, (self.img_dir+file))
		return txt

	def worker_visionapi(self, vision_client, filename_input):
		print('processing "%s"' % filename_input)
		file_name = os.path.join(
			os.path.dirname(__file__), filename_input)

		with io.open(file_name, 'rb') as image_file:
			content = image_file.read()
			image = vision_client.image(
				content=content)
		#languageHints = "it"
		texts = image.detect_text()
		txt = ""
		for text in texts:
			txt += text.description
			# vertices = (['({},{})'.format(bound.x_coordinate, bound.y_coordinate)
			#             for bound in text.bounds.vertices])
			# print('DGB bounds: {}'.format(','.join(vertices)))
		# self.save_output(filename_input + ".txt", txt)
		return txt

	def save_output(self, f_output, text):
		file = open(f_output, "w")
		for i in text:
			file.write(i.encode("utf-8"))
		file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process input PDF file to CSV by OCR')
	parser.add_argument('pdf_filename', nargs='?', default='INPUT.pdf',
						help='Input PDF file')
	parser.add_argument('img_dir', nargs='?', default='images/',
						help='Images directory')
	parser.add_argument('img_prefix', nargs='?', default='a',
						help='Images prefix')
	parser.add_argument('ocr_language', nargs='?', default='ita',
						help='OCR language')
	parser.add_argument('ocr_imageformat', nargs='?', default='png',
						help='OCR image format')
	parser.add_argument('text_output', nargs='?', default="output5.txt",
						help='OCR text output')
	args = parser.parse_args()

	if not args.pdf_filename:
		print('--filename is mandatory')
		sys.exit(1)

	b = CloudOCR(args.ocr_language, args.pdf_filename, args.img_dir, args.ocr_imageformat, args.img_prefix)
	b.pdfimages()
	#b.convert()
	b.list()
	text = b.visionapi()
	b.save_output(args.text_output, text)
