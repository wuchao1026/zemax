# Zemax 评价函数查询

Zemax 光学设计优化操作数（评价函数）速查工具，支持按分类浏览与关键词检索。

**在线访问**：[zemax.w-u.top](https://zemax.w-u.top)（静态导出版，无需后端）

## 功能

- 收录 Zemax 优化评价函数操作数，含名称、说明与分类
- 按类别筛选：数学运算、一阶光学、MTF、PSF、相对照度、公差、ZPL 宏等 30+ 分类
- 关键词即时搜索

## 项目结构

| 文件/目录 | 说明 |
|------|------|
| `app.py` | Flask 版应用（读取 Excel 数据渲染页面） |
| `评价函数.xlsx` | 数据源：操作数名称 / 说明 / 分类 |
| `export_static.py` | 将 Flask 页面导出为静态 HTML |
| `index.html` | 静态导出版（GitHub Pages 实际托管的版本） |
| `templates/`、`static/` | Flask 模板与静态资源 |
| `CNAME` | 自定义域名（zemax.w-u.top） |

## 本地运行（Flask 版）

```powershell
pip install flask pandas openpyxl
python app.py
```

浏览器打开 `http://127.0.0.1:5000`。

## 更新数据

编辑 `评价函数.xlsx`（三列：名称、说明、分类），重新运行 `python export_static.py` 生成新的 `index.html`。

## 部署

通过 GitHub Pages 发布静态版，绑定域名 `zemax.w-u.top`。
