#!/usr/bin/env python3
import os
import re
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION = "1.6.1"


def is_year_dir(name: str) -> bool:
    return re.fullmatch(r"\d{4}", name) is not None


def increase_headings(content: str) -> str:
    """将标题级别增加一级"""
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith("#"):
            # 在标题前添加一个#，增加一级
            line = "##" + line
        new_lines.append(line)
    return "\n".join(new_lines)


def add_page_breaks(content: str) -> str:
    """在标题前添加分页符"""
    # 使用HTML分页符<div style="page-break-before: always;"></div>
    page_break = '<div style="page-break-before: always;"></div>\n\n'

    # 在一级、二级、三级标题前添加分页符
    # 使用正则表达式匹配标题行
    patterns = [
        # r"^(# .+)$",  # 一级标题
        r"^(## .+)$",  # 二级标题
        r"^(### .+)$",  # 三级标题
        r"^(#### .+)$",  # 四级标题
    ]

    for pattern in patterns:
        content = re.sub(
            pattern, lambda m: page_break + m.group(1), content, flags=re.MULTILINE
        )

    return content


def main():
    # 设置目录路径
    merged_dir = os.path.join(BASE_DIR, "merged")
    output_dir = os.path.join(BASE_DIR, "epub")
    output_file = os.path.join(output_dir, f"王烁·认知训练_{VERSION}.epub")

    # 清理旧文件
    if os.path.exists(merged_dir):
        shutil.rmtree(merged_dir)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # 创建必要的目录
    os.makedirs(merged_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 合并Markdown文件
    merged_path = os.path.join(merged_dir, "merged.md")
    year_dirs = sorted([d for d in os.listdir(BASE_DIR) if is_year_dir(d)])

    merged_content = ""
    merged_content += "# 王烁·认知训练\n\n"
    for year in year_dirs:
        merged_content += f"## 30天认知训练营·{year}\n\n"
        year_path = os.path.join(BASE_DIR, year)
        files = sorted(os.listdir(year_path))
        for f in files:
            if f.endswith(".md"):
                file_path = os.path.join(year_path, f)
                with open(file_path, encoding="utf-8") as md:
                    content = md.read()
                    # 增加标题级别
                    content = increase_headings(content)
                    merged_content += content + "\n"

    # 添加分页符
    merged_content = add_page_breaks(merged_content)

    # 写入合并后的文件
    with open(merged_path, "w", encoding="utf-8") as out:
        out.write(merged_content)

    # 构建pandoc命令
    metadata_file = os.path.join(BASE_DIR, "metadata.yaml")
    css_file = os.path.join(BASE_DIR, "style.css")

    pandoc_cmd = [
        "pandoc",
        "--metadata-file",
        metadata_file,
        "--toc",
        "--toc-depth=4",
        "--top-level-division=chapter",
        "--css",
        css_file,
        "--split-level=3",
        "-o",
        output_file,
        merged_path,
    ]

    # 运行pandoc
    try:
        subprocess.run(pandoc_cmd, check=True, cwd=merged_dir)
        print(f"✅ EPUB 已生成：{output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc转换失败：{e}")
    except FileNotFoundError:
        print("❌ 未找到pandoc，请确保已安装pandoc")


if __name__ == "__main__":
    main()
