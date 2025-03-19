// 2212009

grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {
prevtoken = None
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        self.prevtoken = result;
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        self.prevtoken = result;
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        self.prevtoken = result;
        raise ErrorToken(result.text); 
    else:
        result = super().emit()
        self.prevtoken = result
        return result
}

options{
	language = Python3;
}

program: list_declaration EOF; // day

list_declaration: (array_literal | global_variable
             | global_constant | function | struct_type
            | interface_type | struct_func) list_declaration | (array_literal | global_variable
             | global_constant | function | struct_type
            | interface_type | struct_func);

// program: NEWLINE* func_call_thamso EOF;

//TODO: PARSE

struct_type: TYPE ID STRUCT LBRACE data_struct RBRACE (SEMICOLON);
data_struct: (ID type_data (SEMICOLON)) data_struct | (ID type_data (SEMICOLON));//sua day
// initialize_struct: ID COLONASSIGN ((ID list_expr) | (INT_DEC | INT_BIN | INT_OCT | INT_HEX));

interface_type: TYPE ID INTERFACE LBRACE  data_inter  RBRACE (SEMICOLON);
data_inter: (initialize_inter (type_data | ) (SEMICOLON)) data_inter | (initialize_inter (type_data | ) (SEMICOLON)); //sua day
initialize_inter: ID LPAREN (list_interface | ) (type_data | ) RPAREN;
list_interface: data_inter_thamso_list COMMA list_interface | data_inter_thamso_list;
data_inter_thamso_list: data_inter_thamso type_data;
data_inter_thamso: ID  COMMA data_inter_thamso | ID ;

global_variable: VAR ID ((type_data ((ASSIGN (expr)) | )) | (ASSIGN (expr))) SEMICOLON;
local_variable: VAR ID ((type_data ((ASSIGN (expr)) | )) | (ASSIGN (expr)));

global_constant: CONST ID ASSIGN (expr) SEMICOLON;
local_constant: CONST ID ASSIGN (expr);


function: FUNC func_call_str (type_data | ) LBRACE  body_func  RBRACE SEMICOLON; //sua day
data_func: (ID type_data) COMMA data_func | (ID type_data);
body_func: ((assignment_func | if_else | (RETURN (func_call | expr | )) | local_variable | local_constant | for_basic | for_icu | for_range
                | func_call | call_statement | BREAK | CONTINUE) (SEMICOLON)) body_func | ; //sua day

assignment_func: (dot)
             (((COLONASSIGN | EQ | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN)
             expr));
dot: dot (DOT ID | LBRACKET expr RBRACKET) | ID;          
assignment_for: ID (((COLONASSIGN | EQ | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN)
             expr));


if_else: IF  LPAREN  expr  RPAREN  LBRACE  body_func  RBRACE  
        (else_if | )  (ELSE  LBRACE  body_func  RBRACE | );

else_if: (ELSE IF  LPAREN expr RPAREN  LBRACE  body_func  RBRACE) else_if | (ELSE IF  LPAREN expr RPAREN  LBRACE  body_func  RBRACE);

for_basic: FOR expr LBRACE  body_func  RBRACE ;
for_icu: FOR (assignment_for | var_for) SEMICOLON expr SEMICOLON assignment_for LBRACE  body_func  RBRACE ;
for_range: FOR ID COMMA ID COLONASSIGN RANGE expr LBRACE  body_func  RBRACE ;

var_for: VAR ID ((type_data ((ASSIGN (expr)))) | (ASSIGN (expr)));

struct_func: FUNC LPAREN method RPAREN func_call_str (type_data | ) LBRACE body_func RBRACE SEMICOLON;
method: (ID ID) COMMA method | (ID ID); //sua day
func_call_str: ID LPAREN (func_call_thamso_str |  ) RPAREN;
func_call_thamso_str: (data_inter_thamso type_data) COMMA func_call_thamso_str | (data_inter_thamso type_data); //sua day

array_literal: type_array list_expr;
type_array: list_type_arr (type_data);
list_type_arr: (LBRACKET (INT_DEC | INT_BIN | INT_OCT | INT_HEX | ID) RBRACKET) list_type_arr | (LBRACKET (INT_DEC | INT_BIN | INT_OCT | INT_HEX | ID) RBRACKET);
list_expr: LBRACE data_list_expr RBRACE;
data_list_expr: (TRUE | FALSE | NIL | FLOAT_LIT | INT_DEC | INT_BIN | INT_OCT | INT_HEX | STRING_LIT | struct_literal | list_expr | ID) COMMA data_list_expr | (TRUE | FALSE | NIL | FLOAT_LIT | INT_DEC | INT_BIN | INT_OCT | INT_HEX | STRING_LIT | struct_literal | list_expr | ID); //sua day
type_data: ID | INT | FLOAT | BOOLEAN | STRING | type_array;

struct_literal: ID LBRACE (list_elements | ) RBRACE;
list_elements: (ID COLON expr) COMMA list_elements | (ID COLON expr);

//list_expression: expr COMMA list_expression | expr;
expr: expr OR expr1 | expr1;
expr1: expr1 AND expr2 | expr2;
expr2: expr2 (LT | LE | GT | GE | EQ | NE) expr3 | expr3;
expr3: expr3 (ADD | SUB) expr4 | expr4;
expr4: expr4 (MUL | DIV | MOD) expr5 | expr5;
expr5: (NOT | SUB) expr5 | expr6;
expr6: expr6 (DOT (ID | func_call) | LBRACKET expr RBRACKET) | expr7;
expr7: ID | INT_DEC | INT_BIN | INT_OCT | INT_HEX | FLOAT_LIT | LPAREN expr RPAREN | 
        func_call | STRING_LIT | struct_literal | array_literal | TRUE | FALSE | NIL;

// func_call: ((ID (list_arr_index | ) DOT) | ) ID LPAREN (func_call_thamso |  ) RPAREN;
call_statement: dot DOT ID LPAREN (func_call_thamso |  ) RPAREN;
func_call: ID LPAREN (func_call_thamso |  ) RPAREN;
func_call_thamso: expr COMMA func_call_thamso | expr;

//LEXER

//Keywords
IF: 'if';
ELSE: 'else';
FOR: 'for';
RETURN: 'return';
FUNC: 'func';
TYPE: 'type';
STRUCT: 'struct';
INTERFACE: 'interface';
STRING: 'string';
INT: 'int';
FLOAT: 'float';
BOOLEAN: 'boolean';
CONST: 'const';
VAR: 'var';
CONTINUE: 'continue';
BREAK: 'break';
RANGE: 'range';
NIL: 'nil';
TRUE: 'true';
FALSE: 'false';

//Operators
DOT: '.';
COLONASSIGN: ':=';
COLON: ':';

LT: '<';
LE: '<=';
GT: '>';
GE: '>=';
EQ: '==';
NE: '!=';

ASSIGN: '=';
ADD_ASSIGN: '+=';
SUB_ASSIGN: '-=';
MUL_ASSIGN: '*=';
DIV_ASSIGN: '/=';
MOD_ASSIGN: '%=';

AND: '&&';
OR: '||';
NOT: '!';

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';

//Separators
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACKET: '[';
RBRACKET: ']';
SEMICOLON: ';';
COMMA: ',';


//Identifiers
ID: [a-zA-Z_][a-zA-Z0-9_]*;

//Literals
FLOAT_LIT: [0]* INT_DEC DOT [0-9]* ([eE][+-]? [0]* INT_DEC)?;
//INTEGER_LIT: INT_DEC | INT_BIN | INT_OCT | INT_HEX;
INT_DEC: ([0-9] | [1-9][0-9]+);
INT_BIN: [0] [bB] [0-1]+ ;
INT_OCT: [0] [oO] [0-7]+ ;
INT_HEX: [0] [xX] [0-9a-fA-F]+ ;
STRING_LIT: '"' STR_CHAR* '"';
fragment STR_CHAR: ESC_SEQ | ~[\r\n\\"];
fragment ESC_SEQ: '\\' [trn"\\];

fragment ESC_ILLEGAL: '\\' ~[trn"\\];


BOOLEAN_LIT: TRUE | FALSE;

//skip

NEWLINE   : ('\r'? '\n')+ {
    if self.prevtoken is not None and self.prevtoken.type in {
        self.ID, self.RPAREN, self.RBRACKET, self.RBRACE,
        self.INT_DEC, self.INT_BIN, self.INT_OCT, self.INT_HEX,
        self.FLOAT_LIT, self.TRUE, self.FALSE, self.STRING_LIT,
        self.RETURN, self.CONTINUE, self.BREAK,
        self.INT, self.FLOAT, self.BOOLEAN, self.STRING, self.NIL
    }:
        self.text = ";"
        self.type = self.SEMICOLON
        
    else:
        self.skip()
        
};

WS: [ \t\f\r]+ -> skip;
COMMENTS: '/*' (COMMENTS|.)*? '*/' -> skip;
COMMENTS_LINE: '//' ~[\r\n]* -> skip;

//ERROR
ERROR_CHAR: . {raise ErrorToken(self.text)};

UNCLOSE_STRING: '"' STR_CHAR* ('\r\n' | '\n' | EOF) {
    if(len(self.text) >= 2 and self.text[-1] == '\n' and self.text[-2] == '\r'):
        raise UncloseString(self.text[0:-2])
    elif (self.text[-1] == '\n'):
        raise UncloseString(self.text[0:-1])
    else:
        raise UncloseString(self.text[0:])
};

ILLEGAL_ESCAPE: '"' STR_CHAR* ESC_ILLEGAL {
    raise IllegalEscape(self.text[0:])
};

//! LEXER