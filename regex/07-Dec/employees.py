"""
EXERCISE 1 — Email Extraction + Domain Analytics

File: employees.txt

Sample:

John Doe <john.doe@company.com>
Mike Rogers <mike.r@outlook.com>
Sarah Adams <sadams@company.com>
random text here
JANE_SMITH— jane.smith@gmail.
_Jane

✔️ Tasks

Use regex to extract all valid emails

Extract username + domain

Count:

how many @gmail.com, @company.com, etc.

most common username length

Write output files:

emails.csv → username, domain

email_summary.txt

"""
text = '''
John Doe <john.doe@company.com>
Mike Rogers <mike.r@outlook.com>
Sarah Adams <sadams@company.com>
random text here
JANE_SMITH— jane.smith@gmail.
'''

##########################################################################
import re 
pattern = re.compile(r"[A-Z]+[_]*[A-Za-z]*(\s[A-Z][a-z])*")
#pattern = re.compile(r"[A-Z]+[_]*[A-Z]+")
matches = re.finditer(pattern, text)
for match in matches:
    #print(match, end=' ')
    pass

###########################################################################
names = []

with open('employees.txt', 'r') as file, open('output.txt', 'w') as output_file:

    data = file.read()
    #print(data)
    pattern1 = re.compile(r"[A-Z]+[_]*[A-Za-z]*\s[A-Z][a-z]*")
    pattern2 = re.compile(r"[a-z]+[._]?[a-z]*@[a-z]+\.[a-z]{2,3}")
    pattern3 = re.compile("r@[a-z]+\.[a-z]{2,3}")
    matches1 = re.finditer(pattern1, data)
    matches2 = re.finditer(pattern2, data)
    matches3 = re.finditer(pattern3, data)
    for match in matches1:
        print(match, end=' ')
        names.append(match.group())
        output_file.write(match.group() + '\n')
    for match in matches2:
        print(match, end=' ')
        names.append(match.group())
        output_file.write(match.group() + '\n')
    for match in matches3:
        print(match, end=' ')
        names.append(match.group())
        output_file.write(match.group() + '\n')

print("====================================")
print(names)