#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Timing
=====================================================

Copyright (C) 2017 Alan Valejo <alanvalejo@gmail.com> All rights reserved

Timing is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Timing is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Timing. If not, see <http://www.gnu.org/licenses/>.

Required:
	.. _igraph: http://igraph.sourceforge.net
"""

import time
import csv
import json

from contextlib import contextmanager

__maintainer__ = 'Alan Valejo'
__author__ = 'Alan Valejo'
__email__ = 'alanvalejo@gmail.com'
__credits__ = ['Alan Valejo']
__homepage__ = 'https://github.com/alanvalejo/timing'
__license__ = 'GNU'
__docformat__ = 'markdown en'
__version__ = '0.1'
__date__ = '2017-12-01'

class Timing(object):
	"""
	Timing code snippet.
	Usage:
		timing = Timing(['Time [m]', 'Time [s]'], ['Code snippet'])
		timing.get_now()
		mike = Person()
		mike.think()
		timing.add_elapsed()
		timing.print_tabular()
	"""

	def __init__(self, header=[], rows=[]):
		self.start = 0
		self.header = header
		self.rows = rows
		self.elapsed_set = []

	def get_now(self):
		self.start = time.time()

	def add_elapsed(self):
		elapsed = time.time() - self.start
		self.elapsed_set.append([elapsed // 60, '%.4f' % (elapsed % 60)])

	def print_tabular(self):
		max_row = max(self.rows + self.header, key=len)
		format_str = '{:>' + str(len(max_row) + 1) + '}'
		row_format = format_str * (len(self.header))
		print row_format.format(*self.header)
		for row, iten in zip(self.rows, self.elapsed_set):
			print row_format.format(row, *iten)

	def save_csv(self, output):
		with open(output, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(self.header)
			for row, iten in zip(self.rows, self.elapsed_set):
				writer.writerow([row] + iten)

	def save_json(self, output):
		dictionary = dict(zip(self.rows, self.elapsed_set))
		dictionary['header'] = self.header
		with open(output, 'wb') as jsonfile:
			json.dump(dictionary, jsonfile, indent=4)

	def timeit(self, func):
		"""
		Usage: Use the @timing decorator:

		@timing
		def do_work():
			#code
		"""

		@functools.wraps(func)
		def wrap(*args, **kwargs):
			start = time.time()
			func(*args, **kwargs)
			elapsed = time.time() - start
			print('[%s] finished in %dm%.4fs' % (name, minutes, float(seconds)))
			return wrap

	@contextmanager
	def timeit_context(self, name):
		"""
		For example, you can use it like:

		timing = Timing()
		with timing.timeit_context('Code snippet'):
			mike = Person()
			mike.think()
		"""

		start = time.time()
		yield
		elapsed = time.time() - start
		minutes, seconds = elapsed // 60, '%.4f' % (elapsed % 60)
		print('[%s] finished in %dm%.4fs' % (name, minutes, float(seconds)))

	@contextmanager
	def timeit_context_add(self, name):
		"""
		For example, you can use it like:

		timing = Timing(['Time [m]', 'Time [s]'], ['Code snippet'])
		with timeit_context('Code snippet'):
			mike = Person()
			mike.think()
		"""

		start = time.time()
		yield
		elapsed = time.time() - start
		self.rows.append(name)
		self.elapsed_set.append([elapsed // 60, '%.4f' % (elapsed % 60)])
