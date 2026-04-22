import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os
import time
import numpy as np
from utils import MAP_CONFIG, scan_data, load_match_data

# --- Page Config ---
st.set_page_config(page_title="LILA Analytics", layout="wide")

def main():
    # --- UI CSS ---
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
                background-color: #0d1117 !important;
                color: #f0f6fc !important;
                font-family: 'Inter', sans-serif;
            }
            [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; }
            [data-testid="stMetricLabel"] p { color: #ffffff !important; font-weight: 700; text-transform: uppercase; }
            [data-testid="stMetricValue"] > div { color: #58a6ff !important; font-weight: 800; font-family: 'Outfit'; }
            .sidebar-title { color: #58a6ff; font-size: 1.5rem; font-weight: 800; text-align: center; margin-bottom: 20px; font-family: 'Outfit'; }
            [data-testid="stSidebar"] div[data-testid="stExpander"] { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; margin-bottom: 15px; }
            [data-testid="stSidebar"] div[data-testid="stExpander"] summary p { color: #58a6ff !important; font-weight: 800; font-family: 'Outfit' !important; }
            .stButton > button { background: #1c2128; color: #58a6ff; border: 1px solid #58a6ff; border-radius: 12px; font-weight: 700; height: 3rem; width: 100%; }
            .insight-holder { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
            .insight-label { color: #8b949e; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; }
            .insight-value { color: #58a6ff; font-size: 1.4rem; font-weight: 700; font-family: 'Outfit'; }
            .glass-box { background: #161b22; border: 1px solid #30363d; border-radius: 20px; padding: 24px; margin-top: 20px; }
        </style>
    """, unsafe_allow_html=True)

    DATA_PATH = "player_data"
    ASSETS_PATH = os.path.join(DATA_PATH, "minimaps")
    data_index = scan_data(DATA_PATH)

    params = st.query_params
    st.sidebar.markdown('<div class="sidebar-title">🎮 LILA ANALYTICS</div>', unsafe_allow_html=True)
    
    with st.sidebar.expander("📂 DATA SELECTION", expanded=True):
        date_options = sorted(data_index.keys())
        def_date_idx = date_options.index(params["date"]) if "date" in params and params["date"] in date_options else 0
        date = st.selectbox("SELECT DATE", date_options, index=def_date_idx, key="v45_date")
        st.query_params["date"] = date
        
        map_options = sorted(data_index[date].keys())
        def_map_idx = map_options.index(params["map"]) if "map" in params and params["map"] in map_options else 0
        map_name = st.selectbox("SELECT MAP", map_options, index=def_map_idx, key="v45_map")
        st.query_params["map"] = map_name
        
        matches = data_index[date][map_name]
        match_options = list(matches.keys())
        def_mid_idx = match_options.index(params["mid"]) if "mid" in params and params["mid"] in match_options else 0
        match_id = st.selectbox("MATCH ID", match_options, index=def_mid_idx, format_func=lambda x: f"{x[:8]}... ({len(matches[x])} files)", key="v45_mid")
        st.query_params["mid"] = match_id

    if "curr_match" not in st.session_state or st.session_state.curr_match != match_id:
        st.session_state.curr_time = 0.0
        st.session_state.playing = False
        st.session_state.curr_match = match_id

    with st.sidebar.expander("👁️ VISUAL LAYERS", expanded=True):
        show_paths = st.toggle("MOVEMENT PATHS", value=True)
        show_events = st.toggle("EVENT MARKERS", value=True)
        h_type = st.radio("HEATMAP LAYER", ["NONE", "PLAYER DENSITY", "KILL HOTSPOTS"])

    with st.sidebar.expander("🕹️ TACTICAL CONTROLS", expanded=True):
        speed = st.select_slider("SPEED SCALE", [0.5, 1, 2, 5, 10], value=2)
        if st.button("🔄 RESET VIEW"): st.rerun()

    df = load_match_data(matches[match_id])
    if df.empty: return st.error("Telemetry error.")
    df['rel_ts'] = df['rel_ts'] * 1000

    st.markdown(f"<h1>Match Analysis <span style='color:#58a6ff'># {match_id[:8]}</span></h1>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("HUMANS", df[~df['is_bot']]['user_id'].nunique())
    m_col2.metric("BOTS", df[df['is_bot']]['user_id'].nunique())
    m_col3.metric("LOOT", len(df[df['event'] == 'Loot']))
    
    kill_events = df[df['event'].str.contains('Kill', na=False)].copy()
    if not kill_events.empty:
        kill_events['ts_round'] = kill_events['ts'].dt.round('1s')
        unique_kills = kill_events.drop_duplicates(subset=['ts_round', 'x', 'z'])
        m_col4.metric("KILLS", len(unique_kills))
    else: m_col4.metric("KILLS", 0)

    st.markdown("---")
    viz_tab, ins_tab = st.tabs(["🗺️ SPATIAL VISUALIZER", "📈 STRATEGIC INSIGHTS"])

    with viz_tab:
        max_d = float(df['rel_ts'].max())
        c1, c2, c3 = st.columns([1, 1, 6])
        if c1.button("▶️ PLAY" if not st.session_state.playing else "⏸️ PAUSE"):
            st.session_state.playing = not st.session_state.playing
            st.rerun()
        if c2.button("🔄 REPLAY"):
            st.session_state.curr_time = 0.0
            st.session_state.playing = False
            st.rerun()
        
        st.write(f"Timeline: {int(st.session_state.curr_time // 60):02d}:{int(st.session_state.curr_time % 60):02d} / {int(max_d // 60):02d}:{int(max_d % 60):02d}")
        scrub = st.slider("Scrub", 0.0, max_d, st.session_state.curr_time, step=1.0, label_visibility="collapsed", key="v45_slider")
        if not st.session_state.playing: st.session_state.curr_time = scrub

        cfg = MAP_CONFIG[map_name]
        img = Image.open(os.path.join(ASSETS_PATH, cfg["image"]))
        fig = go.Figure()
        fig.add_layout_image(dict(source=img, xref="x", yref="y", x=0, y=1024, sizex=1024, sizey=1024, sizing="stretch", opacity=1, layer="below"))
        
        df_v = df[df['rel_ts'] <= st.session_state.curr_time]
        if h_type != "NONE":
            hd = df_v if h_type == "PLAYER DENSITY" else df_v[df_v['event'].str.contains('Kill', na=False)]
            if not hd.empty: fig.add_trace(go.Histogram2dContour(x=hd['pixel_x'], y=hd['pixel_y'], colorscale='Hot', opacity=0.4, showlegend=False))
        if show_paths:
            for uid, p_df in df_v.groupby('user_id'):
                is_bot = p_df['is_bot'].iloc[0]
                pos = p_df[p_df['event'].str.contains('Position', na=False)]
                if not pos.empty: fig.add_trace(go.Scatter(x=pos['pixel_x'], y=pos['pixel_y'], mode='lines', line=dict(width=3, color='magenta' if is_bot else '#00f2ff'), name=f"P {uid[:4]}"))
        if show_events:
            ev_styles = {'Kill': '#ff4b4b', 'Loot': '#ffd700', 'KilledByStorm': '#58a6ff'}
            for etype, ecolor in ev_styles.items():
                edf = df_v[df_v['event'].str.contains(etype, na=False)].copy()
                if not edf.empty:
                    edf['jx'] = edf['pixel_x'] + np.random.uniform(-4, 4, size=len(edf))
                    edf['jy'] = edf['pixel_y'] + np.random.uniform(-4, 4, size=len(edf))
                    fig.add_trace(go.Scatter(x=edf['jx'], y=edf['jy'], mode='markers', marker=dict(color=ecolor, size=14, line=dict(width=1, color='white')), name=etype))

        fig.update_xaxes(range=[0, 1024], visible=False, fixedrange=False)
        fig.update_yaxes(range=[0, 1024], visible=False, fixedrange=False, scaleanchor="x", scaleratio=1)
        fig.update_layout(dragmode='pan', height=800, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True, legend=dict(font=dict(color="#fff"), orientation="h", y=1.05))
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True, 'displayModeBar': True, 'displaylogo': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with ins_tab:
        st.header("Strategic Intelligence Report")
        i_col1, i_col2, i_col3 = st.columns(3)
        max_dur = df['rel_ts'].max()
        with i_col1: st.markdown(f'<div class="insight-holder"><div class="insight-label">Match Tempo</div><div class="insight-value">{int(max_dur // 60)}m {int(max_dur % 60)}s</div></div>', unsafe_allow_html=True)
        with i_col2: st.markdown(f'<div class="insight-holder"><div class="insight-label">Combat Interactions</div><div class="insight-value">{len(unique_kills)} Events</div></div>', unsafe_allow_html=True)
        with i_col3: st.markdown(f'<div class="insight-holder"><div class="insight-label">Loot Distribution</div><div class="insight-value">{len(df[df["event"] == "Loot"])} Items</div></div>', unsafe_allow_html=True)

    if st.session_state.playing:
        if st.session_state.curr_time < max_d:
            st.session_state.curr_time = min(max_d, st.session_state.curr_time + (speed * 1.5))
            time.sleep(0.01)
            st.rerun()
        else: st.session_state.playing = False; st.rerun()

if __name__ == "__main__":
    main()
