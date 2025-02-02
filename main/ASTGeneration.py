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
    #copy function target/main/MiniGoVisitor.py
    # pass

    # Visit a parse tree produced by MiniGoParser#program. 
    def visitProgram(self, ctx:MiniGoParser.ProgramContext):
        list = [self.visit(i) for i in ctx.list_declaration()]  
        return Program(list)
    

    # Visit a parse tree produced by MiniGoParser#list_declaration.
    def visitList_declaration(self, ctx:MiniGoParser.List_declarationContext):
        if ctx.array_literal():
            return self.visit(ctx.array_literal())
        elif ctx.struct_literal():
            return self.visit(ctx.struct_literal())
        elif ctx.global_variable():
            return self.visit(ctx.global_variable())
        elif ctx.global_constant():
            return self.visit(ctx.global_constant())
        elif ctx.function():
            return self.visit(ctx.function())
        elif ctx.struct_type():
            return self.visit(ctx.struct_type())
        elif ctx.interface_type():
            return self.visit(ctx.interface_type())
        elif ctx.struct_func():
            return self.visit(ctx.struct_func())
        elif ctx.func_call():
            func = self.visit(ctx.getChild(0))
            method = func[0]
            param = func[1]
            return CallExpr('', method, param)
            


    # Visit a parse tree produced by MiniGoParser#struct_type.
    def visitStruct_type(self, ctx:MiniGoParser.Struct_typeContext):
        name = Id(ctx.ID().getText())
        fields = self.visit(ctx.data_struct())
        return StructDecl(name, fields)


    # Visit a parse tree produced by MiniGoParser#data_struct.
    def visitData_struct(self, ctx:MiniGoParser.Data_structContext):
        ds_struct = []

        if ctx.type_data():
            name = Id(ctx.getChild(0).getText())
            type = self.visit(ctx.type_data())
            struct = VariablesDecl(name, type, None)
            ds_struct.append(struct)

        if ctx.data_struct():
            ds_struct.extend(self.visit(ctx.data_struct()))

        return ds_struct


    # # Visit a parse tree produced by MiniGoParser#initialize_struct.
    # def visitInitialize_struct(self, ctx:MiniGoParser.Initialize_structContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#interface_type.
    def visitInterface_type(self, ctx:MiniGoParser.Interface_typeContext):
        name = Id(ctx.ID().getText())
        fields = self.visit(ctx.data_inter())
        return InterfaceDecl(name, fields)


    # Visit a parse tree produced by MiniGoParser#data_inter.
    def visitData_inter(self, ctx:MiniGoParser.Data_interContext):
        data = []
        
        if ctx.initialize_inter():
            initialize_inter = self.visit(ctx.initialize_inter())
            name = initialize_inter[0]
            params = initialize_inter[1]
            returnType = self.visit(ctx.type_data()) if ctx.type_data() else VoidType()
            data.append(FunctionDecl(name, returnType, None, params, []))

        if ctx.data_inter():
            data.extend(self.visit(ctx.data_inter()))

        return data 



    # Visit a parse tree produced by MiniGoParser#initialize_inter.
    def visitInitialize_inter(self, ctx:MiniGoParser.Initialize_interContext):
        method_name = Id(ctx.ID().getText())
        params = []

        if ctx.list_interface():
            params = self.visit(ctx.list_interface())
        
        return [method_name, params]
        

    # Visit a parse tree produced by MiniGoParser#list_interface.
    def visitList_interface(self, ctx:MiniGoParser.List_interfaceContext):
        kq = []
        if ctx.data_inter_thamso_list():
            kq.append(self.visit(ctx.data_inter_thamso_list()))
        if ctx.list_interface():
            kq.extend(self.visit(ctx.list_interface()))

        final = []
        for i in kq:
            if isinstance(i, list):
                final.extend(i)  # Thay vì vòng lặp lồng nhau
            else:
                final.append(i)
        
        return final



    # Visit a parse tree produced by MiniGoParser#data_inter_thamso_list.
    def visitData_inter_thamso_list(self, ctx:MiniGoParser.Data_inter_thamso_listContext):
        name = self.visit(ctx.data_inter_thamso())
        type_ = self.visit(ctx.type_data())

        return [VariablesDecl(n, type_, None) for n in name]


    # Visit a parse tree produced by MiniGoParser#data_inter_thamso.
    def visitData_inter_thamso(self, ctx:MiniGoParser.Data_inter_thamsoContext):
        if ctx.COMMA():
            return [Id(ctx.ID().getText())] + self.visit(ctx.data_inter_thamso())
        return [Id(ctx.ID().getText())]


    # Visit a parse tree produced by MiniGoParser#global_variable.
    def visitGlobal_variable(self, ctx:MiniGoParser.Global_variableContext):
        variable = Id(ctx.getChild(1).getText())
        if ctx.type_data():
            varType = self.visit(ctx.type_data())
            if ctx.expr():
                varInit = self.visit(ctx.expr())
            else:
                varInit = ''
            return VariablesDecl(variable, varType, varInit)
        
        else:
            varType = ''
            varInit = self.visit(ctx.expr())
            return VariablesDecl(variable, varType, varInit)

        


    # Visit a parse tree produced by MiniGoParser#local_variable.
    def visitLocal_variable(self, ctx:MiniGoParser.Local_variableContext):
        variable = Id(ctx.getChild(1).getText())
        if ctx.type_data():
            varType = self.visit(ctx.type_data())
            if ctx.expr():
                varInit = self.visit(ctx.expr())
            else:
                varInit = ''
            return VariablesDecl(variable, varType, varInit)
        
        else:
            varType = ''
            varInit = self.visit(ctx.expr())
            return VariablesDecl(variable, varType, varInit)


    # Visit a parse tree produced by MiniGoParser#global_constant.
    def visitGlobal_constant(self, ctx:MiniGoParser.Global_constantContext):
        constant = Id(ctx.getChild(1).getText())
        value = self.visit(ctx.getChild(3))
        return ConstDecl(constant, value)
        


    # Visit a parse tree produced by MiniGoParser#local_constant.
    def visitLocal_constant(self, ctx:MiniGoParser.Local_constantContext):
        constant = Id(ctx.getChild(1).getText())
        value = self.visit(ctx.getChild(3))
        return ConstDecl(constant, value)


    # Visit a parse tree produced by MiniGoParser#function.
    def visitFunction(self, ctx:MiniGoParser.FunctionContext):
        name = Id(ctx.ID().getText())
        params = self.visit(ctx.data_func()) if ctx.data_func() else []
        returntype = self.visit(ctx.type_data()) if ctx.type_data() else VoidType()
        body = self.visit(ctx.body_func())

        return FunctionDecl(name=name, returnType=returntype, methodReceiver = None, param=params, stmts=body)


    # Visit a parse tree produced by MiniGoParser#data_func.
    def visitData_func(self, ctx:MiniGoParser.Data_funcContext):
        params = []

        name = Id(ctx.ID().getText())
        ptype = self.visit(ctx.type_data())
        params.append(VariablesDecl(name, ptype))

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
            func = self.visit(ctx.getChild(0))
            method = func[0]
            param = func[1]
            body.append(CallStmt('', method, param))
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
        if ctx.arr_index():
            assign = ctx.getChild(2).getText()
            lhs = ArrayCell(Id(ctx.ID().getText()), self.visit(ctx.arr_index()))

        elif ctx.dot_assignment():
            if ctx.list_arr_index():
                assign = ctx.getChild(3).getText()
                lhs = FieldAccess(ArrayCell(Id(ctx.ID().getText()), self.visit(ctx.list_arr_index())), self.visit(ctx.dot_assignment()))
            else:
                assign = ctx.getChild(2).getText()
                lhs = FieldAccess(Id(ctx.ID().getText()), self.visit(ctx.dot_assignment()))
        else:
            lhs = Id(ctx.ID().getText())
            assign = ctx.getChild(1).getText()

        exp = self.visit(ctx.expr())

        return AssignStmt(lhs, assign, exp)


    # Visit a parse tree produced by MiniGoParser#dot_assignment.
    def visitDot_assignment(self, ctx:MiniGoParser.Dot_assignmentContext):
        if ctx.list_type_arr():
            lhs = ArrayCell(Id(ctx.ID().getText()), self.visit(ctx.list_type_arr()))
        else:
            lhs = Id(ctx.ID().getText())

        if ctx.dot_assignment():
            return FieldAccess(lhs, self.visit(ctx.dot_assignment()))
        
        return lhs
            



    # Visit a parse tree produced by MiniGoParser#list_arr_index.
    def visitList_arr_index(self, ctx:MiniGoParser.List_arr_indexContext):
        if ctx.list_arr_index():
            return [self.visit(ctx.arr_index())] + self.visit(ctx.list_arr_index())
        
        return [self.visit(ctx.arr_index())]


    # Visit a parse tree produced by MiniGoParser#arr_index.
    def visitArr_index(self, ctx:MiniGoParser.Arr_indexContext):
        expr = self.visit(ctx.expr())
        return expr


    # Visit a parse tree produced by MiniGoParser#if_else.
    def visitIf_else(self, ctx:MiniGoParser.If_elseContext):
        expr = self.visit(ctx.expr())
        thenStmt = self.visit(ctx.body_func(0))

        elifStmt = None
        if ctx.else_if():
            elifStmt = []
            elif_ctx = ctx.else_if()
            
            while elif_ctx:
                elif_expr = self.visit(elif_ctx.expr())
                elif_body = self.visit(elif_ctx.body_func())
                elifStmt.append((elif_expr, elif_body))
                elif_ctx = elif_ctx.else_if()

        elseStmt = None
        if ctx.ELSE():
            elseStmt = self.visit(ctx.body_func(1))

        return If(expr, thenStmt, elifStmt, elseStmt)



    # Visit a parse tree produced by MiniGoParser#else_if.
    def visitElse_if(self, ctx:MiniGoParser.Else_ifContext):
        expr = self.visit(ctx.expr())
        body = self.visit(ctx.body_func()) 

        next_elif = self.visit(ctx.else_if()) if ctx.else_if() else None

        return [(expr, body)] + (next_elif if next_elif else [])


    # Visit a parse tree produced by MiniGoParser#for_basic.
    def visitFor_basic(self, ctx:MiniGoParser.For_basicContext):
        expr = self.visit(ctx.expr())
        loop = self.visit(ctx.body_func())

        return For(initStmt=None, expr=expr, postStmt=None, loop=loop)


    # Visit a parse tree produced by MiniGoParser#for_icu.
    def visitFor_icu(self, ctx:MiniGoParser.For_icuContext):

        expr = self.visit(ctx.expr())
        loop = self.visit(ctx.body_func())
        postStmt = None
        initStmt = None
            
        if ctx.local_variable():
            initStmt = self.visit(ctx.local_variable())
            postStmt = self.visit(ctx.assignment_func()[0])
        else:
            initStmt = self.visit(ctx.assignment_func(0)[0]) 
            postStmt = self.visit(ctx.assignment_func(1)[0])
        
        
        return For(initStmt=initStmt, expr=expr, postStmt=postStmt, loop=loop)


    # Visit a parse tree produced by MiniGoParser#for_range.
    def visitFor_range(self, ctx:MiniGoParser.For_rangeContext):
        index = Id(ctx.ID(0).getText())
        value = Id(ctx.ID(1).getText())
        array = self.visit(ctx.expr())
        loop = self.visit(ctx.body_func())

        return ForArray(index, value, array, loop)


    # Visit a parse tree produced by MiniGoParser#struct_func.
    def visitStruct_func(self, ctx:MiniGoParser.Struct_funcContext):
        func_call_str = self.visit(ctx.func_call_str())
        name = func_call_str[0]
        params = func_call_str[1]
        returnType = self.visit(ctx.type_data()) if ctx.type_data() else VoidType()
        # methodReceiver = self.visit(ctx.method())
        methodReceiver = None
        if ctx.method():
            methodReceiver = self.visit(ctx.method())
            if isinstance(methodReceiver, VariablesDecl) and isinstance(methodReceiver.varType, Id):
                methodReceiver.varType = ClassType(methodReceiver.varType)
        body = self.visit(ctx.body_func())

        return FunctionDecl(name=name, returnType=returnType, methodReceiver = methodReceiver, param=params, stmts=body)
        
    # Visit a parse tree produced by MiniGoParser#method.
    def visitMethod(self, ctx:MiniGoParser.MethodContext):
        name = Id(ctx.getChild(0).getText())
        mtype = self.visit(ctx.type_data())
        if ctx.method():
            kq = [VariablesDecl(name, mtype)] + self.visit(ctx.method())
        else:
            kq = [VariablesDecl(name, mtype)]
        return kq[0]

    # Visit a parse tree produced by MiniGoParser#func_call_str.
    def visitFunc_call_str(self, ctx:MiniGoParser.Func_call_strContext):
        func_name = Id(ctx.ID().getText())
        params = self.visit(ctx.func_call_thamso_str()) if ctx.func_call_thamso_str() else []
        return [func_name, params]


    # Visit a parse tree produced by MiniGoParser#func_call_thamso_str.
    def visitFunc_call_thamso_str(self, ctx:MiniGoParser.Func_call_thamso_strContext):
        params = []
        param_name = Id(ctx.ID().getText())
        param_type = self.visit(ctx.type_data())
        params.append(VariablesDecl(param_name, param_type))
        
        if ctx.COMMA():
            params.extend(self.visit(ctx.func_call_thamso_str()))
        
        return params


    # Visit a parse tree produced by MiniGoParser#array_literal.
    def visitArray_literal(self, ctx:MiniGoParser.Array_literalContext):
        typ_dimension = self.visit(ctx.type_array())
        typ = typ_dimension.typ
        dimension = typ_dimension.dimensions

        value = self.visit(ctx.list_expr())

        return ArrayLiteral(typ, dimension, value)


    # Visit a parse tree produced by MiniGoParser#type_array.
    def visitType_array(self, ctx:MiniGoParser.Type_arrayContext):
        dimensions = self.visit(ctx.list_type_arr())
        typ = self.visit(ctx.type_data())
        return ArrayType(typ, dimensions)


    # Visit a parse tree produced by MiniGoParser#list_type_arr.
    def visitList_type_arr(self, ctx:MiniGoParser.List_type_arrContext):
        if ctx.list_type_arr():
            return [int(ctx.getChild(1).getText(), 0)] + self.visit(ctx.list_type_arr())
        else:
            return [int(ctx.getChild(1).getText(), 0)]
        

    # Visit a parse tree produced by MiniGoParser#list_expr.
    def visitList_expr(self, ctx:MiniGoParser.List_exprContext):
        return self.visit(ctx.data_list_expr())
        


    # Visit a parse tree produced by MiniGoParser#data_list_expr.
    def visitData_list_expr(self, ctx:MiniGoParser.Data_list_exprContext):
        if ctx.COMMA():

            if ctx.INT_DEC() or ctx.INT_BIN() or ctx.INT_OCT() or ctx.INT_HEX():
                current = [IntLiteral(int(ctx.getChild(0).getText(), 0))]
            elif ctx.FLOAT_LIT():
                current = [FloatLiteral(float(ctx.FLOAT_LIT().getText()))]
            elif ctx.STRING_LIT():
                current = [StringLiteral(ctx.STRING_LIT().getText())]
            elif ctx.list_expr():
                current = [self.visit(ctx.list_expr())]
            elif ctx.expr():
                current = [self.visit(ctx.expr())]
            else:
                current = [self.visit(ctx.expr())]
            
            rest = self.visit(ctx.data_list_expr())

            return current + rest
            
        else:
            if ctx.INT_DEC() or ctx.INT_BIN() or ctx.INT_OCT() or ctx.INT_HEX():
                return [IntLiteral(int(ctx.getChild(0).getText(), 0))]
            elif ctx.FLOAT_LIT():
                return [FloatLiteral(float(ctx.FLOAT_LIT().getText()))]
            elif ctx.STRING_LIT():
                return [StringLiteral(ctx.STRING_LIT().getText())]
            elif ctx.list_expr():
                return [self.visit(ctx.list_expr())]
            else:
                return [self.visit(ctx.expr())]
            



    # Visit a parse tree produced by MiniGoParser#type_data.
    def visitType_data(self, ctx:MiniGoParser.Type_dataContext):
        if ctx.ID():
            return ClassType(Id(ctx.ID().getText()))
        elif ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BooleanType()
        elif ctx.STRING():
            return StringType()
        else:
            return self.visit(ctx.type_array())


    # Visit a parse tree produced by MiniGoParser#struct_literal.
    def visitStruct_literal(self, ctx:MiniGoParser.Struct_literalContext):
        name = Id(ctx.getChild(0).getText())

        if ctx.list_elements():
            value = self.visit(ctx.list_elements())
        else:
            value = []

        return StructLiteral(name, value)


    # Visit a parse tree produced by MiniGoParser#list_elements.
    def visitList_elements(self, ctx:MiniGoParser.List_elementsContext):
        elements = []
        if ctx.COMMA():
            id = Id(ctx.ID().getText())
            expr = self.visit(ctx.expr())
            elements = elements + [(id, expr)]

            elements.extend(self.visit(ctx.list_elements()))

        else:
            id = Id(ctx.ID().getText())
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
                method = func[0]
                param = func[1]
                return CallExpr(obj, method, param)
            else:
                vetrai = self.visit(ctx.getChild(0))
                vephai = Id(ctx.ID().getText())
                return FieldAccess(vetrai, vephai)

        else: 
            vetrai = self.visit(ctx.getChild(0))
            vephai = self.visit(ctx.getChild(2))
            return ArrayCell(vetrai, vephai)
            


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
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.NIL():
            return NilLiteral()
        elif ctx.struct_literal():
            return self.visit(ctx.struct_literal())
        
        elif ctx.array_literal():
            return self.visit(ctx.array_literal())
        
        elif ctx.func_call():
            func = self.visit(ctx.getChild(0))
            method = func[0]
            param = func[1]
            return CallExpr('', method, param)
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
        else:   
            return self.visit(ctx.expr())

    # Visit a parse tree produced by MiniGoParser#call_statement.

    def visitCall_statement(self, ctx:MiniGoParser.Call_statementContext):
        args = self.visit(ctx.func_call_thamso()) if ctx.func_call_thamso() else []
        method = Id(ctx.ID().getText())
        obj = self.visit(ctx.dot_assignment()) if ctx.dot_assignment() else None

        if isinstance(obj, FieldAccess):
            method = obj.fieldname  
            obj = obj.obj  

        temp = None
        temp2 = None

        if ctx.list_arr_index():
            indices = self.visit(ctx.list_arr_index())
            temp = ArrayCell(method, indices[0]) 
            temp2 = obj
        
        return CallStmt(temp, temp2, args)


    # Visit a parse tree produced by MiniGoParser#func_call.
    def visitFunc_call(self, ctx:MiniGoParser.Func_callContext):
        method = Id(ctx.ID().getText())
        if ctx.func_call_thamso():
            param = self.visit(ctx.func_call_thamso())
            return [method, param]
        else:
            return [method, []]


    # Visit a parse tree produced by MiniGoParser#func_call_thamso.
    def visitFunc_call_thamso(self, ctx:MiniGoParser.Func_call_thamsoContext):
        if ctx.func_call_thamso():
            return [self.visit(ctx.expr())] + self.visit(ctx.func_call_thamso())
        return [self.visit(ctx.expr())]
