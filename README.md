# once-utils

A lib with simple style, easy to use

## 安装

```bash
pip install once-utils
```

## 开发

项目采用 `src` 布局：源码在 `src/onceutils/`，测试在 `tests/`，全部配置集中在 `pyproject.toml`。

```bash
# 可编辑安装（含 pytest / build / twine）
pip install -e ".[dev]"

# 运行测试
python -m pytest

# 构建 sdist + wheel
python -m build
```

> 因为是 `src` 布局，源码目录不在 `sys.path` 上，**必须先安装再运行测试**，这样才能确保验证的是真实的打包结果。
