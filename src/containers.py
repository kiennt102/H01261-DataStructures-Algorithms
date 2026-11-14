"""Stack (ngăn xếp) và Queue (hàng đợi) tự viết bằng danh sách liên kết.

- Stack: vào sau ra trước (LIFO)  -> giống chồng đĩa, lấy đĩa trên cùng.
- Queue: vào trước ra trước (FIFO) -> giống xếp hàng mua vé.
"""


class _Node:
    """Một mắt xích: giữ 1 giá trị và trỏ tới mắt xích kế tiếp."""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Stack:
    def __init__(self):
        self._top = None  # mắt xích ở đỉnh stack
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def push(self, value):
        """Cho value vào đỉnh stack."""
        self._top = _Node(value, self._top)
        self._size += 1

    def pop(self):
        """Lấy phần tử ở đỉnh ra."""
        if self._top is None:
            raise IndexError("Stack rỗng")
        value = self._top.value
        self._top = self._top.next
        self._size -= 1
        return value

    def peek(self):
        """Xem phần tử ở đỉnh nhưng không lấy ra."""
        if self._top is None:
            raise IndexError("Stack rỗng")
        return self._top.value


class Queue:
    def __init__(self):
        self._front = None  # đầu hàng (lấy ra ở đây)
        self._back = None   # cuối hàng (thêm vào ở đây)
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def enqueue(self, value):
        """Thêm value vào cuối hàng."""
        node = _Node(value)
        if self._back is None:      # hàng đang rỗng
            self._front = node
        else:
            self._back.next = node
        self._back = node
        self._size += 1

    def dequeue(self):
        """Lấy phần tử ở đầu hàng ra."""
        if self._front is None:
            raise IndexError("Queue rỗng")
        value = self._front.value
        self._front = self._front.next
        if self._front is None:     # vừa lấy hết
            self._back = None
        self._size -= 1
        return value
