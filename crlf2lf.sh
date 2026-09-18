#!/bin/bash
# 将项目内文本文件的 CRLF 换行批量转换为 LF 换行
#
# 用法:
#   ./crlf2lf.sh            # 处理 git 仓库跟踪的文件(自动排除 .git)
#   ./crlf2lf.sh <dir>      # 处理指定目录下的所有文件
#
# Windows 上请用 Git Bash 运行，例如:
#   & "C:\Program Files\Git\bin\bash.exe" crlf2lf.sh
# 注意: PATH 里的 C:\Windows\System32\bash.exe 是 WSL，
#       未安装发行版时无法运行本脚本。
#
# 说明:
#   - 前 8000 字节含 NUL 的二进制文件自动跳过
#   - 只有真正含 CR 的文件才会被改写并打印
#   - 依赖 GNU sed 的 `-i`(Git Bash / Cygwin / Linux 均可用)
set -uo pipefail

TARGET_DIR="${1:-.}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "error: directory not found: $TARGET_DIR" >&2
    exit 1
fi

cd "$TARGET_DIR" || exit 1

# 二进制判定: 前 8000 字节含 NUL 字节
is_binary() {
    local nul
    nul=$(head -c 8000 "$1" 2>/dev/null | LC_ALL=C tr -cd '\0' | wc -c)
    [ "${nul:-0}" -gt 0 ]
}

# 统计文件中的 CR 字节数
# 注意: 不要用 `grep -q $'\r'`，MSYS/Git-for-Windows 的 grep 匹配不到单个 CR
count_cr() {
    LC_ALL=C tr -cd '\r' < "$1" 2>/dev/null | wc -c | tr -d '[:space:]'
}

count=0

process_file() {
    local file="$1"

    [ -f "$file" ] || return 0

    if is_binary "$file"; then
        return 0
    fi

    if [ "$(count_cr "$file")" -eq 0 ]; then
        return 0
    fi

    sed -i 's/\r$//' "$file"
    echo "converted: $file"
    count=$((count + 1))
}

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    while IFS= read -r -d '' file; do
        process_file "$file"
    done < <(git ls-files -z)
else
    while IFS= read -r -d '' file; do
        process_file "$file"
    done < <(find . -type f -not -path './.git/*' -print0)
fi

echo "done, converted ${count} file(s)."
