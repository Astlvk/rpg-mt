# Agent 指南（Python）

修改本仓库 Python 代码后，在提交或结束任务前请执行以下检查（依赖见 `pyproject.toml` 的 `dev` 组，使用 `uv` 运行）。

## 1. Ruff（格式化 + Lint）

```bash
uv run ruff format .
uv run ruff check .
```

若有可自动修复的问题：

```bash
uv run ruff check --fix .
```

## 2. Basedpyright（类型检查）

```bash
uv run basedpyright
```

配置见项目根目录 [`pyrightconfig.json`](./pyrightconfig.json)，默认检查 `app`、`tests`、`alembic` 等目录。

## 建议顺序

```bash
uv run ruff format .
uv run ruff check --fix .
uv run basedpyright
```

三项均通过后再视为 Python 改动完成。
