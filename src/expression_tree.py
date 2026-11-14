"""Cây biểu thức: dùng cây nhị phân để phân tích và tính một biểu thức toán học.

Ví dụ "3 + 4 * 2" được biến thành cây:
        +
       / \\
      3   *
         / \\
        4   2
Lá là số, node trong là toán tử. Các bước:
    chuỗi --tokenize--> list token --to_postfix--> thứ tự hậu tố --build_tree--> cây
Sau khi có cây, mỗi phép duyệt cho một "cách viết" khác nhau của biểu thức:
    preorder  -> tiền tố  (+ 3 * 4 2)
    postorder -> hậu tố   (3 4 2 * +)
    inorder   -> trung tố (có ngoặc)
và duyệt postorder cũng chính là cách để tính giá trị.
"""

from containers import Stack
from binary_tree import BinaryNode, BinaryTree

OPERATORS = ("+", "-", "*", "/")
PRIORITY = {"+": 1, "-": 1, "*": 2, "/": 2}   # * và / ưu tiên hơn + và -


def tokenize(text):
    """Tách chuỗi thành các token (số, toán tử, dấu ngoặc).

    "12+(3*4)" -> ["12", "+", "(", "3", "*", "4", ")"]
    """
    tokens = []
    number = ""                       # số đang đọc dở
    for ch in text:
        if ("0" <= ch <= "9") or ch == ".":
            number += ch
            continue
        if number != "":              # gặp ký tự không phải số -> kết thúc số đang đọc
            tokens.append(number)
            number = ""
        if ch == " ":
            continue
        if ch in OPERATORS or ch == "(" or ch == ")":
            tokens.append(ch)
        else:
            raise ValueError("Ký tự không hợp lệ: " + ch)
    if number != "":
        tokens.append(number)
    return tokens


def to_postfix(tokens):
    """Đổi trung tố sang hậu tố bằng Stack (thuật toán 'shunting-yard').

    Stack giữ các toán tử đang chờ. Gặp toán tử mới thì đẩy ra trước
    những toán tử đang chờ mà ưu tiên cao hơn hoặc bằng (tính từ trái sang phải).
    """
    output = []
    waiting = Stack()
    for token in tokens:
        if token in OPERATORS:
            while (not waiting.is_empty() and waiting.peek() != "("
                   and PRIORITY[waiting.peek()] >= PRIORITY[token]):
                output.append(waiting.pop())
            waiting.push(token)
        elif token == "(":
            waiting.push(token)
        elif token == ")":
            while not waiting.is_empty() and waiting.peek() != "(":
                output.append(waiting.pop())
            if waiting.is_empty():
                raise ValueError("Thừa dấu ')'")
            waiting.pop()             # bỏ dấu '('
        else:
            output.append(token)      # là số: đi thẳng ra output
    while not waiting.is_empty():
        op = waiting.pop()
        if op == "(":
            raise ValueError("Thiếu dấu ')'")
        output.append(op)
    return output


def build_tree(postfix):
    """Dựng cây từ hậu tố bằng Stack các cây con.

    Gặp số: tạo node lá, cho vào stack.
    Gặp toán tử: lấy 2 cây con trên đỉnh làm con phải rồi con trái, nối vào node toán tử mới.
    """
    stack = Stack()
    for token in postfix:
        node = BinaryNode(token)
        if token in OPERATORS:
            if stack.is_empty():
                raise ValueError("Biểu thức sai: thiếu toán hạng")
            right = stack.pop()
            if stack.is_empty():
                raise ValueError("Biểu thức sai: thiếu toán hạng")
            left = stack.pop()
            node.left = left
            node.right = right
            left.parent = node
            right.parent = node
        stack.push(node)
    if stack.is_empty():
        raise ValueError("Biểu thức rỗng")
    root = stack.pop()
    if not stack.is_empty():
        raise ValueError("Biểu thức sai: thiếu toán tử")
    tree = BinaryTree()
    tree.adopt(root)
    return tree


def parse(text):
    """Chuỗi biểu thức -> cây biểu thức."""
    return build_tree(to_postfix(tokenize(text)))


def to_number(token):
    if "." in token:
        return float(token)
    return int(token)


def evaluate(tree):
    """Tính giá trị biểu thức bằng duyệt hậu tố (postorder) và một Stack giá trị.

    Lá: đẩy số vào stack. Toán tử: lấy 2 số trên đỉnh ra tính, đẩy kết quả lại.
    """
    values = Stack()
    for node in tree.postorder():
        if node.is_leaf():
            values.push(to_number(node.value))
        else:
            b = values.pop()
            a = values.pop()
            if node.value == "+":
                values.push(a + b)
            elif node.value == "-":
                values.push(a - b)
            elif node.value == "*":
                values.push(a * b)
            else:
                values.push(a / b)       # chia cho 0 sẽ báo ZeroDivisionError
    result = values.pop()
    if isinstance(result, float) and result.is_integer():
        result = int(result)             # 12.0 -> 12 cho gọn
    return result


def to_prefix(tree):
    """Tiền tố: duyệt preorder. Ví dụ: + 3 * 4 2"""
    return " ".join([node.value for node in tree.preorder()])


def to_postfix_string(tree):
    """Hậu tố: duyệt postorder. Ví dụ: 3 4 2 * +"""
    return " ".join([node.value for node in tree.postorder()])


def to_infix(tree):
    """Trung tố có đầy đủ ngoặc, dựa trên thứ tự Trái - Gốc - Phải.

    Stack chứa node (chưa xử lý) hoặc chuỗi (đã sẵn sàng để in).
    Gặp node toán tử thì đẩy ngược "( trái toán_tử phải )" để pop ra đúng thứ tự.
    """
    if tree.root is None:
        return ""
    parts = []
    stack = Stack()
    stack.push(tree.root)
    while not stack.is_empty():
        item = stack.pop()
        if isinstance(item, str):
            parts.append(item)
        elif item.is_leaf():
            parts.append(item.value)
        else:
            stack.push(")")
            stack.push(item.right)
            stack.push(item.value)
            stack.push(item.left)
            stack.push("(")
    text = "".join(parts)
    if not tree.root.is_leaf():
        text = text[1:-1]                # bỏ cặp ngoặc ngoài cùng
    return text
