#
"""
flat2tsv.py

mechanism to split a flat file into a tsv of the same name based on an index.

might want to borrow the prepend functionality (see 
May also just change the extensions to make it easier.

initialize a sqlite database to keep track of flat file definitions.
should allow something to update the record defintions, but I'm not that concerned right now.

might take it out to the level where each field will get its own row.

update - I'm going to ship this tool with a database - I'm going to try to update the information with
some scripts. this means *most* of the db data in this file will be deprecated.
"""

import os;
from os import path as p; # use this to simplify coding.
import sqlite3;

###   configuration   ###

# this will account for a system that is emitting slices as a one_based index
# that means that to handle a one based index - we need to add -1 to all indexes
# in the start_list. for consistencies sake - we'll simply add the value in functions,
#
offset = 0; # zero based index - no offset.
minimum = 0;
connection = "./flat_definitions.db"
# offset = -1; # one based index - offset by -1 to a zero based index.

### end configuration ###


###    FUNCTION DEFINITIONS    ###

def initialize_db():
    """
    initialize the table within this database that will contain 
    the flat file definition information.
    """
    zed = sqlite3.connect(connection);
    try:
        zed.execute("CREATE TABLE record_definitions(record_id int, record_name varchar(30), record_indices varchar(500))")
        zed.commit()
    except sqlite3.OperationalError as OE:
        print(OE);
        print("Looks like the table already exists...");
    finally:
        zed.commit()

def get_max_index(connection):
    curs = connection.cursor();
    result = curs.execute("SELECT MAX(record_id) from record_definitions")
    rex = result.fetch()
    #for a in  result:
    #   rex = a[0]; # should ony be one value:
    #   print(rex)
    if rex is None: rex = 0
    return int(rex); # I'll add one for every time I insert a new record.
        
# going to store the definition as a list object - maybe tab delimited.
def store_definition(connection, record_name,record_indices):
    curs = connection.cursor()
    ind = get_max_index(connection)+1;
    curs.execute("INSERT INTO record_definitions(record_id, record_name,record_indices) VALUES (CAST('%s' as INT), '%s', '[%s]')"%(
        ind,
        record_name,
        record_indices
    ))
    connection.commit()
    return ind,record_name; # return the id and the name in case something else is keying off of them.
    
def update_definition(connection, record_id, record_indices):
    curs = connection.cursor();
    ind = record_id
    try:
        curs.execute("UPDATE record_definitions SET record_indices = %s WHERE record_id = %s"%(record_indices, record_id));
    except Exception as E:
        print(E)
        raise Exception(E);
    return;
    
    
def load_definition(connection, record_name = None, record_id = None):
    """
    load definitions matching the connection.
    if record_name is wildcard and record_id is None, return all.
    """
    curs= connection.cursor(); # I'm not handling any exceptions - let them run up the tree.
    const = "";
    if record_name:
        const = curs.execute("SELECT * FROM record_definitions WHERE record_name LIKE '%s' "%(record_name))
    elif record_id:
        const = curs.execute("SELECT * FROM record_definitions WHERE record_id LIKE '%s'"%(record_id))
    else:
        const = curs.execute("SELECT * FROM record_definitions")
    return const; # simply return a rowset - this will be the easiest way to be resultant. - can use fetch to dump the values.
    

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

def load_source(source_document):
    source_to_parse = "";
    with open(source_document,'r') as src:
        y = 0;
        x = 0;
        for a in src.readlines():
            y+=1;
            for b in a.split('\t'): x+=1;
            source_to_parse+=a;
    return a,y,x;
        
    
def main_():
    """
    will convert a flat file to a tsv based on the definition document.
    """
    source_document = input("Please enter a definition document to parse: ") # I'll have this set up to read in something akin to the "Pretty" documents.
    dox= load_source(source_document);
    get_start_dex = input("please enter the column where the start position will be found: ")
    get_position_offset = input("is this a one based index? (y/n) ")
    one_based = False;
    if get_position_offset.lower() in ['y','yes']: one_based = True;
    if one_based: offset = -1;
    # need to set up some mechanism for classifying the information - I'll have to figure that one out...
    # I can use segment numbers in this particular instance.
    identifier = input("Please enter some form of identification for this object: " );
    
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
