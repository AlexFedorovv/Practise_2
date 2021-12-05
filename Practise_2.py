import numpy as np
from scipy.special import spherical_jn as jn
from scipy.special import spherical_yn as yn
import matplotlib.pyplot as plt
import os
from urllib.request import urlopen
from re import split


def a_n (n, kr):
    a = jn(n, kr) / h_n(n, kr)
    return a

def b_n (n, kr):
    b = ( kr * jn(n-1, kr) - n * jn(n, kr)) / ( kr * h_n(n-1, kr) - n * h_n(n, kr))
    return b

def h_n(n, kr):
    h = jn(n, kr) + 1j * yn(n, kr)
    return h


variant = 11

file = urlopen('https://jenyay.net/uploads/Student/Modelling/task_02.xml')
list = file.readlines()
my_string = list[variant+1].decode("utf-8")
values = my_string.split("\"")

D = float(values[3])
fmin = float(values[5])
fmax = float(values[7])

print("D=", D)
print("fmin=",fmin)
print("fmax=",fmax)

step = 1e6

r = D / 2
freq = np.arange(fmin, fmax, step)
wavelength = 3e8 / freq
k = 2*np.pi / wavelength

sum_arr = [((-1) ** n) * (n + 0.5) * ( b_n(n, k*r) - a_n(n, k*r)) for n in range(1, 50) ]
Sum = np.sum(sum_arr, axis = 0)
epr = ( wavelength ** 2)/ np.pi * (np.abs(Sum) ** 2)

# Запись в выходной файл
if os.path.exists("results"):
    print("Указанный файл существует")
else:
    print("Файл не существует")
    os.mkdir("results")

file = open("results/result.txt", "w")

for index, freq_val in enumerate(freq):
    file.write(str(freq_val))
    file.write("    ")
    file.write(str(epr[index]))
    file.write("\n")

file.close()

#График
plt.plot(freq/10e6,epr,'r-')
plt.xlabel('$f, МГц$')
plt.ylabel('$\sigma, м^2$')
plt.grid()
plt.show()
