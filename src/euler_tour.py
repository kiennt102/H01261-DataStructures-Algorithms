"""Euler Tour as a Template Method.

The walk around the tree is fixed (the "template"); what happens at each stop
is left to three hooks that a subclass may override:

    pre_visit(node, depth)               just arrived from above
    in_visit(node, depth)                back from the left subtree (binary trees)
    post_visit(node, depth, results)     about to go back up; may return a value

`results` holds the values returned by the children's post_visit, so an
answer can travel from the leaves up to the root. The walk uses an explicit
Stack, not recursion, so very tall trees do not hit Python's recursion limit.

Run:  python euler_tour.py     (ends with "OK")
"""

from containers import Stack
from binary_tree import BinaryTree
from tree import Tree
from expression_tree import parse, to_number


# ---------------------------------------------------------------- templates
class _Frame:
    """State of one node during the walk."""

    def __init__(self, node, depth, slot):
        self.node = node
        self.depth = depth
        self.slot = slot            # index in the parent's results list
        self.stage = 0              # 0 pre, 1 left, 2 in, 3 right, 4 post
        self.results = [None, None]


class BinaryEulerTour:
    """Euler Tour of a BinaryTree: pre-, in- and post-visit hooks."""

    def __init__(self, tree):
        self.tree = tree

    # hooks: override what you need
    def pre_visit(self, node, depth):
        pass

    def in_visit(self, node, depth):
        pass

    def post_visit(self, node, depth, results):
        return None

    def execute(self):
        """Walk the tree and return the value produced at the root's post_visit."""
        if self.tree.root is None:
            return None
        answer = None
        stack = Stack()
        stack.push(_Frame(self.tree.root, 0, 0))
        while not stack.is_empty():
            f = stack.peek()
            node = f.node
            if f.stage == 0:
                self.pre_visit(node, f.depth)
                f.stage = 1
            elif f.stage == 1:
                f.stage = 2
                if node.left is not None:
                    stack.push(_Frame(node.left, f.depth + 1, 0))
            elif f.stage == 2:
                self.in_visit(node, f.depth)
                f.stage = 3
            elif f.stage == 3:
                f.stage = 4
                if node.right is not None:
                    stack.push(_Frame(node.right, f.depth + 1, 1))
            else:
                result = self.post_visit(node, f.depth, f.results)
                stack.pop()
                if stack.is_empty():
                    answer = result
                else:
                    stack.peek().results[f.slot] = result
        return answer


class _GFrame:
    def __init__(self, node, depth, slot):
        self.node = node
        self.depth = depth
        self.slot = slot            # index in the parent's results list
        self.next_child = 0         # next child to enter
        self.entered = False
        self.results = [None] * len(node.children)


class GeneralEulerTour:
    """Euler Tour of a general Tree: only pre- and post-visit make sense."""

    def __init__(self, tree):
        self.tree = tree

    def pre_visit(self, node, depth):
        pass

    def post_visit(self, node, depth, results):
        return None

    def execute(self):
        if self.tree.root is None:
            return None
        answer = None
        stack = Stack()
        stack.push(_GFrame(self.tree.root, 0, 0))
        while not stack.is_empty():
            f = stack.peek()
            if not f.entered:
                self.pre_visit(f.node, f.depth)
                f.entered = True
            if f.next_child < len(f.node.children):
                i = f.next_child
                f.next_child += 1
                stack.push(_GFrame(f.node.children[i], f.depth + 1, i))
            else:
                result = self.post_visit(f.node, f.depth, f.results)
                stack.pop()
                if stack.is_empty():
                    answer = result
                else:
                    stack.peek().results[f.slot] = result
        return answer


# ------------------------------------------- applications (binary tree)
class PreorderTour(BinaryEulerTour):
    """Acting only at pre_visit gives the preorder traversal."""

    def execute(self):
        self.out = []
        super().execute()
        return self.out

    def pre_visit(self, node, depth):
        self.out.append(node.value)


class InorderTour(BinaryEulerTour):
    """Acting only at in_visit gives the inorder traversal."""

    def execute(self):
        self.out = []
        super().execute()
        return self.out

    def in_visit(self, node, depth):
        self.out.append(node.value)


class PostorderTour(BinaryEulerTour):
    """Acting only at post_visit gives the postorder traversal."""

    def execute(self):
        self.out = []
        super().execute()
        return self.out

    def post_visit(self, node, depth, results):
        self.out.append(node.value)


class SizeTour(BinaryEulerTour):
    """Number of nodes: 1 + sizes of the subtrees."""

    def post_visit(self, node, depth, results):
        return 1 + sum(r for r in results if r is not None)


class HeightTour(BinaryEulerTour):
    """Height in edges: 0 for a leaf, else 1 + the taller child."""

    def post_visit(self, node, depth, results):
        heights = [r for r in results if r is not None]
        return 0 if not heights else 1 + max(heights)


class LeafCountTour(BinaryEulerTour):
    def post_visit(self, node, depth, results):
        if node.is_leaf():
            return 1
        return sum(r for r in results if r is not None)


class IndentedPrintTour(BinaryEulerTour):
    """Print the tree, indenting each node by its depth."""

    def execute(self):
        self.lines = []
        super().execute()
        return "\n".join(self.lines)

    def pre_visit(self, node, depth):
        self.lines.append("  " * depth + str(node.value))


class EvaluateTour(BinaryEulerTour):
    """Value of an expression tree: combine the two children at post_visit."""

    def post_visit(self, node, depth, results):
        if node.is_leaf():
            return to_number(node.value)
        a, b = results
        if node.value == "+":
            return a + b
        if node.value == "-":
            return a - b
        if node.value == "*":
            return a * b
        return a / b


class InfixTour(BinaryEulerTour):
    """Expression with brackets: '(' before, operator between, ')' after."""

    def execute(self):
        self.parts = []
        super().execute()
        return "".join(self.parts)

    def pre_visit(self, node, depth):
        if not node.is_leaf():
            self.parts.append("(")

    def in_visit(self, node, depth):
        self.parts.append(str(node.value))

    def post_visit(self, node, depth, results):
        if not node.is_leaf():
            self.parts.append(")")
        return None

    # leaves print their value in in_visit too (no children, so it is the only stop)


# --------------------------------------------- application (general tree)
class FolderSizeTour(GeneralEulerTour):
    """Total size of every folder: own size + total of the children.

    Node values must have .size (a number) like file_system.Entry.
    """

    def post_visit(self, node, depth, results):
        return node.value.size + sum(r for r in results)


# ------------------------------------------------------------------- check
def _check():
    # tree from main.py:      1
    #                       /   \
    #                      2     3
    #                     / \   /
    #                    4   5 6
    bt = BinaryTree()
    r = bt.add_root(1)
    l = bt.add_left(r, 2)
    rr = bt.add_right(r, 3)
    bt.add_left(l, 4)
    bt.add_right(l, 5)
    bt.add_left(rr, 6)

    # the three classic traversals are special cases of the tour
    assert PreorderTour(bt).execute() == [n.value for n in bt.preorder()]
    assert InorderTour(bt).execute() == [n.value for n in bt.inorder()]
    assert PostorderTour(bt).execute() == [n.value for n in bt.postorder()]

    # properties agree with the methods written without the template
    assert SizeTour(bt).execute() == len(bt) == 6
    assert HeightTour(bt).execute() == bt.height() == 2
    assert LeafCountTour(bt).execute() == len(bt.leaves()) == 3

    # empty tree
    assert SizeTour(BinaryTree()).execute() is None

    # expression trees
    e = parse("(3 + 4) * 2")
    assert EvaluateTour(e).execute() == 14
    assert InfixTour(e).execute() == "((3+4)*2)"
    book = parse("((((3+1)*3)/((9-5)+2))-((3*(7-4))+6))")
    assert EvaluateTour(book).execute() == -13       # Figure 8.8 of the book

    # general tree: folder totals
    class Item:
        def __init__(self, name, size=0):
            self.name, self.size = name, size

    t = Tree()
    root = t.add_root(Item("project"))
    docs = t.add_child(root, Item("docs"))
    t.add_child(docs, Item("report", 120))
    t.add_child(docs, Item("notes", 5))
    t.add_child(root, Item("photo", 800))
    assert FolderSizeTour(t).execute() == 925

    # a very tall (skewed) tree: no recursion error
    tall = BinaryTree()
    node = tall.add_root(0)
    for i in range(1, 5000):
        node = tall.add_left(node, i)
    assert HeightTour(tall).execute() == 4999
    return bt, e


if __name__ == "__main__":
    bt, e = _check()
    print("Indented print of the example tree:")
    print(IndentedPrintTour(bt).execute())
    print("Infix of (3 + 4) * 2 :", InfixTour(e).execute())
    print("Value                :", EvaluateTour(e).execute())
    print("OK")
