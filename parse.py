import sys
import lexer
import AST
from util import error, debug

class Parser(object):
    def __init__(self, ctx, stream):
        self.ctx = ctx
        self.lexer = lexer.Lexer(ctx, stream)
        self.tok = lexer.TOK_EOF
        self.prev = lexer.TOK_EOF
        self.buff = ""

    def getnext(self):
        self.buff = self.lexer.buff
        self.tok = self.lexer.gettok()

    def check(self, expected_tok):
        if self.tok == expected_tok:
            return True
        return False

    def accept(self, expected_tok):
        valid = self.check(expected_tok)
        if valid:
            self.getnext()
        return valid

    def expect(self, expected_tok):
        if self.accept(expected_tok):
            return True
        else:
            error("Unexpected token %s, expecting %s at line %d" %
                    (lexer._tokens[self.tok],
                        lexer._tokens[expected_tok],
                        self.lexer.line))
            sys.exit(1)

    def parse(self):
        self.getnext()
        root = self.parse_unit()
        return root

    def parse_unit(self):
        tops = []
        pkgs = []
        while not self.check(lexer.TOK_EOF):
            if self.check(lexer.TOK_PACKAGE):
                pkg = self.parse_package()
                pkgs.append(pkg)
            else:
                g = self.parse_package_statement()
                tops.append(g)
        # TODO: add tops to global package
        return AST.Unit(pkgs)

    def parse_package(self):
        self.expect(lexer.TOK_PACKAGE)
        name = self.parse_ident()
        stmts = []
        self.expect(lexer.TOK_LCURLY)
        while not self.check(lexer.TOK_RCURLY):
            stmt = self.parse_package_statement()
            self.expect(lexer.TOK_SEMI)
            stmts.append(stmt)
        self.expect(lexer.TOK_RCURLY)
        self.expect(lexer.TOK_SEMI)
        return AST.Package(name, stmts)

    def parse_package_statement(self):
        stmt = None
        if self.check(lexer.TOK_VAR):
            stmt = self.parse_var_decl()
        elif self.check(lexer.TOK_CONST):
            stmt = self.parse_const_decl()
        elif self.check(lexer.TOK_CLASS):
            stmt = self.parse_classdef()
        elif self.check(lexer.TOK_IFACE):
            stmt = self.parse_interface()
        elif self.check(lexer.TOK_FUNC):
            stmt = self.parse_function()
        elif self.check(lexer.TOK_ALIAS):
            stmt = self.parse_alias()
        else:
            error("Error! not a package-level construct")
        return stmt

    def parse_statement(self):
        stmt = None
        if self.check(lexer.TOK_FUNC):
            stmt = self.parse_function()
        if self.check(lexer.TOK_VAR):
            stmt = self.parse_var_decl()
        elif self.check(lexer.TOK_CONST):
            stmt = self.parse_const_decl()
        elif self.check(lexer.TOK_IF):
            stmt = self.parse_if_else()
        elif self.check(lexer.TOK_WHILE):
            stmt = self.parse_while()
        elif self.check(lexer.TOK_FOR):
            stmt = self.parse_for()
        elif self.accept(lexer.TOK_CONTINUE):
            return AST.Continue()
        elif self.accept(lexer.TOK_BREAK):
            return AST.Break()
        elif self.accept(lexer.TOK_RETURN):
            expr = None
            if not self.check(lexer.TOK_SEMI):
                expr = self.parse_expression()
            return AST.Return(expr)
        else:
            error("Error! not a statement")
        return stmt

    def parse_classdef(self):
        self.expect(lexer.TOK_CLASS)
        name = self.parse_ident()
        self.expect(lexer.TOK_LCURLY)

        members = []
        methods = []
        while not self.check(lexer.TOK_RCURLY):
            tp = self.parse_type()
            name = self.parse_ident()
            if self.check(lexer.TOK_LCURLY):
                # parsing method definition
                body = self.parse_block()
                meth = AST.Function(name, tp, body)
                methods.append(meth)
                debug("parsed class method")
            else:
                names = [name]
                while self.accept(lexer.TOK_COMMA):
                    name = self.parse_ident()
                    names.append(name)
                member = AST.Decl(AST.DECL_VAR, tp, names)
                members.append(member)
                debug("parsed line of class members")
            self.expect(lexer.TOK_SEMI)
        self.expect(lexer.TOK_RCURLY)
        return AST.Class(name, None, members, methods)

    def parse_interface(self):
        self.expect(lexer.TOK_IFACE)
        name = self.parse_ident()
        self.expect(lexer.TOK_LCURLY)
        methdecls = []
        while not self.check(lexer.TOK_RCURLY):
            ft = self.parse_functype()
            name = self.parse_ident()
            decl = AST.Decl(AST.DECL_CONST, ft, name)
            methdecls.append(decl)
            debug("parsed method decl")
            self.expect(lexer.TOK_SEMI)
        self.expect(lexer.TOK_RCURLY)
        return AST.Interface(name, methdecls)

    def parse_block(self):
        self.expect(lexer.TOK_LCURLY)
        statements = []
        while not self.check(lexer.TOK_RCURLY):
            stmt = self.parse_statement()
            self.expect(lexer.TOK_SEMI)
            statements.append(stmt)
        self.expect(lexer.TOK_RCURLY)
        return statements

    def parse_function(self):
        tp = self.parse_functype()
        name = self.parse_ident()
        body = self.parse_block()
        debug("parsed function")
        return AST.Function(name, tp, body)

    def parse_functype(self):
        self.expect(lexer.TOK_FUNC)
        ret_type = None
        if not self.check(lexer.TOK_LPAREN):
            ret_type = self.parse_type()
        params = self.parse_parameters()
        return AST.FuncType(None, ret_type, params)

    def parse_parameters(self):
        self.expect(lexer.TOK_LPAREN)
        params = []
        if not self.check(lexer.TOK_RPAREN):
            while True:
                if self.accept(lexer.TOK_CONST):
                    k = AST.DECL_CONST
                else:
                    k = AST.DECL_VAR

                tp = self.parse_type()
                rhs = self.parse_decl_rhs()
                param = AST.Decl(k, tp, rhs)
                params.append(param)
                if not self.accept(lexer.TOK_COMMA):
                    break
        self.expect(lexer.TOK_RPAREN)
        return params

    def parse_alias(self):
        self.expect(lexer.TOK_ALIAS)
        tp = self.parse_type()
        name = self.parse_ident()
        return AST.Alias(tp, name)

    def parse_const_decl(self):
        self.expect(lexer.TOK_CONST)
        return self.parse_decl(AST.DECL_CONST)

    def parse_var_decl(self):
        self.expect(lexer.TOK_VAR)
        return self.parse_decl(AST.DECL_VAR)

    def parse_decl(self, kind):
        tp = self.parse_type()
        rhs = self.parse_decl_rhs()
        if self.accept(lexer.TOK_COMMA):
            rhs = []
            while True:
                rhs = self.parse_decl_rhs()
                if not self.accept(lexer.TOK_COMMA):
                    break
        return AST.Decl(kind, tp, rhs)

    def parse_decl_rhs(self):
        name = self.parse_ident()
        expr = None
        if self.accept(lexer.TOK_EQ):
            expr = self.parse_expression()
            rhs = AST.Init(name, expr)
        else:
            rhs = name
        return rhs

    def parse_type(self):
        if self.check(lexer.TOK_FUNC):
            tp = self.parse_functype()
        else:
            tp = self.parse_ident()
            if self.accept(lexer.TOK_COLCOL):
                pkg = tp
                name = self.parse_ident()
                tp = AST.PackageRef(pkg, name)
                debug("parsed qualified type")
        return tp

    def parse_ident(self):
        self.expect(lexer.TOK_IDENT)
        return AST.Ident(self.buff)

    def check_binary_operator(self):
        return (self.check(lexer.TOK_PLUS) or
                self.check(lexer.TOK_MINUS) or
                self.check(lexer.TOK_ASTERISK) or
                self.check(lexer.TOK_FSLASH) or
                self.check(lexer.TOK_PERCENT) or
                self.check(lexer.TOK_CARAT) or
                self.check(lexer.TOK_EQ) or
                self.check(lexer.TOK_NEQ) or
                self.check(lexer.TOK_LT) or
                self.check(lexer.TOK_LTEQ) or
                self.check(lexer.TOK_GT) or
                self.check(lexer.TOK_GTEQ) or
                self.check(lexer.TOK_PIPEPIPE) or
                self.check(lexer.TOK_AMPAMP))

    def get_precedence(self, op):
        if op == lexer.TOK_PIPEPIPE:
            return 1
        elif op == lexer.TOK_AMPAMP:
            return 2
        elif (op == lexer.TOK_EQ or op == lexer.TOK_NEQ or
                op == lexer.TOK_LT or op == lexer.TOK_LTEQ or
                op == lexer.TOK_GT or op == lexer.TOK_GTEQ):
            return 3
        elif op == lexer.TOK_PLUS or op == lexer.TOK_MINUS:
            return 4
        elif (op == lexer.TOK_ASTERISK or
                op == lexer.TOK_FSLASH or op == lexer.TOK_PERCENT):
            return 5
        elif op == lexer.TOK_CARAT:
            return 6
        else:
            return 0

    def parse_expression(self):
        cur = self.parse_unary_expr()

        operators = []
        terms = []

        while self.check_binary_operator():
            terms.append(cur)
            op = self.tok
            self.getnext()

            while len(operators) > 0:
                prec = self.get_precedence(op)
                top = operators[-1]
                top_prec = self.get_precedence(top)
                if (top != lexer.TOK_CARAT and top_prec >= prec) or top_prec > prec:
                    thisop = operators.pop()
                    rhs = terms.pop()
                    lhs = terms.pop()
                    binexpr = AST.BinaryExpr(lhs, rhs, thisop)
                    terms.append(binexpr)
                else:
                    break
            operators.append(op)
            cur = self.parse_unary_expr()

        while len(operators) > 0:
            op = operators.pop()
            lhs = terms.pop()
            cur = AST.BinaryExpr(lhs, cur, op)

        return cur

    def parse_unary_expr(self):
        if self.check(lexer.TOK_EXCLAM) or self.check(lexer.TOK_MINUS):
            op = self.tok
            self.getnext()
            inner = self.parse_unary_expr()
            expr = AST.UnaryExpr(op, inner)
        else:
            expr = self.parse_term()
        return expr

    def parse_term(self):
        term = self.parse_operand()
        while True:
            if self.accept(lexer.TOK_LSQUARE):
                idx = self.parse_expression()
                term = AST.Lookup(term, idx)
                self.expect(lexer.TOK_RSQUARE)
            elif self.check(lexer.TOK_LPAREN):
                args = self.parse_arguments()
                term = AST.Call(term, args)
            elif self.accept(lexer.TOK_PERIOD):
                child = self.parse_ident()
                term = AST.Selector(term, child)
            else:
                break
        return term

    def parse_operand(self):
        operand = None
        if self.check(lexer.TOK_IDENT):
            operand = self.parse_ident()
            if self.accept(lexer.TOK_COLCOL):
                child = self.parse_ident()
                operand = AST.PackageRef(operand, child)
        elif self.accept(lexer.TOK_BOOL):
            if self.buff == "true":
                b = True
            elif self.buff == "false":
                b = False
            else:
                error("Invalid bool! %s" % self.buff)
            operand = AST.BoolLit(b)
        elif self.accept(lexer.TOK_CHAR):
            operand = AST.CharLit(self.buff[0])
        elif self.accept(lexer.TOK_INTEGER):
            operand = AST.IntLit(int(self.buff))
        elif self.accept(lexer.TOK_REAL):
            operand = AST.RealLit(float(self.buff))
        elif self.accept(lexer.TOK_STRING):
            operand = AST.StringLit(self.buff)
        elif self.accept(lexer.TOK_LPAREN):
            operand = self.parse_expression()
            self.expect(lexer.TOK_RPAREN)
        elif self.accept(lexer.TOK_LSQUARE):
            operand = self.parse_list_literal()
        elif self.accept(lexer.TOK_LCURLY):
            operand = self.parse_map_literal()
        elif self.accept(lexer.TOK_FUNC):
            operand = self.parse_func_literal()
        elif self.accept(lexer.TOK_NEW):
            operand = self.parse_class_literal()
        else:
            error("Invalid operand: %s", self.buff)
        return operand

    def parse_list_literal(self):
        self.expect(lexer.TOK_LCURLY)
        lit = []
        if not self.check(lexer.TOK_LCURLY):
            while True:
                expr = self.parse_expression()
                lit.append(expr)
                if not self.accept(lexer.TOK_COMMA):
                    break
        self.expect(lexer.TOK_RCURLY)
        return AST.ListLit(lit)

    def parse_map_literal(self):
        self.expect(lexer.TOK_LSQUARE)
        lit = []
        if not self.check(lexer.TOK_LSQUARE):
            while True:
                key = self.parse_expression()
                self.expect(lexer.TOK_COLON)
                val = self.parse_expression()
                keyval = AST.KeyVal(key, val)
                lit.append(keyval)
                if not self.accept(lexer.TOK_COMMA):
                    break
        self.expect(lexer.TOK_RSQUARE)
        return AST.MapLit(lit)

    def parse_func_literal(self):
        ft = self.parse_functype()
        body = self.parse_block()
        return AST.Function(None, ft, body)

    def parse_class_literal(self):
        self.expect(lexer.TOK_NEW)
        clss = self.parse_type()
        self.expect(lexer.TOK_LCURLY)
        inits = []
        if not self.check(lexer.TOK_RCURLY):
            while True:
                member = self.parse_ident()
                self.expect(lexer.TOK_COLON)
                val = self.parse_expression()
                kv = AST.KeyVal(member, val)
                inits.append(kv)
                if not self.accept(lexer.TOK_COMMA):
                    break
        self.expect(lexer.TOK_RCURLY)
        return AST.ClassLit(clss, None, inits)

    def parse_arguments(self):
        self.expect(lexer.TOK_LPAREN)
        args = []
        if not self.check(lexer.TOK_RPAREN):
            while True:
                expr = self.parse_expression()
                args.append(expr)
                if not self.accept(lexer.TOK_COMMA):
                    break
        self.expect(lexer.TOK_RPAREN)
        return args
