
"""
Mechanism to write XL files into Flat Files - Tab/Comma/Character delimited file.

Quick rundown of my algorithm - 
 
 open the file, get the maximum number of columns ( should by default come in the file definition.)'
 I'll then generate a tab delimited file (by default) which will be the source for the remaining information.
 
 my plan is to usurp my older utilities and build a framework that is more capable than just reading an Excel Spreadsheet.
"""
#XL2FF

import openpyxl as xl
import os;
import os.path as ps; # ps will be the path shell
import sqlite3 as sql; # I'm going to use a sql database to keep the most recent backup of the documents before depositing them on the filesystem.
from shutil import copy;


def load_file(filename):
    """
    will treat anything that doesn't have an xlsx or txt extension as 
    non-existent, to prevent errors...
    returns an open file descriptor to the object.
    """
    name = os.path.split(filename)[1]; # should return everything after the last slash
    type_ = "";
    if filename.split(".")[-1] not in ["xlsx","txt"]:
        raise Exception("Attempted to load a file with the incorrect typing...");
    if ".xlsx" in filename:
        name = xl.load_workbook(filename);
        type_ = 'xlsx'
    elif ".txt" in filename:
        with open(filename,'r') as data:
            name = data.read();
            type_ = "txt"
    return name # return either the file contents (if a csv) or the file workbook (if excel.)
    
def parse_data(workbook):
    """
    works on getting the contents of a workbook, returning it as a set of rows.(or columns)
    that kind of configuration is going to have to happen after the fact.
    
    this will rely on the implementation to make sure that good data is passed.
    will break if bad data is passed in.
    """
    xl_sht = workbook.get_active_sheet();
    data = []
    for a in xl_sht:
        row = "";
        for b in a:
            if b.value is None: row+="\t"
            else: row+=str(b.value);
            row += "\t";# I'll just live with the trailing tab        
        data.append(row);
        print(row)
    return data;
    
def make_flat(directory):
    """
    take an entire directory and convert all excel spreadsheets into a .tsv file with a similar name.
    """
    dir = []
    for a in os.listdir(directory):
        if ".xlsx" in a: dir.append(a)
    for a in dir:
        tmp = ps.split(a); # get the last bit of the file
        out = tmp[1].split('.')[0]+".txt"
        fle = load_file(a);
        data = parse_data(fle);
        with open(tmp[0]+out,'w') as dat:
            for b in data:
                dat.write(b); # should get each new row.
                dat.write('\n'); # append a newline to make it pretty.
        print("Completed iteration for %s."%(a))
    print("Completed task for directory %s."%(directory))
    return;
        


if __name__!="__main__":
    print("You've imported xl2ff.py")