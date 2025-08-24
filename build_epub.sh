#!/bin/bash
set -e  # 出错时退出

VERSION="1.1"

# 工作目录
WORKDIR="$(cd "$(dirname "$0")" && pwd)"
cd "$WORKDIR"

# 合并文件
MERGED_DIR="merged"
MERGED_FILE="merged.md"

# 输出目录和文件
OUTPUT_DIR="epub"
OUTPUT_FILE="王烁·认知训练_$VERSION.epub"

# 如果 merged.md 已存在，先删除
if [ -f "$MERGED_DIR/$MERGED_FILE" ]; then
    echo "🗑️ 发现旧的 merged.md 文件，正在删除..."
    rm "$MERGED_DIR/$MERGED_FILE"
fi

# 确保 merged 目录存在
mkdir -p "$MERGED_DIR"

# 如果 OUTPUT_DIR 已存在，先删除整个目录
if [ -d "$OUTPUT_DIR" ]; then
    echo "🗑️ 发现旧的 $OUTPUT_DIR 目录，正在删除..."
    rm -rf "$OUTPUT_DIR"
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 运行 Python 脚本，生成 merged.md
python3 convert.py

# 进入 merged 目录执行 pandoc
pushd "$MERGED_DIR" > /dev/null

pandoc \
  --metadata-file=../metadata.yaml \
  --toc --toc-depth=3 \
  --top-level-division=chapter \
  --css=../epub.css \
  -o "../$OUTPUT_DIR/$OUTPUT_FILE" \
  "$MERGED_FILE"

popd > /dev/null

# 删除临时 merged.md 文件（保留目录）
# rm -rf "$MERGED_DIR"

echo "✅ EPUB 已生成：$OUTPUT_DIR/$OUTPUT_FILE"
