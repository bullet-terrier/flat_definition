"""
Definition for a field type in a flat file.
"""

class field_entry:
    """
    field in a fixed width file.
    entries will not be aware of files down the line
    primary use will be to divide files for use in other mechanisms.
    I'll begin using slots for more tightly wound classes that need to be used.
    make more use of user type definitions for involved coding projects.
    \
    I was thinking about adding in a dictionary - that would have been a bad idea,
    since it would have been just recreating the same memory hog that I'm trying to
    avoid.
    \
    I can use this to force better use of my classes (which i intend to do)
    DO NOT ASSIGN VALUES TO THE FIELD ENTRY CLASS - ONLY WORK WITH THE INSTANCES.
    """
    __slots__ = [
        "index",
        "position",
        "title",
        "end_position",
        "length",
        "type",
        "reference"
        ]
    def __init__(self,position,end_position=None,index=None,length=None,type=None,reference=None):
        #assert int == type(position);
        #assert type
        self.position = position;
        self.end_position = end_position;
        self.index = index;
        self.length = length;
        self.type = type; # will populate all of these if they are defined.
        self.reference = reference;
        # meta reference to slots:            
        return;
    
    def __del__(self):
        """
        intending to add some behavior to clean up the total set of objects
        this would allow the defitions to be more "fluid" when working across
        multiple revisions.
        """
        pass
    
    def update_from_field(self,f_entry):
        """
        Take a field_entry object as an input argument.
        take a field that was added later, and set the end position of

        looks like I'll need to decide how I want this mechanism to work...
        """
        if (self.index or 0 < f_entry.index or self.index) and (f_entry.position or 0)>(self.end_position or 0):
            self.end_position,updated = f_entry.position,True;
        # leaving this open to other expansions in the future.
        if updated: self.length = (self.end_position or self.position)-self.position;
        return;

class flat_fields:
    """
    representation of an entire file broken up into fields for
    parsing a flat file.
    """
    __slots__=[
        "file_name",
        "file_title",
        "fields",
        "line_length",
        "file_length",
        "file_hash",
        "file_metadata",
        "last_index",
        "max_index"
    ]
    def __init__(self,file_name,file_title):
        self.file_name = file_name;
        self.fields = [];
        self.line_length = None;
        self.file_length = None;
        self.file_hash = None;
        self.file_metadata = None;
        self.last_index = 0;
        self.max_index = 0;
    
    def __del__(self):
        pass

    def add_field(self,field_name,field_position,field_index = 0):
        self.fields.append(field_entry(field_position,None,field_index,None,field_name));# more stringent than the actual field.
                                       