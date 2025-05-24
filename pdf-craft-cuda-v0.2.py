#转换当前目录下所有PDF：生成同名的md文件和存放图像的目录
#   for pdf_file in *.pdf; do     md_file="${pdf_file%.pdf}.md";          python pdf-craft-cuda-v0.2.py "$pdf_file" "$md_file"; done
#转换单个PDF：生成同名的md文件和存放图像的目录
#    python pdf-craft-cuda-v0.2.py pdf_file
#

import os
import sys
import shutil
import warnings
import os
from tqdm import tqdm
from pdf_craft import PDFPageExtractor, MarkDownWriter, ExtractedTableFormat
os.environ['NO_ALBUMENTATIONS_UPDATE'] = '1'  # 禁用Albumentations更新检查
warnings.filterwarnings("ignore", category=UserWarning)  # 忽略UserWarning

def main():
    if len(sys.argv) < 2:
        print("Usage: python test.py path/to/source.pdf [output_markdown_filename]")
        sys.exit(1)

    pdf_file = os.path.abspath(sys.argv[1])
    # 获取文件名
    filename = os.path.basename(pdf_file)
    # 去除扩展名
    filename_without_extension = os.path.splitext(filename)[0]
    filename_with_md = filename_without_extension + ".md"
    #output_dir_path = _project_dir_path("output", clean=True)
    current_working_dir = os.getcwd()
    # 获取文件所在的目录（绝对路径形式）
    directory = os.path.dirname(os.path.abspath(pdf_file))
    output_dir_path=directory

    print(f"文件名 ：{filename_with_md}")
    print(f"当前目录：{current_working_dir}")
    print(f"输入文件：{pdf_file}")
    print(f"所在目录：{directory}")
    print(f"输出目录：{output_dir_path}")

    # 获取输出文件名，默认为 output.md
    if len(sys.argv) >= 3:
        output_md_filename = sys.argv[2]
    else:
        output_md_filename = filename_with_md

    # 如果传入的文件名是相对路径，只在 output 文件夹下生成
    # 如果是绝对路径，则直接使用
    if not os.path.isabs(output_md_filename):
        markdown_path = os.path.join(output_dir_path, output_md_filename)
    else:
        markdown_path = output_md_filename

    extractor = PDFPageExtractor(
        device="cuda",
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
                bar = tqdm(total=n, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
                          ncols=100)

        with MarkDownWriter(markdown_path, filename_without_extension, "utf-8") as md:
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
