# Global dictionary used for storing the rules.
RULE_DICT = {}


def read_grammar(grammar_file):
    with open(grammar_file) as cfg:
        lines = cfg.readlines()
    return [x.replace("->", "").split() for x in lines]


def add_rule(rule):
    global RULE_DICT

    if rule[0] not in RULE_DICT:
        RULE_DICT[rule[0]] = []
    RULE_DICT[rule[0]].append(rule[1:])


def convert_grammar_to_cnf(grammar):
    """
    На вход должны поступить приведенная КС-грамматика 
    (без эпсилон-правил, без цепных правил и без циклов)
    """

    global RULE_DICT
    unit_productions, result = [], []
    index = 0

    for rule in grammar:
        new_rules = []
        if len(rule) == 2 and rule[1][0] != "'":
            # Если продукция состоит из одного нетерминала
            unit_productions.append(rule)
            add_rule(rule)
            continue

        elif len(rule) > 2:
            # Если правило имеет вид `A -> X1 X2 ... Xk` или `A -> X1 X2` 
            terminals = [(item, i) for i, item in enumerate(rule) if item[0] == "'"]
            if terminals:
                # Если правило содержит терминал, то вводится правило `A -> X1' X2'`
                for item in terminals:
                    # Заменяем в правиле терминал на нетерминал
                    rule[item[1]] = f"{rule[0]}{str(index)}"
                    # Добавляем правило `Xi' -> Xi`, где Xi - терминал
                    new_rules.append([f"{rule[0]}{str(index)}", item[0]])
                index += 1
            while len(rule) > 3:
                # Добавляем правило `Xi' -> Xi`
                new_rules.append([f"{rule[0]}{str(index)}", rule[1], rule[2]])
                # Добавляем правило `A -> Xi' <Xk-1 Xk>`
                rule = [rule[0]] + [f"{rule[0]}{str(index)}"] + rule[3:]
                index += 1

        add_rule(rule)
        result.append(rule)
        if new_rules:
            result.extend(new_rules)

    while unit_productions:
        # Удаление цепных правил
        rule = unit_productions.pop()
        if rule[1] in RULE_DICT:
            for item in RULE_DICT[rule[1]]:
                new_rule = [rule[0]] + item
                if len(new_rule) > 2 or new_rule[1][0] == "'":
                    result.insert(0, new_rule)
                else:
                    unit_productions.append(new_rule)
                add_rule(new_rule)

    return result