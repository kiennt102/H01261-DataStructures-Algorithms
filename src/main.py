from tree import Tree
from binary_tree import BinaryTree


def vals(it):
    return [n.value for n in it]


def show(title, it):
    print(f"  {title:<12}: {' '.join(str(v) for v in vals(it))}")


print("=" * 40)
print("CÂY TỔNG QUÁT")
print("=" * 40)
t = Tree()
root = t.add_root("A")
b = t.add_child(root, "B")
c = t.add_child(root, "C")
d = t.add_child(root, "D")
e = t.add_child(b, "E")
t.add_child(b, "F")
t.add_child(d, "G")
print(t.display())
print(f"\n  size={len(t)}  depth(E)={t.depth(e)}") #height={t.height()}  depth(E)={t.depth(e)}")

# show("preorder", t.preorder())
# show("postorder", t.postorder())
# show("level_order", t.level_order())
# assert vals(t.preorder()) == list("ABEFCDG")
# assert vals(t.postorder()) == list("EFBCGDA")
# assert vals(t.level_order()) == list("ABCDEFG")
# assert (len(t), t.height(), t.depth(e)) == (7, 2, 2)

print("\n  remove(B) ->", t.remove(b), "node bị xóa")
print(t.display())
assert len(t) == 4 and vals(t.preorder()) == list("ACDG")

print()
print("=" * 40)
print("CÂY NHỊ PHÂN")
print("=" * 40)
bt = BinaryTree()
r = bt.add_root(1)
l = bt.add_left(r, 2)
rr = bt.add_right(r, 3)
bt.add_left(l, 4)
bt.add_right(l, 5)
bt.add_left(rr, 6)
print(bt.display())
print(f"\n  size={len(bt)}  height={bt.height()}  full={bt.is_full()}  complete={bt.is_complete()}")
show("preorder", bt.preorder())
show("inorder", bt.inorder())
show("postorder", bt.postorder())
show("level_order", bt.level_order())
show("leaves", bt.leaves())
assert vals(bt.preorder()) == [1, 2, 4, 5, 3, 6]
assert vals(bt.inorder()) == [4, 2, 5, 1, 6, 3]
assert vals(bt.postorder()) == [4, 5, 2, 6, 3, 1]
assert vals(bt.level_order()) == [1, 2, 3, 4, 5, 6]
assert (len(bt), bt.height()) == (6, 2)
assert bt.is_complete() and not bt.is_full()
assert vals(bt.leaves()) == [4, 5, 6]
print("\n  remove(2) ->", bt.remove(l), "node bị xóa")
print(bt.display())
assert len(bt) == 3

print("\nOK - mọi kiểm tra đều đạt")
