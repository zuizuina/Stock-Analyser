# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

class ProfitAnalyser:
    def __init__(self, data_dir, result_dir, year):
        self.file_prefix = 'profit'
        self.radio = '营业利润'
        self.data_dir = data_dir
        self.result_dir = result_dir
        self.year = year
        self.colors = ["black", "darkgray", "rosybrown", "darkorange", "wheat",
                       "royalblue", "darkorchid", "teal", "gold", "pink"]
        self.markers = ["o", "v", "^", "<", ">", "D", "d", "s", "*", "p"]
        self.stocks = []
        
    def getFilePrefix(self):
        return self.file_prefix
        
    def get_all_data(self, stocks):
        all_data = []
        for stock_id in stocks:
            lrb = pd.read_csv(
                r'%s/%s_lrb.csv' % (self.data_dir, stock_id),
                encoding='utf-8',
                header=0,
                index_col=None)

            list_lrb = []
            for i in lrb['报表期截止日']:
                list_lrb.append(str(i)) #list_lrb: ['20181231', '20180930'``````]
            list_lrb_0 = []
            for i in list_lrb:
                i_ = i[:4] + '-' + i[4:6] + '-' + i[6:8]
                list_lrb_0.append(i_)  #transfer from '20181231' to '2018-12-31'
            lrb['报告时间'] = [pd.to_datetime(t) for t in list_lrb_0]
            lrb.index = lrb['报告时间'] #Pandas to_datetime() method helps to convert string Date time into Python Date time object ep.2018-12-31
            
            all_data.append(lrb[::-1])
            # time as index in chronological order
            # information of all account items in income statement
        return all_data

    def get_data_month(self, all_data, month):
        all_data_month = []
        for data in all_data:
            data_month = data[data.index.month == month] #If month=12, then select info that start from 1 Jan to 31 Dec in each ear
            all_data_month.append(data_month)
        return all_data_month

    def get_data_ratio(self, all_data):
        results = []
        for data in all_data:
            result = pd.DataFrame()
            result['营业利润'] = data['营业利润'] #to find 营业利润
            # result['营业利润率'] = data['营业利润'] / data['营业收入']
            # result['净利率'] = data['归属于母公司所有者的净利润'] / data['营业收入']
            # result['毛利率'] = (data['营业收入'] - data['营业成本']) / data['营业收入']
            results.append(result)
        return results

    def data_plot(self, all_data):
        if len(all_data) == 0:
            return
        all_plot_data = []
        for data in all_data:
            data_idx = data.index
            data_idx = data_idx[-5:] #find 5 most recent dates time
            plot_data = []
            for idx in data_idx:
                plot_data += data.loc[idx].tolist() #for each of 5 dates, data.loc[idx] is to find all incstatement information at that date
            all_plot_data.append(plot_data)

        x = all_data[0].index
        x = x[-5:]
        x = [t.year for t in x] #comprehension, assign x as 5 most recent dates' year
        x_tick = range(len(x))
        plt.figure()
        plt.xticks(x_tick, x)
        for i in range(len(all_plot_data)):
            plt.plot(x_tick, all_plot_data[i], "--", color=self.colors[i], marker=self.markers[i], label=self.stocks[i])
        plt.xlabel("Year", fontsize=16)
        plt.ylabel("Profit", fontsize=16)
        plt.legend(loc="upper center", ncol=2, fontsize=12)
        plt.savefig(self.result_dir+
                    '/'+
                    self.file_prefix+'-'+
                    '_'.join(self.stocks)+
                    '.png')
    
    def Analyse(self, stocks):
        self.stocks = stocks
        data = self.get_all_data(stocks) #information of all account items in selected stock's income statement (in chronological order)
        data_Dec = self.get_data_month(data, 12) #extract Annual report number
        data_ratio = self.get_data_ratio(data_Dec) #get Profit Account number
        self.data_plot(data_ratio) # Plot Profit Account number with respect to time
