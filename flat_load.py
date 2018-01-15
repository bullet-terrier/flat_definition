# Fixed position slice parser;
#
# I'll have to set up a conversion (later) for zero to one based indices.
# need to get the starting slices -
#
#
#

import os;
import sys;
import time; 
# not sure what else I'll want...
# I *could* dump pywin32 if win32api is defined.


# UGLY PARSER HERE I COMETH

Zed = None; # this is gonna stay None unless 


class field_entry:
    """
    field in a fixed width file.
    
    """
    position = None;
    index = None;
    length = None;
    value = None;
    type = None;


def load_data(file_path):
    """
    take the file path then split it up to look for 
    """