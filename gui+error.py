# -*- coding: utf-8 -*-

from download import Downloader
from shareholder_profit import ShareholderProfitAnalyser
from revenue import RevenueAnalyser
from profit import ProfitAnalyser

import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class StockAnalyseWidget(QWidget):
    def __init__(self, data_dir, result_dir):
        super().__init__()
        
        # Create the data directory and result directory if not exist.
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        
        self.data_dir = data_dir
        self.result_dir = result_dir
        
        self.downloader = Downloader(self.data_dir)
        
        self.all_stock = set()

        self.initUI()

    def initUI(self):
        '''
        Layout Structure
        - overall_layout [QVBoxLayout]
          - crawl_layout [QVBoxLayout]
            - label_layout [QHBoxLayout]
              - crawl_label [QLabel]
            - add_stock_layout [QHBoxLayout]
              - stock_text [QLineEdit]
              - add_stock_btn [QPushButton]
              - stock_file_btn [QPushButton]
            - crawl_progress_layout [QHBoxLayout]
              - progress_label [QLabel]
          - analysis_layout [QHBoxLayout]
            - stock_list_layout [QVBoxLayout]
              - list_title_layout [QHBoxLayout]
                - crawled_list_title [QLabel]
              - crawled_stock_layout [QHBoxLayout]
                - stock_table [QTableWidget]
            - analysis_option_layout [QVBoxLayout]
              - del_stock_btn [QPushButton]
              - shareholder_profit_btn [QPushButton]
            - show_show_result_layout [QVBoxLayout]
              - result_title_layout [QHBoxLayout]
                - result_title [QLabel]
              - result_img_layout [QHBoxLayout]
                - result_label [QLabel]
                  - result_pix [QPixmap]
        '''        
        # crawl_layout begin
        crawl_layout = QVBoxLayout()

        label_layout = QHBoxLayout()
        self.crawl_label = QLabel("Add the stocks to be crawled,such as: SH600775 OR select file 'symbol_test' ", self)
        self.crawl_label.setFont(QFont('Times', 19))
        label_layout.addWidget(self.crawl_label)
        
        add_stock_layout = QHBoxLayout()
        self.stock_text = QLineEdit(self)
        self.stock_text.setFont(QFont('Times', 16))
        add_stock_layout.addWidget(self.stock_text)
        self.add_stock_btn = QPushButton("Add", self)
        self.add_stock_btn.clicked.connect(self.addStock)
        self.add_stock_btn.setFont(QFont('Times', 16))
        add_stock_layout.addWidget(self.add_stock_btn)
        self.stock_file_btn = QPushButton("Select File", self)
        self.stock_file_btn.setObjectName("file")
        self.stock_file_btn.clicked.connect(self.addStockFile)
        self.stock_file_btn.setFont(QFont('Times', 16))
        add_stock_layout.addWidget(self.stock_file_btn)
        
        crawl_progress_layout = QHBoxLayout()
        self.progress_label = QLabel("Crawl Progress: None", self)
        self.progress_label.setFont(QFont('Times', 24))
        crawl_progress_layout.addWidget(self.progress_label)
        
        crawl_layout.addLayout(label_layout)
        crawl_layout.addLayout(add_stock_layout)
        crawl_layout.addLayout(crawl_progress_layout)
        # crawl_layout end

        # analysis_layout begin
        analysis_layout = QHBoxLayout()


        stock_list_layout = QVBoxLayout()
        
        list_title_layout = QHBoxLayout()
        self.crawled_list_title = QLabel("Crawled Stock", self)
        self.crawled_list_title.setFont(QFont('Times', 24))
        list_title_layout.addWidget(self.crawled_list_title)
        
        crawled_stock_layout = QHBoxLayout()
        self.stock_table = QTableWidget(self)
        self.stock_table.setFont(QFont('Times', 16))
        self.stock_table.setShowGrid(False)
        self.stock_table.setColumnCount(1)
        self.stock_table.setRowCount(len(self.all_stock))
        self.stock_table.setHorizontalHeaderLabels(['Stock Symbol'])
        self.stock_table.resizeColumnToContents(0)
        crawled_stock_layout.addWidget(self.stock_table)
        
        stock_list_layout.addLayout(list_title_layout)
        stock_list_layout.addLayout(crawled_stock_layout)
        
        analysis_option_layout = QVBoxLayout()
        
        self.del_stock_btn = QPushButton("Delete", self)
        self.del_stock_btn.clicked.connect(self.deleteStock)
        self.del_stock_btn.setFont(QFont('Times', 16))
        analysis_option_layout.addWidget(self.del_stock_btn)
        
        self.revenue_btn = QPushButton("Analyse Revenue", self)
        self.revenue_btn.clicked.connect(self.analyseRevenue)
        self.revenue_btn.setFont(QFont('Times', 16))
        analysis_option_layout.addWidget(self.revenue_btn)
        
        self.profit_btn = QPushButton("Analyse Profit", self)
        self.profit_btn.clicked.connect(self.analyseProfit)
        self.profit_btn.setFont(QFont('Times', 16))
        analysis_option_layout.addWidget(self.profit_btn)
        
        self.shareholder_profit_btn = QPushButton("Analyse Shareholder Profit", self)
        self.shareholder_profit_btn.clicked.connect(self.analyseShareholderProfit)
        self.shareholder_profit_btn.setFont(QFont('Times', 16))
        analysis_option_layout.addWidget(self.shareholder_profit_btn)
        
        show_result_layout = QVBoxLayout()       
        
        result_title_layout = QHBoxLayout()
        self.result_title = QLabel("Analysis Result", self)
        self.result_title.setFont(QFont('Times', 24))
        result_title_layout.addWidget(self.result_title)
        
        result_img_layout = QHBoxLayout()
        self.result_label = QLabel()
        self.result_pix = QPixmap(640, 480)
        self.result_label.setPixmap(self.result_pix)
        result_img_layout.addWidget(self.result_label)
        
        show_result_layout.addLayout(result_title_layout)
        show_result_layout.addLayout(result_img_layout)


        analysis_layout.addLayout(stock_list_layout)
        analysis_layout.addLayout(analysis_option_layout)
        analysis_layout.addLayout(show_result_layout)
        # analysis_layout end
        
        overall_layout = QVBoxLayout()
        overall_layout.addLayout(crawl_layout)
        overall_layout.addLayout(analysis_layout)

        self.setGeometry(300, 300, 1050, 720)
        self.setWindowTitle('Stock Analyser')
        self.setLayout(overall_layout)
        self.show()
    
    def deleteStock(self):
        selected_stocks = []
        selected_idx = []
        for i in range(len(self.all_stock)):
            cb = self.stock_table.cellWidget(i, 0)
            cb_checked = getattr(cb, "isChecked")
            cb_text = getattr(cb, "text")
            if cb_checked() == True:
                selected_idx.append(i)
                selected_stocks.append(cb_text())
        for i in range(len(selected_idx)):
            self.stock_table.removeRow(selected_idx[i]-i)
            self.all_stock.remove(selected_stocks[i]) 

    def addStock(self):
        self.progress_label.setText('Crawl Progress: 0/1')

        stock_id = self.stock_text.text()
        if stock_id in self.all_stock == True or stock_id == '':
            return
        
        all_stock_list=[]
        with open('symbol.txt','r') as f:
            for line in f:
                all_stock_list.extend(list(line.strip('\n').split(',')))
        if stock_id not in all_stock_list:
            reply = QMessageBox.question(self, 'Wrong Input', 'Please input again',QMessageBox.Yes)
            return
        
        self.downloader.downloadStock([stock_id])
        
        row_id = len(self.all_stock)
        self.all_stock.add(stock_id)
        self.stock_table.setRowCount(len(self.all_stock))
        self.stock_table.setCellWidget(row_id, 0, QCheckBox(stock_id))

        self.progress_label.setText('Crawl Progress: 1/1')

    def addStockFile(self):
        file_tup = QFileDialog.getOpenFileName(self,  "Select File", "./", "All Files (*);;Text Files (*.txt)")
        #to check if it is valid or not
        if len(file_tup) == 0 or file_tup[0] == '':
            return

        stocks = []
        with open(file_tup[0], 'r', encoding='utf-8') as f:
            stocks = [s.strip() for s in f.readlines()]
        stocks_len = len(stocks)

        self.progress_label.setText('Crawl Progress: 0/' + str(stocks_len))
        QCoreApplication.processEvents()

        downloaded_cnt = 0
        while len(stocks) > 0:
            to_download = stocks[:5]
            to_download = [stock_id for stock_id in to_download if not(stock_id in self.all_stock == True or stock_id == '')]
            
            self.downloader.downloadStock(to_download)
            
            for stock_id in to_download:
                row_id = len(self.all_stock)
                self.all_stock.add(stock_id)
                self.stock_table.setRowCount(len(self.all_stock))
                self.stock_table.setCellWidget(row_id, 0, QCheckBox(stock_id))
    
            stocks = stocks[5:]
            downloaded_cnt += len(to_download)
            
            self.progress_label.setText('Crawl Progress: ' + str(downloaded_cnt) + '/' + str(stocks_len))
            QCoreApplication.processEvents()
            
    def analyseRevenue(self):
        # Init analyser
        analyser = RevenueAnalyser(self.data_dir, self.result_dir, 2019)
        # Find which stocks have been chosen
        selected_stocks = []
        for i in range(len(self.all_stock)):
            cb = self.stock_table.cellWidget(i, 0)
            cb_checked = getattr(cb, "isChecked")
            cb_text = getattr(cb, "text")
            if cb_checked() == True:
                selected_stocks.append(cb_text())
        # Only use the first 10 stocks to analyse
        selected_stocks = selected_stocks[:10]
        analyser.Analyse(selected_stocks)
        # Show the result
        self.result_pix = QPixmap(self.result_dir +
                                  '/' +
                                  analyser.getFilePrefix()+'-'+
                                  '_'.join(selected_stocks)+
                                  '.png')
        self.result_label.setPixmap(self.result_pix)
    
    def analyseProfit(self):
        # Init analyser
        analyser = ProfitAnalyser(self.data_dir, self.result_dir, 2019)
        # Find which stocks have been chosen
        selected_stocks = []
        for i in range(len(self.all_stock)):
            cb = self.stock_table.cellWidget(i, 0)
            cb_checked = getattr(cb, "isChecked")
            cb_text = getattr(cb, "text")
            if cb_checked() == True:
                selected_stocks.append(cb_text())
        # Only use the first 10 stocks to analyse
        selected_stocks = selected_stocks[:10]
        analyser.Analyse(selected_stocks)
        # Show the result
        self.result_pix = QPixmap(self.result_dir +
                                  '/' +
                                  analyser.getFilePrefix()+'-'+
                                  '_'.join(selected_stocks)+
                                  '.png')
        self.result_label.setPixmap(self.result_pix)
    
    def analyseShareholderProfit(self):
        # Init analyser
        analyser = ShareholderProfitAnalyser(self.data_dir, self.result_dir, 2019)
        # Find which stocks have been chosen
        selected_stocks = []
        for i in range(len(self.all_stock)):
            cb = self.stock_table.cellWidget(i, 0)
            cb_checked = getattr(cb, "isChecked")
            cb_text = getattr(cb, "text")
            if cb_checked() == True:
                selected_stocks.append(cb_text())
        # Only use the first 10 stocks to analyse
        selected_stocks = selected_stocks[:10]
        analyser.Analyse(selected_stocks)
        # Show the result
        self.result_pix = QPixmap(self.result_dir +
                                  '/' +
                                  analyser.getFilePrefix()+'-'+
                                  '_'.join(selected_stocks)+
                                  '.png')
        self.result_label.setPixmap(self.result_pix)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sw = StockAnalyseWidget('./stock_data', './analysis_results')
    sys.exit(app.exec_())
