package example {

alias real float
const float pi = 3.141592653589793

class Number {
    real n

    func real () get {
        return n
    }
}

class TreeNode<V> {
    TreeNode left, right
    V val

    func (TreeNode node) insert {
        # ...
    }

    func (V newval) insertVal {
        n := new TreeNode{val:newval}
        insert(n)
    }
}

alias TreeNode Tree

func int (int x) squared {
    return x * x
}

func<T> int (list<T> items, T target) find {
    # ...
    return 0
}

func int () main {
    tree := new Tree<Number>{}
    tree.insertVal(new Number{n:pi})

    idx0 := find(["hello", "world", "goodbye"], "world")
    idx1 := find([1, 2, 3, 4, 5, 6, 7], 4)

    return 0
}

}
