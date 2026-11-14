"""Cây nhị phân: mỗi node có tối đa 2 con (trái và phải).

Mọi phép duyệt dùng Stack hoặc Queue (không đệ quy) và trả về một list các node.
"""

from containers import Stack, Queue


class BinaryNode:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent   # node cha (None nếu là gốc)
        self.left = None       # con trái
        self.right = None      # con phải

    def is_leaf(self):
        return self.left is None and self.right is None


class BinaryTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    # ---------- thêm / xóa ----------
    def add_root(self, value):
        if self.root is not None:
            raise ValueError("Cây đã có gốc")
        self.root = BinaryNode(value)
        self._size = 1
        return self.root

    def add_left(self, parent, value):
        if parent.left is not None:
            raise ValueError("Đã có con trái")
        parent.left = BinaryNode(value, parent)
        self._size += 1
        return parent.left

    def add_right(self, parent, value):
        if parent.right is not None:
            raise ValueError("Đã có con phải")
        parent.right = BinaryNode(value, parent)
        self._size += 1
        return parent.right

    def adopt(self, node):
        """Dùng một node đã được nối sẵn các con làm gốc của cây (dựng cây từ dưới lên)."""
        self.root = node
        node.parent = None
        self._size = self._count(node)

    def remove(self, node):
        """Xóa node và cả cây con của nó. Trả về số node bị xóa."""
        removed = self._count(node)

        parent = node.parent
        if parent is None:               # xóa gốc = xóa cả cây
            self.root = None
        elif parent.left is node:
            parent.left = None
        else:
            parent.right = None
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
            if current.left is not None:
                stack.push(current.left)
            if current.right is not None:
                stack.push(current.right)
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
            if node.left is not None:
                queue.enqueue((node.left, d + 1))
            if node.right is not None:
                queue.enqueue((node.right, d + 1))
        return highest

    def leaves(self):
        """Danh sách các node lá (không có con)."""
        result = []
        for node in self.preorder():
            if node.is_leaf():
                result.append(node)
        return result

    def is_full(self):
        """Cây 'đầy': mỗi node có 0 hoặc đúng 2 con (không node nào chỉ có 1 con)."""
        stack = Stack()
        if self.root is not None:
            stack.push(self.root)
        while not stack.is_empty():
            node = stack.pop()
            has_left = node.left is not None
            has_right = node.right is not None
            if has_left != has_right:          # chỉ có 1 con -> không đầy
                return False
            if has_left:
                stack.push(node.left)
                stack.push(node.right)
        return True

    def is_complete(self):
        """Cây 'hoàn chỉnh': các tầng đầy, tầng cuối dồn về bên trái.

        Duyệt từng tầng. Khi gặp chỗ trống đầu tiên (con None) thì
        từ đó trở đi không được thấy node thật nào nữa.
        """
        queue = Queue()
        if self.root is not None:
            queue.enqueue(self.root)
        seen_empty = False
        while not queue.is_empty():
            node = queue.dequeue()
            for child in (node.left, node.right):
                if child is None:
                    seen_empty = True
                elif seen_empty:
                    return False
                else:
                    queue.enqueue(child)
        return True

    # ---------- duyệt ----------
    def preorder(self):
        """Gốc -> Trái -> Phải.

        Cho con phải vào stack trước, con trái sau, để con trái ra trước.
        """
        result = []
        if self.root is None:
            return result
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            node = stack.pop()
            result.append(node)
            if node.right is not None:
                stack.push(node.right)
            if node.left is not None:
                stack.push(node.left)
        return result

    def inorder(self):
        """Trái -> Gốc -> Phải.

        Từ node hiện tại cứ đi sang trái, vừa đi vừa cho vào stack.
        Hết đường thì lấy ra 1 node, ghi nhận nó, rồi rẽ sang con phải của nó.
        """
        result = []
        stack = Stack()
        current = self.root
        while current is not None or not stack.is_empty():
            while current is not None:         # đi hết nhánh trái
                stack.push(current)
                current = current.left
            current = stack.pop()              # node trái nhất chưa ghi nhận
            result.append(current)
            current = current.right            # rẽ sang phải
        return result

    def postorder(self):
        """Trái -> Phải -> Gốc.

        Mẹo: làm giống preorder nhưng đổi chỗ trái/phải (Gốc -> Phải -> Trái),
        rồi đảo ngược kết quả sẽ được Trái -> Phải -> Gốc.
        """
        result = []
        if self.root is None:
            return result
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            node = stack.pop()
            result.append(node)
            if node.left is not None:
                stack.push(node.left)
            if node.right is not None:
                stack.push(node.right)
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
            if node.left is not None:
                queue.enqueue(node.left)
            if node.right is not None:
                queue.enqueue(node.right)
        return result

    # ---------- in cây ----------
    def display(self):
        """In cây thành sơ đồ nhánh, L = con trái, R = con phải:
        1
        ├── L: 2
        └── R: 3
        """
        if self.root is None:
            return "(cây rỗng)"
        lines = [str(self.root.value)]
        stack = Stack()
        self._push_children(stack, self.root, "")
        while not stack.is_empty():
            node, label, prefix, is_last = stack.pop()
            if is_last:
                lines.append(prefix + "└── " + label + ": " + str(node.value))
                self._push_children(stack, node, prefix + "    ")
            else:
                lines.append(prefix + "├── " + label + ": " + str(node.value))
                self._push_children(stack, node, prefix + "│   ")
        return "\n".join(lines)

    def _push_children(self, stack, node, prefix):
        """Cho các con có thật của node vào stack (phải vào trước, trái vào sau).

        Mỗi phần tử gồm: (node con, nhãn L/R, phần đầu dòng, có phải con cuối không).
        """
        if node.left is not None and node.right is not None:
            stack.push((node.right, "R", prefix, True))
            stack.push((node.left, "L", prefix, False))
        elif node.left is not None:
            stack.push((node.left, "L", prefix, True))
        elif node.right is not None:
            stack.push((node.right, "R", prefix, True))
