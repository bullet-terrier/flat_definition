#!./Python/python.exe
"""
make_pretty.py

Take a 'human readable' mess and make it into something
easier to tackle programmatically, strip line padding if
working with a delimited file, otherwise we'll see what 
it comes back with.

input will (generally) be a string., ideally launching
from a file, and landing with a file. will prepend "pretty"
to the filename.

I'm running through some troubleshooting to make better use of the
utility.
"""

import os;
import os.path;
import sys;
import string;
import shutil; # might add functionality to archive the old files.

pattern = None;

def make_pretty(filename, new_name = "pretty_"):
        """
        general form of the make_pretty function. doesn't need to be executed from
        within the class.
        """
        filename = os.path.realpath(filename);
        pretty_data = "";
        try:
            with open(filename,"r") as delt:
                for a in delt.readlines():
                    ctr=0;
                    for b in a:
                        if b not in string.whitespace:
                            ctr =1;
                            break; # escape the inner loop, save clock time.
                    if ctr>0:
                        pretty_data+=a; # I could break it at the first non- whitespace character
                        continue;  # escape the inner loop
            filename_2 = prepend_filename(filename,new_name);
            with open(filename_2,'w') as fi:
                fi.write(pretty_data)
        except Exception as ex:
            input("%s\nDo you understand? "%(str(ex)));
        print("completed operation on: %s"%(filename))
        return;
    

def prepend_filename(filename, prepend_data=""):
    """
    Python function to prepend data to a file – you could try any arbitrary data that
    Can be represented as a string (if you’re feeling ambitious/bored, look up datetime module)
    """
    filename_ = os.path.realpath(filename)
    path__,filename__ = os.path.split(filename_)
    filename__ = "%s%s"%(prepend_data,filename__)
    return "%s%s%s"%(path__,os.sep,filename__)# littered with typos


class ugly_file:
    """
    *** DON'T USE ME - INCOMPLETE ***
    ugly_files are the type of input we're expecting.
    attributes will be "ugly","pretty","stripped"
    might eventually add extensions for encryption.
    
    Encoding might not matter at this point, I'll leave it in for now.
    """
    __slots__ = [
    'encoding',   # choose an encoding (default will be ascii)
    'ugly',       # representation of the initial file state
    'pretty',     # representation of the cleaned file state
    'stripped',   # representation of the stripped down (sans whitespace) file
    'path',       # representation of the file path (ideally full-path)
    'name'        # filename (part 2 of os.path.split(filename))
    ]
    def __init__(self, filename = None, path = None, encoding = None):
        """
        this will work by passing a relative path in to filename - I'll need
        to handle the case where it is only a relpath.
        """
        self.encoding = encoding or 'ascii'
        self.name = os.path.basename(filename); # immediately assume that this will be none
        # I'll simply add a mechanism to generate the fullpath from the filename - 
        # if it doesn't exist, we might run into an error...
        #if os.path.isabs(filename): self.path = os.path.split(filename)[0];
        try:
            self.path = os.path.realpath(filename)
            self.filename = os.path.realpath(filename)
        except Exception as Echo:
            print(Echo); # that should handle things for the most part.
            self.path = None;

    def filename_prepend(self, prepend_data="",filename = None):
        """
        prepend 'prepend_data' to 'filename'
        will default to the filename supplied with the file.
        """
        pass;
        # this will need to split the filename and then write the prepended data
        filename_ = os.path.realpath(filename)
        path__, filename__ = os.path.split(filename)
        filename__ = "%s%s"%(prepend_data,filename__);
        return "%s%s%s"%(path__,os.sep,filename__)
        
    def make_pretty(self,filename = None):
        """
        function will work by passing in a path, then removing extraneous characters and lines.
        will remove each line that is only Null or whitespace.
        """
        filename = filename or self.name; # allow the input to override the instance variable
        pretty_data = "";
        try:
            with open(filename,"r") as delt:
                for a in delt.readlines():
                    ctr=0;
                    for b in a:
                        if b not in string.whitespace:
                            ctr =1;
                            break; # escape the inner loop, save clock time.
                    if ctr>0:
                        pretty_data+=a; # I could break it at the first non- whitespace character
                        continue;  # escape the inner loop
            filename = os.path.realpath(filename)
            path = os.path.split(filename)[0]
            filename_2 = os.path.split(filename)[-1]
            filename_2 = "pretty_%s"%(filename_2)
            filename_2 = path+os.sep+filename_2;
            with open(filename_2,'w') as fi:
                fi.write(pretty_data)
        except Exception as ex:
            input("%s\nDo you understand? "%(str(ex)));

def pretty_path(path,pattern=None):
    targs = []
    for a in os.listdir(path):
        if pattern:
            if pattern in a: targs.append(a);
        else: targs.append(a)
    for a in targs:
        print(a)
        make_pretty(a)
    return;
            
def argv_():
    for a in sys.argv[1:]:
        if "=" in a: pattern = a.split("=")[-1] # get the pattern
        if os.path.isdir(a): 
            if pattern: pretty_path(a,pattern);
            else: pretty_path(a);
        elif os.path.isfile(a): make_pretty(a);
        else: print("Not sure what to do with '%s'"%(a))
        
def interact_(val,pat = None):
    rt_ = None;
    if os.path.isdir(val): 
        if pat:
            pretty_path(val,pat)
        else:
            pretty_path(val);
        rt_ = True;
    elif os.path.isfile(val): 
        make_pretty(val);
        rt_ = True;
    elif "=" in val:
        pattern = val.split("=")[-1]
        rt_ = True; # return for input.
    else: 
        print("Not sure what to do with '%s'"%(val))
        rt_ = False;
    return rt_;


def main_():
    """
    main loop - iterate through a set of files and make them pretty if they match a pattern.
    """
    pattern = "txt"; # by default i'm going to let it look for patterns with text.
    pass
    if len(sys.argv)>1: # handle the cmdline args
        pass
    else:
        print("Ctrl+c to quit (or pass a non-file/non-directory item)")
        print("Enter a pattern to match as pattern='val' will look for pattern in filename.")
        fn = input("Enter a path to make pretty(directory will run against everything): ")
        while fn:
            if type(fn) != str: 
                fn = input("Enter a path to make pretty(directory will run against everything): ")            
            try:                
                if not (os.path.isfile(fn) or os.path.isdir(fn)) and "=" in fn:
                    pattern = fn.split("=")[-1];
                    fn = True;
                    continue;
                if pattern: fn = interact_(fn,pattern)
                else: fn = interact_(fn)
            except Exception as e:
                print(e);
                fn = False;            
                
if __name__=="__main__": main_();
else: print("imported make_pretty.py");