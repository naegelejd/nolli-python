DECL_VAR = 0
DECL_CONST = 1

def make_node(tp, line, col, *args):
    n = tp(*args)
    n.line = line
    n.col = col
    return n

class Node(object):
    line = 1
    col = 1

class __Literal(Node):
    def __init__(self, val):
        self.val = val

class BoolLit(__Literal):
    pass
class CharLit(__Literal):
    pass
class IntLit(__Literal):
    pass
class RealLit(__Literal):
    pass
class StringLit(__Literal):
    pass
class ListLit(__Literal):
    pass
class MapLit(__Literal):
    pass

class ClassLit(Node):
    def __init__(self, tp, tmpl, items):
        self.tp = tp
        self.tmpl = tmpl
        self.items = items

class Ident(Node):
    def __init__(self, val):
        self.val = val

class UnaryExpr(Node):
    def __init__(self, right, op):
        self.right = right
        self.op = op

class BinaryExpr(Node):
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

class __Call(Node):
    def __init__(self, func, args):
        self.func = func
        self.args = args

class Call(__Call):
    pass

class KeyVal(Node):
    def __init__(self, key, val):
        self.key = key
        self.val = val

class Lookup(Node):
    def __init__(self, container, index):
        self.container = container
        self.index = index

class Selector(Node):
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

class PackageRef(Node):
    def __init__(self, pkg, name):
        self.pkg = pkg
        self.name = name

class Function(Node):
    def __init__(self, name, tp, body):
        self.name = name
        self.tp = tp
        self.body = body

class TmplType(Node):
    def __init__(self, name, tmpls):
        self.name = name
        self.tmpls = tmpls

class QualType(Node):
    def __init__(self, pkg, name):
        self.pkg = pkg
        self.name = name

class FuncType(Node):
    def __init__(self, tmpl, ret_type, params):
        self.tmpl = tmpl
        self.ret_type = ret_type
        self.params = params

class Decl(Node):
    def __init__(self, kind, tp, rhs):
        self.kind = kind
        self.tp = tp
        self.rhs = rhs

class Init(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Bind(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Assign(Node):
    def __init__(self, lhs, expr, op):
        self.lhs = lhs
        self.expr = expr
        self.op = op

class IfElse(Node):
    def __init__(self, cond, if_body, else_body):
        self.cond = cond
        self.if_body = if_body
        self.else_body = else_body

class While(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class For(Node):
    def __init__(self, var, rnge, body):
        self.var = var
        self.rnge = rnge
        self.body = body

class CallStmt(__Call):
    pass

class Return(Node):
    def __init__(self, expr):
        self.expr = expr

class Break(Node):
    pass
class Continue(Node):
    pass

class Alias(Node):
    def __init__(self, tp, name):
        self.tp = tp
        self.name = name

class Using(Node):
    def __init__(self, names):
        self.names = names

class Class(Node):
    def __init__(self, name, tmpl, members, methods):
        self.name = name
        self.tmpl = tmpl
        self.members = members
        self.methods = methods

class Interface(Node):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

class Package(Node):
    def __init__(self, name, glbls):
        self.name = name
        self.glbls = glbls

class Unit(Node):
    def __init__(self, pkgs):
        self.pkgs = pkgs
