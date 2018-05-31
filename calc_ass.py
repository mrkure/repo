# -*- coding: utf-8 -*-
"""
Created on Tue May 29 20:09:30 2018

@author: zdenek
"""
import os
import sys
sys.path.append('D:/scripts')
import numpy as np
import pandas as pd
import functions_io as fio
import functions_plot as fplot
import matplotlib.pyplot as plt
import functions_data_processing as fdproc
pd.options.display.max_colwidth = 1500
fplot.set_rc_params()
cwd = fio.get_script_dir(__file__)
plt.ioff() 

"""
# =============================================================================
# user settings 
# =============================================================================
#"""
used_dirs_keys       = []
skip_rows            = 1

low_threshold        = 1
high_threshold       = 5

max_marker           = 'o'
min_marker           = 'o'
                             
c_map_single_graph   = fplot.C_map(['red','blue', 'green']) 
c_map_root_graph     = fplot.C_map(['red','blue', 'green'])
c_map_combined_graph = fplot.C_map(['red','blue', 'green'])    

results_dir,         = 'results', 
results_name         = 'results.xlsx'
single_file_graphs   = 'single_file_graphs' 
root_dir_graphs      = 'root_dir_graphs' 
combined_graph       = 'combined_graph'
combined_graph_name  = 'data'

"""
# =============================================================================
# calculation
# =============================================================================
#"""
# creating dir structure for results
os.makedirs('{}/{}'.format(cwd, results_dir), exist_ok=True)
os.makedirs('{}/{}/{}'.format(cwd, results_dir, combined_graph), exist_ok=True)
os.makedirs('{}/{}/{}'.format(cwd, results_dir, single_file_graphs), exist_ok=True)
abs_paths    = fio.get_files(cwd, extension = ['csv'], contains = used_dirs_keys, not_contains=['~'], print_path=False)
root_dirs    = fio.get_parts_of_paths_list(abs_paths, -3)
sample_dirs  = fio.get_parts_of_paths_list(abs_paths, -2)
filenames    = fio.get_parts_of_paths_list(abs_paths, -1)

frame  = pd.DataFrame({'abs_paths':abs_paths, 'root_dir':root_dirs,'sample_dir':sample_dirs, 'filename':filenames})

unique_root_dirs = list(sorted(set(root_dirs)))

   
results_frames_list  = []  
# =============================================================================
#  main loop
# =============================================================================
for number, root_dir in enumerate(unique_root_dirs):
    os.makedirs('{}/{}/{}'.format(cwd, results_dir, root_dir_graphs), exist_ok=True)
    filtered_frame = frame[ frame.root_dir == root_dir]

    for file, root_dir, sample_dir, filename in zip(filtered_frame.abs_paths, filtered_frame.root_dir, filtered_frame.sample_dir, filtered_frame.filename):
        print('Processing file ...... {} / {}'.format(root_dir, sample_dir))
        data_frame = pd.read_csv(file, delimiter=';', decimal = ',', usecols=[2,1], skiprows=2)
        
        time                   = np.array(data_frame['sec'])
        force                  = np.array(data_frame['N'])
        min_index, min_value   = fdproc.minimum_index_calculation_using_derivation(time, force, low_threshold, high_threshold)
        max_index, max_value   = fdproc.maximum_index_calculation_by_index(time, force, 0, min_index)


        results_frame = pd.DataFrame( [[root_dir, sample_dir, filename, max_value ]], columns = ['root_dir', 'sample_dir', 'filename', 'max_force']) 
        results_frames_list.append(results_frame)

        plt.figure()  # single figure
        plt.plot(  time, force, c=c_map_single_graph.get_color(False), label='')
        plt.plot(time[min_index], force[min_index], 'r', marker = min_marker)
        plt.plot(time[max_index], force[max_index], 'k', marker = max_marker)
        fplot.set_plot_config(xa_label='Time [s]', ya_label='Force [N]', title='{}; {}'.format(root_dir, sample_dir)) 
        fplot.add_label(sample_dir, c_map_single_graph.get_color(False))
        fplot.add_label('maximum_force', 'k', 0, '-', max_marker, 6)
        fplot.add_label('minimum_force', 'r', 0, '-', min_marker, 6)
        plt.savefig( '{}/{}/{}/{}_{}.png'.format( cwd, results_dir, single_file_graphs, root_dir, sample_dir))        
        plt.close()
        
        plt.figure(number) # dirr figure
        plt.plot(  data_frame['sec'], data_frame['N'], c=c_map_root_graph.get_color(False), label='')
        plt.plot(time[max_index], force[max_index], 'ko')
        
        plt.figure(len(unique_root_dirs)+1) # combined figure
        plt.plot(  data_frame['sec'], data_frame['N'], c=c_map_combined_graph.get_color(False), label='')  
        plt.plot(time[max_index], force[max_index], 'ko')
   
    c_map_single_graph.get_color(True)   

     
    plt.figure(number) # dirr figure
    fplot.add_label(root_dir, c_map_root_graph.get_color(True))
    fplot.add_label('maximum_force', 'k', 0, '-', max_marker, 6)
    fplot.set_plot_config(xa_label='Time [s]', ya_label='Force [N]', title='{}'.format(root_dir)) 
    plt.savefig( '{}/{}/{}/{}.png'.format( cwd, results_dir, root_dir_graphs, root_dir))   
    plt.close()   


    
    fplot.add_label(root_dir, c_map_combined_graph.get_color(True))  


plt.figure(len(unique_root_dirs)+1) # combined figure
fplot.add_label('maximum_force', 'k', 0, '-', max_marker, 6)
fplot.set_plot_config(xa_label='Time [s]', ya_label='Force [N]', title='{}'.format(combined_graph_name)) 
plt.savefig( '{}/{}/{}/{}.png'.format( cwd, results_dir, combined_graph, 'combined_graph'))   
plt.close() 
 
results_frame = pd.concat(results_frames_list, ignore_index=True)

# =============================================================================
# saving data
# =============================================================================
writer = pd.ExcelWriter('{}/{}/{}'.format( cwd, results_dir, results_name), engine='xlsxwriter')
results_frame.to_excel(writer,'Sheet1', index=False)
writer.save()


input("press Enter to exit ;) ") 













