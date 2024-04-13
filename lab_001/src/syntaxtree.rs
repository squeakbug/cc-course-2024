use crate::treenode::TreeNode;

pub struct SyntaxTree {
    pub root: Option<TreeNode>,
}

impl SyntaxTree {
    pub fn new() -> Self {
        Self { root: None }
    }

    pub fn from_regex(_: String) -> Self {
        SyntaxTree::new()
    }
}

impl Default for SyntaxTree {
    fn default() -> Self {
        Self::new()
    }
}
