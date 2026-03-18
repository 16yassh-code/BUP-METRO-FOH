from __future__ import annotations

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="BUILDUP – Metro FOH Tracker",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="expanded",
)


STATIONS = ["LDN", "ATL", "AEC", "ABP"]
SECTION_CONFIG = {
    "Sample Submission Tracker": {
        "columns": [
            "Description",
            "Form Submission",
            "Sample Submission",
            "Approval Status",
            "Completion Date",
        ],
        "date_columns": ["Form Submission", "Sample Submission", "Completion Date"],
    },
    "Shop Drawings": {
        "columns": [
            "Activity Description",
            "Duration (Days)",
            "Start Date",
            "Target Date",
            "Completion Date",
        ],
        "date_columns": ["Start Date", "Target Date", "Completion Date"],
    },
    "Procurement": {
        "columns": [
            "Activity Description",
            "Lead Time (Days)",
            "Start Date",
            "Target Delivery Date",
            "Completion Date",
        ],
        "date_columns": ["Start Date", "Target Delivery Date", "Completion Date"],
    },
    "Installation": {
        "columns": [
            "Activity Description",
            "Duration (Days)",
            "Start Date",
            "Target Completion Date",
            "Completion Date",
        ],
        "date_columns": ["Start Date", "Target Completion Date", "Completion Date"],
    },
}
STATUS_OPTIONS = ["Approved", "Under Review", "Pending", "Not Started"]
STATUS_COLORS = {
    "Approved": "#d8f3dc",
    "Under Review": "#fff3bf",
    "Pending": "#ffd8d8",
    "Not Started": "#ffd8d8",
}


def station_seed(station: str) -> dict[str, list[dict[str, str | int | None]]]:
    return {
        "Sample Submission Tracker": [
            {
                "Description": f"{station} Ceiling Panel",
                "Form Submission": "2026-03-01",
                "Sample Submission": "2026-03-05",
                "Approval Status": "Approved",
                "Completion Date": "2026-03-08",
            },
            {
                "Description": f"{station} Feature Stone",
                "Form Submission": "2026-03-03",
                "Sample Submission": "2026-03-09",
                "Approval Status": "Under Review",
                "Completion Date": None,
            },
            {
                "Description": f"{station} Signage Package",
                "Form Submission": "2026-03-07",
                "Sample Submission": None,
                "Approval Status": "Pending",
                "Completion Date": None,
            },
        ],
        "Shop Drawings": [
            {
                "Activity Description": f"{station} FOH Wall Elevations",
                "Duration (Days)": 7,
                "Start Date": "2026-03-04",
                "Target Date": "2026-03-11",
                "Completion Date": "2026-03-10",
            },
            {
                "Activity Description": f"{station} Ticket Hall Details",
                "Duration (Days)": 10,
                "Start Date": "2026-03-08",
                "Target Date": "2026-03-18",
                "Completion Date": None,
            },
            {
                "Activity Description": f"{station} Wayfinding Coordination",
                "Duration (Days)": 6,
                "Start Date": "2026-03-12",
                "Target Date": "2026-03-18",
                "Completion Date": None,
            },
        ],
        "Procurement": [
            {
                "Activity Description": f"{station} Stainless Steel Trims",
                "Lead Time (Days)": 21,
                "Start Date": "2026-03-02",
                "Target Delivery Date": "2026-03-23",
                "Completion Date": None,
            },
            {
                "Activity Description": f"{station} Lighting Fixtures",
                "Lead Time (Days)": 28,
                "Start Date": "2026-03-06",
                "Target Delivery Date": "2026-04-03",
                "Completion Date": None,
            },
            {
                "Activity Description": f"{station} Feature Glass Panels",
                "Lead Time (Days)": 18,
                "Start Date": "2026-03-10",
                "Target Delivery Date": "2026-03-28",
                "Completion Date": None,
            },
        ],
        "Installation": [
            {
                "Activity Description": f"{station} Ceiling Grid Installation",
                "Duration (Days)": 12,
                "Start Date": "2026-03-09",
                "Target Completion Date": "2026-03-21",
                "Completion Date": None,
            },
            {
                "Activity Description": f"{station} Stone Cladding Install",
                "Duration (Days)": 16,
                "Start Date": "2026-03-15",
                "Target Completion Date": "2026-03-31",
                "Completion Date": None,
            },
            {
                "Activity Description": f"{station} Signage Fixing",
                "Duration (Days)": 5,
                "Start Date": "2026-03-20",
                "Target Completion Date": "2026-03-25",
                "Completion Date": None,
            },
        ],
    }


def initial_data() -> dict[str, dict[str, pd.DataFrame]]:
    data: dict[str, dict[str, pd.DataFrame]] = {}
    for station in STATIONS:
        seeded = station_seed(station)
        data[station] = {}
        for section, rows in seeded.items():
            df = pd.DataFrame(rows)
            for date_column in SECTION_CONFIG[section]["date_columns"]:
                df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
            data[station][section] = df
    return data


def apply_light_theme() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(165, 214, 255, 0.42), transparent 26%),
                    linear-gradient(180deg, #f8fbff 0%, #eef4fb 100%);
                color: #17324d;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #f5f9ff 0%, #edf3fb 100%);
                border-right: 1px solid #dbe6f3;
            }

            .hero {
                padding: 1.8rem;
                border-radius: 24px;
                background: linear-gradient(135deg, #ffffff 0%, #eaf4ff 100%);
                border: 1px solid #dce8f5;
                box-shadow: 0 18px 40px rgba(35, 71, 112, 0.08);
                margin-bottom: 1.25rem;
            }

            .station-card {
                padding: 1.25rem;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #dce8f5;
                box-shadow: 0 14px 30px rgba(35, 71, 112, 0.07);
                min-height: 220px;
            }

            .page-banner {
                padding: 1.2rem 1.4rem;
                border-radius: 20px;
                background: linear-gradient(135deg, #ffffff 0%, #eef7ff 100%);
                border: 1px solid #dce8f5;
                box-shadow: 0 12px 28px rgba(35, 71, 112, 0.07);
                margin-bottom: 1rem;
            }

            .metric-strip {
                padding: 0.85rem 1rem;
                border-radius: 16px;
                background: #ffffff;
                border: 1px solid #dce8f5;
                text-align: center;
            }

            .progress-shell {
                width: 100%;
                height: 10px;
                border-radius: 999px;
                background: #e8eef5;
                overflow: hidden;
                margin: 0.65rem 0 0.85rem;
            }

            .progress-fill {
                height: 100%;
                border-radius: 999px;
                background: linear-gradient(90deg, #6ab7ff 0%, #1f7ae0 100%);
            }

            .section-block {
                margin-top: 1.2rem;
                margin-bottom: 0.55rem;
            }

            .section-heading {
                font-size: 1.1rem;
                font-weight: 700;
                color: #17324d;
                margin-bottom: 0.25rem;
            }

            div[data-testid="stExpander"] {
                border: 1px solid #dce8f5;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.92);
                overflow: hidden;
                box-shadow: 0 10px 24px rgba(35, 71, 112, 0.06);
            }

            .small-copy {
                color: #5d7692;
                font-size: 0.95rem;
                margin-bottom: 0.75rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def table_column_config(section: str) -> dict[str, st.column_config.Column]:
    config: dict[str, st.column_config.Column] = {}
    for column in SECTION_CONFIG[section]["date_columns"]:
        config[column] = st.column_config.DateColumn(column, format="YYYY-MM-DD")

    if "Approval Status" in SECTION_CONFIG[section]["columns"]:
        config["Approval Status"] = st.column_config.SelectboxColumn(
            "Approval Status",
            options=STATUS_OPTIONS,
            required=True,
        )

    if "Duration (Days)" in SECTION_CONFIG[section]["columns"]:
        config["Duration (Days)"] = st.column_config.NumberColumn(
            "Duration (Days)", min_value=0, step=1
        )

    if "Lead Time (Days)" in SECTION_CONFIG[section]["columns"]:
        config["Lead Time (Days)"] = st.column_config.NumberColumn(
            "Lead Time (Days)", min_value=0, step=1
        )
    return config


def filter_dataframe(df: pd.DataFrame, filter_term: str) -> pd.DataFrame:
    if not filter_term:
        return df
    mask = df.fillna("").astype(str).apply(
        lambda row: row.str.contains(filter_term, case=False, na=False).any(), axis=1
    )
    return df[mask].reset_index(drop=True)


def style_status_table(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    if "Approval Status" not in df.columns:
        return df.style

    def highlight_status(value: str) -> str:
        color = STATUS_COLORS.get(value, "#ffffff")
        return f"background-color: {color}; color: #17324d; font-weight: 600;"

    return df.style.map(highlight_status, subset=["Approval Status"])


def station_metrics(station: str) -> dict[str, int | float | str]:
    station_data = st.session_state.station_data[station]
    total_items = sum(len(df) for df in station_data.values())
    completed_items = sum(
        int(df["Completion Date"].notna().sum())
        for df in station_data.values()
        if "Completion Date" in df.columns
    )
    approved_samples = int(
        station_data["Sample Submission Tracker"]["Approval Status"]
        .fillna("Not Started")
        .eq("Approved")
        .sum()
    )
    review_samples = int(
        station_data["Sample Submission Tracker"]["Approval Status"]
        .fillna("Not Started")
        .eq("Under Review")
        .sum()
    )
    pending_samples = int(
        station_data["Sample Submission Tracker"]["Approval Status"]
        .fillna("Not Started")
        .isin(["Pending", "Not Started"])
        .sum()
    )
    progress = round((completed_items / total_items) * 100, 1) if total_items else 0.0

    if progress >= 75:
        stage = "On Track"
    elif progress >= 40:
        stage = "In Progress"
    else:
        stage = "Early Stage"

    return {
        "Station": station,
        "Tracked Items": total_items,
        "Completed": completed_items,
        "Progress %": progress,
        "Approved Samples": approved_samples,
        "Under Review": review_samples,
        "Pending Samples": pending_samples,
        "Overall Status": stage,
    }


def home_summary_dataframe() -> pd.DataFrame:
    return pd.DataFrame([station_metrics(station) for station in STATIONS])


def station_filter_options(station: str) -> list[str]:
    values = set()
    for df in st.session_state.station_data[station].values():
        first_column = df.columns[0]
        values.update(str(item) for item in df[first_column].dropna().tolist())
    return ["All"] + sorted(values)


def render_home() -> None:
    summary_df = home_summary_dataframe()
    total_tracked = int(summary_df["Tracked Items"].sum())
    total_completed = int(summary_df["Completed"].sum())
    avg_progress = round(float(summary_df["Progress %"].mean()), 1)
    active_reviews = int(summary_df["Under Review"].sum())

    st.markdown(
        """
        <div class="hero">
            <h1 style="margin:0; color:#17324d;">BUILDUP – Metro FOH</h1>
            <p style="margin:0.5rem 0 0; color:#58708b; font-size:1.05rem;">
                Central dashboard for tracking progress across all Metro FOH stations before drilling into each station page.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_metrics = st.columns(4)
    top_values = [
        ("Stations", str(len(STATIONS))),
        ("Tracked Items", str(total_tracked)),
        ("Completed Items", str(total_completed)),
        ("Average Progress", f"{avg_progress}%"),
    ]
    for col, (label, value) in zip(top_metrics, top_values):
        with col:
            st.markdown(
                f"""
                <div class="metric-strip">
                    <div style="font-size:0.82rem; color:#6a819b;">{label}</div>
                    <div style="font-size:1.7rem; font-weight:700; color:#17324d;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <div class="section-block">
            <div class="section-heading">Station Snapshot</div>
            <div class="small-copy">
                Each card shows current completion progress, sample approval position, and overall station health.
                There are currently {active_reviews} sample items under review across the project.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    for col, station in zip(cols, STATIONS):
        metrics = station_metrics(station)
        with col:
            st.markdown(
                f"""
                <div class="station-card">
                    <div style="font-size:0.82rem; color:#6a819b; letter-spacing:0.08em;">STATION</div>
                    <div style="font-size:2rem; font-weight:700; color:#17324d; margin-top:0.35rem;">{station}</div>
                    <div style="margin-top:0.65rem; color:#4f6884; font-size:0.95rem;">
                        {metrics["Overall Status"]} • {metrics["Completed"]} of {metrics["Tracked Items"]} items complete
                    </div>
                    <div class="progress-shell">
                        <div class="progress-fill" style="width:{metrics["Progress %"]}%;"></div>
                    </div>
                    <div style="display:flex; justify-content:space-between; color:#5d7692; font-size:0.92rem;">
                        <span>Progress</span>
                        <span>{metrics["Progress %"]}%</span>
                    </div>
                    <p style="color:#5d7692; line-height:1.5; margin-top:0.7rem;">
                        Approved: {metrics["Approved Samples"]} | Under Review: {metrics["Under Review"]} | Pending: {metrics["Pending Samples"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="section-block">
            <div class="section-heading">Portfolio Overview</div>
            <div class="small-copy">
                Compare all stations side by side. This summary will become the main control point once you provide final station-specific table content.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Progress %": st.column_config.ProgressColumn(
                "Progress %",
                min_value=0,
                max_value=100,
                format="%.1f%%",
            )
        },
    )


def render_station_page(station: str) -> None:
    station_data = st.session_state.station_data[station]
    selected_filter = st.selectbox(
        "Search by product / activity",
        station_filter_options(station),
        key=f"filter_{station}",
    )
    active_filter = "" if selected_filter == "All" else selected_filter

    total_rows = sum(len(df) for df in station_data.values())
    approved_count = len(
        station_data["Sample Submission Tracker"][
            station_data["Sample Submission Tracker"]["Approval Status"] == "Approved"
        ]
    )

    st.markdown(
        f"""
        <div class="page-banner">
            <h1 style="margin:0; color:#17324d;">{station} FOH Page</h1>
            <p style="margin:0.45rem 0 0; color:#5d7692;">
                Project tables for submissions, shop drawings, procurement, and installation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(3)
    metrics = [
        ("Live Tables", "4"),
        ("Tracked Items", str(total_rows)),
        ("Approved Samples", str(approved_count)),
    ]
    for col, (label, value) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-strip">
                    <div style="font-size:0.82rem; color:#6a819b;">{label}</div>
                    <div style="font-size:1.7rem; font-weight:700; color:#17324d;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    for section_name, df in station_data.items():
        filtered_df = filter_dataframe(df, active_filter)
        with st.expander(section_name, expanded=True):
            st.markdown(
                f'<div class="small-copy">{section_name} for {station}. Edit cells inline where needed.</div>',
                unsafe_allow_html=True,
            )

            edited_df = st.data_editor(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                num_rows="dynamic",
                column_config=table_column_config(section_name),
                key=f"editor_{station}_{section_name}",
            )

            station_data[section_name] = edited_df.reset_index(drop=True)
            st.dataframe(
                style_status_table(station_data[section_name]),
                use_container_width=True,
                hide_index=True,
            )


if "station_data" not in st.session_state:
    st.session_state.station_data = initial_data()

apply_light_theme()

st.sidebar.markdown("## BUILDUP")
page = st.sidebar.radio("Navigation", ["Home"] + STATIONS, label_visibility="collapsed")

if page == "Home":
    render_home()
else:
    render_station_page(page)
