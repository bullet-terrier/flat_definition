# bullet-terrier
# Load Definitions from XL files.
#
#

# BELOW HERE WE WILL ASSIGN COLUMNS TO PARTICULAR FIELDS.

#row, then column index:

# this will only apply to one file - I'll set up a meta config
# to parse this information in other versions.
# file.values - that could work pretty well, if I want to load the entire structure into memory.

field_num = 0; # this is also another field that we don't necessarily need, but can make use of.
field_start = 1; # column containing field_start definitions.
field_end = 2; # field containing field_end definitions. (for the sake of my process we don't need this.)
data_start = 1; # as a general rule assume that the beginning of the data is at the beginning of the file.

import os;
import flat_field;

xl_ = None;
xl_success = False;
try:
    import openpyxl as xl_;
    xl_success = True;
except Exception as xl_fail:
    print(xl_fail)

def get_definitions(file_name,data_start = 1,field_file_name = None):
    """
    Run through, and generate a set of the field defintions.
    this will provide the basis for which I'll run the Translate/Load
    functions over the output data.
    \
    I'll allow the field_file_name to be None for now, since
    an identifier is not necessary for what I want to accomplish.
    """
    pass
    excel_document = openpyxl.load_workbook(file_name);# I *may* need to convert this to work with a fqfp
    excel_worksheet = excel_document.get_active_sheet();
    # tested through this point - not sure what needs to be pushed as configurations.
    