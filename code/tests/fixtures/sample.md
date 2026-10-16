---
marp: true
title: Lambda verifier smoke test
---

<div>

```python
ID = lambda x: x
TRUE = lambda t: lambda f: t
FALSE = lambda t: lambda f: f
to_bool = lambda b: b(True)(False)
```

</div>

---

```text
---
This separator is inside a non-Python fence.
```

```python
>>> to_bool(TRUE)
True
>>> to_bool(FALSE)
False
>>> OTHER = ID
```

---

```python
>>> OTHER(TRUE) is TRUE
True
>>> omega = lambda x: x(x)
>>> omega(omega)
Traceback (most recent call last):
  ...
RecursionError: maximum recursion depth exceeded
```

```python
# 実行しない
BROKEN = 1 / 0
```
