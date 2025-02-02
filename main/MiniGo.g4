grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language = Python3;
}

program: (NEWLINE* list_declaration NEWLINE*)* EOF; // day

list_declaration: (array_literal | struct_literal | func_call | global_variable
             | global_constant | function | struct_type //| initialize_struct
            | interface_type | struct_func) ;

// program: NEWLINE* func_call_thamso EOF;

//TODO: PARSE

struct_type: TYPE ID STRUCT LBRACE NEWLINE* data_struct NEWLINE* RBRACE (SEMICOLON NEWLINE* | NEWLINE+);
data_struct: (ID type_data (SEMICOLON NEWLINE* | NEWLINE+)) data_struct | ;
// initialize_struct: ID COLONASSIGN ((ID list_expr) | (INT_DEC | INT_BIN | INT_OCT | INT_HEX));

interface_type: TYPE ID INTERFACE LBRACE NEWLINE* data_inter NEWLINE* RBRACE (SEMICOLON NEWLINE* | NEWLINE+);
data_inter: (initialize_inter (type_data | ) (SEMICOLON NEWLINE* | NEWLINE+)) data_inter | ; 
initialize_inter: ID LPAREN (list_interface | ) (type_data | ) RPAREN;
list_interface: data_inter_thamso_list COMMA list_interface | data_inter_thamso_list;
data_inter_thamso_list: data_inter_thamso type_data;
data_inter_thamso: ID  COMMA data_inter_thamso | ID ;

global_variable: VAR ID ((type_data ((ASSIGN (expr)) | )) | (ASSIGN (expr))) SEMICOLON;
local_variable: VAR ID ((type_data ((ASSIGN (expr)) | )) | (ASSIGN (expr)));

global_constant: CONST ID ASSIGN (expr) SEMICOLON;
local_constant: CONST ID ASSIGN (expr);


function: FUNC ID LPAREN (data_func | ) RPAREN (type_data | ) LBRACE NEWLINE* body_func NEWLINE* RBRACE;
data_func: (ID type_data) COMMA data_func | (ID type_data);
body_func: ((assignment_func | if_else | (RETURN (func_call | expr | )) | local_variable | local_constant | for_basic | for_icu | for_range
                | func_call | call_statement | BREAK | CONTINUE) (SEMICOLON NEWLINE* | NEWLINE+)) body_func | ; //day

assignment_func: (ID | ID arr_index | ID (list_arr_index | ) dot_assignment)
             (((COLONASSIGN | EQ | ADD_ASSIGN | SUB_ASSIGN | MUL_ASSIGN | DIV_ASSIGN | MOD_ASSIGN)
             expr));
dot_assignment: DOT (ID | (ID list_type_arr)) dot_assignment | DOT (ID | (ID list_type_arr));
list_arr_index: arr_index list_arr_index | arr_index;
arr_index: LBRACKET expr RBRACKET;


if_else: IF  LPAREN  expr  RPAREN NEWLINE* LBRACE NEWLINE* body_func NEWLINE* RBRACE NEWLINE* 
        (else_if | ) NEWLINE* (ELSE NEWLINE* LBRACE NEWLINE* body_func NEWLINE* RBRACE | );

else_if: (ELSE IF  LPAREN expr RPAREN NEWLINE* LBRACE NEWLINE* body_func NEWLINE* RBRACE) else_if | (ELSE IF  LPAREN expr RPAREN NEWLINE* LBRACE NEWLINE* body_func NEWLINE* RBRACE);

for_basic: FOR expr LBRACE NEWLINE* body_func NEWLINE* RBRACE;
for_icu: FOR (assignment_func | local_variable) SEMICOLON expr SEMICOLON assignment_func LBRACE NEWLINE* body_func NEWLINE* RBRACE;
for_range: FOR ID COMMA ID COLONASSIGN RANGE expr LBRACE NEWLINE* body_func NEWLINE* RBRACE;

struct_func: FUNC LPAREN method RPAREN func_call_str (type_data | ) LBRACE body_func RBRACE;
method: (ID type_data) COMMA method | (ID type_data);
func_call_str: ID LPAREN (func_call_thamso_str |  ) RPAREN;
func_call_thamso_str: (ID type_data) COMMA func_call_thamso_str | (ID type_data);

array_literal: type_array list_expr;
type_array: list_type_arr (type_data);
list_type_arr: (LBRACKET (INT_DEC | INT_BIN | INT_OCT | INT_HEX) RBRACKET) list_type_arr | (LBRACKET (INT_DEC | INT_BIN | INT_OCT | INT_HEX) RBRACKET);
list_expr: LBRACE data_list_expr RBRACE;
data_list_expr: (FLOAT_LIT | INT_DEC | INT_BIN | INT_OCT | INT_HEX | STRING_LIT | LBRACE expr RBRACE | list_expr | expr) COMMA data_list_expr | (FLOAT_LIT | INT_DEC | INT_BIN | INT_OCT | INT_HEX | STRING_LIT | LBRACE expr RBRACE | list_expr | expr);
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
call_statement: ID (list_arr_index | ) dot_assignment LPAREN (func_call_thamso |  ) RPAREN;
func_call: ID LPAREN (func_call_thamso |  ) RPAREN;
func_call_thamso: expr COMMA func_call_thamso | expr;

// ! ---------------- LEXER DEADLINE PASS 13 TEST CASE 23:59 16/1 ----------------------- */

//TODO Keywords 3.3.2 pdf
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

//TODO Operators 3.3.3 pdf
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

//TODO Separators 3.3.4 pdf
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACKET: '[';
RBRACKET: ']';
SEMICOLON: ';';
COMMA: ',';


//TODO Identifiers 3.3.1 pdf
ID: [a-zA-Z_][a-zA-Z0-9_]*;

//TODO Literals 3.3.5 pdf
FLOAT_LIT: INT_DEC DOT [0-9]* ([eE][+-]?INT_DEC)?;
//INTEGER_LIT: INT_DEC | INT_BIN | INT_OCT | INT_HEX;
INT_DEC: [0-9] | [1-9][0-9]+{
    self.text = str(int(self.text, 10))
};
INT_BIN: [0] [bB] [0-1]+{
    self.text = str(int(self.text, 2))
};
INT_OCT: [0] [oO] [0-7]+{
    self.text = str(int(self.text, 8))
};
INT_HEX: [0] [xX] [0-9a-fA-F]+{
    self.text = str(int(self.text, 16))
};
STRING_LIT: '"' STR_CHAR* '"'{
    self.text = self.text[1:-1]};
fragment STR_CHAR: ESC_SEQ | ~[\r\n\\"];
fragment ESC_SEQ: '\\' [trn"\\];
// INTERPRETED_STRING_LIT : '"' (~["\\] | ESCAPED_VALUE)* '"';

// fragment ESCAPED_VALUE:
//     '\\' (
//         'u' INT_HEX INT_HEX INT_HEX INT_HEX
//         | 'U' INT_HEX INT_HEX INT_HEX INT_HEX INT_HEX INT_HEX INT_HEX INT_HEX
//         | [abfnrtv\\'"]
//         | INT_OCT INT_OCT INT_OCT
//         | 'x' INT_HEX INT_HEX
//     )
// ;

fragment ESC_ILLEGAL: '\\' ~[trn"\\];


BOOLEAN_LIT: TRUE | FALSE;

//TODO skip 3.1 and 3.2 pdf

COMMENTS: '/*' (COMMENTS|.)*? '*/' -> skip;
COMMENTS_LINE: '//' ~[\r\n]* -> skip;
NEWLINE   : [\r\n]+;
WS: [ \t\f\r]+ -> skip; // skip spaces, tabs 

//TODO ERROR pdf BTL1 + lexererr.py
ERROR_CHAR: . {raise ErrorToken(self.text)};

UNCLOSE_STRING: '"' STR_CHAR* ('\r' | '\n' | EOF) {
    if(len(self.text) >= 2 and self.text[-1] == '\n' and self.text[-2] == '\r'):
        raise UncloseString(self.text[1:-2])
    elif (self.text[-1] == '\n'):
        raise UncloseString(self.text[1:-1])
    else:
        raise UncloseString(self.text[1:])
};

ILLEGAL_ESCAPE: '"' STR_CHAR* ESC_ILLEGAL {
    raise IllegalEscape(self.text[1:])
};

//! ---------------- LEXER ----------------------- */