import ast
import doctest
from pathlib import Path
import subprocess
import sys

import pytest

from tools.check_slides import Block, CORE, extract_blocks, parse_doctest


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "tools" / "check_slides.py"


def run_fixture(tmp_path, markdown, preload=False):
    path = tmp_path / "slides.md"
    path.write_text(markdown, encoding="utf-8")
    cmd = [sys.executable, str(CHECKER), str(path)]
    if preload:
        cmd.append("--preload-core")
    return subprocess.run(cmd, text=True, capture_output=True, timeout=10)


def test_sample():
    sample = ROOT / "code" / "tests" / "fixtures" / "sample.md"
    result = subprocess.run([sys.executable, str(CHECKER), str(sample)],
                            text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "blocks run=3 / doctests=2 / examples=6 / skipped=1" in result.stdout
    assert "INFO names only in slides: OTHER" in result.stdout


def test_failures_have_slide_and_exact_markdown_line(tmp_path):
    result = run_fixture(tmp_path, "---\nmarp: true\n---\nTitle\n---\n"
                         "<div>\n```python\n>>> to_int(ONE)\n2\n```\n</div>\n",
                         preload=True)
    assert result.returncode == 1
    assert "FAIL slide 2, markdown line 8" in result.stdout


def test_exec_failure(tmp_path):
    result = run_fixture(tmp_path, "```python\nMISSING(NAME)\n```\n")
    assert result.returncode == 1
    assert "FAIL slide 1, markdown line 2: NameError" in result.stdout


def test_preloaded_recursion_error_doctests(tmp_path):
    markdown = """```python
>>> Y(FACT_BODY)
Traceback (most recent call last):
  ...
RecursionError: maximum recursion depth exceeded
>>> omega(omega)
Traceback (most recent call last):
  ...
RecursionError: maximum recursion depth exceeded
```\n"""
    result = run_fixture(tmp_path, markdown, preload=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "examples=2" in result.stdout


@pytest.mark.parametrize("source", [
    "ID = lambda different: different",
    ">>> ID = lambda different: different",
])
def test_ast_mismatch_in_plain_and_doctest(tmp_path, source):
    result = run_fixture(tmp_path, f"```python\n{source}\n```\n")
    assert result.returncode == 1
    assert "AST mismatch for ID" in result.stdout


def test_formatting_does_not_change_ast(tmp_path):
    result = run_fixture(tmp_path, "```python\nID = (\n lambda x: x\n)\n```\n")
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("source", [
    "BAD = True", "BAD = 1", "BAD = 'x'",
    "BAD = lambda x: x if x else x", "BAD = lambda x: x + x",
    "BAD = lambda x: x or x", "BAD = lambda x: -x",
    "BAD = lambda x: x == x", "BAD = lambda x, y: x",
    "BAD = lambda: ID", "class BAD: pass",
    "def BAD(x):\n    return x",
    "BAD = lambda x: [x]", "BAD = lambda x: {x: x}",
    "BAD = lambda x: {x}", "BAD = lambda x: (x, x)",
    "BAD = lambda x: x.__class__", "BAD = lambda x: x[x]",
    "BAD = lambda x: [y for y in x]",
    "BAD = lambda x: {y: y for y in x}",
    "BAD = lambda x: {y for y in x}",
    "BAD = lambda x: (y for y in x)",
    "BAD = lambda x: f'{x}'", "BAD = lambda x: (y := x)",
    "BAD = lambda x: x()", "BAD = lambda x: x(x, x)",
    "BAD = lambda x: x(value=x)", "BAD = lambda x: x(x, value=x)",
    "BAD = lambda x: x(*x)", "BAD = lambda x: x(**x)",
    "BAD = lambda x=ID: x", "BAD = lambda *x: x",
    "BAD = lambda **x: x", "BAD = lambda x, *, y: x",
    "BAD = lambda x, *args: x", "BAD = lambda x, **kwargs: x",
    "BAD = lambda x: BAD(x)",
    "BAD = lambda x: LATER(x)\nLATER = lambda x: x",
])
def test_slide_rule_lint(tmp_path, source):
    result = run_fixture(tmp_path, f"```python\n{source}\n```\n")
    assert result.returncode == 1
    assert "rule lint BAD" in result.stdout


def test_windows_and_expected_outputs_are_exempt(tmp_path):
    result = run_fixture(tmp_path, """```python
>>> def to_any(n=1):
...     return [n + 1, True, "ok"]
>>> to_any()
[2, True, 'ok']
```
```python
>>> to_int(ADD(TWO)(THREE))
5
```\n""", preload=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_window_function_and_lambda_are_different_asts(tmp_path):
    result = run_fixture(tmp_path, """```python
def to_int(n):
    return n(lambda x: x + 1)(0)
```
```python
>>> to_int(TWO)
2
```\n""", preload=True)
    assert result.returncode == 1, result.stdout
    assert "AST mismatch for to_int" in result.stdout


def test_doctest_definitions_persist_into_exec(tmp_path):
    result = run_fixture(tmp_path, """```python
>>> NEW = lambda x: x
```
```python
NEW(NEW)
```
```python
>>> NEW(NEW) is NEW
True
```\n""")
    assert result.returncode == 0, result.stdout


def test_skip_has_no_execution_consistency_or_lint(tmp_path):
    result = run_fixture(tmp_path, "```python\n# 実行しない\nID = 1 / 0\n```\n")
    assert result.returncode == 0, result.stdout
    assert "skipped=1" in result.stdout


@pytest.mark.parametrize("rhs", ["lambda x: ALIAS(x)", "ALIAS(ID)", "ALIAS"])
@pytest.mark.parametrize("separator", ["\n", "\n```\n```python\n"])
def test_redefinition_cannot_reference_its_old_name(tmp_path, rhs, separator):
    result = run_fixture(tmp_path,
                         "```python\nALIAS = lambda x: x" + separator
                         + f"ALIAS = {rhs}\n```\n", preload=True)
    assert result.returncode == 1, result.stdout
    assert "self reference: ALIAS" in result.stdout


def test_reusing_earlier_names_and_redefining_without_self_reference(tmp_path):
    result = run_fixture(tmp_path, """```python
ALIAS = ID
```
```python
OTHER = ALIAS(ID)
ALIAS = OTHER
```\n""", preload=True)
    assert result.returncode == 0, result.stdout


def test_style_warnings_are_not_failures(tmp_path):
    source = "# " + "x" * 65 + "\n" + "\n".join("ID(ID)" for _ in range(12))
    result = run_fixture(tmp_path, f"```python\n{source}\n```\n", preload=True)
    assert result.returncode == 0, result.stdout
    assert "warnings=2" in result.stdout


def test_extract_html_other_fences_frontmatter_and_indentation():
    markdown = """---
marp: true
---
<div>
```python
ID = lambda x: x
```
</div>
```text
---
```
---
  ```python
  >>> ID(ID) is ID
  True
  ```
"""
    blocks = list(extract_blocks(markdown))
    assert [(block.slide, block.line) for block in blocks] == [(1, 6), (2, 14)]


@pytest.mark.parametrize("source, reason", [
    ("(lambda x, y: x)(1, 2)", "lambda needs one argument"),
    ("if True:\n    BAD = 1", "If is not an allowed"),
    ("for BAD in []:\n    pass", "For is not an allowed"),
    ("while True:\n    pass", "While is not an allowed"),
    ("with MISSING():\n    BAD = 1", "With is not an allowed"),
    ("try:\n    BAD = 1\nexcept Exception:\n    pass", "Try is not an allowed"),
    ("BAD, WORSE = 1, 2", "assignment needs a single Name target"),
    ("[BAD] = [1]", "assignment needs a single Name target"),
    ("BAD = WORSE = lambda x: x", "assignment needs a single Name target"),
    ("ID.value = ID", "assignment needs a single Name target"),
    ("ID[ID] = ID", "assignment needs a single Name target"),
    ("BAD: object = 1", "AnnAssign is not an allowed"),
    ("BAD += 1", "AugAssign is not an allowed"),
    ("import os", "Import is not an allowed"),
    ("assert True", "Assert is not an allowed"),
    ("async def to_any():\n    return 1", "AsyncFunctionDef is not an allowed"),
])
@pytest.mark.parametrize("doctest_source", [False, True])
def test_whole_block_lint(tmp_path, source, reason, doctest_source):
    if doctest_source:
        source = ">>> " + source.replace("\n", "\n... ")
    result = run_fixture(tmp_path, f"```python\n{source}\n```\n")
    assert result.returncode == 1, result.stdout
    assert reason in result.stdout


@pytest.mark.parametrize("signature", [
    "lambda x, y: x", "lambda: ID", "lambda x=ID: x",
    "lambda *x: x", "lambda **x: x", "lambda x, *, y: x",
    "lambda x, *args: x", "lambda x, **kwargs: x",
    "lambda x: lambda y, z: y",
])
@pytest.mark.parametrize("prompt", ["", ">>> "])
def test_lambdas_nested_inside_observations_are_checked(tmp_path, signature, prompt):
    result = run_fixture(tmp_path,
                         f"```python\n{prompt}print({signature})\n```\n")
    assert result.returncode == 1, result.stdout
    assert "rule lint <observation>: lambda needs one argument" in result.stdout


@pytest.mark.parametrize("source, reason", [
    ("BAD = lambda n: to_int(n)", "window reference: to_int"),
    ("BAD = to_int", "window reference: to_int"),
    ("BAD = lambda n: to_missing(n)", "window reference: to_missing"),
    ("BAD = lambda x: UNKNOWN(x)", "forward/undefined reference: UNKNOWN"),
    ("BAD = lambda x: print(x)", "forward/undefined reference: print"),
    ("BAD = lambda x: ID(x)", "forward/undefined reference: ID"),
])
def test_free_references_must_be_prior_pure_definitions(tmp_path, source, reason):
    result = run_fixture(tmp_path, f"```python\n{source}\n```\n")
    assert result.returncode == 1, result.stdout
    assert reason in result.stdout


def test_preloaded_window_reference_is_still_rejected(tmp_path):
    result = run_fixture(tmp_path, "```python\nBAD = lambda n: to_int(n)\n```\n",
                         preload=True)
    assert result.returncode == 1, result.stdout
    assert "window reference: to_int" in result.stdout


@pytest.mark.parametrize("separator", ["\n", "\n```\n```python\n",
                                       "\n```\n```python\n>>> "])
def test_forward_reference_in_same_or_later_blocks(tmp_path, separator):
    result = run_fixture(tmp_path,
                         "```python\nBAD = lambda x: LATER(x)" + separator
                         + "LATER = lambda x: x\n```\n")
    assert result.returncode == 1, result.stdout
    assert "forward/undefined reference: LATER" in result.stdout


def test_names_are_available_in_statement_and_doctest_order(tmp_path):
    result = run_fixture(tmp_path, """```python
EARLY = lambda x: x
LATER = lambda x: EARLY(x)
```
```python
>>> NEW = LATER
>>> LAST = NEW
```
```python
FINAL = LAST
```
```python
>>> FINAL("ok")
'ok'
```\n""")
    assert result.returncode == 0, result.stdout + result.stderr


def test_bound_names_are_not_dependencies(tmp_path):
    result = run_fixture(tmp_path, """```python
LOCAL = lambda LOCAL: LOCAL
SHADOW = lambda to_missing: to_missing
POSITIONAL = lambda x, /: x
```\n""")
    assert result.returncode == 0, result.stdout


def test_preload_is_required_for_core_dependencies(tmp_path):
    markdown = "```python\nBAD = lambda x: ID(x)\n```\n"
    result = run_fixture(tmp_path, markdown, preload=True)
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("prompted", [False, True])
def test_incorrect_core_window_function_is_rejected(tmp_path, prompted):
    source = "def to_list(l, conv=lambda x: x):\n    return []"
    if prompted:
        source = ">>> " + source.replace("\n", "\n... ")
    result = run_fixture(tmp_path, f"```python\n{source}\n```\n")
    assert result.returncode == 1, result.stdout
    assert "markdown line 2: AST mismatch for to_list" in result.stdout


def test_core_window_function_matches_without_positions_or_formatting(tmp_path):
    core_source = CORE.read_text(encoding="utf-8")
    window = next(node for node in ast.parse(core_source).body
                  if isinstance(node, ast.FunctionDef) and node.name == "to_list")
    source = ast.unparse(window)
    result = run_fixture(tmp_path, f"Title\n\n```python\n\n{source}\n```\n"
                         "```python\n>>> to_list(NIL)\n[]\n```\n", preload=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_plain_window_definitions_and_observation_probes(tmp_path):
    result = run_fixture(tmp_path, """```python
def to_probe(value="a"):
    result = []
    for item in [value]:
        result.append(item)
    return result
to_any = lambda: {"value": True}
PROBE_ID = lambda x: x
print(PROBE_ID("a"), to_probe("b"))
PROBE_ID("a"), to_any(), (lambda x: x)("b")
```
```python
>>> PROBE_ID("a"), to_probe("b")
('a', ['b'])
>>> (lambda x: "a")(print("probe"))
probe
'a'
>>> (lambda x, /: x)("b")
'b'
```\n""")
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("source, line", [
    ("ID = lambda x: WRONG\n>>> to_int(ONE)\n1", 2),
    (">>> to_int(ONE)\n1\n\nBAD = 1", 5),
    (">>> to_int(ONE)\n1\n\nBAD = 1\n\n>>> to_int(TWO)\n2", 5),
    (">>> # a prompted comment\n\nBAD = 1\n>>> to_int(ONE)\n1", 4),
    ("... orphaned continuation\n>>> to_int(ONE)\n1", 2),
])
def test_unprompted_doctest_text_is_rejected(tmp_path, source, line):
    result = run_fixture(tmp_path, f"```python\n{source}\n```\n", preload=True)
    assert result.returncode == 1, result.stdout
    assert f"markdown line {line}: text outside doctest example:" in result.stdout


def test_doctest_comments_and_continuations_are_allowed(tmp_path):
    result = run_fixture(tmp_path, """```python
# Before the examples.
>>> # A comment-only prompt.
>>> ALIAS = (lambda x:
...     x)

# Between examples.
>>> ALIAS("a")
'a'

# After the examples.
```\n""")
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("info", ["python", "python title=demo", "py",
                                  "py title=demo", "python\tfoo"])
@pytest.mark.parametrize("fence", ["```", "~~~~"])
def test_python_fence_info_first_token(tmp_path, info, fence):
    result = run_fixture(tmp_path, f"{fence}{info}\nBAD = 1\n{fence}\n")
    assert result.returncode == 1, result.stdout
    assert "markdown line 2: rule lint BAD: Constant" in result.stdout


@pytest.mark.parametrize("source", [
    "```python\nID = lambda x: x\n", "~~~py\nID = lambda x: x\n",
    "````text\n```python\nBAD = 1\n```\n",
    "```text\n~~~python\nBAD = 1\n~~~\n",
    "```javascript\n", "```\n",
    "```python\nID = lambda x: x\n```\n```text\nunfinished\n",
])
def test_any_unclosed_fence_is_a_failure(tmp_path, source):
    result = run_fixture(tmp_path, source)
    assert result.returncode == 1, result.stdout
    assert "Unclosed " in result.stdout and "fence at line" in result.stdout


@pytest.mark.parametrize("source", [
    "Just prose.\n", "```text\nID = lambda x: x\n```\n",
    "```pythonish\nBAD = 1\n```\n",
    "<!--\n```python\nBAD = 1\n```\n-->\n",
])
def test_no_python_blocks_is_a_failure(tmp_path, source):
    result = run_fixture(tmp_path, source)
    assert result.returncode == 1, result.stdout
    assert "no python blocks found" in result.stdout


def test_html_comment_separators_and_fences_are_ignored(tmp_path):
    markdown = """---
marp: true
---
Title
<!--
---
```python
BAD = 1
```
~~~text
-->
<!-- inline --> <!-- another
---
-->
---
```py title=demo
MISSING(NAME)
```
"""
    blocks = list(extract_blocks(markdown))
    assert [(block.slide, block.line) for block in blocks] == [(2, 17)]
    result = run_fixture(tmp_path, markdown)
    assert result.returncode == 1, result.stdout
    assert "FAIL slide 2, markdown line 17: NameError" in result.stdout
    assert "failures=1" in result.stdout


def test_html_comment_markers_inside_fences_are_literal(tmp_path):
    markdown = """```text
<!--
---
```
---
```python
print("<!--")
```
---
```py
ALIAS = lambda x: x
```
"""
    blocks = list(extract_blocks(markdown))
    assert [(block.slide, block.line) for block in blocks] == [(2, 7), (3, 11)]
    result = run_fixture(tmp_path, markdown)
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("wide_char", ["界", "Ａ"])
@pytest.mark.parametrize("count, warnings", [(31, 0), (32, 1)])
def test_style_warning_counts_east_asian_columns(tmp_path, wide_char, count, warnings):
    result = run_fixture(tmp_path, "```python\n# " + wide_char * count + "\n```\n")
    assert result.returncode == 0, result.stdout
    assert f"warnings={warnings}" in result.stdout
    if warnings:
        assert "markdown line 2: line has 66 columns (max 64)" in result.stdout


@pytest.mark.parametrize("want, enabled", [
    ("'a  b'\n", set()),
    ("<function <lambda> at 0x...>\n", {doctest.ELLIPSIS}),
    ("[1,\n 2]\n", {doctest.NORMALIZE_WHITESPACE}),
    ("Traceback (most recent call last):\n  ...\nRecursionError: ...\n",
     {doctest.IGNORE_EXCEPTION_DETAIL, doctest.ELLIPSIS,
      doctest.NORMALIZE_WHITESPACE}),
])
def test_automatic_doctest_options_are_per_example(want, enabled):
    block = Block('>>> print("probe")\n' + want, 1, 2)
    test, problems = parse_doctest(doctest.DocTestParser(), block, {}, "slides.md")
    assert not problems
    assert {flag for flag, active in test.examples[0].options.items() if active} == enabled


def test_function_repr_ellipsis_and_multiline_observations(tmp_path):
    result = run_fixture(tmp_path, """```python
>>> lambda v: omega(omega)(v)
<function <lambda> at 0x...>
>>> to_list(RANGE(ONE)(THREE), to_int)
[1,
 2, 3]
```\n""", preload=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_normalize_whitespace_does_not_leak_between_examples(tmp_path):
    result = run_fixture(tmp_path, """```python
>>> print("two\\nlines")
two
lines
>>> print("a b")
a  b
```\n""")
    assert result.returncode == 1, result.stdout
    assert "FAIL slide 1, markdown line 5" in result.stdout
    assert "failures=1" in result.stdout


def test_exception_type_is_still_checked(tmp_path):
    result = run_fixture(tmp_path, """```python
>>> omega(omega)
Traceback (most recent call last):
  ...
ValueError: ...
```\n""", preload=True)
    assert result.returncode == 1, result.stdout
    assert "failures=1" in result.stdout
