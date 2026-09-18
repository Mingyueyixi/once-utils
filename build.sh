#!/bin/bash
# 用 uv build 构建 sdist + wheel(替代旧的 pip install build && python -m build)
# 需要本机已安装 uv(https://docs.astral.sh/uv/getting-started/installation/)

if [ -d "./dist" ]; then
    rm -rf ./dist/*
fi

echo "building package..."
uv build
echo "building package completed..."