import os
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app import build_nav_types, load_items

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")
dist_dir = os.path.join(BASE_DIR, "dist")
dist_static_dir = os.path.join(dist_dir, "static")
os.makedirs(dist_static_dir, exist_ok=True)

env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html"]),
)
template = env.get_template("export.html")
items = load_items()
html = template.render(
    items=items,
    nav_types=build_nav_types(items),
    file_name="评价函数.xlsx",
)

with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

shutil.copy2(os.path.join(static_dir, "styles.css"), os.path.join(dist_static_dir, "styles.css"))

# 额外在根目录生成 index.html，方便直接双击打开
with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print(os.path.join(BASE_DIR, "index.html"))
print(os.path.join(dist_dir, "index.html"))
