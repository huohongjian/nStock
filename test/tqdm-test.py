#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from tqdm import tqdm, trange
from time import sleep



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
