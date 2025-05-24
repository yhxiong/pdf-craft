
import os
import sys
import shutil
from tqdm import tqdm
from pdf_craft import PDFPageExtractor, MarkDownWriter, ExtractedTableFormat

def main():
    if len(sys.argv) < 2:
        print("Usage: python -W ignore::FutureWarning test.py path/to/source.pdf [output_markdown_filename]")
        sys.exit(1)

    pdf_file = os.path.abspath(sys.argv[1])
    #output_dir_path = _project_dir_path("output", clean=True)
    current_working_dir = os.getcwd()
    # 获取文件所在的目录（绝对路径形式）
    directory = os.path.dirname(os.path.abspath(pdf_file))
    output_dir_path=directory

    print(f"当前目录：{current_working_dir}")
    print(f"输入文件：{pdf_file}")
    print(f"当前文件所在目录：{directory}")
    print(f"输出目录：{output_dir_path}")

    # 获取输出文件名，默认为 output.md
    if len(sys.argv) >= 3:
        output_md_filename = sys.argv[2]
    else:
        output_md_filename = "output.md"

    # 如果传入的文件名是相对路径，只在 output 文件夹下生成
    # 如果是绝对路径，则直接使用
    if not os.path.isabs(output_md_filename):
        markdown_path = os.path.join(output_dir_path, output_md_filename)
    else:
        markdown_path = output_md_filename

    extractor = PDFPageExtractor(
        device="cpu",
        model_dir_path=_project_dir_path("models"),
        extract_table_format=ExtractedTableFormat.MARKDOWN,
    )
    bar: tqdm | None = None
    try:
        def report_progress(i: int, n: int):
            nonlocal bar
            if bar:
                bar.update(i)
            else:
                bar = tqdm(total=n)

        with MarkDownWriter(markdown_path, "images", "utf-8") as md:
            for block in extractor.extract(pdf_file, report_progress=report_progress):
                md.write(block)

        print(f"转换完成，输出文件：{markdown_path}")

    finally:
        if bar:
            bar.close()

def _project_dir_path(name: str, clean: bool = False) -> str:
    path = os.path.join(__file__, "..", "..", name)
    path = os.path.abspath(path)
    if clean:
        shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)
    return path

if __name__ == "__main__":
    main()
