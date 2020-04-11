#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper
=====================================================

Copyright (C) 2017 Alan Valejo <alanvalejo@gmail.com> All rights reserved

This program comes with ABSOLUTELY NO WARRANTY. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS
WITH YOU.

Owner or contributors are not liable for any direct, indirect, incidental, special, exemplary, or consequential
damages, (such as loss of data or profits, and others) arising in any way out of the use of this software,
even if advised of the possibility of such damage.

This program is free software and distributed in the hope that it will be useful: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with this program. If not,
see http://www.gnu.org/licenses/.

Giving credit to the author by citing the papers
"""

import numpy
import PyPDF2
import logging
import csv
import os

from scipy import sparse

# from scipy.ndimage import rotate
# from scipy.misc import imread, imsave
from scipy.io import arff

__maintainer__ = 'Alan Valejo'
__email__ = 'alanvalejo@gmail.com'
__author__ = 'Alan Valejo'
__credits__ = ['Alan Valejo']
__homepage__ = 'https://www.alanvalejo.com.br'
__license__ = 'GNU.GPL.v3'
__docformat__ = 'markdown en'
__version__ = '0.1'
__date__ = '2019-08-08'

def is_non_zero_file(path):
	return os.path.isfile(path) and os.path.getsize(path) > 0

def write_ncol(output, edgelist):
	with open(output, 'w') as f:
		f.write(edgelist)

def write_pajek(output, obj_count, edgelist):
	with open(output, 'w') as f:
		f.write('*Vertices ' + str(obj_count) + '\n')
		for i in range(0, obj_count):
			f.write(str(i+1) + ' \"' + str(i) + '\"\n')
		f.write('*Edges ' + '\n')
		for line in edgelist.split('\n'):
			if len(line.split(' ')) == 1:
				break
			u, v, w = line.split(' ')
			f.write(str(int(u) + 1) + ' ' + str(int(v) + 1) + ' ' + w + '\n')

def loadarff(filename, class_column=True):

	# Read and create X and y
	data, meta = arff.loadarff(filename)
	corpus_ = data[meta.names()[:-1]] # Everything but the last column
	corpus = corpus_.copy()
	corpus = numpy.asarray(corpus.tolist(), dtype=numpy.float32)
	X = sparse.csr_matrix(corpus)
	y, K = [None] * 2
	if class_column:
		y = data[meta.names()[-1]] # Everything but the last column
		y = encode_categorical(y) # or y = pd.Series(y).astype('category').cat.codes.values
		K = len(numpy.unique(y))
	return X, y, K

def initialize_logger(dir='log', output='log'):

	if not os.path.exists(dir):
		os.makedirs(dir)
	if not dir.endswith('/'):
		dir += '/'

	output = dir + output

	# level [INFO, DEBUG, ERROR]
	# message type [info, error, warning, debug, critical]
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# Create console handler and set level to info
	# info, waning
	handler = logging.StreamHandler()
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	# Create error file handler and set level to error
	# error, critical
	handler = logging.FileHandler(output + '-error.log', 'w+')
	handler.setLevel(logging.ERROR)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	# Create debug file handler and set level to debug
	# info, warning, error, debug, critical
	handler = logging.FileHandler(output + '-debug.log', 'w+')
	handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	return logger

def encode_categorical(array):

	d = {key: value for (key, value) in zip(numpy.unique(array), numpy.arange(len(array)))}
	shape = array.shape
	array = array.ravel()
	new_array = numpy.zeros(array.shape, dtype=numpy.int)
	for i in range(len(array)):
		new_array[i] = d[array[i]]
	return new_array.reshape(shape)

def detect_delimiter(filename):

	# Detect wich delimiter and which columns to use is used in the data
	with open(filename, 'r') as f:
		first_line = f.readline()
	sniffer = csv.Sniffer()
	dialect = sniffer.sniff(first_line)

	return dialect.delimiter

def detect_ncol(filename):

	# Detect number of columns
	with open(filename, 'r') as f:
		first_line = f.readline()
	sniffer = csv.Sniffer()
	dialect = sniffer.sniff(first_line)
	ncols = len(first_line.split(dialect.delimiter))

	return ncols

def save_csr_as_dense(filename, X, fmt='%.2f'):
	numpy.savetxt(filename, X.todense(), delimiter=',', fmt=fmt)

# def rotate_png(filename):
#
# 	img = imread(filename + '.png')
# 	rotate_img = rotate(img, -90)
# 	imsave(filename + '-rtt.png', rotate_img)

def rotate_pdf(filename):

	pdf_in = open(filename + '.pdf', 'rb')
	pdf_reader = PyPDF2.PdfFileReader(pdf_in)
	pdf_writer = PyPDF2.PdfFileWriter()

	for pagenum in range(pdf_reader.numPages):
		page = pdf_reader.getPage(pagenum)
		page.rotateClockwise(90)
		pdf_writer.addPage(page)

	pdf_out = open(filename + '-rtt.pdf', 'wb')
	pdf_writer.write(pdf_out)
	pdf_out.close()
	pdf_in.close()

def remap(x, o_min, o_max, n_min, n_max):

	# Range check
	if o_min == o_max:
		return None
	if n_min == n_max:
		return None

	# Check reversed input range
	reverseInput = False
	old_min = min(o_min, o_max)
	old_max = max(o_min, o_max)
	if not old_min == o_min:
		reverseInput = True

	# Check reversed output range
	reverseOutput = False
	new_min = min(n_min, n_max)
	new_max = max(n_min, n_max)
	if not new_min == n_min:
		reverseOutput = True

	portion = (x - old_min) * (new_max - new_min) / (old_max - old_min)
	if reverseInput:
		portion = (old_max - x) * (new_max - new_min) / (old_max - old_min)

	result = portion + new_min
	if reverseOutput:
		result = new_max - portion

	return result
