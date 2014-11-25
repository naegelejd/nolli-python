import sys
import parse
import graph

class Nolli(object):
    def __init__(self):
        pass

    def compile(self, stream):
        p = parse.Parser(self, stream)
        root = p.parse()
        with open('astdump.dot', 'w') as f:
            graph.graph_AST(root, f)

def main():
    if len(sys.argv) < 2:
        print("Missing filename")
        sys.exit(1)

    stream = ""
    with open(sys.argv[1]) as f:
        stream = f.read()

    ctx = Nolli()
    ctx.compile(stream)

if __name__ == "__main__":
    main()
