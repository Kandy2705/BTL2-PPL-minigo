"""
 * Initial code for Assignment 1, 2
 * Programming Language Principles
 * Author: Võ Tiến
 * Link FB : https://www.facebook.com/Shiba.Vo.Tien
 * Link Group : https://www.facebook.com/groups/khmt.ktmt.cse.bku
 * Date: 20.01.2025
"""
from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *
from functools import reduce

##! continue update
class ASTGeneration(MiniGoVisitor):
    # Visit a parse tree produced by MiniGoParser#program.
    def visitProgram(self, ctx:MiniGoParser.ProgramContext):
        test = self.visit(ctx.list_declaration())
        return Program(test)


    # Visit a parse tree produced by MiniGoParser#list_declaration.
    def visitList_declaration(self, ctx:MiniGoParser.List_declarationContext):
        declarations = []

        if ctx.array_literal():
            declarations.append(self.visit(ctx.array_literal()))
        elif ctx.global_variable():
            declarations.append(self.visit(ctx.global_variable()))
        elif ctx.global_constant():
            declarations.append(self.visit(ctx.global_constant()))
        elif ctx.function():
            declarations.append(self.visit(ctx.function()))
        elif ctx.struct_type():
            declarations.append(self.visit(ctx.struct_type()))
        elif ctx.interface_type():
            declarations.append(self.visit(ctx.interface_type()))
        elif ctx.struct_func():
            declarations.append(self.visit(ctx.struct_func()))

        if ctx.list_declaration():
            declarations.extend(self.visit(ctx.list_declaration()))

        return declarations
        


    # Visit a parse tree produced by MiniGoParser#struct_type.
    def visitStruct_type(self, ctx:MiniGoParser.Struct_typeContext):
        name = ctx.ID().getText()
        fields = self.visit(ctx.data_struct())
        return StructType(name=name, elements=fields, methods=[])


    # Visit a parse tree produced by MiniGoParser#data_struct.
    def visitData_struct(self, ctx:MiniGoParser.Data_structContext):
        fields = []
        if ctx.type_data():
            field_name = ctx.getChild(0).getText()
            field_type = self.visit(ctx.type_data())
            fields.append((field_name, field_type))
        if ctx.data_struct():
            fields.extend(self.visit(ctx.data_struct()))
        return fields


    # Visit a parse tree produced by MiniGoParser#interface_type.
    def visitInterface_type(self, ctx:MiniGoParser.Interface_typeContext):
        name = ctx.ID().getText()  
        methods = self.visit(ctx.data_inter())
        return InterfaceType(name, methods)


    # Visit a parse tree produced by MiniGoParser#data_inter.
    def visitData_inter(self, ctx:MiniGoParser.Data_interContext):
        data = []
        
        if ctx.initialize_inter():
            initialize_inter = self.visit(ctx.initialize_inter())
            name = initialize_inter[0]
            params = initialize_inter[1]
            returnType = self.visit(ctx.type_data()) if ctx.type_data() else VoidType()
            param_types = [param.varType for param in params]
            proto = Prototype(name=name,
                              params=param_types,
                              retType=returnType)
            data.append(proto)

        if ctx.data_inter():
            data.extend(self.visit(ctx.data_inter()))

        return data 


    # Visit a parse tree produced by MiniGoParser#initialize_inter.
    def visitInitialize_inter(self, ctx:MiniGoParser.Initialize_interContext):
        method_name = ctx.ID().getText()
        params = []

        if ctx.list_interface():
            params = self.visit(ctx.list_interface())
        
        return [method_name, params]


    # Visit a parse tree produced by MiniGoParser#list_interface.
    def visitList_interface(self, ctx:MiniGoParser.List_interfaceContext):
        result = []
        result.extend(self.visit(ctx.data_inter_thamso_list()))
        if ctx.list_interface():
            result.extend(self.visit(ctx.list_interface()))
        return result
        # final = []
        # for i in kq:
        #     if isinstance(i, list):
        #         final.extend(i)
        #     else:
        #         final.append(i)
        
        # return final


    # Visit a parse tree produced by MiniGoParser#data_inter_thamso_list.
    def visitData_inter_thamso_list(self, ctx:MiniGoParser.Data_inter_thamso_listContext):
        names = self.visit(ctx.data_inter_thamso())
        type_ = self.visit(ctx.type_data())
        # return [VariablesDecl(n, type_, None) for n in name]
        return [VarDecl(varName=n, varType=type_, varInit=None) for n in names]


    # Visit a parse tree produced by MiniGoParser#data_inter_thamso.
    def visitData_inter_thamso(self, ctx:MiniGoParser.Data_inter_thamsoContext):
        if ctx.COMMA():
            return [ctx.ID().getText()] + self.visit(ctx.data_inter_thamso())
        return [ctx.ID().getText()]


    # Visit a parse tree produced by MiniGoParser#global_variable.
    def visitGlobal_variable(self, ctx:MiniGoParser.Global_variableContext):
        variable = ctx.getChild(1).getText()
        if ctx.type_data():
            varType = self.visit(ctx.type_data())
            if ctx.expr():
                varInit = self.visit(ctx.expr())
            else:
                varInit = None
            return VarDecl(variable, varType, varInit)
        
        else:
            varType = None
            varInit = self.visit(ctx.expr())
            return VarDecl(variable, varType, varInit)


    # Visit a parse tree produced by MiniGoParser#local_variable.
    def visitLocal_variable(self, ctx:MiniGoParser.Local_variableContext):
        variable = ctx.getChild(1).getText()
        if ctx.type_data():
            varType = self.visit(ctx.type_data())
            if ctx.expr():
                varInit = self.visit(ctx.expr())
            else:
                varInit = None
            return VarDecl(variable, varType, varInit)
        
        else:
            varType = None
            varInit = self.visit(ctx.expr())
            return VarDecl(variable, varType, varInit)


    # Visit a parse tree produced by MiniGoParser#global_constant.
    def visitGlobal_constant(self, ctx:MiniGoParser.Global_constantContext):
        constant = ctx.getChild(1).getText()
        value = self.visit(ctx.getChild(3))
        return ConstDecl(conName=constant, conType=None, iniExpr=value)


    # Visit a parse tree produced by MiniGoParser#local_constant.
    def visitLocal_constant(self, ctx:MiniGoParser.Local_constantContext):
        constant = ctx.getChild(1).getText()
        value = self.visit(ctx.getChild(3))
        return ConstDecl(conName=constant, conType=None, iniExpr=value)


    # Visit a parse tree produced by MiniGoParser#function.
    def visitFunction(self, ctx:MiniGoParser.FunctionContext):
        func_info = self.visit(ctx.func_call_str())  
        name = func_info[0]
        params = func_info[1]
        retType = self.visit(ctx.type_data()) if ctx.type_data() else VoidType()
        body_stmts = self.visit(ctx.body_func())
        body = Block(member=body_stmts)
        return FuncDecl(name=name, params=params, retType=retType, body=body)


    # Visit a parse tree produced by MiniGoParser#data_func.
    def visitData_func(self, ctx:MiniGoParser.Data_funcContext):
        params = []

        name = Id(ctx.ID().getText())
        ptype = self.visit(ctx.type_data())
        params.append(VarDecl(name, ptype, None))

        if ctx.data_func():
            params.extend(self.visit(ctx.data_func()))

        return params


    # Visit a parse tree produced by MiniGoParser#body_func.
    def visitBody_func(self, ctx:MiniGoParser.Body_funcContext):
        body = []
        if ctx.assignment_func(): #xong
            body.append(self.visit(ctx.assignment_func()))
        elif ctx.if_else():
            body.append(self.visit(ctx.if_else()))
        elif ctx.RETURN(): #xong
            if ctx.func_call():
                body.append(Return(self.visit(ctx.func_call())))
            elif ctx.expr():
                body.append(Return(self.visit(ctx.expr())))
            else:
                body.append(Return(None))
        elif ctx.local_variable(): #xong
            body.append(self.visit(ctx.local_variable()))
        elif ctx.local_constant(): #xong
            body.append(self.visit(ctx.local_constant()))
        elif ctx.for_basic(): 
            body.append(self.visit(ctx.for_basic()))
        elif ctx.for_icu():
            body.append(self.visit(ctx.for_icu()))
        elif ctx.for_range():
            body.append(self.visit(ctx.for_range()))
        elif ctx.func_call(): #xong
            body.append(self.visit(ctx.func_call()))
        elif ctx.call_statement(): #xong
            body.append(self.visit(ctx.call_statement()))
        elif ctx.BREAK(): #xong
            body.append(Break())
        elif ctx.CONTINUE(): #xong
            body.append(Continue())

        if ctx.body_func():
            body.extend(self.visit(ctx.body_func()))

        return body


    # Visit a parse tree produced by MiniGoParser#assignment_func.
    def visitAssignment_func(self, ctx:MiniGoParser.Assignment_funcContext):
        assign = ctx.getChild(1).getText()
        lhs = self.visit(ctx.dot())
        rhs = self.visit(ctx.expr())
        if ctx.ADD_ASSIGN():
            return Assign(lhs, BinaryOp("+", lhs, rhs))
        elif ctx.SUB_ASSIGN():
            return Assign(lhs,BinaryOp("-", lhs, rhs))
        elif ctx.MUL_ASSIGN():
            return Assign(lhs,BinaryOp("*", lhs, rhs))
        elif ctx.DIV_ASSIGN():
            return Assign(lhs,BinaryOp("/", lhs, rhs))
        elif ctx.MOD_ASSIGN():
            return Assign(lhs,BinaryOp("%", lhs, rhs))
        elif ctx.EQ():
            return Assign(lhs,BinaryOp("=", lhs, rhs))
        else:
            return Assign(lhs, rhs)


    # Visit a parse tree produced by MiniGoParser#dot.
    def visitDot(self, ctx:MiniGoParser.DotContext):
        if (ctx.getChildCount() == 1):
            return Id(ctx.ID().getText())
        lhs = self.visit(ctx.getChild(0))
        rhs = None
        
        if ctx.LBRACKET():
            rhs = self.visit(ctx.getChild(2))
            return ArrayCell(lhs, [rhs])
        else:
            rhs = ctx.getChild(2).getText()
            return FieldAccess(lhs, rhs)



    # Visit a parse tree produced by MiniGoParser#assignment_for.
    def visitAssignment_for(self, ctx:MiniGoParser.Assignment_forContext):
        assign = ctx.getChild(1).getText()
        lhs = Id(ctx.ID().getText())
        rhs = self.visit(ctx.expr())
        if ctx.ADD_ASSIGN():
            return Assign(lhs,BinaryOp("+", lhs, rhs))
        elif ctx.SUB_ASSIGN():
            return Assign(lhs,BinaryOp("-", lhs, rhs))
        elif ctx.MUL_ASSIGN():
            return Assign(lhs,BinaryOp("*", lhs, rhs))
        elif ctx.DIV_ASSIGN():
            return Assign(lhs,BinaryOp("/", lhs, rhs))
        elif ctx.MOD_ASSIGN():
            return Assign(lhs,BinaryOp("%", lhs, rhs))
        elif ctx.EQ():
            return Assign(lhs,BinaryOp("=", lhs, rhs))
        else:
            return Assign(lhs, rhs)


    # Visit a parse tree produced by MiniGoParser#if_else.
    def visitIf_else(self, ctx:MiniGoParser.If_elseContext):
        cond = self.visit(ctx.expr())
        then_stmts = self.visit(ctx.body_func(0))
        then_block = Block(member=then_stmts)

        else_block = None
        if ctx.else_if():
            current_else = None
            elif_list = self.visit(ctx.else_if())
            for econd, eblock in reversed(elif_list):
                current_else = If(expr=econd, thenStmt=Block(member=eblock), elseStmt=current_else)
            else_block = current_else
        if ctx.ELSE():
            else_stmts = self.visit(ctx.body_func(1))
            new_else = Block(member=else_stmts)
            if else_block is not None:
                cur = else_block
                while cur.elseStmt is not None:
                    cur = cur.elseStmt
                cur.elseStmt = new_else
            else:
                else_block = new_else
        return If(expr=cond, thenStmt=then_block, elseStmt=else_block)


    # Visit a parse tree produced by MiniGoParser#else_if.
    def visitElse_if(self, ctx:MiniGoParser.Else_ifContext):
        pairs = []
        expr_val = self.visit(ctx.expr())
        body_stmts = self.visit(ctx.body_func())
        pairs.append((expr_val, body_stmts))
        if ctx.else_if():
            pairs.extend(self.visit(ctx.else_if()))
        return pairs


    # Visit a parse tree produced by MiniGoParser#for_basic.
    def visitFor_basic(self, ctx:MiniGoParser.For_basicContext):
        expr = self.visit(ctx.expr())
        loop_stmts = self.visit(ctx.body_func())
        loop = Block(member=loop_stmts)

        return ForBasic(expr, loop)


    # Visit a parse tree produced by MiniGoParser#for_icu.
    def visitFor_icu(self, ctx:MiniGoParser.For_icuContext):
        expr = self.visit(ctx.expr())
        loop_stmts = self.visit(ctx.body_func())
        loop = Block(member=loop_stmts)
            
        if ctx.var_for():
            initStmt = self.visit(ctx.var_for())
            postStmt = self.visit(ctx.assignment_for()[0])
        else:
            initStmt = self.visit(ctx.assignment_for(0)) 
            postStmt = self.visit(ctx.assignment_for(1))
        
        return ForStep(initStmt, expr, postStmt, loop)



    # Visit a parse tree produced by MiniGoParser#for_range.
    def visitFor_range(self, ctx:MiniGoParser.For_rangeContext):
        index = Id(ctx.ID(0).getText())
        value = Id(ctx.ID(1).getText())
        array = self.visit(ctx.expr())
        loop_stmts = self.visit(ctx.body_func())
        loop = Block(member=loop_stmts)

        return ForEach(index, value, array, loop)


    # Visit a parse tree produced by MiniGoParser#var_for.
    def visitVar_for(self, ctx:MiniGoParser.Var_forContext):
        variable = ctx.getChild(1).getText()
        if ctx.type_data():
            varType = self.visit(ctx.type_data())
            varInit = self.visit(ctx.expr())
            return VarDecl(variable, varType, varInit)
        else:
            varType = None
            varInit = self.visit(ctx.expr())
            return VarDecl(variable, varType, varInit)


    # Visit a parse tree produced by MiniGoParser#struct_func.
    def visitStruct_func(self, ctx:MiniGoParser.Struct_funcContext):
        func_call_info = self.visit(ctx.func_call_str())
        method_name = func_call_info[0]
        params = func_call_info[1]
        retType = self.visit(ctx.type_data()) if ctx.type_data() else VoidType()
        body_stmts = self.visit(ctx.body_func())
        body = Block(member=body_stmts)
        receiver_decl = None
        if ctx.method():
            receiver_decl = self.visit(ctx.method())
        func_decl = FuncDecl(name=method_name, params=params, retType=retType, body=body)
        if receiver_decl:
            return MethodDecl(receiver=receiver_decl.varName, recType=receiver_decl.varType, fun=func_decl)
        return func_decl


    # Visit a parse tree produced by MiniGoParser#method.
    def visitMethod(self, ctx:MiniGoParser.MethodContext):
        name = ctx.getChild(0).getText()
        mtype = Id(ctx.getChild(1).getText())
        if ctx.method():
            kq = [VarDecl(name, mtype, None)] + self.visit(ctx.method())
        else:
            kq = [VarDecl(name, mtype, None)]
        return kq[0]


    # Visit a parse tree produced by MiniGoParser#func_call_str.
    def visitFunc_call_str(self, ctx:MiniGoParser.Func_call_strContext):
        name = ctx.ID().getText()
        params = []
        if ctx.func_call_thamso_str():
            params = self.visit(ctx.func_call_thamso_str())
        return [name, params]


    # Visit a parse tree produced by MiniGoParser#func_call_thamso_str.
    def visitFunc_call_thamso_str(self, ctx:MiniGoParser.Func_call_thamso_strContext):
        params = []
        param_name = self.visit(ctx.data_inter_thamso())
        param_type = self.visit(ctx.type_data()) if ctx.type_data() else None
        params.extend([ParamDecl(n, param_type) for n in param_name])

        if ctx.COMMA():
            params.extend(self.visit(ctx.func_call_thamso_str()))
        
        return params


    # Visit a parse tree produced by MiniGoParser#array_literal.
    def visitArray_literal(self, ctx:MiniGoParser.Array_literalContext):
        typ_dimension = self.visit(ctx.type_array())
        typ = typ_dimension.eleType
        dimension = typ_dimension.dimens

        value = self.visit(ctx.list_expr())

        return ArrayLiteral(eleType=typ, dimens=dimension, value=value)


    # Visit a parse tree produced by MiniGoParser#type_array.
    def visitType_array(self, ctx:MiniGoParser.Type_arrayContext):
        dimensions = self.visit(ctx.list_type_arr())
        typ = self.visit(ctx.type_data())
        return ArrayType(dimensions, typ)


    # Visit a parse tree produced by MiniGoParser#list_type_arr.
    def visitList_type_arr(self, ctx:MiniGoParser.List_type_arrContext):
        if ctx.list_type_arr():
            return [Id(ctx.ID().getText()) if ctx.ID() else IntLiteral(ctx.getChild(1).getText())] + self.visit(ctx.list_type_arr())
        else:
            return [Id(ctx.ID().getText()) if ctx.ID() else IntLiteral(ctx.getChild(1).getText())]


    # Visit a parse tree produced by MiniGoParser#list_expr.
    def visitList_expr(self, ctx:MiniGoParser.List_exprContext):
        return self.visit(ctx.data_list_expr())


    # Visit a parse tree produced by MiniGoParser#data_list_expr.
    def visitData_list_expr(self, ctx:MiniGoParser.Data_list_exprContext):

        if ctx.COMMA():

            if ctx.INT_DEC() or ctx.INT_BIN() or ctx.INT_OCT() or ctx.INT_HEX():
                current = [IntLiteral(int(ctx.getChild(0).getText(), 0))]
            elif ctx.TRUE():
                current = [BooleanLiteral(True)]
            elif ctx.FALSE():
                current = [BooleanLiteral(False)]
            elif ctx.NIL():
                current = [NilLiteral()]
            elif ctx.FLOAT_LIT():
                current = [FloatLiteral(float(ctx.FLOAT_LIT().getText()))]
            elif ctx.STRING_LIT():
                current = [StringLiteral(ctx.STRING_LIT().getText()[1:-1])]
            elif ctx.list_expr():
                current = [self.visit(ctx.list_expr())]
            elif ctx.ID():
                current = [ctx.ID().getText()]
            else:
                current = [self.visit(ctx.struct_literal())]
            
            rest = self.visit(ctx.data_list_expr())

            return current + rest
            
        else:
            if ctx.INT_DEC() or ctx.INT_BIN() or ctx.INT_OCT() or ctx.INT_HEX():
                current = [IntLiteral(int(ctx.getChild(0).getText(), 0))]
            elif ctx.TRUE():
                current = [BooleanLiteral(True)]
            elif ctx.FALSE():
                current = [BooleanLiteral(False)]
            elif ctx.NIL():
                current = [NilLiteral()]
            elif ctx.FLOAT_LIT():
                current = [FloatLiteral(float(ctx.FLOAT_LIT().getText()))]
            elif ctx.STRING_LIT():
                current = [StringLiteral(ctx.STRING_LIT().getText()[1:-1])]
            elif ctx.list_expr():
                current = [self.visit(ctx.list_expr())]
            elif ctx.ID():
                current = [ctx.ID().getText()]
            else:
                current = [self.visit(ctx.struct_literal())]

            return current


    # Visit a parse tree produced by MiniGoParser#type_data.
    def visitType_data(self, ctx:MiniGoParser.Type_dataContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.STRING():
            return StringType()
        else:
            return self.visit(ctx.type_array())


    # Visit a parse tree produced by MiniGoParser#struct_literal.
    def visitStruct_literal(self, ctx:MiniGoParser.Struct_literalContext):
        name = ctx.getChild(0).getText()

        if ctx.list_elements():
            value = self.visit(ctx.list_elements())
        else:
            value = []

        return StructLiteral(name, value)


    # Visit a parse tree produced by MiniGoParser#list_elements.
    def visitList_elements(self, ctx:MiniGoParser.List_elementsContext):
        elements = []
        if ctx.COMMA():
            id = ctx.ID().getText()
            expr = self.visit(ctx.expr())
            elements = elements + [(id, expr)]

            elements.extend(self.visit(ctx.list_elements()))

        else:
            id = ctx.ID().getText()
            expr = self.visit(ctx.expr())
            elements = elements + [(id, expr)]

        return elements


    # Visit a parse tree produced by MiniGoParser#expr.
    def visitExpr(self, ctx:MiniGoParser.ExprContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr1())
        else:
            toantu = ctx.getChild(1).getText()
            vetrai = self.visit(ctx.getChild(0))
            vephai = self.visit(ctx.getChild(2))
            return BinaryOp(toantu, vetrai, vephai)


    # Visit a parse tree produced by MiniGoParser#expr1.
    def visitExpr1(self, ctx:MiniGoParser.Expr1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr2())
        else:
            toantu = ctx.getChild(1).getText()
            vetrai = self.visit(ctx.getChild(0))
            vephai = self.visit(ctx.getChild(2))
            return BinaryOp(toantu, vetrai, vephai)


    # Visit a parse tree produced by MiniGoParser#expr2.
    def visitExpr2(self, ctx:MiniGoParser.Expr2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr3())
        else:
            toantu = ctx.getChild(1).getText()
            vetrai = self.visit(ctx.getChild(0))
            vephai = self.visit(ctx.getChild(2))
            return BinaryOp(toantu, vetrai, vephai)


    # Visit a parse tree produced by MiniGoParser#expr3.
    def visitExpr3(self, ctx:MiniGoParser.Expr3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr4())
        else:
            toantu = ctx.getChild(1).getText()
            vetrai = self.visit(ctx.getChild(0))
            vephai = self.visit(ctx.getChild(2))
            return BinaryOp(toantu, vetrai, vephai)


    # Visit a parse tree produced by MiniGoParser#expr4.
    def visitExpr4(self, ctx:MiniGoParser.Expr4Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr5())
        else:
            toantu = ctx.getChild(1).getText()
            vetrai = self.visit(ctx.getChild(0))
            vephai = self.visit(ctx.getChild(2))
            return BinaryOp(toantu, vetrai, vephai)


    # Visit a parse tree produced by MiniGoParser#expr5.
    def visitExpr5(self, ctx:MiniGoParser.Expr5Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr6())
        else:
            toantu = ctx.getChild(0).getText()
            vephai = self.visit(ctx.getChild(1))
            return UnaryOp(toantu, vephai)


    # Visit a parse tree produced by MiniGoParser#expr6.
    def visitExpr6(self, ctx:MiniGoParser.Expr6Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr7())
        elif ctx.getChildCount() == 3:
            if ctx.func_call():
                obj = self.visit(ctx.getChild(0))
                func = self.visit(ctx.getChild(2))
                method = func.funName
                param = func.args
                return MethCall(obj, method, param)
            else:
                vetrai = self.visit(ctx.getChild(0))
                vephai = ctx.ID().getText()
                return FieldAccess(vetrai, vephai)

        else: 
            # vetrai = self.visit(ctx.getChild(0))
            # vephai = self.visit(ctx.getChild(2))
            # return ArrayCell(vetrai, [vephai])
            expr6 = self.visit(ctx.expr6())
            if type(expr6) == ArrayCell:
                return ArrayCell(expr6.arr, expr6.idx + [self.visit(ctx.expr())])
            return ArrayCell(expr6, [self.visit(ctx.expr())])

    # Visit a parse tree produced by MiniGoParser#expr7.
    def visitExpr7(self, ctx:MiniGoParser.Expr7Context):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.INT_DEC():
            return IntLiteral(int(ctx.INT_DEC().getText(), 0))
        elif ctx.INT_BIN():
            return IntLiteral(int(ctx.INT_BIN().getText(), 0))
        elif ctx.INT_OCT():
            return IntLiteral(int(ctx.INT_OCT().getText(), 0))
        elif ctx.INT_HEX():
            return IntLiteral(int(ctx.INT_HEX().getText(), 0))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText()[1:-1])
        elif ctx.NIL():
            return NilLiteral()
        elif ctx.struct_literal():
            return self.visit(ctx.struct_literal())
        
        elif ctx.array_literal():
            return self.visit(ctx.array_literal())
        
        elif ctx.func_call():
            return self.visit(ctx.func_call())
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
        else:   
            return self.visit(ctx.expr())


    # Visit a parse tree produced by MiniGoParser#call_statement.
    def visitCall_statement(self, ctx:MiniGoParser.Call_statementContext):
        receiver = self.visit(ctx.dot())
        metName = ctx.ID().getText()
        args = self.visit(ctx.func_call_thamso()) if ctx.func_call_thamso() else []
        return MethCall(receiver=receiver, metName=metName, args=args)


    # Visit a parse tree produced by MiniGoParser#func_call.
    def visitFunc_call(self, ctx:MiniGoParser.Func_callContext):
        funName = ctx.ID().getText()
        args = self.visit(ctx.func_call_thamso()) if ctx.func_call_thamso() else []
        return FuncCall(funName=funName, args=args)


    # Visit a parse tree produced by MiniGoParser#func_call_thamso.
    def visitFunc_call_thamso(self, ctx:MiniGoParser.Func_call_thamsoContext):
        if ctx.func_call_thamso():
            return [self.visit(ctx.expr())] + self.visit(ctx.func_call_thamso())
        return [self.visit(ctx.expr())]


