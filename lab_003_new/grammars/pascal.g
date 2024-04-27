program -> block
block -> 'begin' operator_list 'end'
operator_list -> operator
operator_list -> operator_list ';' operator
operator -> id '=' expr
expr -> arithExpr relOp arithExpr
expr -> arithExpr
arithExpr -> arithExpr plusOp term
arithExpr -> term
term -> term multOp factor
term -> factor
factor -> id
factor -> const
factor -> '(' arithExpr ')'
relOp -> RELOP
relOp -> RELOP
relOp -> RELOP
relOp -> RELOP
relOp -> RELOP
relOp -> RELOP
plusOp -> PLUSOP
plusOp -> PLUSOP
multOp -> MULTOP
multOp -> MULTOP
id -> ID
const -> CONST

BEGIN = begin
END = end
RELOP = [(<)(<=)(=)(<>)(>)(>=)]
PLUSOP = [(+)(-)]
MULTOP = [(*)(/)]
ID = [a-zA-Z][a-zA-Z0-9]*
CONST = [a-zA-Z][a-zA-Z0-9]*
FLOAT = [0-9]+.[0-9]+
INTEGER = [0-9]+
SEP = ;