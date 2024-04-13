use std::{cell::RefCell, rc::Rc};

type TreeNodeRef = Rc<RefCell<TreeNode>>;

#[derive(Debug, Clone)]
pub struct TreeNode {
    pub val: i32,
    pub left: Option<TreeNodeRef>,
    pub right: Option<TreeNodeRef>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tree() {
        let mut node_a = TreeNode {
            val: 20,
            left: None,
            right: None,
        };
        let mut node_b = TreeNode {
            val: 30,
            left: None,
            right: None,
        };
        let mut node_c = TreeNode {
            val: 40,
            left: None,
            right: None,
        };
        let node_d = TreeNode {
            val: 50,
            left: None,
            right: None,
        };
        let node_e = TreeNode {
            val: 60,
            left: None,
            right: None,
        };
        let node_f = TreeNode {
            val: 70,
            left: None,
            right: None,
        };

        //      a
        //    /   \
        //   b     c
        //  / \     \
        // d   e     f
        node_b.left = Some(Rc::new(RefCell::new(node_d)));
        node_b.right = Some(Rc::new(RefCell::new(node_e)));
        node_c.right = Some(Rc::new(RefCell::new(node_f)));
        node_a.left = Some(Rc::new(RefCell::new(node_b)));
        node_a.right = Some(Rc::new(RefCell::new(node_c)));
    }
}
