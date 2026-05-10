from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "trip_config.json"


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        st.error(f"找不到配置文件：{CONFIG_PATH}")
        st.stop()

    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        st.error(f"配置文件 JSON 格式错误：{exc}")
        st.stop()


def get_config(config: dict[str, Any], key: str, default: Any) -> Any:
    value: Any = config
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            st.warning(f"配置缺少字段：{key}")
            return default
        value = value[part]
    return value


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(32, 83, 64, 0.16), rgba(65, 105, 130, 0.08));
        }
        [data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-radius: 0.95rem;
            padding: 0.8rem 1rem;
            background: rgba(255, 255, 255, 0.04);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
        }
        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 2rem 2.2rem;
            border-radius: 1.45rem;
            border: 1px solid rgba(128, 128, 128, 0.18);
            background:
                radial-gradient(circle at top right, rgba(129, 197, 144, 0.36), transparent 32%),
                linear-gradient(135deg, rgba(47, 102, 82, 0.22), rgba(65, 105, 130, 0.14));
            margin-bottom: 1.2rem;
            box-shadow: 0 18px 48px rgba(0, 0, 0, 0.08);
        }
        .hero-kicker {
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            background: rgba(47, 102, 82, 0.15);
            color: rgb(32, 83, 64);
            font-size: 0.82rem;
            font-weight: 650;
            letter-spacing: 0.06em;
            margin-bottom: 0.65rem;
        }
        .soft-card {
            min-height: 128px;
            padding: 1.05rem 1.1rem;
            border-radius: 1rem;
            border: 1px solid rgba(128, 128, 128, 0.18);
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(128, 128, 128, 0.05));
            margin: 0.55rem 0;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.05);
        }
        .card-label {
            color: rgba(128, 128, 128, 0.98);
            font-size: 0.82rem;
            font-weight: 650;
            letter-spacing: 0.04em;
            margin-bottom: 0.35rem;
        }
        .card-value {
            font-size: 1.06rem;
            font-weight: 720;
            line-height: 1.55;
        }
        .time-row {
            display: grid;
            grid-template-columns: 92px 1fr;
            gap: 0.9rem;
            align-items: start;
            padding: 0.95rem 1rem;
            border-radius: 1rem;
            border: 1px solid rgba(128, 128, 128, 0.16);
            background: rgba(128, 128, 128, 0.055);
            margin-bottom: 0.75rem;
        }
        .time-pill {
            display: inline-block;
            text-align: center;
            padding: 0.3rem 0.55rem;
            border-radius: 999px;
            background: rgba(47, 102, 82, 0.14);
            color: rgb(32, 83, 64);
            font-weight: 720;
            font-size: 0.82rem;
        }
        .section-title {
            margin: 1.2rem 0 0.65rem;
            padding-bottom: 0.35rem;
            border-bottom: 1px solid rgba(128, 128, 128, 0.15);
        }
        .badge {
            display: inline-block;
            padding: 0.22rem 0.6rem;
            border-radius: 999px;
            background: rgba(47, 102, 82, 0.12);
            color: rgb(32, 83, 64);
            font-size: 0.8rem;
            font-weight: 650;
            margin: 0 0.35rem 0.35rem 0;
        }
        .risk-card {
            border-left: 5px solid rgba(196, 127, 46, 0.85);
            padding: 0.85rem 1rem;
            border-radius: 0.8rem;
            background: rgba(196, 127, 46, 0.08);
            margin-bottom: 0.55rem;
        }
        .small-muted {
            color: rgba(128, 128, 128, 0.95);
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str | None = None) -> None:
    subtitle_html = (
        f'<div class="small-muted">{escape(subtitle)}</div>' if subtitle else ""
    )
    st.markdown(
        f"""
        <div class="section-title">
            <h2 style="margin-bottom: 0.15rem;">{escape(title)}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(label: str, value: str, detail: str = "") -> str:
    detail_html = f'<div class="small-muted">{escape(detail)}</div>' if detail else ""
    return f"""
        <div class="soft-card">
            <div class="card-label">{escape(label)}</div>
            <div class="card-value">{escape(value)}</div>
            {detail_html}
        </div>
    """


def render_list(items: list[str]) -> None:
    for item in items:
        st.markdown(f"- {item}")


def render_checklist(items: list[str], key_prefix: str) -> None:
    for index, item in enumerate(items):
        st.checkbox(item, key=f"{key_prefix}_{index}_{item}")


def render_header(config: dict[str, Any]) -> None:
    trip = get_config(config, "trip", {})
    title = trip.get("title", "周末行程计划")
    dates = trip.get("dates", [])
    date_text = " 至 ".join(dates) if dates else "日期待确认"

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-kicker">WEEKEND FIELD PLAN</div>
            <h1 style="margin: 0 0 0.45rem 0;">{escape(title)}</h1>
            <div class="small-muted">{escape(date_text)} · {escape(trip.get("origin", "出发地待确认"))}出发</div>
            <p style="max-width: 760px; margin-top: 0.85rem; font-size: 1.04rem; line-height: 1.7;">
                {escape(trip.get("primary_goal", ""))}
            </p>
            <span class="badge">两日自驾</span>
            <span class="badge">北灵山徒步</span>
            <span class="badge">农家乐下厨</span>
            <span class="badge">鸡鸣驿人文游</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_people, col_cars, col_return, col_review = st.columns(4)
    col_people.metric("人数", f"{trip.get('people', '待填')} 人")
    col_cars.metric("车辆", f"{trip.get('cars', '待填')} 车")
    col_return.metric("返程", trip.get("return_target", "待确认"))
    col_review.metric("天气复核", get_config(config, "weather.review_time", "待确认"))


def render_overview(config: dict[str, Any]) -> None:
    trip = get_config(config, "trip", {})
    routes = get_config(config, "routes", {})

    section_title("行程总览", "把两天的交通、徒步、住宿和返程压缩成一张可执行路线图。")
    st.info(
        f"{trip.get('people', 6)} 人、{trip.get('cars', 2)} 车从{trip.get('origin', '天津市区')}出发，"
        "第一天北灵山/韭菜坡徒步和下厨，第二天鸡鸣驿古城半日游后返津。"
    )

    cols = st.columns(3)
    cols[0].markdown(
        info_card(
            "第一段车程",
            f"{routes.get('day1_drive', {}).get('from', '待确认')} -> {routes.get('day1_drive', {}).get('to', '待确认')}",
            routes.get("day1_drive", {}).get("planned_time", ""),
        ),
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        info_card(
            "徒步强度",
            f"{routes.get('hike', {}).get('distance', '待确认')} · {routes.get('hike', {}).get('elevation_gain', '待确认')}",
            f"硬回撤：{routes.get('hike', {}).get('hard_turnaround_time', '待确认')}",
        ),
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        info_card(
            "第二天",
            routes.get("day2_drive", {}).get("to", "待确认"),
            routes.get("day2_drive", {}).get("return", ""),
        ),
        unsafe_allow_html=True,
    )

    st.markdown("#### 关键风险")
    for item in [
        "第一天车程加徒步时间紧，必须早出发并执行 15:00 回撤。",
        "北灵山海拔高，遇雨和风会明显降温，装备不达标时应降级。",
        "野韭菜只作少量体验式采摘，遵守当地管理要求。",
    ]:
        st.markdown(
            f'<div class="risk-card">{escape(item)}</div>', unsafe_allow_html=True
        )


def render_timeline(config: dict[str, Any]) -> None:
    section_title("两日时间轴", "按时间块拆解每天的行程动作，适合出发当天照着执行。")
    schedule = get_config(config, "schedule", [])
    if not schedule:
        st.warning("暂无时间轴数据。")
        return

    tabs = st.tabs(
        [f"{day.get('day', 'Day')} · {day.get('date', '')}" for day in schedule]
    )
    for tab, day in zip(tabs, schedule, strict=False):
        with tab:
            for index, (time_range, activity) in enumerate(
                day.get("items", []), start=1
            ):
                st.markdown(
                    f"""
                    <div class="time-row">
                        <div><span class="time-pill">{escape(time_range)}</span></div>
                        <div><strong>步骤 {index}</strong><br>{escape(activity)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with st.expander("徒步执行规则", expanded=True):
        hike = get_config(config, "routes.hike", {})
        st.write(f"路线：{hike.get('name', '待确认')}")
        st.write(f"距离：{hike.get('distance', '待确认')}")
        st.write(f"爬升：{hike.get('elevation_gain', '待确认')}")
        st.write(f"预计耗时：{hike.get('duration', '待确认')}")
        st.write(f"硬回撤时间：{hike.get('hard_turnaround_time', '待确认')}")
        render_list(hike.get("rules", []))


def render_weather(config: dict[str, Any]) -> None:
    weather = get_config(config, "weather", {})
    section_title(
        "天气和降级决策", "把天气不确定性提前转成明确的执行、降级和取消条件。"
    )
    st.warning(weather.get("current_reading", "天气信息待确认"))
    st.write(f"复核时间：{weather.get('review_time', '待确认')}")
    st.write(f"当前决策：{weather.get('decision', '待确认')}")

    go_tab, downgrade_tab, cancel_tab = st.tabs(["正常执行", "降级", "取消徒步"])
    with go_tab:
        render_checklist(weather.get("go", []), "weather_go")
    with downgrade_tab:
        render_checklist(weather.get("downgrade", []), "weather_downgrade")
    with cancel_tab:
        render_checklist(weather.get("cancel_hike", []), "weather_cancel")


def render_lodging(config: dict[str, Any]) -> None:
    lodging = get_config(config, "lodging", {})
    section_title("住宿候选和电话确认", "优先保证车程、厨房、停车、热水和可取消政策。")

    with st.expander("住宿硬性条件", expanded=True):
        render_checklist(lodging.get("must_have", []), "lodging_must")

    st.markdown("#### 优先级")
    for index, item in enumerate(lodging.get("preferred_order", []), start=1):
        st.write(f"{index}. {item}")

    st.markdown("#### 候选住宿")
    for index, candidate in enumerate(lodging.get("candidates", [])):
        with st.container(border=True):
            st.markdown(f"##### {candidate.get('name', '候选住宿')}")
            col_area, col_phone = st.columns([2, 1])
            col_area.write(f"区域：{candidate.get('area', '待确认')}")
            col_phone.write(f"电话：{candidate.get('phone', '待确认')}")
            st.write(f"选择理由：{candidate.get('why', '待确认')}")
            with st.expander("电话确认事项"):
                render_checklist(candidate.get("verify", []), f"lodging_verify_{index}")


def render_packing(config: dict[str, Any]) -> None:
    packing = get_config(config, "packing", {})
    section_title("装备和采购清单", "个人装备、公共安全物资和晚餐食材分开勾选。")
    personal_tab, shared_tab, dinner_tab = st.tabs(["个人必带", "公共装备", "晚餐采购"])

    with personal_tab:
        render_checklist(packing.get("personal", []), "packing_personal")
    with shared_tab:
        render_checklist(packing.get("shared", []), "packing_shared")
    with dinner_tab:
        render_checklist(packing.get("dinner", []), "packing_dinner")


def render_cars(config: dict[str, Any]) -> None:
    car_plan = get_config(config, "car_plan", {})
    section_title(
        "两车分组和分工", "两辆车各自固定司机、副驾和物资责任人，减少临场混乱。"
    )
    st.write(car_plan.get("assignment_rule", "分组规则待确认"))

    cars = car_plan.get("template", [])
    if cars:
        st.table(cars)

    st.markdown("#### 角色分工")
    render_list(car_plan.get("roles", []))

    with st.expander("车长检查"):
        render_checklist(
            [
                "油量或电量足够",
                "胎压、玻璃水、雨刮正常",
                "每车至少 1 根车载充电线",
                "副驾负责导航和群消息",
                "次日司机不饮酒或只极少量",
            ],
            "car_check",
        )


def render_final_check(config: dict[str, Any]) -> None:
    section_title("出发前最终确认", "按时间点完成天气、住宿、人车和上车前检查。")
    render_checklist(get_config(config, "final_check", []), "final_check")

    st.markdown("#### 上车前重点")
    render_checklist(
        [
            "身份证",
            "防滑徒步鞋",
            "雨衣或冲锋衣",
            "保暖层",
            "1.5-2L 水",
            "午餐路餐",
            "个人药品和充电宝",
        ],
        "boarding_check",
    )


def main() -> None:
    st.set_page_config(
        page_title="北灵山周末两日计划",
        page_icon="BS",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_styles()
    config = load_config()

    render_header(config)

    st.sidebar.markdown("### 北灵山周末计划")
    st.sidebar.caption("轻量网页版 · 数据来自根目录 JSON 配置")
    page = st.sidebar.radio(
        "页面导航",
        ["总览", "时间轴", "天气决策", "住宿", "装备采购", "车辆分工", "最终确认"],
    )
    st.sidebar.divider()
    st.sidebar.markdown("#### 快速提醒")
    st.sidebar.markdown("- 15:00 硬回撤")
    st.sidebar.markdown("- 雨天不登顶")
    st.sidebar.markdown("- 野韭菜少量体验")
    st.sidebar.caption("数据来源：trip_config.json")

    if page == "总览":
        render_overview(config)
    elif page == "时间轴":
        render_timeline(config)
    elif page == "天气决策":
        render_weather(config)
    elif page == "住宿":
        render_lodging(config)
    elif page == "装备采购":
        render_packing(config)
    elif page == "车辆分工":
        render_cars(config)
    elif page == "最终确认":
        render_final_check(config)


if __name__ == "__main__":
    main()
