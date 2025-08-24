#!/usr/bin/env python3
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def is_year_dir(name: str) -> bool:
    return re.fullmatch(r"\d{4}", name) is not None


def adjust_headings(line: str) -> str:
    """把原始文档的标题层级整体降一级"""
    if line.startswith("#"):
        hashes, rest = line.split(" ", 1) if " " in line else (line, "")
        return "#" + hashes + " " + rest
    return line


def main():
    # 确保 merged 目录存在
    merged_dir = os.path.join(BASE_DIR, "merged")
    os.makedirs(merged_dir, exist_ok=True)

    # merged.md 的路径
    merged_path = os.path.join(merged_dir, "merged.md")

    year_dirs = sorted([d for d in os.listdir(BASE_DIR) if is_year_dir(d)])

    with open(merged_path, "w", encoding="utf-8") as out:
        for year in year_dirs:
            out.write(f"# {year}\n\n")
            year_path = os.path.join(BASE_DIR, year)
            files = sorted(os.listdir(year_path))
            for f in files:
                if f.endswith(".md"):
                    file_path = os.path.join(year_path, f)
                    with open(file_path, encoding="utf-8") as md:
                        for line in md:
                            out.write(adjust_headings(line))
                        out.write("\n")


if __name__ == "__main__":
    main()
