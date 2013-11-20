import sys
import re
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import LatexFormatter

lex = PythonLexer()
formatter = LatexFormatter()

class environment:
    def __init__(self, out, filename):
        self.out = out
        self.filename = filename
        self.globals = {}
    def exe(self, code):
        self.out,sys.stdout = sys.stdout,self.out
        exec(code, self.globals)
        self.out,sys.stdout = sys.stdout,self.out

# Allow an arbitrary "global" indentation per chunk.
def fix_indent(s):
    out = []
    global_indent = len(re.match("\s*", s).group(0))
    for line in s.split("\n"):
        out.append(line[global_indent:])
    return "\n".join(out)

i,o,enc,cwd = sys.argv[1:]
text = open(i).read()
open('/home/christoph/pylog.txt', 'w').write(text)
out = open(o, 'w')
env = environment(out, i)
chunks = re.split('\n<<>>\n(@echo\n)?(.*?)\n@\n', text, flags=re.DOTALL)

out.write(chunks[0])
for i in range(2, len(chunks)-1, 3):
    if chunks[i-1]:
        out.write('\n' + highlight(chunks[i], lex, formatter) + '\n')
    env.exe(fix_indent(chunks[i].strip("\n")))
    out.write(chunks[i+1])
