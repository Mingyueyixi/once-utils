# once-utils

> A Python utility library with simple style, easy to use.

## 简介

`once-utils` 是一组零依赖的轻量 Python 工具，覆盖日常脚本里常见的几类需求。

## 模块

| 模块 | 作用 |
|---|---|
| `onceutils._convert` | 类型 / 数据转换 |
| `onceutils._cmd` | 命令行执行 |
| `onceutils._iter` | 迭代工具（含 `filter2list`） |
| `onceutils._random` | 随机数据生成 |
| `onceutils._pymodule` | Python 模块操作 |
| `onceutils.ex_dict` | dict 扩展 |
| `onceutils.http` | HTTP 客户端封装 |
| `onceutils.analysis` | 文本 / 结构分析 |
| `onceutils.xjson` | JSON 处理 |

## 安装

```bash
pip install once-utils
```

> 安装名（distribution name）是 `once-utils`，**导入名**为 `onceutils`（无连字符、全小写）。这是 PEP 503 的规范化约定，社区主流项目（`scikit-learn` / `sklearn`、`python-dateutil` / `dateutil`、`Flask-SQLAlchemy` / `flask_sqlalchemy` 等）都这么处理。

## 特性

- **零依赖**：仅依赖 Python 标准库
- **类型完备**：包内附带 `py.typed`（PEP 561），mypy / pyright / Pylance 可直接基于源码注解做类型检查
- **src 布局**：源码在 `src/onceutils/`，避免与本地 `utils.py` 误撞名

## 兼容

Python 3.6+。

## 开发

依赖 [uv](https://github.com/astral-sh/uv)。项目采用 `src` 布局，源码在 `src/onceutils/`，测试在 `tests/`，所有打包 / 发布配置集中在 `pyproject.toml`。

```bash
uv sync               # 同步依赖（含 dev 组，自动创建 .venv）
uv run pytest         # 运行测试
uv build              # 构建 sdist + wheel
uv publish            # 发布到 PyPI（需配置凭据）
```

`uv run` 会自动激活 `.venv` 并把工具注入 `$PATH`，不必手动 `source .venv/bin/activate`。

> 因采用 `src` 布局，源码目录不在 `sys.path` 上，**必须先 `uv sync` 再跑测试**，才能验证真实的打包结果。

仓库脚本封装了以上流程：

| 脚本 | 作用 |
|---|---|
| `install.sh` | 可编辑安装：`pip install -e .` |
| `run_test.sh` | 运行测试：`uv run pytest ./tests -vs` |
| `build.sh` | 构建 sdist + wheel：`uv build` |
| `publish.sh` | 发布到 PyPI：`uv publish dist/*` |
| `crlf2lf.sh` | 批量将文本文件 CRLF → LF |

### 换行风格

仓库统一使用 **LF**。若文件被 IDE 误写成 CRLF，可用脚本批量回写：

```bash
# Git Bash / Linux / Cygwin
./crlf2lf.sh                # 处理整个项目（git 跟踪的文件）
./crlf2lf.sh src/onceutils  # 处理指定目录
```

脚本自动跳过二进制文件、只改写真正含 CR 的文件。Windows 上请用 Git Bash 运行：

```powershell
& "C:\Program Files\Git\bin\bash.exe" crlf2lf.sh
```

> 注意：PATH 里的 `bash.exe` 通常指向未安装发行版的 WSL，直接 `bash crlf2lf.sh` 会失败。

## License

MIT