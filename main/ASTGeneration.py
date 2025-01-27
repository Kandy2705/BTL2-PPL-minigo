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
        return Program(self.visit(ctx.func_call_thamso()))


    # Visit a parse tree produced by MiniGoParser#struct_type.
    def visitStruct_type(self, ctx:MiniGoParser.Struct_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#data_struct.
    def visitData_struct(self, ctx:MiniGoParser.Data_structContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#initialize_struct.
    def visitInitialize_struct(self, ctx:MiniGoParser.Initialize_structContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#interface_type.
    def visitInterface_type(self, ctx:MiniGoParser.Interface_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#data_inter.
    def visitData_inter(self, ctx:MiniGoParser.Data_interContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#initialize_inter.
    def visitInitialize_inter(self, ctx:MiniGoParser.Initialize_interContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#data_inter_thamso.
    def visitData_inter_thamso(self, ctx:MiniGoParser.Data_inter_thamsoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#global_variable.
    def visitGlobal_variable(self, ctx:MiniGoParser.Global_variableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#local_variable.
    def visitLocal_variable(self, ctx:MiniGoParser.Local_variableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#global_constant.
    def visitGlobal_constant(self, ctx:MiniGoParser.Global_constantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#local_constant.
    def visitLocal_constant(self, ctx:MiniGoParser.Local_constantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#function.
    def visitFunction(self, ctx:MiniGoParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#data_func.
    def visitData_func(self, ctx:MiniGoParser.Data_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#body_func.
    def visitBody_func(self, ctx:MiniGoParser.Body_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#assignment_func.
    def visitAssignment_func(self, ctx:MiniGoParser.Assignment_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#dot_assignment.
    def visitDot_assignment(self, ctx:MiniGoParser.Dot_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#list_arr_index.
    def visitList_arr_index(self, ctx:MiniGoParser.List_arr_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#arr_index.
    def visitArr_index(self, ctx:MiniGoParser.Arr_indexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#if_else.
    def visitIf_else(self, ctx:MiniGoParser.If_elseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#else_if.
    def visitElse_if(self, ctx:MiniGoParser.Else_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#for_basic.
    def visitFor_basic(self, ctx:MiniGoParser.For_basicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#for_icu.
    def visitFor_icu(self, ctx:MiniGoParser.For_icuContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#for_range.
    def visitFor_range(self, ctx:MiniGoParser.For_rangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#struct_func.
    def visitStruct_func(self, ctx:MiniGoParser.Struct_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#func_call_str.
    def visitFunc_call_str(self, ctx:MiniGoParser.Func_call_strContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#func_call_thamso_str.
    def visitFunc_call_thamso_str(self, ctx:MiniGoParser.Func_call_thamso_strContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniGoParser#array_literal.
    def visitArray_literal(self, ctx:MiniGoParser.Array_literalContext):
        typ_dimension = self.visit(ctx.type_array())
        typ = typ_dimension[0]
        dimension = typ_dimension[1]

        value = self.visit(ctx.list_expr())

        return ArrayLiteral(typ, dimension, value)


    # Visit a parse tree produced by MiniGoParser#type_array.
    def visitType_array(self, ctx:MiniGoParser.Type_arrayContext):
        dimensions = self.visit(ctx.list_type_arr())
        typ = self.visit(ctx.type_data())
        return (typ, dimensions)


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
            return Id(ctx.ID().getText())
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

        return self.visitChildren(ctx)


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
