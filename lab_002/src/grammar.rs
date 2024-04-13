#![allow(dead_code)]

use std::collections::{HashMap, HashSet};

#[derive(Clone, Debug, Hash, Eq, PartialEq)]
pub enum RightRulePart {
    Eps,
    Sym(Vec<String>),
}

#[derive(Clone, Debug, Hash, Eq, PartialEq)]
pub struct CFGRule {
    pub left: String,
    pub right: RightRulePart,
}

#[derive(Clone)]
pub enum RightRulePartStr {
    Eps,
    Sym(Vec<&'static str>),
}

#[derive(Clone)]
pub struct CFGRuleStr {
    pub left: &'static str,
    pub right: RightRulePartStr,
}

#[derive(Debug, Eq, PartialEq)]
pub struct CFG {
    pub terms: HashSet<String>,
    pub non_terms: HashSet<String>,
    pub rules: HashSet<CFGRule>,
    pub start_sym: String,
}

impl CFG {
    pub fn new(
        terms: Vec<&'static str>,
        non_terms: Vec<&'static str>,
        rules: Vec<CFGRuleStr>,
        start_sym: &'static str,
    ) -> Self {
        let rules = rules
            .into_iter()
            .map(|rule| CFGRule {
                left: String::from(rule.left),
                right: match rule.right {
                    RightRulePartStr::Eps => RightRulePart::Eps,
                    RightRulePartStr::Sym(right) => {
                        RightRulePart::Sym(right.into_iter().map(|r| String::from(r)).collect())
                    }
                },
            })
            .collect();
        let non_terms = non_terms.into_iter().map(|nt| String::from(nt)).collect();
        let terms = terms.into_iter().map(|t| String::from(t)).collect();
        let start_sym = String::from(start_sym);
        Self {
            non_terms,
            rules,
            start_sym,
            terms,
        }
    }

    fn get_rules_by_term(&self, left: &String) -> Vec<&CFGRule> {
        self.rules
            .iter()
            .filter_map(|prod| match &prod.left {
                x if x == left => Some(prod),
                _ => None,
            })
            .collect()
    }

    fn remove_rules_by_term(&mut self, left: &String) {
        let new_rules: HashSet<CFGRule> = self
            .rules
            .iter()
            .filter_map(|prod| match &prod.left {
                x if x != left => Some(prod),
                _ => None,
            })
            .cloned()
            .collect();
        self.rules = new_rules;
    }

    // Автор знает, что идеоматичнее было бы описать тип-итератор над продукциями,
    // чтобы в одном scope не было mutable borrow и immutable borrow
    // Но так как по условию не требуется оптимизировать программу, то текущее решение допустимо
    fn add_new_rules(&mut self, aj: &String, ai: &String, ai_right: &Vec<String>) {
        let chains_j: Vec<CFGRule> = self.get_rules_by_term(aj).into_iter().cloned().collect();
        for chain_j in chains_j.iter() {
            let ref trj_right = chain_j.right;
            if let RightRulePart::Sym(ref right_j) = trj_right {
                let mut new_vec = right_j.clone();
                new_vec.extend(ai_right.clone().into_iter().skip(1));
                let new_rule = CFGRule {
                    left: ai.clone(),
                    right: RightRulePart::Sym(new_vec),
                };
                self.rules.insert(new_rule);
            }
        }
    }

    /// Преобразование грамматики к форме без косвенной левой рекурсии
    pub fn elim_left_rec(&mut self) {
        let mut non_terms = Vec::from_iter(self.non_terms.iter().cloned());
        non_terms.sort();
        for i in 0..non_terms.len() {
            for j in 0..i {
                let chains_i: Vec<CFGRule> = self.get_rules_by_term(&non_terms[i]).into_iter().cloned().collect();
                self.remove_rules_by_term(&non_terms[i]);
                for chain in chains_i.into_iter() {
                    // Проходимся по всем продукциями с левой частью Ai
                    if let RightRulePart::Sym(ref right) = chain.right {
                        // Если правая часть не Eps, а строка
                        if let Some(ft) = right.first() {
                            // Если справа ненулевая строка
                            if ft == &non_terms[j] {
                                // Если первый символ правой части нетерминала Ai совпадает с нетерминалом Aj
                                // Заменяем продукцию с нетерминалом Aj на продукции с правыми частями от Ai
                                self.add_new_rules(&non_terms[j], &non_terms[i], right);
                            }
                        }
                    }
                }
            }
            self.elim_left_rec_simple();
        }
    }

    /// Преобразование грамматики к форме без правил вида `A -> Ax`
    pub fn elim_left_rec_simple(&mut self) {
        let lr_terms: HashSet<String> = self
            .rules
            .iter()
            .filter_map(|rule| {
                if let RightRulePart::Sym(right) = &rule.right {
                    if let Some(ft) = right.first() {
                        if ft == &rule.left {
                            return Some(&rule.left);
                        }
                    }
                }
                return None;
            })
            .cloned()
            .collect();

        for term in lr_terms.iter() {
            self.elim_left_rec_term(term);
        }
    }

    fn elim_left_rec_term(&mut self, term: &String) {
        let mut new_rules: HashSet<CFGRule> = HashSet::new();
        for rule in self.rules.iter() {
            if &rule.left == term {
                if let RightRulePart::Sym(right) = &rule.right {
                    if let Some(ft) = right.first() {
                        let new_rule: CFGRule;
                        let mut new_right;
                        let new_left;
                        if ft == &rule.left {
                            let left_cloned = rule.left.clone();
                            new_left = format!("{left_cloned}'");
                            new_right = right[1..].to_vec();
                            new_right.push(new_left.clone());

                            let eps_rule = CFGRule {
                                left: new_left.clone(),
                                right: RightRulePart::Eps,
                            };
                            new_rules.insert(eps_rule);
                        } else {
                            new_left = rule.left.clone();
                            let left_cloned = rule.left.clone();
                            new_right = right.clone();
                            new_right.push(format!("{left_cloned}'").clone());
                        }
                        self.non_terms.insert(new_left.clone());
                        new_rule = CFGRule {
                            left: new_left,
                            right: RightRulePart::Sym(new_right),
                        };
                        new_rules.insert(new_rule);
                    }
                } else {
                    new_rules.insert(rule.clone());
                }
            } else {
                new_rules.insert(rule.clone());
            }
        }

        self.rules = new_rules;
    }

    // Получение нетерминалов, из которых выводимы eps (пустой символ)
    fn get_eps_gen_nonterms(&self) -> HashSet<String> {
        let mut eps_nonterms_pred = HashSet::<String>::new();
        let mut eps_nonterms_cur = HashSet::<String>::new();

        for rule in self.rules.iter() {
            if let RightRulePart::Eps = rule.right {
                eps_nonterms_cur.insert(rule.left.clone());
            }
        }

        while eps_nonterms_pred != eps_nonterms_cur {
            eps_nonterms_pred = eps_nonterms_cur.clone();
            for rule in self.rules.iter() {
                let mut is_w_in_right: bool = true;
                if let RightRulePart::Sym(ref right) = rule.right {
                    for sym in right.iter() {
                        if !eps_nonterms_pred.contains(sym) {
                            is_w_in_right = false;
                        }
                    }
                }
                if is_w_in_right {
                    eps_nonterms_cur.insert(rule.left.clone());
                }
            }
        }

        eps_nonterms_cur
    }

    // Удаление всех правила вида `A -> eps`
    fn remove_eps_rules(&mut self) {
        let new_rules: HashSet<CFGRule> = self
            .rules
            .iter()
            .filter_map(|prod| match &prod.right {
                RightRulePart::Eps => None,
                _ => Some(prod),
            })
            .cloned()
            .collect();
        self.rules = new_rules;
    }

    // Добавляет правила `S' -> eps` и `S' -> S`
    fn change_start_sym(&mut self) {
        let start_sym = self.start_sym.clone();
        let new_start_sym = format!("{start_sym}'");
        let eps_rule = CFGRule {
            left: new_start_sym.clone(),
            right: RightRulePart::Eps,
        };
        self.rules.insert(eps_rule);

        let start_rule = CFGRule {
            left: new_start_sym.clone(),
            right: RightRulePart::Sym(vec![start_sym]),
        };
        self.rules.insert(start_rule);

        self.non_terms.insert(new_start_sym.clone());
        self.start_sym = new_start_sym;
    }

    pub fn get_right_parts(&self, syms: Vec<String>, eps_get_nonterms: &HashSet<String>) -> Vec<Vec<String>> {
        let new_firsts = if let Some(first) = syms.first() {
            if eps_get_nonterms.contains(first) {
                vec![vec![String::from("")], vec![first.clone()]]
            } else {
                vec![vec![first.clone()]]
            }
        } else {
            return vec![];
        };

        let rem = Vec::from(&syms[1..]);
        let rem_rules = self.get_right_parts(rem, eps_get_nonterms);
        let mut result: Vec<Vec<String>> = vec![];
        for new_first in new_firsts.iter() {
            let mut rule_result: Vec<Vec<String>> = vec![];
            if rem_rules.len() == 0 {
                rule_result.push(new_first.clone());
            } else {
                for new_rule in rem_rules.iter() {
                    let mut new_first_cloned = new_first.clone();
                    new_first_cloned.extend(new_rule.clone());
                    rule_result.push(new_first_cloned);
                }
            }
            result.extend(rule_result);
        }
        result
    }

    pub fn get_new_rules(&self, base_rule: &CFGRule, eps_get_nonterms: &HashSet<String>) -> Vec<CFGRule> {
        let mut result: Vec<CFGRule> = vec![];
        if let RightRulePart::Sym(ref right) = base_rule.right {
            let new_rights = self.get_right_parts(right.clone(), &eps_get_nonterms);
            let new_rights = new_rights.into_iter().map(|right_rule| {
                right_rule.into_iter().filter(|s| !s.is_empty()).collect::<Vec<String>>()
            }).collect::<Vec<Vec<String>>>();

            for new_right in new_rights.into_iter() {
                let new_rule = CFGRule {
                    left: base_rule.left.clone(),
                    right: RightRulePart::Sym(new_right)
                };
                result.push(new_rule);
            }
        }
        result
    }

    /// Преобразование грамматики к форме без eps-правил
    pub fn elim_eps_rules(&mut self) {
        let eps_gen_nonterms = self.get_eps_gen_nonterms();

        let mut new_rules: HashSet<CFGRule> = HashSet::new();
        for rule in self.rules.iter() {
            let new_rule = self.get_new_rules(&rule, &eps_gen_nonterms);
            new_rules.extend(new_rule);
        }
        self.rules = new_rules;

        self.remove_eps_rules();
        if eps_gen_nonterms.contains(&self.start_sym) {
            self.change_start_sym();
        }
    }

    fn get_chain_pair(&self, nt: &String) -> HashSet<String> {
        let mut set_cur = HashSet::from_iter(vec![nt.clone()]);
        let mut set_pred = HashSet::new();

        while set_pred != set_cur {
            set_pred = set_cur.clone();
            for rule in self.rules.iter() {
                if set_pred.contains(&rule.left) {
                    if let RightRulePart::Sym(ref right) = rule.right {
                        if let Some(rt) = right.first() {
                            if right.len() == 1 && self.non_terms.contains(rt) {
                                set_cur.insert(rt.clone());
                            }
                        }
                    }
                }
            }
        }

        set_cur
    }

    fn get_chain_pairs(&self) -> HashMap<String, HashSet<String>> {
        let mut result = HashMap::new();
        for nt in self.non_terms.iter() {
            let pair = self.get_chain_pair(nt);
            result.insert(nt.clone(), pair);
        }
        result
    }

    fn remove_chain_pairs(&mut self) {
        let new_rules: HashSet<CFGRule> = self
            .rules
            .iter()
            .filter_map(|prod| {
                if let RightRulePart::Sym(ref right) = prod.right {
                    if let Some(term) = right.first() {
                        if self.non_terms.contains(&prod.left) && right.len() == 1 && self.non_terms.contains(term) {
                            None
                        } else {
                            Some(prod)
                        }
                    } else {
                        None
                    }
                } else {
                    None
                }
            })
            .cloned()
            .collect();
        self.rules = new_rules;
    }

    /// Преобразование грамматики к форме без цепных правил
    pub fn elim_chain_rules(&mut self) {
        self.elim_eps_rules();
        let chain_pairs = self.get_chain_pairs();

        let mut new_rules = HashSet::new();
        for rule in self.rules.iter() {
            for (chain_key, chain_val) in chain_pairs.iter() {
                if chain_val.contains(&rule.left) {
                    let new_rule = CFGRule {
                        left: chain_key.clone(),
                        right: rule.right.clone(),
                    };
                    new_rules.insert(new_rule);
                }
            }
        }
        self.rules = new_rules;

        self.remove_chain_pairs();
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use super::{CFGRuleStr, RightRulePartStr, CFG};

    #[test]
    pub fn test_elim_left_rec_simple() {
        let terms = vec!["a", "+", "*", "(", ")"];
        let non_terms = vec!["F", "E", "T"];
        let rules = vec![
            CFGRuleStr {
                left: "E",
                right: RightRulePartStr::Sym(vec!["E", "+", "T"]),
            },
            CFGRuleStr {
                left: "E",
                right: RightRulePartStr::Sym(vec!["T"]),
            },
            CFGRuleStr {
                left: "T",
                right: RightRulePartStr::Sym(vec!["T", "*", "F"]),
            },
            CFGRuleStr {
                left: "T",
                right: RightRulePartStr::Sym(vec!["F"]),
            },
            CFGRuleStr {
                left: "F",
                right: RightRulePartStr::Sym(vec!["(", "E", ")"]),
            },
            CFGRuleStr {
                left: "F",
                right: RightRulePartStr::Sym(vec!["a"]),
            },
        ];
        let start_sym = "E";
        let mut cfg = CFG::new(terms, non_terms, rules, start_sym);

        cfg.elim_left_rec_simple();
    }

    #[test]
    pub fn test_elim_left_rec() {
        let terms = vec!["a", "b", "c", "d"];
        let non_terms = vec!["A", "S"];
        let rules = vec![
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["A", "a"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["b"]),
            },
            CFGRuleStr {
                left: "A",
                right: RightRulePartStr::Sym(vec!["A", "c"]),
            },
            CFGRuleStr {
                left: "A",
                right: RightRulePartStr::Sym(vec!["S", "d"]),
            },
        ];
        let start_sym = "S";
        let mut cfg = CFG::new(terms, non_terms, rules, start_sym);

        cfg.elim_left_rec();

        let target_terms = vec!["a", "b", "c", "d"];
        let target_non_terms = vec!["A", "S", "A'", "S'"];
        let target_rules = vec![
            CFGRuleStr {
                left: "S'",
                right: RightRulePartStr::Eps,
            },
            CFGRuleStr {
                left: "A'",
                right: RightRulePartStr::Sym(vec!["c", "A'"]),
            },
            CFGRuleStr {
                left: "S'",
                right: RightRulePartStr::Sym(vec!["d", "A'", "a", "S'"]),
            },
            CFGRuleStr {
                left: "A",
                right: RightRulePartStr::Sym(vec!["S", "d", "A'"]),
            },
            CFGRuleStr {
                left: "A'",
                right: RightRulePartStr::Eps,
            },
        ];
        let target_start_sym = "S";
        let target_cfg = CFG::new(target_terms, target_non_terms, target_rules, target_start_sym);

        assert_eq!(target_cfg, cfg);
        println!("cfg = {:?}", cfg);
    }

    #[test]
    pub fn test_elim_eps_rules() {
        let terms = vec!["a", "b", "c", "d"];
        let non_terms = vec!["A", "S"];
        let rules = vec![
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["A", "a"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["b"]),
            },
            CFGRuleStr {
                left: "A",
                right: RightRulePartStr::Sym(vec!["A", "c"]),
            },
            CFGRuleStr {
                left: "A",
                right: RightRulePartStr::Sym(vec!["S", "d"]),
            },
            CFGRuleStr {
                left: "A",
                right: RightRulePartStr::Eps,
            },
        ];
        let start_sym = "S";
        let mut cfg = CFG::new(terms, non_terms, rules, start_sym);

        print!("cfg =\n{:?}\n", cfg);
        cfg.elim_eps_rules();
        print!("cfg =\n{:?}\n", cfg);
    }

    #[test]
    pub fn test_elim_eps_rules_default() {
        let terms = vec!["a", "b"];
        let non_terms = vec!["S"];
        let rules = vec![
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["a", "S", "b", "S"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["b", "S", "a", "S"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Eps,
            },
        ];
        let start_sym = "S";
        let mut cfg = CFG::new(terms, non_terms, rules, start_sym);

        cfg.elim_eps_rules();

        let target_terms = vec!["a", "b"];
        let target_non_terms = vec!["S", "S'"];
        let target_rules = vec![
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["a", "S", "b", "S"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["a", "b", "S"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["a", "S", "b"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["a", "b"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["b", "S", "a", "S"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["b", "a", "S"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["b", "S", "a"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["b", "a"]),
            },
            CFGRuleStr {
                left: "S'",
                right: RightRulePartStr::Eps,
            },
            CFGRuleStr {
                left: "S'",
                right: RightRulePartStr::Sym(vec!["S"]),
            },
        ];
        let target_start_sym = "S'";
        let target_cfg = CFG::new(target_terms, target_non_terms, target_rules, target_start_sym);

        assert_eq!(target_cfg, cfg)
    }

    #[test]
    pub fn test_get_right_parts() {
        let terms = vec!["a", "b", "c", "d"];
        let non_terms = vec!["A", "S"];
        let rules = vec![
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["A", "a"]),
            },
            CFGRuleStr {
                left: "S",
                right: RightRulePartStr::Sym(vec!["b"]),
            },
            CFGRuleStr {
                left: "A",
                right: RightRulePartStr::Sym(vec!["A", "c"]),
            },
            CFGRuleStr {
                left: "A",
                right: RightRulePartStr::Sym(vec!["S", "d"]),
            },
            CFGRuleStr {
                left: "A",
                right: RightRulePartStr::Eps,
            },
        ];
        let start_sym = "S";
        let cfg = CFG::new(terms, non_terms, rules, start_sym);

        let nonterm_syms = vec![String::from("S")];
        let right_parts = cfg.get_right_parts(
            vec!["a", "S", "b", "S"].into_iter().map(|s| String::from(s)).collect(),
            &HashSet::from_iter(nonterm_syms.into_iter())
        );

        assert_eq!(right_parts, vec![
            vec!["a", "", "b", ""],
            vec!["a", "", "b", "S"],
            vec!["a", "S", "b", ""],
            vec!["a", "S", "b", "S"]]);
    }

    #[test]
    pub fn test_elim_chain_rules_default() {
        let terms = vec!["a", "+", "*", "(", ")"];
        let non_terms = vec!["F", "E", "T"];
        let rules = vec![
            CFGRuleStr {
                left: "E",
                right: RightRulePartStr::Sym(vec!["E", "+", "T"]),
            },
            CFGRuleStr {
                left: "E",
                right: RightRulePartStr::Sym(vec!["T"]),
            },
            CFGRuleStr {
                left: "T",
                right: RightRulePartStr::Sym(vec!["T", "*", "F"]),
            },
            CFGRuleStr {
                left: "T",
                right: RightRulePartStr::Sym(vec!["F"]),
            },
            CFGRuleStr {
                left: "F",
                right: RightRulePartStr::Sym(vec!["(", "E", ")"]),
            },
            CFGRuleStr {
                left: "F",
                right: RightRulePartStr::Sym(vec!["a"]),
            },
        ];
        let start_sym = "E";
        let mut cfg = CFG::new(terms, non_terms, rules, start_sym);

        cfg.elim_chain_rules();

        let target_terms = vec!["a", "+", "*", "(", ")"];
        let target_non_terms = vec!["F", "E", "T"];
        let target_rules = vec![
            CFGRuleStr {
                left: "E",
                right: RightRulePartStr::Sym(vec!["E", "+", "T"]),
            },
            CFGRuleStr {
                left: "T",
                right: RightRulePartStr::Sym(vec!["T", "*", "F"]),
            },
            CFGRuleStr {
                left: "E",
                right: RightRulePartStr::Sym(vec!["T", "*", "F"]),
            },
            CFGRuleStr {
                left: "T",
                right: RightRulePartStr::Sym(vec!["(", "E", ")"]),
            },
            CFGRuleStr {
                left: "F",
                right: RightRulePartStr::Sym(vec!["(", "E", ")"]),
            },
            CFGRuleStr {
                left: "E",
                right: RightRulePartStr::Sym(vec!["(", "E", ")"]),
            },
            CFGRuleStr {
                left: "E",
                right: RightRulePartStr::Sym(vec!["a"]),
            },
            CFGRuleStr {
                left: "F",
                right: RightRulePartStr::Sym(vec!["a"]),
            },
            CFGRuleStr {
                left: "T",
                right: RightRulePartStr::Sym(vec!["a"]),
            },
        ];
        let target_start_sym = "E";
        let target_cfg = CFG::new(target_terms, target_non_terms, target_rules, target_start_sym);
        assert_eq!(target_cfg, cfg)
    }
}
