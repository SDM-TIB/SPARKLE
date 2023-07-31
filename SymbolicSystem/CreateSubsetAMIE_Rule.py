#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import sys


def subset_AMIE_rule(percentile, path, f_name):
    result = pd.read_csv(path + f_name+ '.csv')
    df = result.loc[result.F1_Score>np.percentile(result.F1_Score.to_list(), int(percentile))]
    df.to_csv(path+f_name+'_'+percentile+'.csv', index=None)


def main(*args):
    subset_AMIE_rule(args[0], args[1], args[2])


if __name__ == '__main__':
    main(*sys.argv[1:])
