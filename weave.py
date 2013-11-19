import sys
import io
import re

class environment:
    def __init__(self, out):
        self.out = out
    def exe(self, code):
        self.out,sys.stdout = sys.stdout,self.out
        exec code
        self.out,sys.stdout = sys.stdout,self.out

def fix_indent(s):
    out = []
    global_indent = len(re.match("\s*", s).group(0))
    for line in s.split("\n"):
        out.append(line[global_indent:])
    return "\n".join(out)


i,o,enc,cwd = sys.argv[1:]
text = open(i).read()
out = open(o, 'w')
env = environment(out)
chunks = re.split('<%python(\[echo\])? *\n(.*?)%>', text, flags=re.DOTALL)

out.write(chunks[0])
for i in range(0, len(chunks)-1, 3):
    env.exe(fix_indent(chunks[i+2].strip("\n")))
    out.write(chunks[i+3])

