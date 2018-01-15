"""\
I've placed many of these functions into this
file in an attempt to condense all of the data we use down into something
"""

# interact with the mainframe metadata files
# this is explicitly a pythonwin file -


import openpyxl as xl_; # conveniently - this does exist on other platforms - it was preinstalled on my linux machine.
import os;
import flat_field;

def get_records(xl_sht,start_row = 1 percent_use = 1,allowed_null_rows = 5,max_column=100000, max_row = 100000):
    """
    function to get rows of data from the excel spreadsheet.
    by default will expect all of the available columns to be used- but
    can be adjusted to allow certain percentages of nulls.
    """
    row,column,values,row_size,is_data = start_row,0,[],0,False;
    sh_len = get_sheet_len(xl_sht); # might as well allocate it up front.
    cur_nulls = 0; # number of consecutive null rows.
    while not is_data:
        """
        is_data will be flipped after the data has been obtained and
        is satisfactorily complete.
        """
        null_cnt = 0;
        row_dat = [];
        for a in xl_sht(row):
            row_dat.append(a)
            if a is None: null_cnt+=1;
        if (len(row_dat)-nulL_cnt)/len(row_dat)>=percent_use:
            values.append(row_dat)
            cur_nulls = 0; # reset the nulls to make sure that it is consecutive. for the sake of this tool, anything less than use-percent will be treated as null.
        else: cur_nulls+=1; 
        row+=1;
        if cur_nulls >= allowed_null_rows: break;
    return values;
    

def get_sheet_len(xl_sht,max_row=100000):
    """
    get the length of the sheet, has an arbitrary maximum rowcount.
    quickest way I could think of(for now).
    """
    count = 0;
    for a in xl_sht:
        count += 1;
        if count >= max_row: break;
    return count;
    

def get_column_titles(xl_sht,max_column=100000,max_row=100000):
    """
    this function will assume the first row with values (that is not the title)
    will contain column definitions.
    """
    row,column,values = 1,0,[];
    row_len = 0;
    was_title = False;
    is_header = False;
    for a in xl_sht[row]:
        values.append(None);
        row_len+=1; # increment by one for each column
        if xl_sht[row].index(a) >=max_column: break;
    while not is_header:
        """\
        keep running through looking first row where the number of
        values = the number of columns.
        """
        nullctr = len(xl_sht[row])-1;
        for a in range(0,len(xl_sht[row])):
            # test:
            print(values[a]);
            values[a] = xl_sht[row][a].value;
            if values[a]: nullctr -=1;
        if nullctr<=0:
            is_header = True;
            break;
        row+=1;
        if row>=max_row: break;
    return values,row;

def get_file_title(xl_sht,max_row = 10000):
    """
    returns the first non-null row as the file title.
    this will be added only if there is a title bool set.
    \
    this does work as designed.
    """
    row,column,values = 1,0,None;
    while not values:
        for a in xl_sht[row]:
            values = a.value
            if values: break; # escape!
            column +=1;
        row +=1;
        if row >= max_row: break; # escape! (prevent infinite looping)
    return values,row;
        
def file_def_factory(xl_file):
    """
    load in an excel file, return a tuple of a freshly minted
    file_definition object, and an open descriptor to an XL file
    """
    xl_doc = xl_.load_workbook(xl_file);
    xl_sht = xl_doc.get_active_sheet();
    #fl_rep = flat_fields(xl_file); # complete this line.