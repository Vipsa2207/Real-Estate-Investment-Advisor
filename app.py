import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from pathlib import Path
from insights import INSIGHTS, INVESTOR_RECS, PLATFORM_RECS, REALITY_CHECK
import plotly.graph_objects as go

st.set_page_config(page_title="SqFt Signal | Property Investment Advisor", page_icon="📡", layout="wide")

PALETTE = ["#1F3B57", "#2A9D8F", "#E9C46A", "#E76F51", "#8D99AE"]  # same as notebook

st.markdown("""
<style>
.hero {background: linear-gradient(120deg, #1F3B57 0%, #2A9D8F 100%);
       padding: 28px 32px; border-radius: 16px; color: white; margin-bottom: 18px;}
.hero h1 {color: white; margin: 0; font-size: 2.2rem;}
.hero p  {color: #E9EEF3; margin: 6px 0 0 0; font-size: 1.05rem;}
.hero .tag {display:inline-block; background: rgba(255,255,255,0.15); padding: 4px 12px;
            border-radius: 20px; margin: 10px 8px 0 0; font-size: 0.85rem;}
</style>
""", unsafe_allow_html=True)

DATA_PATH = Path(__file__).parent / "data" / "india_housing_cleaned.csv.gz"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    # CSV loses category order, so set it again (see Phase 7 note)
    df["Public_Transport_Accessibility"] = pd.Categorical(
        df["Public_Transport_Accessibility"], ["Low", "Medium", "High"], ordered=True)
    df["Furnished_Status"] = pd.Categorical(
        df["Furnished_Status"], ["Unfurnished", "Semi-furnished", "Furnished"], ordered=True)
    return df

df = load_data()

APP_NAME = "SqFt Signal"
TAGLINE = "Cut through the noise. Find the deals that matter."
SUBTITLE = "India Property Investment Advisor · Is it a good investment? What will it be worth in 5 years?"

st.markdown(f"""
<div class="hero">
  <h1>📡 {APP_NAME}</h1>
  <p style="font-size:1.25rem; font-weight:600; color:white;">{TAGLINE}</p>
  <p>{SUBTITLE}</p>
  <span class="tag">📊 {len(df):,} properties</span>
  <span class="tag">🏙️ {df['City'].nunique()} cities</span>
  <span class="tag">🗺️ {df['State'].nunique()} states</span>
  <span class="tag">📈 5% annual growth assumption</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stSidebar"] .stButton button {background: #2A9D8F; border: none; border-radius: 10px;}
[data-testid="stSidebar"] .stButton button:hover {background: #E9C46A;}
[data-testid="stSidebar"] .stButton button p {color: white; font-weight: 600;}
[data-testid="stSidebar"] {background: linear-gradient(180deg, #1F3B57 0%, #24566B 100%);}
[data-testid="stSidebar"] * {color: #F7F9FB;}
[data-testid="stSidebar"] [data-baseweb="select"] * {color: #1F3B57;}   /* dropdown text stays dark */
.match-box {background: rgba(255,255,255,0.12); border-radius: 12px; padding: 12px; text-align: center; margin: 8px 0;}
.match-box .num {font-size: 1.8rem; font-weight: 700; color: #E9C46A;}
</style>
""", unsafe_allow_html=True)

DEFAULTS = {"f_state": [], "f_city": [], "f_type": [], "f_bhk": [],
            "f_price": (10, 500), "f_size": (500, 5000)}

for k, v in DEFAULTS.items():          # set defaults on first load only
    st.session_state.setdefault(k, v)

def reset_filters():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v

sb = st.sidebar
sb.markdown("## 📡 SqFt Signal")
sb.caption("Filter the market")

states = sorted(df["State"].unique())
sb.multiselect("🗺️ State", states, key="f_state", placeholder="All states")

city_pool = df[df["State"].isin(st.session_state.f_state)] if st.session_state.f_state else df
cities = sorted(city_pool["City"].unique())
st.session_state.f_city = [c for c in st.session_state.f_city if c in cities]   # drop cities no longer valid
sb.multiselect("🏙️ City", cities, key="f_city", placeholder="All cities")

sb.multiselect("🏠 Property Type", sorted(df["Property_Type"].unique()), key="f_type", placeholder="All types")
sb.multiselect("🛏️ BHK", [1, 2, 3, 4, 5], key="f_bhk", placeholder="All BHK")
sb.slider("💰 Price (₹ Lakhs)", 10, 500, key="f_price")
sb.slider("📐 Size (sq ft)", 500, 5000, step=50, key="f_size")

sb.button("🔄 Reset filters", on_click=reset_filters, use_container_width=True)

s = st.session_state
fdf = df[df["Price_in_Lakhs"].between(*s.f_price) & df["Size_in_SqFt"].between(*s.f_size)]
if s.f_state: fdf = fdf[fdf["State"].isin(s.f_state)]
if s.f_city:  fdf = fdf[fdf["City"].isin(s.f_city)]
if s.f_type:  fdf = fdf[fdf["Property_Type"].isin(s.f_type)]
if s.f_bhk:   fdf = fdf[fdf["BHK"].isin(s.f_bhk)]

sb.markdown(f"""<div class="match-box"><div class="num">{len(fdf):,}</div>
<div>matching properties ({len(fdf) / len(df):.1%} of market)</div></div>""", unsafe_allow_html=True)

if fdf.empty:
    st.warning("No properties match these filters. Try widening your selection or click 🔄 Reset filters.")
    st.stop()

st.markdown("""
<style>
.kpi {background: white; border-radius: 14px; padding: 16px 18px; box-shadow: 0 2px 10px rgba(31,59,87,0.08);
      border-left: 6px solid var(--accent); height: 100%;}
.kpi .label {font-size: 0.85rem; color: #5B6B7B; font-weight: 600;}
.kpi .value {font-size: 1.7rem; font-weight: 800; color: #1F3B57; margin: 4px 0;}
.kpi .sub   {font-size: 0.8rem; color: #2A9D8F; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

def kpi_card(col, icon, label, value, sub, accent):
    col.markdown(f"""<div class="kpi" style="--accent:{accent}">
        <div class="label">{icon} {label}</div>
        <div class="value">{value}</div>
        <div class="sub">{sub}</div></div>""", unsafe_allow_html=True)

def vs_market(filtered_value, market_value):
    return f"{(filtered_value / market_value - 1) * 100:+.1f}% vs market"

c1, c2, c3, c4, c5 = st.columns(5)

med_ppsf = fdf["Price_per_SqFt_Rs"].median()
avg_price = fdf["Price_in_Lakhs"].mean()
good_n = int(fdf["Good_Investment"].sum())

kpi_card(c1, "🏘️", "Properties", f"{len(fdf):,}", f"{len(fdf) / len(df):.1%} of market", PALETTE[0])
kpi_card(c2, "📐", "Median Price / Sq Ft", f"₹{med_ppsf:,.0f}",
         vs_market(med_ppsf, df["Price_per_SqFt_Rs"].median()), PALETTE[1])
kpi_card(c3, "💰", "Average Price", f"₹{avg_price:,.1f} L",
         vs_market(avg_price, df["Price_in_Lakhs"].mean()), PALETTE[2])
kpi_card(c4, "✅", "Good Investments", f"{good_n / len(fdf):.1%}", f"{good_n:,} properties", PALETTE[1])
kpi_card(c5, "📈", "Avg Value in 5 Years", f"₹{fdf['Future_Price_5Y'].mean():,.1f} L",
         f"+₹{fdf['Expected_Gain_Lakhs'].mean():,.1f} L expected gain", PALETTE[3])

st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] {gap: 8px; margin-top: 18px;}
.stTabs [data-baseweb="tab"] {background: #E9EEF3; border-radius: 10px 10px 0 0; padding: 10px 18px;}
.stTabs [data-baseweb="tab"] p {font-weight: 600; font-size: 0.95rem;}
.stTabs [aria-selected="true"] {background: #1F3B57;}
.stTabs [aria-selected="true"] p {color: white;}
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Market Pulse", "🔍 Insight Explorer", "🧮 Investment Checker",
                                        "🏆 Top Picks", "💡 Recommendations"])
def style_fig(fig, height=380):
    fig.update_layout(height=height, template="plotly_white", title_font_size=16,
                      font=dict(color="#1F3B57"), margin=dict(l=10, r=10, t=55, b=10))
    return fig

with tab1:
    st.caption("📌 All charts below update live with your sidebar filters. Hover for exact values.")
    col_a, col_b = st.columns(2)

    fig = px.histogram(fdf, x="Price_per_SqFt_Rs", nbins=80, color_discrete_sequence=[PALETTE[0]],
                       title="Price per Sq Ft Distribution (zoomed to ₹40,000)")
    fig.add_vline(x=med_ppsf, line_dash="dash", line_color=PALETTE[3],
                  annotation_text=f"Median ₹{med_ppsf:,.0f}", annotation_position="top right")
    fig.update_xaxes(title="Price per Sq Ft (₹)", range=[0, 40000])
    fig.update_yaxes(title="Properties")
    col_a.plotly_chart(style_fig(fig), use_container_width=True)

    sc = fdf["Investment_Score"].value_counts().reindex(range(6), fill_value=0)
    fig = px.bar(x=sc.index, y=sc.values, text=sc.values, title="Deal Score Distribution (criteria met, 0–5)",
                 color=sc.index, color_continuous_scale=[PALETTE[3], PALETTE[2], PALETTE[1]])
    fig.update_traces(texttemplate="%{text:,}", textposition="outside", textangle=0)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(title="Deal Score", dtick=1)
    fig.update_yaxes(title="Properties")
    col_b.plotly_chart(style_fig(fig), use_container_width=True)

    col_c, col_d = st.columns(2)

    city_g = fdf.groupby("City")["Good_Investment"].agg(["mean", "count"])
    city_g = city_g[city_g["count"] >= 50].sort_values("mean", ascending=False).head(10)
    if city_g.empty:
        col_c.info("Not enough properties per city for a ranking. Widen the filters.")
    else:
        fig = px.bar(x=city_g["mean"] * 100, y=city_g.index, orientation="h", text=city_g["mean"] * 100,
                     title="Top 10 Cities by Good Investment Rate", color_discrete_sequence=[PALETTE[1]])
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_yaxes(title="", autorange="reversed")
        fig.update_xaxes(title="Good Investments (%)", range=[0, city_g["mean"].max() * 120])
        col_c.plotly_chart(style_fig(fig), use_container_width=True)

    size_g = fdf.groupby("Size_Band")["Good_Investment"].mean().reindex(["Small", "Medium", "Large"]) * 100
    fig = px.bar(x=size_g.index, y=size_g.values, text=size_g.values, title="Good Investment Rate by Home Size",
                 color=size_g.index, color_discrete_sequence=PALETTE[:3])
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textangle=0)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title="Size Band")
    fig.update_yaxes(title="Good Investments (%)", range=[0, max(size_g.max() * 1.2, 10)])
    col_d.plotly_chart(style_fig(fig), use_container_width=True)

st.markdown("""
<style>
.insight {background: white; border-radius: 14px; padding: 20px 22px; border-top: 5px solid #2A9D8F;
          box-shadow: 0 2px 10px rgba(31,59,87,0.08);}
.insight h4 {color: #1F3B57; margin: 14px 0 4px 0; font-size: 1rem;}
.insight p  {margin: 0; line-height: 1.5;}
</style>
""", unsafe_allow_html=True)

CHART_DIR = Path(__file__).parent / "assets" / "charts"
q_keys = list(INSIGHTS)
st.session_state.setdefault("q_choice", q_keys[0])

def move_q(step):
    i = q_keys.index(st.session_state.q_choice)
    st.session_state.q_choice = q_keys[(i + step) % len(q_keys)]   # % wraps around: after the last comes the first

with tab2:
    st.caption("📌 These analyses use the full market (250,000 properties). Sidebar filters do not apply here.")
    b1, b2, b3 = st.columns([1, 6, 1])
    b1.button("◀ Prev", on_click=move_q, args=(-1,), use_container_width=True)
    b2.selectbox("Choose an analysis", q_keys, key="q_choice", label_visibility="collapsed")
    b3.button("Next ▶", on_click=move_q, args=(1,), use_container_width=True)

    item = INSIGHTS[st.session_state.q_choice]
    left, right = st.columns([3, 2])
    left.image(str(CHART_DIR / item["img"]), use_container_width=True)
    right.markdown(f"""<div class="insight">
        <h4>🔎 What we found</h4><p>{item['found']}</p>
        <h4>💡 Investor takeaway</h4><p>{item['takeaway']}</p>
        <h4>📊 Why this chart</h4><p>{item['chart']}</p></div>""", unsafe_allow_html=True)

st.markdown("""
<style>
.verdict {border-radius: 14px; padding: 18px 24px; color: white; margin: 14px 0;}
.verdict.good {background: linear-gradient(120deg, #2A9D8F, #3FB8A9);}
.verdict.bad  {background: linear-gradient(120deg, #E76F51, #F08A6F);}
.verdict h2 {color: white; margin: 0; font-size: 1.6rem;}
.verdict p  {color: white; margin: 4px 0 0 0;}
.reason {background: white; border-radius: 10px; padding: 10px 14px; margin-bottom: 8px;
         border-left: 5px solid var(--c); box-shadow: 0 1px 6px rgba(31,59,87,0.06);}
.reason b {color: #1F3B57;}
.reason span {color: #5B6B7B; font-size: 0.85rem;}
.stFormSubmitButton button, .stDownloadButton button {background: #2A9D8F; border: none; border-radius: 10px;}
.stFormSubmitButton button p, .stDownloadButton button p {color: white; font-weight: 600;}
.stFormSubmitButton button:hover, .stDownloadButton button:hover {background: #1F3B57;}
</style>
""", unsafe_allow_html=True)

GROWTH_RATE, YEARS = 0.05, 5

def evaluate(p):
    """Applies the notebook's Good_Investment rule (Step 4.7) to one property."""
    city_ppsf = df.loc[df["City"] == p["city"], "Price_per_SqFt_Rs"]
    city_med = city_ppsf.median()
    ppsf = p["price"] * 100000 / p["size"]
    t_level = {"Low": 1, "Medium": 2, "High": 3}[p["transport"]]
    infra = ((p["schools"] - 1) / 9 + (p["hospitals"] - 1) / 9 + (t_level - 1) / 2) / 3 * 10
    n_am = len(p["amenities"])
    ready = p["availability"] == "Ready to Move"

    checks = [
        ("Value: below city median (must-have)", ppsf < city_med,
         f"₹{ppsf:,.0f}/sq ft vs {p['city']} median ₹{city_med:,.0f}"),
        ("Ready to move", ready, "Rental income can start immediately" if ready else "Construction delay risk; no income yet"),
        ("Strong infrastructure (score ≥ 6.5)", infra >= 6.5, f"Infrastructure score {infra:.1f} / 10"),
        ("Amenity-rich (4+ amenities)", n_am >= 4, f"{n_am} {'amenity' if n_am == 1 else 'amenities'}"),
        ("Security available", p["security"] == "Yes", "Gated / secured property" if p["security"] == "Yes" else "No security listed"),
    ]
    score = sum(ok for _, ok, _ in checks)
    return dict(ppsf=ppsf, city_med=city_med, cheaper_than=(city_ppsf > ppsf).mean() * 100, infra=infra,
                checks=checks, score=score, good=checks[0][1] and score >= 3,
                values=[p["price"] * (1 + GROWTH_RATE) ** t for t in range(YEARS + 1)])

with tab3:
    st.markdown("#### 🧮 Check any property in seconds")
    st.caption("Enter the details and click Check. Uses the same rule as the analysis: below the city median price per sq ft, plus at least 2 of 4 quality criteria.")

    l1, l2 = st.columns(2)
    states_all = sorted(df["State"].unique())
    in_state = l1.selectbox("🗺️ State", states_all, index=states_all.index("Maharashtra"))
    cities_in = sorted(df.loc[df["State"] == in_state, "City"].unique())
    in_city = l2.selectbox("🏙️ City", cities_in, index=cities_in.index("Pune") if "Pune" in cities_in else 0)

    with st.form("checker"):
        f1, f2, f3 = st.columns(3)
        ptype = f1.selectbox("🏠 Property type", ["Apartment", "Independent House", "Villa"])
        bhk = f1.selectbox("🛏️ BHK", [1, 2, 3, 4, 5], index=2)
        size = f1.number_input("📐 Size (sq ft)", 500, 5000, 2400, step=50)
        price = f1.number_input("💰 Price (₹ Lakhs)", 10.0, 500.0, 150.0, step=5.0)

        avail = f2.radio("🏗️ Availability", ["Ready to Move", "Under Construction"], horizontal=True)
        transport = f2.select_slider("🚇 Public transport", ["Low", "Medium", "High"], value="High")
        security = f2.radio("🔒 Security", ["Yes", "No"], horizontal=True)
        furnished = f2.selectbox("🛋️ Furnishing", ["Unfurnished", "Semi-furnished", "Furnished"], index=1)

        schools = f3.slider("🏫 Nearby schools", 1, 10, 6)
        hospitals = f3.slider("🏥 Nearby hospitals", 1, 10, 5)
        amenities = f3.multiselect("🏊 Amenities", ["Gym", "Pool", "Garden", "Clubhouse", "Playground"],
                                   default=["Gym", "Pool", "Garden", "Playground"])
        parking = f3.radio("🚗 Parking", ["Yes", "No"], horizontal=True)

        submitted = st.form_submit_button("🔍 Check this property", use_container_width=True)

    if submitted:   # remember the inputs so results stay visible when other widgets are used
        st.session_state.chk = dict(state=in_state, city=in_city, ptype=ptype, bhk=bhk, size=size, price=price,
                                    availability=avail, transport=transport, security=security, furnished=furnished,
                                    schools=schools, hospitals=hospitals, amenities=amenities, parking=parking)

    if "chk" not in st.session_state:
        st.info("👆 Fill in the details (a demo property is pre-filled) and click **Check this property**.")
    else:
        p = st.session_state.chk
        r = evaluate(p)
        quality = r["score"] - int(r["checks"][0][1])
        if r["good"]:
            msg = f"Priced below the {p['city']} median and meets {quality} of 4 quality criteria."
        elif not r["checks"][0][1]:
            msg = f"Priced above the {p['city']} median. The must-have value test fails, whatever the features."
        else:
            msg = f"Good value, but meets only {quality} of 4 quality criteria (at least 2 needed)."
        cls, title = ("good", "✅ GOOD INVESTMENT") if r["good"] else ("bad", "❌ NOT A GOOD INVESTMENT")
        st.markdown(f'<div class="verdict {cls}"><h2>{title}</h2><p>{msg}</p></div>', unsafe_allow_html=True)

        g1, g2, g3 = st.columns(3)
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=r["score"], number={"suffix": " / 5"},
            title={"text": "Deal Score"},
            gauge={"axis": {"range": [0, 5], "dtick": 1}, "bar": {"color": PALETTE[0]},
                   "steps": [{"range": [0, 3], "color": "#F6D5CD"}, {"range": [3, 5], "color": "#CDEBE7"}],
                   "threshold": {"line": {"color": PALETTE[3], "width": 4}, "value": 3}}))
        gauge = style_fig(gauge, 260)
        gauge.update_layout(margin=dict(l=35, r=35, t=60, b=10))   # room for the 0 and 5 labels
        g1.plotly_chart(gauge, use_container_width=True)

        meter = go.Figure(go.Indicator(mode="number+delta", value=r["ppsf"], number={"prefix": "₹", "valueformat": ",.0f"},
            title={"text": f"Price / sq ft vs {p['city']} median"},
            delta={"reference": r["city_med"], "relative": True, "valueformat": ".1%",
                   "increasing": {"color": PALETTE[3]}, "decreasing": {"color": PALETTE[1]}}))
        g2.plotly_chart(style_fig(meter, 260), use_container_width=True)

        gain = r["values"][-1] - p["price"]
        kpi_card(g3, "📈", "Estimated value in 5 years", f"₹{r['values'][-1]:,.1f} L",
                 f"+₹{gain:,.1f} L gain · cheaper per sq ft than {r['cheaper_than']:.0f}% of {p['city']}", PALETTE[1])

        r1, r2 = st.columns([1, 1])
        r1.markdown("##### 📋 Why? The 5 criteria")
        for name, ok, detail in r["checks"]:
            r1.markdown(f'<div class="reason" style="--c:{PALETTE[1] if ok else PALETTE[3]}">'
                        f'{"✅" if ok else "❌"} <b>{name}</b><br><span>{detail}</span></div>', unsafe_allow_html=True)

        labels = ["Today"] + [f"Year {t}" for t in range(1, YEARS + 1)]
        fig = px.line(x=labels, y=r["values"], markers=True, text=[f"₹{v:,.1f} L" for v in r["values"]],
                      title="Estimated value, year by year (5% p.a.)", color_discrete_sequence=[PALETTE[1]])
        fig.update_traces(textposition="top center", line_width=3, marker_size=9)
        fig.update_xaxes(title="")
        fig.update_yaxes(title="Value (₹ Lakhs)", range=[0, max(r["values"]) * 1.2])
        r2.plotly_chart(style_fig(fig, 360), use_container_width=True)

        report = "\n".join([
            "SqFt Signal: Investment Report", "=" * 32,
            f"Property: {p['bhk']} BHK {p['ptype']} in {p['city']}, {p['state']}",
            f"Size: {p['size']:,} sq ft | Price: Rs {p['price']:,.1f} lakhs | Price per sq ft: Rs {r['ppsf']:,.0f}",
            f"City median price per sq ft: Rs {r['city_med']:,.0f} ({(r['ppsf'] / r['city_med'] - 1) * 100:+.1f}%)",
            f"Verdict: {'GOOD INVESTMENT' if r['good'] else 'NOT A GOOD INVESTMENT'} (Deal Score {r['score']}/5)",
            "", "Criteria:"] +
            [f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}".replace("₹", "Rs ") for name, ok, detail in r["checks"]] +
            ["", f"Estimated value after 5 years (5% p.a.): Rs {r['values'][-1]:,.1f} lakhs (gain Rs {gain:,.1f} lakhs)",
             "Note: rule-based assessment on a synthetic dataset. Not financial advice."])
        st.download_button("📄 Download investment report", report, file_name="sqft_signal_report.txt",
                           mime="text/plain", use_container_width=True)

st.markdown("""
<style>
.pick {background: white; border-radius: 14px; padding: 16px 18px; margin-bottom: 16px;
       border-top: 5px solid #E9C46A; box-shadow: 0 2px 10px rgba(31,59,87,0.08);}
.pick .top {display: flex; justify-content: space-between; font-size: 0.8rem;}
.pick .score {background: #1F3B57; color: #E9C46A; padding: 2px 10px; border-radius: 12px; font-weight: 700;}
.pick .id {color: #8D99AE;}
.pick h4 {margin: 10px 0 2px 0; color: #1F3B57;}
.pick .loc {color: #5B6B7B; font-size: 0.85rem;}
.pick .price {font-size: 1.4rem; font-weight: 800; color: #1F3B57; margin-top: 8px;}
.pick .price small {font-size: 0.85rem; font-weight: 500; color: #5B6B7B;}
.pick .value {color: #2A9D8F; font-weight: 600; font-size: 0.9rem;}
.pick .future {font-size: 0.85rem; color: #1F3B57; margin-top: 4px;}
.pick .badges span {display: inline-block; background: #E9EEF3; border-radius: 12px; padding: 2px 8px;
                    margin: 6px 4px 0 0; font-size: 0.75rem;}
.rec {background: white; border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;
      border-left: 5px solid var(--c); box-shadow: 0 1px 6px rgba(31,59,87,0.06);}
.rec b {color: #1F3B57;}
.rec .ev {display: block; color: #5B6B7B; font-size: 0.82rem; margin-top: 4px;}
</style>
""", unsafe_allow_html=True)

def pick_card(col, p):
    below = (1 - p["Price_per_SqFt_Rs"] / p["City_Median_PPSF"]) * 100
    col.markdown(f"""<div class="pick">
      <div class="top"><span class="score">⭐ {int(p['Investment_Score'])}/5</span><span class="id">Listing #{int(p['ID'])}</span></div>
      <h4>{int(p['BHK'])} BHK {p['Property_Type']}</h4>
      <div class="loc">📍 {p['City']}, {p['State']} · {p['Locality']}</div>
      <div class="price">₹{p['Price_in_Lakhs']:,.1f} L <small>· {int(p['Size_in_SqFt']):,} sq ft</small></div>
      <div class="value">₹{p['Price_per_SqFt_Rs']:,.0f}/sq ft · {below:.0f}% below city median</div>
      <div class="future">📈 ₹{p['Future_Price_5Y']:,.1f} L in 5 years</div>
      <div class="badges"><span>{'✅ Ready' if p['Is_Ready_To_Move'] else '🏗️ Under construction'}</span>
        <span>🚇 {p['Public_Transport_Accessibility']} transport</span><span>🏊 {int(p['Amenities_Count'])} amenities</span>
        <span>{'🔒 Secure' if p['Has_Security'] else '🔓 No security'}</span></div></div>""", unsafe_allow_html=True)

with tab4:
    good = fdf[fdf["Good_Investment"] == 1]
    st.markdown("#### 🏆 Top picks in your filtered market")
    st.caption(f"{len(good):,} Good Investments match your filters; {(good['Investment_Score'] == 5).sum():,} score a perfect 5/5. "
               "Picks are ranked by Deal Score first, then by your chosen order.")
    st.caption("⚠️ In a real market, listings priced 90%+ below the city median would need verification first "
               "(possible data errors or misleading ads). Here they reflect the synthetic data.")
    sort_by = st.radio("Rank by", ["Best value (furthest below city median)", "Lowest price", "Largest size"], horizontal=True)

    if good.empty:
        st.info("No Good Investments match these filters. Try widening them in the sidebar.")
    else:
        rules = {"Best value (furthest below city median)": ("Price_vs_City_Median", True),
                 "Lowest price": ("Price_in_Lakhs", True), "Largest size": ("Size_in_SqFt", False)}
        col_name, asc = rules[sort_by]
        picks = good.sort_values(["Investment_Score", col_name], ascending=[False, asc]).head(9)
        for i in range(0, len(picks), 3):              # 3 cards per row
            row = st.columns(3)
            for col, (_, p) in zip(row, picks.iloc[i:i + 3].iterrows()):
                pick_card(col, p)

with tab5:
    st.markdown("#### 💡 Business recommendations")
    st.caption("Every recommendation is backed by the analysis of 250,000 properties (📊 = evidence).")
    left, right = st.columns([3, 2])

    left.markdown("##### 🧑‍💼 For investors")
    for icon, title, action, evidence in INVESTOR_RECS:
        left.markdown(f'<div class="rec" style="--c:#2A9D8F">{icon} <b>{title}</b>: {action}'
                      f'<span class="ev">📊 {evidence}</span></div>', unsafe_allow_html=True)

    right.markdown("##### 🏢 For real-estate platforms")
    for icon, title, action, evidence in PLATFORM_RECS:
        right.markdown(f'<div class="rec" style="--c:#1F3B57">{icon} <b>{title}</b>: {action}'
                       f'<span class="ev">📊 {evidence}</span></div>', unsafe_allow_html=True)

    with right.expander("⚠️ Data reality check", expanded=True):
        st.markdown(REALITY_CHECK)