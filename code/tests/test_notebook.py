"""notebooks/lambda.ipynb が自己完結して動き、参照実装とずれていないことを確かめる。"""
import ast
import contextlib
import io
import json
import re

import pytest

from tools.check_slides import CORE, definitions

from conftest import ROOT

NOTEBOOK = ROOT / "notebooks" / "lambda.ipynb"
EXERCISE = re.compile(r"^(MY_(\w+)) = None", re.MULTILINE)


@pytest.fixture(scope="module")
def notebook():
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))


def code_cells(notebook):
    return ["".join(cell["source"]) for cell in notebook["cells"]
            if cell["cell_type"] == "code"]


@pytest.fixture(scope="module")
def namespace(notebook):
    """全コードセルを上から順に実行した名前空間。"""
    ns = {"__name__": "__notebook__"}
    with contextlib.redirect_stdout(io.StringIO()):
        for source in code_cells(notebook):
            exec(compile(source, str(NOTEBOOK), "exec"), ns)
    return ns


def test_saved_without_outputs(notebook):
    assert notebook["nbformat"] == 4
    ids = [cell["id"] for cell in notebook["cells"]]
    assert len(ids) == len(set(ids))
    # スライドからの #scrollTo=secN リンクの飛び先
    assert {f"sec{n}" for n in range(10)} <= set(ids)
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["outputs"] == []
            assert cell["execution_count"] is None


def test_python310_syntax(notebook):
    for source in code_cells(notebook):
        ast.parse(source, feature_version=(3, 10))


def test_self_contained(notebook):
    for source in code_cells(notebook):
        assert "lambda_core" not in source


def test_definitions_match_core(notebook):
    core = {name: ast.dump(rhs) for name, rhs, _ in
            definitions(ast.parse(CORE.read_text(encoding="utf-8")))}
    seen = set()
    for source in code_cells(notebook):
        for name, rhs, _ in definitions(ast.parse(source)):
            if name in core:
                assert ast.dump(rhs) == core[name], name
                seen.add(name)
    assert seen == set(core)


def test_runs_top_to_bottom(namespace):
    assert namespace["to_int"](namespace["FACT"](namespace["FIVE"])) == 120


def test_exercise_checks_accept_answers(notebook, namespace):
    cells = [source for source in code_cells(notebook)
             if EXERCISE.search(source)]
    assert cells
    for source in cells:
        filled = EXERCISE.sub(r"\1 = \2", source)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            exec(compile(filled, str(NOTEBOOK), "exec"), dict(namespace))
        lines = out.getvalue().splitlines()
        results = [line for line in lines if line.endswith("件正解")]
        assert results and not any(line.startswith("NG ") for line in lines)
        for line in results:
            ok, total = line.removesuffix(" 件正解").split("/")
            assert ok == total, line
