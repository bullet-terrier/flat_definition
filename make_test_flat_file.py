#
"""

make a test flat file - this will take in a list of tuples, and generate a 
file based on the contents.
[
1) start position (0 based)
2) char
]
,
record length = 255. (default length will be 255)
"""

def make_flat_file(definition, length = 255):
    """
    build an arbitrary flat file row for testing.
    this will simply be used to make sure that columns are lining up and 
    meeting the specifications that were given.
    """
    fields = []
    for i in range(0,length): fields.append(0);
    values = "";
    for a in definition:
        try:
            if definition.index(a)<len(a)-1:
                for b in range(a[0],defintion.index(a)+1[0]):fields[b] = a[1];
            else:
                for b in range(a[0],length): fields[b] = a[1];
        except Exception as e:
            e;
            continue;
        print(fields)
    for a in fields: values += str(a);
    return values;