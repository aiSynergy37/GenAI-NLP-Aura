text ="""
[SPAM] WIN $5000 NOW!!! Click here: fakeurl.biz
[HAM] Hey John, can we meet tomorrow at 3 PM?
[SPAM] Limited offer!!! BUY NOW!!!
random broken line
[HAM] Your invoice for order 39291 is ready.
"""

import re 
pattern = re.compile(r"!{2,}")
#pattern = re.compile(r"[A-Z]+[_]*[A-Z]+")
matches = re.finditer(pattern, text)
for match in matches:
    #print(match, end=' ')
    pass

###########################################################################
spam = []

with open('emails.txt', 'r') as file, open('spam_output.txt', 'w') as output_file:

    data = file.read()
    #print(data)
    for line in data.splitlines():
        pattern = re.compile(r"!{2,}")
        if pattern.search(line):
            output_file.write(line + "\n")
            


print("=============================================")