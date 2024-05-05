program -> block
block -> BEGIN operator_list END
operator_list -> operator
operator_list -> operator_list SEP operator
operator -> id ASSIGN expr
expr -> arithExpr RELOP arithExpr
expr -> arithExpr
arithExpr -> arithExpr PLUSOP term
arithExpr -> term
term -> term MULTOP factor
term -> factor
factor -> id
factor -> const
factor -> LEFT_PAREN arithExpr RIGHT_PAREN
id -> ID
id -> INTEGER
const -> CONST

BEGIN = begin
END = end
LEFT_PAREN = \(
RIGHT_PAREN = \)
RELOP = [(<)(<=)(=)(<>)(>)(>=)]
PLUSOP = [+-]
MULTOP = [*/]
ID = [a-zA-Z][a-zA-Z0-9]*
CONST = [a-zA-Z][a-zA-Z0-9]*
FLOAT = [0-9]+.[0-9]+
INTEGER = [0-9]+
SEP = ;
ASSIGN = =
