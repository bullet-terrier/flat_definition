#
"""
flat2tsv.py

mechanism to split a flat file into a tsv of the same name based on an index.

might want to borrow the prepend functionality (see 
May also just change the extensions to make it easier.
"""

import os;
from os import path as p; # use this to simplify coding.

###   configuration   ###

# this will account for a system that is emitting slices as a one_based index
# that means that to handle a one based index - we need to add -1 to all indexes
# in the start_list. for consistencies sake - we'll simply add the value in functions,
#
offset = 0; # zero based index - no offset.
minimum = 0;
# offset = -1; # one based index - offset by -1 to a zero based index.

### end configuration ###


###    FUNCTION DEFINITIONS    ###

def process_indices(start_list, offset_ = None):
    """
    handle the index offset and return it as a list.
    if it's a known quantity, then we'll just approach it
    as such.
    
    offset will be added so if it is a one based index - we'll
    need to invert it.
    """
    pass;
    offset_ = offset_ or offset;
    if type(start_list) != list: raise TypeError("start_list must be a list object");
    if type(offset_) not in [float,int]: raise TypeError("offset must be a numeric object");
    new_list = []
    for a in start_list:
        # should give a thorough bit of output.
        if type(a) not in [float,int]: raise TypeError("start_list must contain only numeric types!\nerror at index: %s.\nvalue: %s"%(start_list.index(a),a)); 
        if a < minimum: a = minimum; # this will prevent index values out of bound (though might not be an issue, I'll give it a go.)
        new_list.append(a+offset_);
        
    return new_list;
    
def read_from_indices(string_val, start_list):
    """
    read through the string - 
    will break each object down based on the start index.
    """
    mx = len(string_val); # should get the last index;
    last_dex = 0;
    slices = [];
    for a in range(0,len(string_val)):
        if a > 0:
            if a in start_list: 
                slices.append(string_val[last_dex:a])
                last_dex = a;
            if a == mx-1:
                slices.append(string_val[last_dex:mx])
                last_dex = mx;
                break; # should be unecessary, as it should exit from here anyway.
    return slices; # these will be the values.


    
def main_():
    """
    will convert a flat file to a tsv based on the definition document.
    """
    pass
###  END FUNCTION DEFINITIONS  ###




### OBJECT DEFINITIONS (INCOMPLETE) ###
class flat:
    """
    object representing a flat file.
    """
    pass
    __slots__ = [
        "update_on_function",
        "contents",
        "rows",
        "length",
        "indices", # this should be the position within each row where each column would start.
        "column_names",
        "row_length", # row length will be a fixed value - otherwise we'd end up with inconsistent data.
        "indeces_with_offset",
        "index_offset",# this should inherit from the configurable offset, unless it is overridden.
        "name",
        "path",
        "extension",
        "load_file"        
    ]    
    def read_from_indices(string_val, start_list):
        """
        read through the string - 
        will break each object down based on the start index.
        """
        mx = len(string_val); # should get the last index;
        last_dex = 0;
        slices = [];
        for a in range(0,len(string_val)):
            if a > 0:
                if a in start_list: 
                    slices.append(string_val[last_dex:a])
                    last_dex = a;
                if a == mx-1:
                    slices.append(string_val[last_dex:mx])
                    last_dex = mx;
                    break; # should be unecessary, as it should exit from here anyway.
        return slices; # these will be the values.                
        
    def __init__(self, file_path, indices =[], offset_ = None, update_on_function = None):
        """
        offering capacity to update self when a function is called that could calculate
        new values for the object attributes. This could lead to unpredictable behaviour
        in some constructs, so I'm disabling it by default, but it's there if you're intrigued.
        """
        pass;
        if p.isabs(file_path): self.path = file_path;
        elif p.isdir(file_path): self.path = file_path;
        elif p.isfile(file_path): self.path = file_path;
        else: raise TypeError("file_path must be a pathname")
        self.name = p.basename(file_path);
        self.indices = indices;
        self.index_offset = offset_ or offset; 
        self.load_file = False;
        self.update_on_function = update_on_function or False;
        
    def _process_offset_(self, indices = None, offset_ = None ):
        """
        establish the index_offset.
        (offers one more chance for override.);
        """
        pass
        offset_ = offset_ or self.index_offset;
        if type(offset_) not in [float, int, double]: raise TypeError("offset_ must be a numeric type!")
        indices = indices or self.indices; 
        if type(indices) not in [list,tuple,string]: raise TypeError("indices must be an iterable type!");
        if self.indices in (None,[]): self.indices = indices; # if undefined - update to establish a default.
        _indices_=  [];
        for a in indices:
            _indices_.append(a+offset_)
        if self.update_on_function:
            self.index_offset = offset_;
            self.indices = indices;
            self.indices_with_offset = _indices_;
        return _indices_;
    
    def _convert_(self):
        """
        function to return a tsv object based on the defintion of the flat file.
        """       
        pass
    
class tsv:
    """
    object representing a tsv file.
    Convert won't be available for this one immediately - as it'll need to be 
    written in a way to find the maximum length item in each row.
    """
    pass
    __slots__ = [
        "contents",
        "rows",
        "has_headers",
        "header_names",
        "columns",
        "name",
        "path",
        "extension"
    ]
    
    def load_contents(path):
        pass;
    
    def __init__(self):
        pass;
        
### OBJECT DEFINITIONS (INCOMPLETE) ###
