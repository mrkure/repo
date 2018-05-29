# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 22:11:27 2018

@author: Zdenek
"""
import re
import os
import os.path

def get_root_dirs(input_files_root_dir, contains=[], not_contains=[], print_path = False):
    """Returns all root dirs in input dir    
    
    Parameters
    ----------       
    input_files_root_dir : string
        upmost directory path to start the search        
    contains : list of strings
        strings that should be included in the whole filepath, use | symbol for or statement, for example ['a|b']
    not_contains : list of strings
        strings that should not be included in the whole filepath, use | symbol for or statement, for example ['a|b']
    print_path : bool
        print found path strings
    Returns
    -------
    out : list of strings
        list of whole file paths
    """
    full_paths_list           = []  
    input_files_root_dir      = os.path.normpath(input_files_root_dir)
   
    for root, dirs, files in os.walk(input_files_root_dir):
        for dirr in dirs:
            accept_file = True
            full_path = os.path.join(root, dirr)

            for string in contains:
                if not re.findall(string, dirr):
                    accept_file = False
                else:pass
            
            for string in not_contains:
                if re.findall(string, dirr):
                    accept_file = False
                else:pass
            
            if accept_file:
                full_paths_list.append(full_path)
            else:pass 
        
        break
    full_paths_list.sort()
    if print_path:
        for i in full_paths_list:
            print (i)
    return  full_paths_list
# =============================================================================
# TEST
#path = r"D:/root"
#dirs = get_root_dirs(path, contains=[r'^\d{1,3}_+'], not_contains=[], print_path = True) 
# =============================================================================
    
""" 
===============================================================================
 GET_ALL_FILES_FROM_SUBDIRECTORIES
===============================================================================
"""
def get_files(input_files_root_dir, extension=[], contains=[], not_contains=[], search_subdirs = True, print_path = False):
    """Returns all files in input dir and also all files in all subdirs with selected extension and substring    
    
    Parameters
    ----------       
    input_files_root_dir : string
        upmost directory to start the search        
    extension : list of strings
        allowed file extensions - if empty, all are allowed
    contains : list of strings
        strings that should be included in the whole filepath, use | symbol for or statement, for example ['a|b']
    not_contains : list of strings
        strings that should not be included in the whole filepath, use | symbol for or statement, for example ['a|b']
    print_path : bool
        print found path strings
    search_subdirs : Bool
        sets if subdirs or only root dir should be searched for files
    Returns
    -------
    out : list of strings
        list of whole file paths
    """
    full_paths_list           = []  
    input_files_root_dir      = os.path.normpath(input_files_root_dir)
   
    for root, dirs, files in os.walk(input_files_root_dir):
        for file in files:
            accept_file = False
            full_path = os.path.join(root, file)
            ext = os.path.splitext(full_path)[1]

            if len(extension) == 0:
                accept_file = True
            else: pass       
            for string in extension:
                if '.{}'.format(string) == ext:
                    accept_file = True
                else: pass
            
            for string in contains:
                if not string in full_path:
                    accept_file = False
                else: pass
            
            for string in not_contains:
                if string in full_path:
                    accept_file = False
                else: pass
            
            if accept_file:
                full_paths_list.append(full_path)
            else: pass 
        
        full_paths_list.sort()
        if not search_subdirs:
            break
        
    if print_path:
        for i in full_paths_list:
            print (i)
            
    return  full_paths_list
# =============================================================================
#TEST
#path = r"D:\root\w1._ecrsamples"
#files = get_files(path, contains=[r"D:\root\w1._ecrsamples"], not_contains=[], search_subdirs = True, extension = ['xlsx'],  print_path = True) 
# =============================================================================

""" 
===============================================================================
 GET_PART_OF_GIVEN_OS_PATH
===============================================================================
"""
def get_part_of_path(input_dir_name, nth_part):
    """Returns part of given file path
    
    Parameters
    ----------       
    input_dir_name : string
        input directory name        
    nth_part : number
        for example: -2 = last dir, -1 = file name
    Returns
    -------
    out : string
        selected part of input path
    """
    input_dir_name = os.path.normpath(input_dir_name)
    dir_name       = input_dir_name.split(os.sep)[nth_part]   
    return dir_name
# =============================================================================
#TEST     
#path1 = r"X:\Dnox\Tesla\2018\E1800002-01\data\recording\hydra_data\ED1800052\BMPviskositatskorrektur\file1.txt"
#print(path1)
#print(get_part_of_given_os_path(path1, -1))
#print(get_part_of_given_os_path(path1, -2))
#print(get_part_of_given_os_path(path1, -3))
# =============================================================================

""" 
===============================================================================
 GET_PARTS_OF_GIVEN_OS_PATH_LIST
===============================================================================
"""
def get_parts_of_paths_list(full_paths_list, nth):
    """Returns part of given file path
    
    Parameters
    ----------    
   
    full_paths_list : list of strings
        input directory names list        
    nth : number
        for example: -2 = last dir, -1 = file name
    Returns
    -------
    out : list of strings
        list of selected parts of input paths list
    """
    name_list  = []     
    for path in full_paths_list:
        name_list.append( get_part_of_path(path, nth) )        
    return name_list
# =============================================================================
# #TEST
#path1 = r"X:\Dnox\Tesla\2018\E1800002-01\data\recording\hydra_data\ED1800052\BMPviskositatskorrektur\file1.txt"
#print(get_parts_of_given_os_path_list(path_list, -1))
#print(get_parts_of_given_os_path_list(path_list, -2))
#print(get_parts_of_given_os_path_list(path_list, -3))
# =============================================================================

""" 
#===============================================================================
# GET CURRENT SCIPT DIR
#===============================================================================
""" 
def get_script_dir(_object):
    """Returns dir path to current script
    
    Parameters
    ----------       
    script attribute:  
        use script attribute __file__ as a parameter
    Returns
    -------
    out : string
        Returns dir path to current script
    """
    script_path = os.path.normpath(os.path.abspath(_object)) 
    return os.path.split(script_path)[0]  

# =============================================================================
# #TEST
#print(get_script_dir(__file__))
# =============================================================================
