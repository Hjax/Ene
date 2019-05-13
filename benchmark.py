# benchmark.py
import os

os.system("py -3.7 -O -m cProfile -o profile_name.prof bot/main.py")
os.system("snakeviz profile_name.prof")