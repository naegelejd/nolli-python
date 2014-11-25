from __future__ import print_function
import sys

import AST

outfile = sys.stdout

def emit(msg):
    print(msg, file=outfile)

def graph_AST(root, fout=sys.stdout):
    global outfile
    outfile = fout
    emit('digraph hierarchy {\nnode [color=Green,fontcolor=Blue]')
    graph(root, 0)
    emit('}')

def graph(node, ID):
    graphers = {
        list: graph_list,
        AST.BoolLit: graph_BoolLit,
        AST.CharLit: graph_CharLit,
        AST.IntLit: graph_IntLit,
        AST.RealLit: graph_RealLit,
        AST.StringLit: graph_StringLit,
        AST.ListLit: graph_ListLit,
        AST.MapLit: graph_MapLit,
        AST.ClassLit: graph_ClassLit,
        AST.Ident: graph_Ident,
        AST.UnaryExpr: graph_UnaryExpr,
        AST.BinaryExpr: graph_BinaryExpr,
        AST.Call: graph_Call,
        AST.KeyVal: graph_KeyVal,
        AST.Lookup: graph_Lookup,
        AST.Selector: graph_Selector,
        AST.PackageRef: graph_PackageRef,
        AST.Function: graph_Function,
        AST.TmplType: graph_TmplType,
        AST.QualType: graph_QualType,
        AST.FuncType: graph_FuncType,
        AST.Decl: graph_Decl,
        AST.Init: graph_Init,
        AST.Bind: graph_Bind,
        AST.Assign: graph_Assign,
        AST.IfElse: graph_IfElse,
        AST.While: graph_While,
        AST.For: graph_For,
        AST.CallStmt: graph_CallStmt,
        AST.Return: graph_Return,
        AST.Break: graph_Break,
        AST.Continue: graph_Continue,
        AST.Alias: graph_Alias,
        AST.Using: graph_Using,
        AST.Class: graph_Class,
        AST.Interface: graph_Interface,
        AST.Package: graph_Package,
        AST.Unit: graph_Unit,
    }

    grapher = graphers[type(node)]
    return grapher(node, ID)

def graph_list(node, ID):
    rID = ID
    add_label(node, rID)
    for elem in node:
        ID = add_relation(elem, rID, ID)
    return ID

def graph_literal(node, ID):
    emit('%d [label="%s: %s"]' % (ID, type(node), node.val))
    return ID

def graph_BoolLit(node, ID):
    return graph_literal(node, ID)

def graph_CharLit(node, ID):
    return graph_literal(node, ID)

def graph_IntLit(node, ID):
    return graph_literal(node, ID)

def graph_RealLit(node, ID):
    return graph_literal(node, ID)

def graph_StringLit(node, ID):
    return graph_literal(node, ID)

def graph_Ident(node, ID):
    return graph_literal(node, ID)

def graph_ListLit(node, ID):
    return graph_literal(node, ID)

def graph_MapLit(node, ID):
    return graph_literal(node, ID)

def graph_ClassLit(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.tp, rID, ID)
    if node.tmpls:
        ID = add_relation(node.tmpls, rID, ID)
    return add_relation(node.items, rID, ID)

def graph_UnaryExpr(node, ID):
    rID = ID
    add_label(node, rID)
    return add_relation(node.expr, rID, ID)

def graph_BinaryExpr(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.lhs, rID, ID)
    return add_relation(node.rhs, rID, ID)

def graph_Call(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.func, rID, ID)
    return add_relation(node.args, rID, ID)

def graph_KeyVal(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.key, rID, ID)
    return add_relation(node.val, rID, ID)

def graph_Lookup(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.container, rID, ID)
    return add_relation(node.index, rID, ID)

def graph_Selector(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.parent, rID, ID)
    return add_relation(node.child, rID, ID)

def graph_PackageRef(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.pkg, rID, ID)
    return add_relation(node.name, rID, ID)

def graph_Function(node, ID):
    rID = ID
    add_label(node, rID)
    if node.name:
        ID = add_relation(node.name, rID, ID)
    ID = add_relation(node.tp, rID, ID)
    return add_relation(node.body, rID, ID)

def graph_TmplType(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.name, rID, ID)
    return add_relation(node.tmpls, rID, ID)

def graph_QualType(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.pkg, rID, ID)
    return add_relation(node.name, rID, ID)

def graph_FuncType(node, ID):
    rID = ID
    add_label(node, rID)
    if node.tmpl:
        ID = add_relation(node.tmpl, rID, ID)
    if node.ret_type:
        ID = add_relation(node.ret_type, rID, ID)
    if node.params:
        ID = add_relation(node.params, rID, ID)
    return ID

def graph_Decl(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.tp, rID, ID)
    # if node.rhs:
    ID = add_relation(node.rhs, rID, ID)
    return ID

def graph_Init(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.name, rID, ID)
    return add_relation(node.expr, rID, ID)

def graph_Bind(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.name, rID, ID)
    return add_relation(node.expr, rID, ID)

def graph_Assign(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.lhs, rID, ID)
    return add_relation(node.expr, rID, ID)

def graph_IfElse(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.cond, rID, ID)
    ID = add_relation(node.if_body, rID, ID)
    if node.else_body:
        ID = add_relation(node.else_body, rID, ID)
    return ID

def graph_While(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.cond, rID, ID)
    return add_relation(node.body, rID, ID)

def graph_For(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.var, rID, ID)
    ID = add_relation(node.rnge, rID, ID)
    return add_relation(node.body, rID, ID)

def graph_CallStmt(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.func, rID, ID)
    return add_relation(node.args, rID, ID)

def graph_Return(node, ID):
    rID = ID
    add_label(node, rID)
    if node.expr:
        ID = add_relation(node.expr, rID, ID)
    return ID

def graph_Break(node, ID):
    add_label(node, ID)
    return ID

def graph_Continue(node, ID):
    add_label(node, ID)
    return ID

def graph_Alias(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.tp, rID, ID)
    return add_relation(node.name, rID, ID)

def graph_Using(node, ID):
    rID = ID
    add_label(node, ID)
    return add_relation(node.names, rID, ID)

def graph_Class(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.name, ID)
    if node.tmpls:
        ID = add_relation(node.tmpls, ID)
    ID = add_relation(node.members, ID)
    return add_relation(node.methods, ID)

def graph_Interface(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.name, ID)
    return add_relation(node.methods, ID)

def graph_Package(node, ID):
    rID = ID
    add_label(node, rID)
    ID = add_relation(node.name, rID, ID)
    return add_relation(node.glbls, rID, ID)

def graph_Unit(node, ID):
    rID = ID
    add_label(node, rID)
    return add_relation(node.pkgs, rID, ID)

def add_label(node, ID):
    emit('%d [label="%s"]' % (ID, node.__class__))

def add_relation(child, parID, curID):
    curID += 1
    emit('%d -> %d' % (parID, curID))
    return graph(child, curID)
