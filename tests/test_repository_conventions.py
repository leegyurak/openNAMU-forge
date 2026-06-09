import ast
import re
from pathlib import Path

import pytest

REPOSITORY_FILES = (
    Path("opennamu_forge/infrastructure/admin_repository.py"),
    Path("opennamu_forge/infrastructure/backlink_repository.py"),
    Path("opennamu_forge/infrastructure/bbs_repository.py"),
    Path("opennamu_forge/infrastructure/document_meta_repository.py"),
    Path("opennamu_forge/infrastructure/history_repository.py"),
    Path("opennamu_forge/infrastructure/html_filter_repository.py"),
    Path("opennamu_forge/infrastructure/recent_block_repository.py"),
    Path("opennamu_forge/infrastructure/setting_repository.py"),
    Path("opennamu_forge/infrastructure/topic_repository.py"),
    Path("opennamu_forge/infrastructure/user_agent_repository.py"),
    Path("opennamu_forge/infrastructure/user_notice_repository.py"),
    Path("opennamu_forge/infrastructure/user_setting_repository.py"),
    Path("opennamu_forge/infrastructure/vote_repository.py"),
    Path("opennamu_forge/infrastructure/wiki_repository.py"),
)
class RepositoryControlFlowVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.lines: set[int] = set()

    def visit_If(self, node: ast.If) -> None:
        self.lines.add(node.lineno)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self.lines.add(node.lineno)

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


class RepositoryListCallVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.lines: set[int] = set()

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == "list":
            self.lines.add(node.lineno)
        self.generic_visit(node)


class RepositoryReturnAnnotationVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.lines: set[int] = set()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if not node.name.startswith("_") and node.returns is not None:
            annotation = ast.unparse(node.returns)
            if re.search(
                r"\b("
                r"AdminList|AdminRecord|Acl|Backlink|BbsData|BbsSet|DataSet|History|"
                r"HtmlFilter|Other|RecentBlock|RecentChange|RecentDiscuss|Topic|"
                r"TopicSet|UserAgentData|UserNotice|UserSet|Vote|WikiData"
                r")\b",
                annotation,
            ):
                self.lines.add(node.lineno)
        self.generic_visit(node)


@pytest.mark.parametrize("repository_file", REPOSITORY_FILES, ids=str)
def test_repository는_제어문을_직접_사용하지_않는다(repository_file):
    tree = ast.parse(repository_file.read_text(encoding="utf-8"))
    visitor = RepositoryControlFlowVisitor()
    visitor.visit(tree)

    assert sorted(visitor.lines) == []


@pytest.mark.parametrize("repository_file", REPOSITORY_FILES, ids=str)
def test_repository는_list_타입변환을_사용하지_않는다(repository_file):
    tree = ast.parse(repository_file.read_text(encoding="utf-8"))
    visitor = RepositoryListCallVisitor()
    visitor.visit(tree)

    assert sorted(visitor.lines) == []


@pytest.mark.parametrize("repository_file", REPOSITORY_FILES, ids=str)
def test_repository는_sqlmodel_row를_return_annotation으로_노출하지_않는다(repository_file):
    tree = ast.parse(repository_file.read_text(encoding="utf-8"))
    visitor = RepositoryReturnAnnotationVisitor()
    visitor.visit(tree)

    assert sorted(visitor.lines) == []
