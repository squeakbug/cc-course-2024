use regex_lexer::dfs::{DotPrintable, FiniteAutomata, SymbolType};

pub fn main() {
    let mut nfa = FiniteAutomata::minimal();
    let state1 = nfa.add_state();
    let state2 = nfa.add_state();
    nfa.add_transition(0, SymbolType::Alpha(b'a'), state1);
    nfa.add_transition(0, SymbolType::Alpha(b'b'), state2);
    let dot_nfa = nfa.to_dot_notation();
    println!("{}", &dot_nfa);
}
