import ast
import json

# src = """
# def add(x, y):
#     return x + y
# print(add(3, 5))
# """
#
# tree = ast.parse(src)
# print (ast.dump(tree))
#
# # 遍历AST节点
# for node in ast.walk(tree):
#     print(type(node).__name__)
#     print(ast.dump(node))
#     print()
def contains_recursion(tree):
    def recursive_search(node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'factorial':
            return True
        for child in ast.iter_child_nodes(node):
            if recursive_search(child):
                return True
        return False

    for node in ast.walk(tree):
        if recursive_search(node):
            return True
    return False


def get_ast_analysis(question_id,file_path, language):
    ast_status = ""
    ast_advice = ""

    if language != 'python':
        return "AST analysis only available for Python code."

    with open(file_path, "r") as source:
        tree = ast.parse(source.read())
        print(tree)

    if question_id == "5":
        if contains_recursion(tree):
            ast_status = "Accepted"
            ast_advice = "您的代码已包含递归调用"
        else:
            ast_status = "Wrong logic"
            ast_advice = "您的代码未包含递归调用"


    return ast_status, ast_advice
