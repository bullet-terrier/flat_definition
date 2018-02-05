# flat_definition
Python parser to load flat file definitions from arbitrary sources.
Currently, will read a Microsoft Excel File (thanks to OpenPyXl) and can 
seek out column headers, and attempt to identify a file header.

use xl2ff.py to create a tsv file from an excel spreadsheet-
use make_pretty.py to remove extraneous lines from the output.

these two modules will be the main utility necessary for these file operations.

============================================================================

The next step in the evolution of this process will be to include a CLI, and
GUI set, that will allow the data to be consistently extracted from an XL 
sheet into more "process-friendly" forms. Ideally this will emit one (or all)
of the following:
    SQL insert/update statments
    CSV/TSV files
    Column Delimited Flat files

Based on the contents of the XL spreadsheet- a slightly different direction
than was intended at the inception of the task, but it could be handy.



# flat2tsv.py
python functions to take an arbitrary set of indices, parse a file into columns,
then attempt to write those columns out as an easier to work with tsv file.

I'm going to need to set up some form of interface to allow updates to file definitions,
and I might even add in some form of cached data to keep track of how to index the files.

anything that cuts down on the number of read/writes to mutable files will help 
the overall project out.



============================================================================
Primary goal will be to extract definition data concerning fixed width files
that aren't delimited, in order to process them in a business sense.

Any contributions and suggestions would be more than appreciated.

Thanks,

Bullet-Terrier
