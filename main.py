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
  generate_page(
    from_path=os.path.join(os.path.dirname(__file__), "content", "index.md"),
    template_path=os.path.join(os.path.dirname(__file__), "static", "template.html"),
    dest_path=os.path.join(os.path.dirname(__file__), dst, "index.html")
  )
  

if __name__ == "__main__":
  main()