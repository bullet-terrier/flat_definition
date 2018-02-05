#
"""
methods to extract specific columns from a data file - 
providing a general form.
"""

import petl
import os
import datetime

def log_output(contents, logname = "activity_log.log"):
    """
    consistently write the files output to a log.
    """
    n = datetime.datetime.now # get the time the value appears
    with open(logname,'a') as log:
        if type(contents) == list:
            for a in contents:
                log.write("%s\t%s"%(n().strftime("%Y-%m-%d %H:%M"),str(a)));
                if "\n" not in a:
                    log.write("\n");
        else:
            log.write("%s\t%s"%(n().strftime("%Y-%m-%d %H:%M"),str(contents)))
            if "\n" not in contents:
                log.write("\n");

# take a petl representation of a table, and return 
# an array of tuples representing the data.
# we'll call this meta languate PQL petl Query Language.
# better yet - EQL (etl query language);
def get_cols(ptl_obj,col_array, start_row = 0,end_row = None):
    """
    return a tuple of the designated column numbers from the system.
    """
    ret_obj = []
    for a in ptl_obj:
        try:
            log_output(a)
            tup = []
            for b in col_array:
                try:
                    tup.append(a[b]);
                except Exception as echo:
                    tup.append(None)
                    log_output(echo,"./error_log.log")
            ret_obj.append(tuple(tup))
        except Exception as e:
            log_output(e,"./error_log.log");
        end_row = end_row or len(ret_obj)-1 # set it to the last possible index if it isn't set.
        if end_row < len(ret_obj)-1: ret_obj = ret_obj[:end_row]
        # if they've set a non-zero starting index, truncate the dataset to represent that.
        if start_row > 0: ret_obj = ret_obj[start_row:]
    return ret_obj;
    
def condense(path = ".",use_tsv=True):
    """
    Couldn't be more pleased with this thing.
    
    utility method for moi - 
    all I want it to do is generate a bunch of PETL
    objects that will allow me to extract columns.
    
    Should take some of the output in such a way that I
    can populate a database with patterns for rapid 
    matching later.
    
    I do want to add my scoring mechanism in to the 
    row/column generator when I can.
    """
    objects = []
    # I'll use os.listdir(path) to try and seek everything
    try:
        x = os.listdir(path); # get the state at the start.
        log_output(x) # make a note of what was found.
        for a in x:
            pair = []
            try:
                if use_tsv: pair.append(petl.fromtsv(a))
                else: pair.append(petl.fromcsv(a))
                pair.append(os.path.basename(a))
                log_output("Added petl object for %s"%(a))
                objects.append(tuple(pair))
            except Exception as ECHO:
                log_output(ECHO, "./error_log.log");
                log_output("Exception has occurred: %s"%(ECHO))
    except Exception as eddy:
        log_output(ECHO, "./error_log.log");
        log_output("Exception has occurred: %s"%(eddy));
    return objects;
    
def convert_1_to_0(data_set,column_to_convert=0,index_base=0):
    """
    take some dataset (likely to be tuples) and pass the column number 
    that needs to be converted. 
    
    will take the index base, and determine what the first defined field is.
    if it is not the base, it will shift all subsequent columns to match the 
    current index base.
    """