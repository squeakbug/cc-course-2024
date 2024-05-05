expr -> arithExpr RELOP arithExpr           {expr.val = RELOP arithExpr_1.val arithExpr_2.val}
expr -> arithExpr                           {expr.val = arithExpr.val}
arithExpr -> arithExpr PLUSOP term          {arithExpr.val = PLUSOP arithExpr.val term.val}
arithExpr -> term                           {arithExpr.val = term.val}
term -> term MULTOP factor                  {term.val = MULTOP term.val factor.val}
term -> factor                              {term.val = factor.val}
factor -> id                                {factor.val = id.val}
factor -> const                             {factor.val = const.val}
factor -> LEFT_PAREN arithExpr RIGHT_PAREN  {factor.val = LEFT_PAREN arithExpr RIGHT_PAREN}
id -> ID                                    {id.val = ID}
id -> INTEGER                               {id.val = int(INTEGER)}
const -> CONST                              {const.val = int(CONST)}

LEFT_PAREN = \(
RIGHT_PAREN = \)
RELOP = [(<)(<=)(=)(<>)(>)(>=)]
PLUSOP = [+-]
MULTOP = [*/]
ID = [a-zA-Z][a-zA-Z0-9]*
CONST = [a-zA-Z][a-zA-Z0-9]*
FLOAT = [0-9]+.[0-9]+
INTEGER = [0-9]+
