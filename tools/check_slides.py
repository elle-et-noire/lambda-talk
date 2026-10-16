"""Execute cumulative slide examples and compare definitions with the core."""

import argparse
import ast
import doctest
import io
from pathlib import Path
import re
import sys
import textwrap
import unicodedata
from dataclasses import dataclass


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "code" / "lambda_core.py"
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*?)\s*$")
PROMPT = re.compile(r"^[ \t]*>>>(?:[ \t]|$)", re.MULTILINE)


@dataclass
class Block:
    code: str
    slide: int
    line: int


def visible_prose(line, in_comment):
    """Mask HTML comments, carrying comment state across prose lines."""
    visible = []
    while line:
        marker = "-->" if in_comment else "<!--"
        index = line.find(marker)
        if index < 0:
            visible.append(" " * len(line) if in_comment else line)
            break
        end = index + len(marker)
        visible.append(" " * end if in_comment
                       else line[:index] + " " * len(marker))
        line = line[end:]
        in_comment = not in_comment
    return "".join(visible), in_comment


def extract_blocks(markdown):
    """Ignore front matter, fenced separators, and HTML comments."""
    lines = markdown.splitlines()
    start = 0
    if lines and lines[0].lstrip("\ufeff").strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() in {"---", "..."}:
                start = index + 1
                break
    slide = 1
    fence = None
    language = None
    body = []
    first_line = 0
    in_comment = False
    for index in range(start, len(lines)):
        line = lines[index]
        match = FENCE.match(line)
        if fence is not None:
            if (match and match[1][0] == fence[0]
                    and len(match[1]) >= len(fence)
                    and not match[2].strip()):
                if language in {"python", "py"}:
                    yield Block(textwrap.dedent("\n".join(body)),
                                slide, first_line)
                fence = None
            else:
                body.append(line)
            continue
        # Comment markers inside fence info strings are literal, like those
        # in the fenced body. Only prose changes the HTML comment state.
        if in_comment or not match:
            line, in_comment = visible_prose(line, in_comment)
            match = FENCE.match(line)
        if match:
            fence = match[1]
            tokens = match[2].split()
            language = tokens[0] if tokens else ""
            body = []
            first_line = index + 2
        elif line.strip() == "---":
            slide += 1
    if fence is not None:
        raise ValueError(f"Unclosed {language or 'unlabelled'} fence "
                         f"at line {first_line - 1}")


def definitions(tree):
    """Yield top-level names, RHS/function nodes, and source locations."""
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            yield node.targets[0].id, node.value, node.lineno
        elif isinstance(node, ast.FunctionDef):
            yield node.name, node, node.lineno


def free_names(node, bound=frozenset()):
    if isinstance(node, ast.Name):
        return {node.id} if isinstance(node.ctx, ast.Load) and (
            node.id not in bound) else set()
    if isinstance(node, ast.Lambda):
        args = node.args
        defaults = args.defaults + [d for d in args.kw_defaults if d]
        names = set().union(*(free_names(d, bound) for d in defaults))
        parameters = args.posonlyargs + args.args + args.kwonlyargs
        local = {arg.arg for arg in parameters}
        local.update(a.arg for a in (args.vararg, args.kwarg) if a)
        return names | free_names(node.body, bound | local)
    return set().union(*(free_names(child, bound)
                         for child in ast.iter_child_nodes(node)))


def unary_lambda(node):
    args = node.args
    return (len(args.posonlyargs) + len(args.args) == 1
            and not (args.kwonlyargs or args.vararg or args.kwarg
                     or args.defaults or args.kw_defaults))


def lint_pure(node):
    """Allow only names, unary lambdas, and unary calls in pure RHSs."""
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
        return []
    if isinstance(node, ast.Expression):
        return lint_pure(node.body)
    if isinstance(node, ast.Lambda):
        problems = [] if unary_lambda(node) else [
            (node.lineno, "lambda needs one argument")]
        return problems + lint_pure(node.body)
    if isinstance(node, ast.Call):
        problems = []
        if len(node.args) != 1 or node.keywords:
            problems.append((node.lineno,
                             "call needs one positional argument, no keywords"))
        for child in [node.func, *node.args]:
            problems.extend(lint_pure(child))
        return problems
    return [(node.lineno, type(node).__name__)]


def lint_definition(name, rhs):
    """Windows deliberately permit ordinary Python, including signatures."""
    return [] if name.startswith("to_") else lint_pure(rhs)


def lint_tree(tree, check_dependencies=True, known_names=frozenset()):
    """Check every top-level statement, tracking definitions in source order."""
    available = set(known_names)
    issues = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if (len(node.targets) != 1
                    or not isinstance(node.targets[0], ast.Name)):
                issues.append(("<assignment>", node.lineno,
                               "assignment needs a single Name target"))
                continue
            name = node.targets[0].id
            rhs = node.value
            issues.extend((name, line, reason)
                          for line, reason in lint_definition(name, rhs))
            if not name.startswith("to_"):
                for reference in sorted(free_names(rhs)):
                    if reference == name:
                        reason = f"self reference: {reference}"
                    elif reference.startswith("to_"):
                        reason = f"window reference: {reference}"
                    elif check_dependencies and reference not in available:
                        reason = f"forward/undefined reference: {reference}"
                    else:
                        continue
                    issues.append((name, node.lineno, reason))
            available.add(name)
        elif isinstance(node, ast.FunctionDef) and node.name.startswith("to_"):
            available.add(node.name)
        elif isinstance(node, ast.Expr):
            # Observation syntax may use Python probes, windows, print,
            # tuples, and comparisons. Its lambdas must still be unary.
            issues.extend(("<observation>", child.lineno,
                           "lambda needs one argument")
                          for child in ast.walk(node.value)
                          if isinstance(child, ast.Lambda)
                          and not unary_lambda(child))
        else:
            issues.append((getattr(node, "name", "<statement>"), node.lineno,
                           f"{type(node).__name__} is not an allowed "
                           "top-level statement"))
    return issues


def parse_doctest(parser, block, namespace, path):
    """Keep examples and diagnose prose/code silently dropped by doctest."""
    source = textwrap.dedent(block.code.expandtabs())
    parts = parser.parse(source, f"slide-{block.slide}")
    examples = []
    problems = []
    source_lines = source.splitlines(keepends=True)
    cursor = 0
    for part in parts:
        if isinstance(part, doctest.Example):
            examples.append(part)
            end_line = (part.lineno + len(part.source.splitlines())
                        + len(part.want.splitlines()))
            cursor = sum(map(len, source_lines[:end_line]))
            # No global relaxations: each expectation selects its options.
            part.options.update({
                doctest.IGNORE_EXCEPTION_DETAIL:
                    part.want.startswith("Traceback"),
                doctest.ELLIPSIS: "..." in part.want,
                doctest.NORMALIZE_WHITESPACE:
                    len(part.want.splitlines()) > 1,
            })
        elif part:
            # Searching also accounts for comment-only prompts, which the
            # parser consumes without returning an Example.
            start = source.index(part, cursor)
            first_line = block.line + source.count("\n", 0, start)
            problems.extend((first_line + offset,
                             "text outside doctest example: " + line.strip())
                            for offset, line in enumerate(part.splitlines())
                            if line.strip() and not line.lstrip().startswith("#"))
            cursor = start + len(part)
    test = doctest.DocTest(examples, namespace, f"slide-{block.slide}",
                           str(path), block.line - 1, block.code)
    # DocTest copies globs by default. Share the actual dictionary.
    test.globs = namespace
    return test, problems


class SlideRunner(doctest.DocTestRunner):
    def __init__(self, slide, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slide = slide

    def location(self, out, test, example):
        line = test.lineno + example.lineno + 1
        out(f"FAIL slide {self.slide}, markdown line {line}\n")

    def report_failure(self, out, test, example, got):
        self.location(out, test, example)
        super().report_failure(out, test, example, got)

    def report_unexpected_exception(self, out, test, example, exc_info):
        self.location(out, test, example)
        super().report_unexpected_exception(out, test, example, exc_info)


def check(path, preload_core=False):
    core_source = CORE.read_text(encoding="utf-8")
    core_entries = list(definitions(ast.parse(core_source)))
    core_defs = {name: ast.dump(rhs) for name, rhs, _ in core_entries}
    known_names = set(core_defs) if preload_core else set()
    namespace = {"__name__": "__slides__"}
    if preload_core:
        exec(compile(core_source, str(CORE), "exec"), namespace)
    counts = dict(run=0, doctests=0, examples=0, skipped=0,
                  warnings=0, failures=0)
    slide_only = set()
    parser = doctest.DocTestParser()

    def failure(block, line, message):
        counts["failures"] += 1
        print(f"FAIL slide {block.slide}, markdown line {line}: {message}")

    try:
        blocks = list(extract_blocks(path.read_text(encoding="utf-8")))
    except ValueError as error:
        print(f"FAIL {path}: {error}")
        return 1
    if not blocks:
        print(f"FAIL {path}: no python blocks found")
        return 1
    for block in blocks:
        lines = block.code.splitlines()
        if len(lines) > 12:
            counts["warnings"] += 1
            print(f"WARN slide {block.slide}, markdown line {block.line}: "
                  f"block has {len(lines)} lines (max 12)")
        for offset, line in enumerate(lines):
            width = sum(2 if unicodedata.east_asian_width(char) in {"W", "F"}
                        else 1 for char in line)
            if width > 64:
                counts["warnings"] += 1
                print(f"WARN slide {block.slide}, markdown line "
                      f"{block.line + offset}: line has {width} columns "
                      "(max 64)")
        if lines and lines[0] == "# 実行しない":
            counts["skipped"] += 1
            continue
        counts["run"] += 1
        is_doctest = bool(PROMPT.search(block.code))
        try:
            failures_before = counts["failures"]
            if is_doctest:
                test, problems = parse_doctest(parser, block, namespace, path)
                for line, reason in problems:
                    failure(block, line, reason)
                sources = [(ex.source, block.line + ex.lineno)
                           for ex in test.examples]
                counts["doctests"] += 1
                counts["examples"] += len(test.examples)
            else:
                sources = [(block.code, block.line)]
            available = set(known_names)
            for source, first_line in sources:
                try:
                    tree = ast.parse(source)
                except SyntaxError as error:
                    failure(block, first_line + (error.lineno or 1) - 1,
                            f"SyntaxError: {error.msg}")
                    continue
                for name, line, reason in lint_tree(
                        tree, known_names=available):
                    failure(block, first_line + line - 1,
                            f"rule lint {name}: {reason}")
                for name, rhs, line in definitions(tree):
                    available.add(name)
                    if name in core_defs:
                        if ast.dump(rhs) != core_defs[name]:
                            failure(block, first_line + line - 1,
                                    f"AST mismatch for {name}")
                    else:
                        slide_only.add(name)
            # Invalid compound statements may loop forever; never execute
            # a block that failed static checks.
            if counts["failures"] != failures_before:
                continue
            if is_doctest:
                output = io.StringIO()
                runner = SlideRunner(block.slide)
                result = runner.run(test, out=output.write,
                                    clear_globs=False)
                counts["failures"] += result.failed
                print(output.getvalue(), end="")
            else:
                # Padding preserves markdown line numbers in tracebacks.
                padded = "\n" * (block.line - 1) + block.code
                exec(compile(padded, str(path), "exec"), namespace)
            known_names.update(available & namespace.keys())
        except Exception as error:
            line = (error.lineno if isinstance(error, SyntaxError)
                    else block.line)
            traceback = error.__traceback__
            while traceback is not None:
                if traceback.tb_frame.f_code.co_filename == str(path):
                    line = traceback.tb_lineno
                    break
                traceback = traceback.tb_next
            failure(block, line,
                    f"{type(error).__name__}: {error}")
    if slide_only:
        print("INFO names only in slides: " + ", ".join(sorted(slide_only)))
    print("Summary: blocks run={run} / doctests={doctests} / "
          "examples={examples} / skipped={skipped} / warnings={warnings} / "
          "failures={failures}".format(**counts))
    return int(counts["failures"] > 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--preload-core", action="store_true")
    args = parser.parse_args()
    return check(args.markdown, args.preload_core)


if __name__ == "__main__":
    sys.exit(main())
