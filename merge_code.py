import os
import sys

USAGE = "USAGE: python merge_code.py [-h|--help] [-a] [-m MESSAGE] [-o OUTPUT_FILE] files... \n\
	-h, --help:     Print help page \n\
	-A:             Print full path for each file (only base name by default) \n\
	-a:             Print hidden files as well (disabled by default) \n\
	-m MESSAGE:     Prepend MESSAGE at the beginning of the generated text (nothing by default) \n\
	-o OUTPUT_FILE: Specify the location to store the generated text (stdout by default) \n\
	files:          Files whose contents are merged into a combined. If directories are passed in, this will work for all files recursively "

def parse_args():
	res = {}
	res['files'] = []
	res['message_flag'] = False
	res['output_flag'] = False
	res['abs'] = False
	res['all'] = False
	if len(sys.argv) == 1:
		sys.argv += ['-h']
	i = 1
	while i < len(sys.argv):
		if sys.argv[i] == '-h' or sys.argv[i] == '--help':
			print(USAGE)
			exit()
		if sys.argv[i] == '-A':
			res['abs'] = True
		elif sys.argv[i] == '-a':
			res['all'] = True
		elif sys.argv[i] == '-m':
			if i == len(sys.argv) - 1:
				print('Error: Missing parameter for "-m" flag')
				exit()
			else:
				i += 1
				res['message_flag'] = True
				res['message'] = sys.argv[i]
		elif sys.argv[i] == '-o':
			if i == len(sys.argv) - 1:
				print('Error: Missing parameter for "-o" flag')
				exit()
			else:
				i += 1
				res['output_flag'] = True
				res['output'] = sys.argv[i]

		else:
			res['files'].append(sys.argv[i])
		i += 1
	return res

def print_file(f, abs_flag, out):
	with open(f) as raw:
		out.write("{}".format(os.path.abspath(f)) if abs_flag else os.path.basename(f))
		out.write("\n")
		counter = 1
		for line in raw:
			out.write("{}\t{}".format(counter, line))
			counter += 1
		out.write("\n\n")

def walk_dir(files, abs_flag, all_flag, out):
	for i in files:
		if os.path.isdir(i):
			tmp = os.listdir(i)
			if all_flag == False:
				for item in tmp:
					if item[0] == '.':
						tmp.remove(item)
			tmp = [os.path.abspath(i) + os.sep + x for x in tmp]
			walk_dir(tmp, abs_flag, all_flag, out)
		else:
			print_file(i, args['abs'], out)

args = parse_args()

out = sys.stdout
if args['output_flag']:
	out = open(args['output'], 'w')

if args['message_flag']:
	out.write("{}\n\n".format(args['message']))

walk_dir(args['files'], args['abs'], args['all'], out)

out.close()