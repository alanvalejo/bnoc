#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Args

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

Giving credit to the author by citing the papers.
"""

import argparse
import json
import yaml
import os

from datetime import datetime

__maintainer__ = 'Alan Valejo'
__email__ = 'alanvalejo@gmail.com'
__author__ = 'Alan Valejo'
__credits__ = ['Alan Valejo']
__homepage__ = 'https://www.alanvalejo.com.br'
__license__ = 'GNU.GPL.v3'
__docformat__ = 'markdown en'
__version__ = '0.1'
__date__ = '2019-08-08'

def setup_parser(filename):

	with open(filename) as f:
		args = json.load(f)
		args = json.dumps(args)
		args = yaml.safe_load(args)

	descriptions = 'description'
	if 'descriptions' in args:
		descriptions = args.pop('descriptions', None)

	parser = argparse.ArgumentParser(description=descriptions)
	parser._action_groups.pop()
	parser.register("type", "bool", str2bool)
	required = parser.add_argument_group('required arguments')
	optional = parser.add_argument_group('optional arguments')

	for key, value in args.items():
		long = key
		if 'long' in value:
			long = value.pop('long', None)
		if 'type' in value:
			value['type'] = eval(value['type'])
		args = ['-%s' % key, '--%s' % long]
		kwargs = value
		if value['required']:
			required.add_argument(*args, **kwargs)
		else:
			optional.add_argument(*args, **kwargs)

	parser._action_groups.append(required)
	parser._action_groups.append(optional)

	return parser

def str2bool(v):
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')

def update_json(options):

	if hasattr(options, 'conf') and options.conf:
		with open(options.conf) as f:
			json_dict = json.load(f)
			argparse_dict = vars(options)
			argparse_dict.update(json_dict)

def check_output(options, output_default='out'):

	if options.output_directory is None:
		options.output_directory = os.path.dirname(os.path.abspath(options.input)) + '/'
	else:
		if not os.path.exists(options.output_directory):
			os.makedirs(options.output_directory)
	if not options.output_directory.endswith('/'):
		options.output_directory += '/'
	if hasattr(options, 'input'):
		output_default, options.extension = os.path.splitext(os.path.basename(options.input))
	if options.output is None:
		options.output = options.output_directory + output_default
	else:
		options.output = options.output_directory + options.output
	if hasattr(options, 'unique_key') and options.unique_key:
		now = datetime.now()
		options.output = options.output_directory + options.output + '_' + now.strftime('%Y%m%d%H%M%S%f')
