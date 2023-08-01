#!/usr/bin/env python
# coding: utf-8
import sys
import pandas as pd
import string


def load_graph(file_name):
    data = pd.read_csv(file_name, delimiter='\t', header=None)  #
    data.columns = ['s', 'p', 'o']
    data.replace('type', 'Type', regex=True, inplace=True)
    # data.replace('>', '', regex=True, inplace=True)
    # data.replace('<', '', regex=True, inplace=True)
    # data.replace(' .', '', regex=True, inplace=True)
    return data


def create_terms(data, file_name):
    pd.DataFrame(list(string.ascii_uppercase) + list(set(data.p.unique())), columns=['term']).to_csv(file_name,
                                                                                                     index=None)


# path = '../KG/FrenchRoyalty/french_training.tsv'
def main(*args):
    """Load Knowledge Graph"""
    data = load_graph(args[0])
    """List of Terms considered in Datalog program"""
    create_terms(data, args[1])


if __name__ == '__main__':
    main(*sys.argv[1:])
