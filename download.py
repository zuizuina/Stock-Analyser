# -*- coding: utf-8 -*-

import os
import requests
from multiprocessing.dummy import Pool as ThreadPool

class Downloader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.lrb_base_url = 'http://api.xueqiu.com/stock/f10/incstatement.csv?page=1&size=10000&symbol='
        self.llb_base_url = 'http://api.xueqiu.com/stock/f10/cfstatement.csv?page=1&size=10000&symbol='
        self.fzb_base_url = 'http://api.xueqiu.com/stock/f10/balsheet.csv?page=1&size=10000&symbol='
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Cookie': 'xq_a_token=4c6af5a6a2c8e7862e51b7761695e6e88e768a3'
        }
    
    def download_lrb(self, url):
        r = requests.get(url, headers=self.headers)
        filename = os.path.join(self.data_dir, url.split('=')[-1] + '_lrb.csv')
        with open(filename, 'wb') as f:
            f.write(r.content)

    def download_fzb(self, url):
        r = requests.get(url, headers=self.headers)
        filename = os.path.join(self.data_dir, url.split('=')[-1] + '_fzb.csv')
        with open(filename, 'wb') as f:
            f.write(r.content)

    def download_llb(self, url):
        r = requests.get(url, headers=self.headers)
        filename = os.path.join(self.data_dir, url.split('=')[-1] + '_llb.csv')
        with open(filename, 'wb') as f:
            f.write(r.content)
    
    def downloadStock(self, stock_codes):
        lrb_urls = [self.lrb_base_url + code for code in stock_codes]
        fzb_urls = [self.fzb_base_url + code for code in stock_codes]
        llb_urls = [self.llb_base_url + code for code in stock_codes]
        pool = ThreadPool(5)
        pool.map(self.download_lrb, lrb_urls)
        pool.close()
        pool.join()
        pool = ThreadPool(5)
        pool.map(self.download_fzb, fzb_urls)
        pool.close()
        pool.join()
        pool = ThreadPool(5)
        pool.map(self.download_llb, llb_urls)
        pool.close()
        pool.join()
