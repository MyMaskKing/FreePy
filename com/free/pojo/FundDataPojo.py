#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 
# Author    : 
# File    : SiteDateByJsonPojo.py
# 调用的例：from 包的路径.类名 import 类名
class FundDataPojo(object):
    def _init_(self,fund_cd,fund_title,fund_time,NVA,LJJZ,growth_day,growth_week,growth_month,growth_three_month,growth_six_month,growth_year,growth_two_year,growth_three_year,growth_all,growth_current_year,establishment_date,service_charge,row_data_bak):
        self.fund_cd = fund_cd # 基金代码
        self.fund_title = fund_title # 基金简称
        self.fund_time = fund_time # 日期
        self.NVA = NVA # 单位净值
        self.LJJZ = LJJZ # 累计净值
        self.growth_day = growth_day # 日增长率
        self.growth_week = growth_week # 日增长率近1周
        self.growth_month = growth_month # 日增长率近1月
        self.growth_three_month = growth_three_month # 日增长率近3月
        self.growth_six_month = growth_six_month # 日增长率近6月
        self.growth_year = growth_year # 日增长率近1年
        self.growth_two_year = growth_two_year # 日增长率近2年
        self.growth_three_year = growth_three_year # 日增长率近3年
        self.growth_all = growth_all # 日增长率成立以来
        self.growth_current_year = growth_current_year # 日增长率(当年)
        self.establishment_date = establishment_date # 成立日期
        self.service_charge = service_charge # 手续费
        self.row_data_bak = row_data_bak # 备份当前基金数据
    # 【基金代码】的Set方法
    def set_fund_cd(self, fund_cd):
        self.fund_cd = fund_cd
    # 【基金代码】的Get方法
    def get_fund_cd(self):
        return self.fund_cd
    # 【基金简称】的Set方法
    def set_fund_title(self, fund_title):
        self.fund_title = fund_title
    # 【基金简称】的Get方法
    def get_fund_title(self):
        return self.fund_title
    # 【日期】的Set方法
    def set_fund_time(self, fund_time):
        self.fund_time = fund_time
    # 【日期】的Get方法
    def get_fund_time(self):
        return self.fund_time
    # 【单位净值】的Set方法
    def set_NVA(self, NVA):
        self.NVA = NVA
    # 【单位净值】的Get方法
    def get_NVA(self):
        return self.NVA
    # 【累计净值】的Set方法
    def set_LJJZ(self, LJJZ):
        self.LJJZ = LJJZ
    # 【累计净值】的Get方法
    def get_LJJZ(self):
        return self.LJJZ
    # 【日增长率】的Set方法
    def set_growth_day(self, growth_day):
        self.growth_day = growth_day
    # 【日增长率】的Get方法
    def get_growth_day(self):
        return self.growth_day
    # 【日增长率近1周】的Set方法
    def set_growth_week(self, growth_week):
        self.growth_week = growth_week
    # 【日增长率近1周】的Get方法
    def get_growth_week(self):
        return self.growth_week
    # 【日增长率近1月】的Set方法
    def set_growth_month(self, growth_month):
        self.growth_month = growth_month
    # 【日增长率近1月】的Get方法
    def get_growth_month(self):
        return self.growth_month
    # 【日增长率近3月】的Set方法
    def set_growth_three_month(self, growth_three_month):
        self.growth_three_month = growth_three_month
    # 【日增长率近3月】的Get方法
    def get_growth_three_month(self):
        return self.growth_three_month
    # 【日增长率近6月】的Set方法
    def set_growth_six_month(self, growth_six_month):
        self.growth_six_month = growth_six_month
    # 【日增长率近6月】的Get方法
    def get_growth_six_month(self):
        return self.growth_six_month
    # 【日增长率近1年】的Set方法
    def set_growth_year(self, growth_year):
        self.growth_year = growth_year
    # 【日增长率近1年】的Get方法
    def get_growth_year(self):
        return self.growth_year
    # 【日增长率近2年】的Set方法
    def set_growth_two_year(self, growth_two_year):
        self.growth_two_year = growth_two_year
    # 【日增长率近2年】的Get方法
    def get_growth_two_year(self):
        return self.growth_two_year
    # 【日增长率近3年】的Set方法
    def set_growth_three_year(self, growth_three_year):
        self.growth_three_year = growth_three_year
    # 【日增长率近3年】的Get方法
    def get_growth_three_year(self):
        return self.growth_three_year
    # 【日增长率成立以来】的Set方法
    def set_growth_all(self, growth_all):
        self.growth_all = growth_all
    # 【日增长率成立以来】的Get方法
    def get_growth_all(self):
        return self.growth_all
    # 【日增长率(当年)】的Set方法
    def set_growth_current_year(self, growth_current_year):
        self.growth_current_year = growth_current_year
    # 【日增长率(当年)】的Get方法
    def get_growth_current_year(self):
        return self.growth_current_year
    # 【成立日期】的Set方法
    def set_establishment_date(self, establishment_date):
        self.establishment_date = establishment_date
    # 【成立日期】的Get方法
    def get_establishment_date(self):
        return self.establishment_date
    # 【手续费】的Set方法
    def set_service_charge(self, service_charge):
        self.service_charge = service_charge
    # 【手续费】的Get方法
    def get_service_charge(self):
        return self.service_charge
    # 【备份当前基金数据】的Set方法
    def set_row_data_bak(self, row_data_bak):
        self.row_data_bak = row_data_bak
    # 【备份当前基金数据】的Get方法
    def get_row_data_bak(self):
        return self.row_data_bak
