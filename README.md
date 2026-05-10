# 北灵山周末两日计划

这个目录用 `uv` 管理运行环境，并把行程计划拆成结构化配置和可生成的执行版文档。

## 使用方式

启动网页：

```bash
uv run streamlit run app.py
```

生成 Markdown 执行文档：

```bash
uv run python scripts/render_plan.py
```

运行后会生成：

- `dist/beilingshan_weekend_plan.md`：最终执行版行程单
- `dist/call_script.md`：住宿电话确认话术
- `dist/packing_checklist.md`：个人、公共和晚餐采购清单
- `dist/car_assignment.md`：两车分组和导航确认表
- `dist/final_check.md`：出发前最终核对单

## 文件说明

- `app.py`：Streamlit 网页入口，展示总览、时间轴、天气决策、住宿、装备采购、车辆分工和最终确认。
- `trip_config.json`：日期、路线、住宿候选、天气降级规则、分工和采购清单。
- `notebooklm_ppt_brief.md`：面向 NotebookLM/PPT 生成的结构化资料包。
- `scripts/render_plan.py`：用 Python 标准库渲染 Markdown，不依赖第三方包。

出发前一天重点更新根目录 `trip_config.json` 里的天气、住宿和车辆分组。网页会在刷新后读取最新配置；如需同步 Markdown 文档，再重新运行生成命令。
