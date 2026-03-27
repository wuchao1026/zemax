import os
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

TYPE_LABEL_MAP = {
    "常用数学运算": "数学运算",
    "镜头参数约束": "镜头参数",
    "实际光线数据约束": "实际光线",
    "非序列物体数据约束": "非序列物体",
    "一阶光学性能": "一阶光学",
    "镜头属性约束": "镜头属性",
    "近轴光线数据约束": "近轴光线",
    "非序列光线追迹和探测器操作数": "非序列",
    "高斯光束数据": "高斯光束",
    "光学膜层和偏振光线追迹数据约束": "膜层偏振",
    "玻璃数据约束": "玻璃数据",
    "系统数据变化": "系统变化",
    "控制评价函数的操作数": "控制项",
    "梯度折射率控制操作数": "梯度折射",
    "组件位置约束": "组件位置",
    "鬼像聚焦控制": "鬼像聚焦",
    "热膨胀系数数据": "热膨胀",
    "光纤耦合操作数": "光纤耦合",
    "附加数据约束": "附加数据",
    "多重结构数据data)": "多重结构",
    "参数数据约束": "参数数据",
    "用户自定义操作数": "用户操作",
    "相对照度操作数": "相对照度",
    "最佳拟合球面数据": "拟合球面",
    "用ZPL宏优化": "ZPL宏",
    "物理光学传播": "物理光学",
    "灵敏度公差数据": "灵敏度公差",
    "光学制造全息图光学构造约束": "制造全息",
    "PSF/斯特列尔比值": "PSF",
    "MTF数据": "MTF",
    "傅科分析": "傅科",
    "圈入能量": "圈能",
}


def load_items():
    file_path = os.path.join(os.getcwd(), "评价函数.xlsx")
    if not os.path.exists(file_path):
        return []
    df = pd.read_excel(file_path, header=None, engine="openpyxl")
    df = df.iloc[:, :3]
    df.columns = ["name", "desc", "type"]
    df = df.dropna(how="all")
    df["name"] = df["name"].astype(str).str.strip()
    df["type"] = df["type"].astype(str).fillna("").str.strip()
    df["desc"] = df["desc"].astype(str).fillna("").str.strip()
    items = []
    for _, row in df.iterrows():
        if row["name"]:
            items.append(
                {"name": row["name"], "type": row["type"], "desc": row["desc"]}
            )
    return items


def build_nav_types(items):
    type_count = {}
    for item in items:
        type_name = item["type"] or "未分类"
        type_count[type_name] = type_count.get(type_name, 0) + 1
    for item in items:
        type_name = item["type"] or "未分类"
        item["nav_type"] = type_name if type_count.get(type_name, 0) > 3 else "其他函数"

    nav_count = {}
    for item in items:
        nav_type = item["nav_type"]
        nav_count[nav_type] = nav_count.get(nav_type, 0) + 1

    sorted_types = sorted(
        (
            (type_name, count)
            for type_name, count in nav_count.items()
            if type_name != "其他函数"
        ),
        key=lambda x: (-x[1], x[0]),
    )
    nav_types = [{"name": "全部", "count": len(items), "key": "全部"}]
    nav_types.extend(
        {
            "name": TYPE_LABEL_MAP.get(type_name, type_name),
            "count": count,
            "key": type_name,
        }
        for type_name, count in sorted_types
    )
    if nav_count.get("其他函数"):
        nav_types.append(
            {"name": "其他函数", "count": nav_count["其他函数"], "key": "其他函数"}
        )
    return nav_types


@app.route("/")
def index():
    items = load_items()
    nav_types = build_nav_types(items)
    return render_template(
        "index.html",
        items=items,
        nav_types=nav_types,
        file_name="评价函数.xlsx",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
