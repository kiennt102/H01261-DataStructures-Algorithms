"""Cây tổng quát: mỗi node có thể có nhiều con.

Mọi phép duyệt dùng Stack hoặc Queue (không đệ quy) và trả về một list các node.
"""

from containers import Stack, Queue


class TreeNode:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent   # node cha (None nếu là gốc)
        self.children = []     # danh sách node con

    def is_leaf(self):
        return len(self.children) == 0


class Tree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    # ---------- thêm / xóa ----------
    def add_root(self, value):
        if self.root is not None:
            raise ValueError("Cây đã có gốc")
        self.root = TreeNode(value)
        self._size = 1
        return self.root

    def add_child(self, parent, value):
        """Thêm node mới làm con (cuối cùng) của parent."""
        child = TreeNode(value, parent)
        parent.children.append(child)
        self._size += 1
        return child

    def remove(self, node):
        """Xóa node và cả cây con của nó. Trả về số node bị xóa."""
        removed = self._count(node)

        if node.parent is None:          # xóa gốc = xóa cả cây
            self.root = None
        else:                            # gỡ node khỏi danh sách con của cha
            siblings = node.parent.children
            for i in range(len(siblings)):
                if siblings[i] is node:
                    del siblings[i]
                    break
            node.parent = None

        self._size -= removed
        return removed

    def _count(self, node):
        """Đếm số node trong cây con gốc node."""
        total = 0
        stack = Stack()
        stack.push(node)
        while not stack.is_empty():
            current = stack.pop()
            total += 1
            for child in current.children:
                stack.push(child)
        return total

    # ---------- thuộc tính ----------
    def depth(self, node):
        """Độ sâu = số cạnh từ node đi lên gốc."""
        d = 0
        while node.parent is not None:
            node = node.parent
            d += 1
        return d

    def height(self):
        """Chiều cao = số cạnh của đường dài nhất từ gốc xuống lá (cây rỗng: -1).

        Đi từng tầng bằng Queue, mỗi node nhớ kèm độ sâu của nó.
        """
        if self.root is None:
            return -1
        highest = 0
        queue = Queue()
        queue.enqueue((self.root, 0))          # (node, độ sâu)
        while not queue.is_empty():
            node, d = queue.dequeue()
            if d > highest:
                highest = d
            for child in node.children:
                queue.enqueue((child, d + 1))
        return highest

    def find(self, value):
        """Tìm node đầu tiên có giá trị value, không thấy trả về None."""
        for node in self.preorder():
            if node.value == value:
                return node
        return None

    # ---------- duyệt ----------
    def preorder(self):
        """Cha trước, rồi tới các con.

        Stack lấy ra theo thứ tự ngược lại lúc cho vào,
        nên phải cho con cuối vào trước để con đầu ra trước.
        """
        result = []
        if self.root is None:
            return result
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            node = stack.pop()
            result.append(node)
            for child in reversed(node.children):
                stack.push(child)
        return result

    def postorder(self):
        """Các con trước, rồi tới cha.

        Mẹo: làm giống preorder nhưng cho con vào stack theo thứ tự thuận
        (cha, con cuối ... con đầu), rồi đảo ngược kết quả.
        """
        result = []
        if self.root is None:
            return result
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            node = stack.pop()
            result.append(node)
            for child in node.children:
                stack.push(child)
        result.reverse()
        return result

    def level_order(self):
        """Duyệt từng tầng, từ trên xuống, trái sang phải (dùng Queue)."""
        result = []
        if self.root is None:
            return result
        queue = Queue()
        queue.enqueue(self.root)
        while not queue.is_empty():
            node = queue.dequeue()
            result.append(node)
            for child in node.children:
                queue.enqueue(child)
        return result

    # ---------- in cây ----------
    def display(self):
        """In cây thành sơ đồ nhánh:
        A
        ├── B
        │   └── E
        └── C
        """
        if self.root is None:
            return "(cây rỗng)"
        lines = [str(self.root.value)]
        stack = Stack()
        self._push_children(stack, self.root, "")
        while not stack.is_empty():
            node, prefix, is_last = stack.pop()
            if is_last:
                lines.append(prefix + "└── " + str(node.value))
                self._push_children(stack, node, prefix + "    ")
            else:
                lines.append(prefix + "├── " + str(node.value))
                self._push_children(stack, node, prefix + "│   ")
        return "\n".join(lines)

    def _push_children(self, stack, node, prefix):
        """Cho các con của node vào stack (con cuối vào trước).

        Mỗi phần tử gồm: (node con, phần đầu dòng, có phải con cuối không).
        """
        last = len(node.children) - 1
        i = last
        while i >= 0:
            stack.push((node.children[i], prefix, i == last))
            i -= 1
