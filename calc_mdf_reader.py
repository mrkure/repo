# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 14:19:23 2018

@author: CAZ2BJ
"""
import numpy as np
import matplotlib.pyplot as plt
import functions_io as fio
import functions_csv as fcsv
import functions_plot as fplot
import functions_excel as fexcel
import functions_data_processing as fdp
import mdfreader



path       = r'X:\Dnox\Erprobung\13_Data_transfer\Carda\ED1801047.dat'
data_file  = mdfreader.mdf(path,noDataLoading=False)
info       = mdfreader.mdfinfo()



channels   = info.listChannels(path) # returns only the list of channels    info=mdfreader.mdfinfo()
dictionary = {}


for channel in channels:
    dictionary.update({channel:data_file.getChannel(channel)})
    
#
#dick       = dictionary['CoSCR_st']
#data       = dick['data']
#
#
#
#res = data_file.resample(masterChannel='time')
