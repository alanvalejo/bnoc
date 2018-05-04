import os

d = str(0.3)
m = str(0.3)
n = str(0.01)

for index, v in enumerate(range(1000, 101000, 1000)):
	v1 = str(v / 2)
	v2 = str(v / 2)
	o = str(index + 1)
	c = str(int(v * 0.01))

	print 'python ../bnoc.py -v ' + v1 + ' ' + v2 + ' -d ' + d + ' -m ' + m + ' -c ' + c + ' -b -n ' + n + ' -dir exp-time/ -o ' + o
	os.system('python ../bnoc.py -v ' + v1 + ' ' + v2 + ' -d ' + d + ' -m ' + m + ' -c ' + c + ' -b -n ' + n + ' -dir exp-time/ -o ' + o)
