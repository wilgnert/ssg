import os
import shutil
from src.generator import generate_page

def prepare_dst(dst):
  if not os.path.isdir(dst):
    raise ValueError(f"{dst} is not a directory")  
  # wipe directory
  shutil.rmtree(dst)
  os.makedirs(dst)


def main():
  src = "static/"
  dst = "public/"
  # copy tree from src to dst
  prepare_dst(dst)
  shutil.copytree(src, dst, dirs_exist_ok=True)
  # get all file paths from content directory
  content_files = []
  for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "content")):
    for file in files:
      content_files.append(os.path.join(root, file))
  # generate all pages
  for file in content_files:
    if file.endswith(".md"):
      # get relative path from content directory
      rel_path = os.path.relpath(file, os.path.join(os.path.dirname(__file__), "content"))
      # get destination path
      dest_path = os.path.join(dst, rel_path.replace(".md", ".html"))
      # create directories
      os.makedirs(os.path.dirname(dest_path), exist_ok=True)
      # generate page
      generate_page(
        from_path=file,
        template_path=os.path.join(os.path.dirname(__file__), "static", "template.html"),
        dest_path=dest_path
      )

  

if __name__ == "__main__":
  main()