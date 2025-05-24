from pdf_craft import PDFPageExtractor, MarkDownWriter

extractor = PDFPageExtractor(
  device="cpu", # If you want to use CUDA, please change to device="cuda" format.
  model_dir_path="/Users/xyh/.cache/huggingface/hub/models--hfl--rbt3/.no_exist/0aa0527ff4170f29e1dfd3eb6ef60dc67e1bf75c/model.safetensors", # The folder address where the AI ​​model is downloaded and installed
)
with MarkDownWriter("result.md", "images", "utf-8") as md:
  for block in extractor.extract(pdf="test1_4.pdf"):
    md.write(block)