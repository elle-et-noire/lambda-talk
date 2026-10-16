import ast
from pathlib import Path
import re

from tools.check_slides import definitions, lint_tree


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "code" / "lambda_core.py"


def test_pure_world_rules_and_dependencies():
    tree = ast.parse(CORE.read_text(encoding="utf-8"))
    assert not lint_tree(tree)
    assert all(isinstance(node, (ast.Assign, ast.FunctionDef))
               for node in tree.body)


def test_core_slide_sizes():
    source = CORE.read_text(encoding="utf-8")
    assert all(len(line) <= 64 for line in source.splitlines())
    for node in ast.parse(source).body:
        assert node.end_lineno - node.lineno + 1 <= 12


def test_outline_exact_definitions_and_parameters():
    outline = (ROOT / "plan" / "outline.md").read_text(encoding="utf-8")
    section = outline.split("## 命名と定義の仕様", 1)[1]
    spec = section.split("```python\n", 1)[1].split("```", 1)[0]
    exact_lines = [line for line in spec.splitlines()
                   if re.match(r"^(?:[A-Z_]+|omega) = ", line)]
    expected = dict((name, ast.dump(rhs)) for name, rhs, _ in
                    definitions(ast.parse("\n".join(exact_lines))))
    actual = dict((name, ast.dump(rhs)) for name, rhs, _ in
                  definitions(ast.parse(CORE.read_text(encoding="utf-8"))))
    for name, rhs in expected.items():
        assert actual[name] == rhs, name


def test_rule_lint_catches_forbidden_constructs():
    for source in [
        "BAD = 0", "BAD = True", "BAD = 'x'",
        "BAD = lambda x: x if x else x",
        "def BAD(x):\n    return x", "class BAD: pass",
        "BAD = lambda x: x + x", "BAD = lambda x: x and x",
        "BAD = lambda x: not x", "BAD = lambda x: x == x",
        "BAD = lambda: ID", "BAD = lambda x, y: x",
        "BAD = lambda x=ID: x", "BAD = lambda *x: x",
        "BAD = lambda x: BAD(x)",
        "BAD = lambda x: LATER(x)\nLATER = lambda x: x",
    ]:
        assert lint_tree(ast.parse(source)), source
    assert not lint_tree(ast.parse("to_any = lambda: 1 + 2"))
    assert not lint_tree(ast.parse("A = lambda B: B\nB = lambda x: x"))
