#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from tqdm import tqdm, trange
from time import sleep



bar = trange(10)
for i in bar:
	bar.set_description("Processing %d" % i)
	sleep(0.1)
	if not (i % 3):
		tqdm.write("Done task %i" % i)

'''
for i in trange(10):
	sleep(0.1)



pbar = tqdm(["a", "b", "c", "d"])
for char in pbar:
	pbar.set_description("Processing %s" % char)
	sleep(0.5)


bar = trange(10)
for i in bar:
	sleep(0.1)
	if not (i % 3):
		tqdm.write("Done task %i" % i)



with tqdm(total=100) as pbar:
	for i in range(10):
		sleep(0.1)
		pbar.update(10)

'''
'''
def fnw(x, a, b):
	sleep(0.2)
	tqdm.write(str(x.name))
	tqdm.pandas()
	print(a, b)
	return 'q'


import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randint(0, 100, (10, 6)))
print(df)
# Register `pandas.progress_apply` with `tqdm`
# (can use `tqdm_gui`, `tqdm_notebook`, optional kwargs, etc.)
tqdm.pandas(desc="my bar!")





# Now you can use `progress_apply` instead of `apply`
#df.progress_apply(fnw)

#print(d)

r = df.progress_apply(fnw, axis=1, a='aa', b='ba')

print(r)
print(df)
# can also groupby:
# df.groupby(0).progress_apply(lambda x: x**2)
'''
