# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# import statsmodels.api as sm

# df = pd.read_csv(r'E:\PUBG_API\full_stk.csv')


# print(df['5_min'].mean())

# print(df['15_min'].mean())


# X = df[['5_min', '10_min', '15_min', '20_min', '25_min', '30_min', 'kills', 'heals', 'boosts', 'damageDealt', 'distance']]
# y = df['winPlace']


# model = sm.OLS(y, X)
# results = model.fit()
# print(results.summary())

import pycuda.autoinit
import pycuda.driver as drv
import numpy

from pycuda.compiler import SourceModule
mod = SourceModule("""
__global__ void multiply_them(float *dest, float *a, float *b)
{
  const int i = threadIdx.x;
  dest[i] = a[i] * b[i];
}
""")

multiply_them = mod.get_function("multiply_them")

a = numpy.random.randn(400).astype(numpy.float32)
b = numpy.random.randn(400).astype(numpy.float32)

dest = numpy.zeros_like(a)
multiply_them(
        drv.Out(dest), drv.In(a), drv.In(b),
        block=(400,1,1), grid=(1,1))

print(dest-a*b)