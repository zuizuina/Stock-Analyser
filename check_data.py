# -*- coding: utf-8 -*-

import pandas as pd

symbol = []

with open('symbol.txt', 'r', encoding='utf-8') as f:
    symbol = [s.strip() for s in f.readlines()]

notFound = []
for stock_id in symbol:
    lrb = pd.read_csv(
        r'%s/%s_lrb.csv' % ('stock_data', stock_id),
        encoding='utf-8',
        header=0,
        index_col=None)
    find = False
    for k in lrb.keys():
        if k == '营业利润':
            find = True
            break
    if find == False:
        notFound.append(stock_id)

print("not found:", len(notFound), notFound)
