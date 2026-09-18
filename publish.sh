#!/bin/bash
# 用 uv publish 上传到 PyPI(替代旧的 pip install twine && twine upload)
# 需要在环境变量里提供 token:
#   export UV_PUBLISH_TOKEN=pypi-xxxx   # 或 PYPI_TOKEN(uv 会自动识别)
#
# 推荐做法: GitHub Actions 上用 Trusted Publishing(OIDC),
#           详见 https://docs.astral.sh/uv/guides/publish/

# 既上传 sdist 也上传 wheel(uv build 产物)
uv publish dist/*