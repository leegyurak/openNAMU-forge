import ast
from pathlib import Path

import pytest

TEST_FILES = tuple(Path("tests").rglob("test_*.py"))
LOOP_NODE_TYPES = (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


class LoopUsageVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.lines: set[int] = set()

    def visit_For(self, node: ast.For) -> None:
        self.lines.add(node.lineno)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.lines.add(node.lineno)

    def visit_While(self, node: ast.While) -> None:
        self.lines.add(node.lineno)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self.lines.add(node.lineno)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self.lines.add(node.lineno)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self.lines.add(node.lineno)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self.lines.add(node.lineno)


@pytest.mark.parametrize("test_file", TEST_FILES, ids=str)
def test_테스트_케이스_반복은_parametrize만_사용한다(test_file):
    tree = ast.parse(test_file.read_text(encoding="utf-8"))
    visitor = LoopUsageVisitor()
    visitor.visit(tree)

    assert sorted(visitor.lines) == []
