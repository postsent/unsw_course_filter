import re

s = 'asdf=5;iwantthis123jasd'
sub1 = "asdf=5;"
sub2 = "123jasd"
result = re.search(f"{sub1}(.*){sub2}", s)
print(result.group(1))