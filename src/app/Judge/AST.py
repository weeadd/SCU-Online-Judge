import ast

src = """
def add(x, y):
    return x + y
print(add(3, 5))
"""

tree = ast.parse(src)
print (ast.dump(tree))

# 遍历AST节点
for node in ast.walk(tree):
    print(type(node).__name__)
    print(ast.dump(node))
    print()
