import streamlit as st
import pandas as pd
import numpy as np
import ast
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# PAGE CONFIG
st.set_page_config(
    page_title="Skincare Acne EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #F4F6FA; }

  [data-testid="stSidebar"] { background: #1E293B !important; }
  [data-testid="stSidebar"] * { color: #CBD5E1 !important; }
  [data-testid="stSidebar"] .stMultiSelect label,
  [data-testid="stSidebar"] .stSelectbox label {
    color: #94A3B8 !important;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .hero {
    background: linear-gradient(135deg, #1E293B 0%, #0F4C81 60%, #1565C0 100%);
    border-radius: 18px;
    padding: 48px 56px;
    margin-bottom: 32px;
  }
  .hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    color: #E0F0FF;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    margin-bottom: 16px;
  }
  .hero h1 {
    color: #FFFFFF;
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0 0 10px 0;
    line-height: 1.2;
  }
  .hero p {
    color: #BAD4F5;
    font-size: 1rem;
    margin: 0;
    font-weight: 400;
    line-height: 1.6;
  }

  .metric-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 22px 24px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }
  .metric-card .label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748B;
    margin-bottom: 8px;
    font-weight: 600;
  }
  .metric-card .value {
    font-size: 2rem;
    color: #0F172A;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
  }
  .metric-card .sub { font-size: 0.78rem; color: #94A3B8; }

  .section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 4px 0;
  }
  .section-sub {
    font-size: 0.84rem;
    color: #64748B;
    margin-bottom: 20px;
  }

  .insight-box {
    background: #EFF6FF;
    border-left: 4px solid #2563EB;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin-top: 8px;
    font-size: 0.88rem;
    color: #1E3A5F;
    line-height: 1.65;
  }
  .insight-box strong { color: #1D4ED8; }

  .conclusion-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 28px 30px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 16px;
  }
  .conclusion-card h3 {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #2563EB;
  }
  .conclusion-card ul { padding-left: 18px; margin: 0; }
  .conclusion-card li {
    margin-bottom: 8px;
    font-size: 0.87rem;
    line-height: 1.6;
    color: #334155;
  }
  .conclusion-card li strong { color: #0F172A; }

  .dict-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 22px 26px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 18px;
  }
  .dict-card h3 {
    font-size: 1rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #2563EB;
  }
  .dict-note {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.84rem;
    color: #1E3A5F;
    margin-top: 14px;
    line-height: 1.6;
  }

  .divider { border: none; border-top: 1px solid #E2E8F0; margin: 28px 0; }
  .footer { text-align: center; color: #94A3B8; font-size: 0.78rem; padding: 20px 0 8px; }
</style>
""", unsafe_allow_html=True)

# COLOR PALETTE
PALETTE = {
    "Comedonal":    "#2563EB",
    "Inflammatory": "#DC2626",
    "Cyst":         "#16A34A",
}

def plotly_layout(fig, title="", height=420):
    fig.update_layout(
        template="plotly_white",
        title=dict(text=title, font=dict(size=14, color="#0F172A", family="Inter"), x=0, xanchor="left"),
        height=height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, sans-serif", color="#334155"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", font=dict(size=11, color="#334155")),
        margin=dict(l=16, r=16, t=48, b=16),
        hoverlabel=dict(bgcolor="#0F172A", font_color="#F1F5F9", font_size=12, bordercolor="#2563EB"),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#F1F5F9", showline=False, zeroline=False, tickfont=dict(color="#64748B", size=11))
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", showline=False, zeroline=False, tickfont=dict(color="#64748B", size=11))
    return fig

# DATA LOADER — baca dari file CSV asli
@st.cache_data
def load_data():
    df = pd.read_csv("skincare_clean.csv")

    # Pastikan kolom turunan ada
    if "Sensitivity_Label" not in df.columns:
        df["Sensitivity_Label"] = df["Sensitivity"].map({"Yes": "Sensitif", "No": "Non-Sensitif"})
    else:
        df["Sensitivity_Label"] = df["Sensitivity"].map({"Yes": "Sensitif", "No": "Non-Sensitif"})

    # Parse Ingredients_List dari string ke list
    def parse_ingredients(val):
        try:
            return ast.literal_eval(val)
        except:
            return [i.strip() for i in str(val).split('+')]

    df["_ing_parsed"] = df["Ingredients_List"].apply(parse_ingredients)

    # Bangun dataframe frekuensi bahan aktif dari data asli
    rows = []
    for _, row in df.iterrows():
        for ing in row["_ing_parsed"]:
            rows.append({"Internal_Type": row["Internal_Type"], "Ingredients_List": ing.strip()})
    df_ing = pd.DataFrame(rows).groupby(["Internal_Type","Ingredients_List"]).size().reset_index(name="Jumlah")

    # Top 5 per tipe jerawat
    df_ing = df_ing.sort_values("Jumlah", ascending=False).groupby("Internal_Type").head(5).reset_index(drop=True)

    return df, df_ing

df_clean, df_ing = load_data()

# Nilai unik dari data asli
age_options  = sorted(df_clean["Age_Group"].unique().tolist())
skin_options = sorted(df_clean["Skin_Type"].unique().tolist())
acne_options = sorted(df_clean["Internal_Type"].unique().tolist())

# SIDEBAR
with st.sidebar:
    st.markdown("## Filter Data")
    st.markdown("---")
    sel_acne = st.multiselect("Tipe Jerawat",      options=acne_options,  default=acne_options)
    sel_skin = st.multiselect("Tipe Kulit",         options=skin_options,  default=skin_options)
    sel_age  = st.multiselect("Rentang Usia",       options=age_options,   default=age_options)
    sel_sens = st.multiselect(
        "Sensitivitas Kulit",
        options=["Yes","No"], default=["Yes","No"],
        format_func=lambda x: "Sensitif" if x=="Yes" else "Non-Sensitif"
    )
    st.markdown("---")
    st.markdown("### Tentang Dataset")
    st.markdown(f"""
    **Skincare Treatment Dataset**

    Dataset hasil cleaning dan feature engineering dari notebook EDA.

    - Total baris: {len(df_clean):,}
    - Total kolom: {len(df_clean.columns)}
    - Tipe jerawat: {', '.join(acne_options)}
    """)

# FILTER
df_f = df_clean[
    df_clean["Internal_Type"].isin(sel_acne) &
    df_clean["Skin_Type"].isin(sel_skin) &
    df_clean["Age_Group"].isin(sel_age) &
    df_clean["Sensitivity"].isin(sel_sens)
]
df_ing_f = df_ing[df_ing["Internal_Type"].isin(sel_acne)]

if df_f.empty:
    st.warning("Tidak ada data yang sesuai dengan filter. Silakan ubah pilihan di sidebar.")
    st.stop()

# HERO
st.markdown("""
<div class="hero">
  <div class="badge">Exploratory Data Analysis</div>
  <h1>Skincare Acne Treatment Dashboard</h1>
  <p>
    Analisis distribusi jenis jerawat, bahan aktif, dan profil kulit pengguna<br>
    untuk mendukung sistem rekomendasi perawatan yang personal.
  </p>
</div>
""", unsafe_allow_html=True)

# METRIC CARDS
c1, c2, c3, c4 = st.columns(4)
for col, val, lbl, sub in [
    (c1, len(df_f),                        "Total Data (Filtered)",  f"dari {len(df_clean):,} total baris"),
    (c2, df_f["Internal_Type"].nunique(),  "Tipe Jerawat",           "aktif dipilih"),
    (c3, df_f["Skin_Type"].nunique(),      "Tipe Kulit",             "aktif dipilih"),
    (c4, df_f["Ingredients"].nunique(),    "Kombinasi Ingredients",  "unik dalam filter"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="label">{lbl}</div>
          <div class="value">{val:,}</div>
          <div class="sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ==============================================================
# SECTION 1 — DISTRIBUSI DEMOGRAFI
# ==============================================================
st.markdown('<p class="section-title">Distribusi Jerawat berdasarkan Demografi</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Pertanyaan Bisnis 1 — Distribusi tipe jerawat berdasarkan usia dan sensitivitas kulit</p>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    age_data = df_f.groupby(["Age_Group","Internal_Type"]).size().reset_index(name="Jumlah Kasus")
    age_data["Age_Group"] = pd.Categorical(age_data["Age_Group"], categories=age_options, ordered=True)
    age_data = age_data.sort_values("Age_Group")
    fig_age = px.bar(age_data, x="Age_Group", y="Jumlah Kasus", color="Internal_Type",
                     color_discrete_map=PALETTE, barmode="group",
                     labels={"Age_Group": "Rentang Usia", "Internal_Type": "Tipe Jerawat"})
    fig_age.update_traces(hovertemplate="<b>%{x}</b><br>Tipe: %{customdata[0]}<br>Kasus: <b>%{y}</b><extra></extra>")
    plotly_layout(fig_age, "Distribusi Jerawat per Rentang Usia")
    st.plotly_chart(fig_age, use_container_width=True)

with col_b:
    sens_data = df_f.copy()
    sens_data["Sensitivity_Label"] = sens_data["Sensitivity"].map({"Yes":"Sensitif","No":"Non-Sensitif"})
    sens_data = sens_data.groupby(["Sensitivity_Label","Internal_Type"]).size().reset_index(name="Jumlah Kasus")
    fig_sens = px.bar(sens_data, x="Sensitivity_Label", y="Jumlah Kasus", color="Internal_Type",
                      color_discrete_map=PALETTE, barmode="group",
                      labels={"Sensitivity_Label": "Sensitivitas Kulit", "Internal_Type": "Tipe Jerawat"})
    fig_sens.update_traces(hovertemplate="<b>%{x}</b><br>Tipe: %{customdata[0]}<br>Kasus: <b>%{y}</b><extra></extra>")
    plotly_layout(fig_sens, "Distribusi Jerawat per Sensitivitas Kulit")
    st.plotly_chart(fig_sens, use_container_width=True)

st.markdown("""
<div class="insight-box">
  <strong>Insight:</strong> Distribusi ketiga tipe jerawat tersebar merata dan seimbang di seluruh
  rentang usia maupun tingkat sensitivitas kulit. Dataset ini bersifat sintetis untuk keperluan
  pemodelan — bukan data epidemiologi. Dalam implementasi nyata, usia dan sensitivitas tetap menjadi
  variabel penting dalam personalisasi rekomendasi.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ==============================================================
# SECTION 2 — BAHAN AKTIF
# ==============================================================
st.markdown('<p class="section-title">Bahan Aktif per Tipe Jerawat</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Pertanyaan Bisnis 2 — Bahan aktif paling efektif untuk masing-masing kondisi jerawat</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Bar Chart Interaktif", "Bubble Chart", "Tabel Pivot"])

with tab1:
    df_ing_sorted = df_ing_f.sort_values("Jumlah", ascending=True)
    label_y = df_ing_sorted["Ingredients_List"] + "  (" + df_ing_sorted["Internal_Type"] + ")"
    fig_ing = px.bar(df_ing_sorted, x="Jumlah", y=label_y, color="Internal_Type",
                     color_discrete_map=PALETTE, orientation="h", text="Jumlah",
                     labels={"y": "Bahan Aktif", "Jumlah": "Kemunculan", "Internal_Type": "Tipe Jerawat"})
    fig_ing.update_traces(textposition="outside",
                          hovertemplate="<b>%{customdata[0]}</b><br>Tipe: %{customdata[1]}<br>Kemunculan: <b>%{x}</b><extra></extra>")
    plotly_layout(fig_ing, "Top 5 Bahan Aktif per Tipe Jerawat", height=500)
    fig_ing.update_layout(xaxis_range=[0, df_ing_f["Jumlah"].max() * 1.2])
    st.plotly_chart(fig_ing, use_container_width=True)

with tab2:
    fig_bubble = px.scatter(df_ing_f, x="Internal_Type", y="Ingredients_List",
                            size="Jumlah", color="Internal_Type", color_discrete_map=PALETTE,
                            size_max=55, text="Jumlah",
                            labels={"Internal_Type": "Tipe Jerawat", "Ingredients_List": "Bahan Aktif"})
    fig_bubble.update_traces(textposition="middle center",
                             textfont=dict(color="white", size=11),
                             hovertemplate="<b>%{y}</b><br>Tipe: %{x}<br>Kemunculan: <b>%{customdata[0]}</b><extra></extra>")
    plotly_layout(fig_bubble, "Bubble Chart — Ukuran = Frekuensi Kemunculan", height=500)
    st.plotly_chart(fig_bubble, use_container_width=True)

with tab3:
    pivot = df_ing_f.pivot_table(index="Ingredients_List", columns="Internal_Type",
                                  values="Jumlah", fill_value=0).astype(int)
    pivot["Total"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("Total", ascending=False)
    st.dataframe(
        pivot.style.background_gradient(cmap="Blues", subset=[c for c in pivot.columns if c != "Total"]).format("{:,}"),
        use_container_width=True
    )

# Ambil insight dinamis dari data
top_ing = df_ing.sort_values("Jumlah", ascending=False)
top_per_type = top_ing.groupby("Internal_Type").first().reset_index()
insight_lines = "".join([
    f"<li><strong>{r['Ingredients_List']}</strong> mendominasi untuk {r['Internal_Type']} ({r['Jumlah']}x).</li>"
    for _, r in top_per_type.iterrows()
])
st.markdown(f"""
<div class="insight-box">
  <strong>Insight:</strong>
  <ul style="margin: 8px 0 0 0; padding-left: 18px;">
    {insight_lines}
  </ul>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ==============================================================
# SECTION 3 — DISTRIBUSI TIPE KULIT
# ==============================================================
st.markdown('<p class="section-title">Distribusi Jerawat berdasarkan Tipe Kulit</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Pertanyaan Bisnis 3 — Distribusi jenis jerawat berdasarkan tipe kulit pengguna</p>', unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])

with col_left:
    skin_data = df_f.groupby(["Skin_Type","Internal_Type"]).size().reset_index(name="Jumlah Kasus")
    skin_data["Skin_Type"] = pd.Categorical(skin_data["Skin_Type"],
                                             categories=[s for s in skin_options if s in sel_skin], ordered=True)
    skin_data = skin_data.sort_values("Skin_Type")
    fig_skin = px.bar(skin_data, x="Skin_Type", y="Jumlah Kasus", color="Internal_Type",
                      color_discrete_map=PALETTE, barmode="group", text="Jumlah Kasus",
                      labels={"Skin_Type": "Tipe Kulit", "Internal_Type": "Tipe Jerawat"})
    fig_skin.update_traces(textposition="outside",
                           hovertemplate="<b>%{x}</b><br>Tipe: %{customdata[0]}<br>Kasus: <b>%{y}</b><extra></extra>")
    plotly_layout(fig_skin, "Distribusi Jerawat per Tipe Kulit")
    st.plotly_chart(fig_skin, use_container_width=True)

with col_right:
    acne_counts = df_f["Internal_Type"].value_counts().reset_index()
    acne_counts.columns = ["Tipe Jerawat", "Jumlah"]
    fig_donut = px.pie(acne_counts, names="Tipe Jerawat", values="Jumlah",
                       color="Tipe Jerawat", color_discrete_map=PALETTE, hole=0.55)
    fig_donut.update_traces(textposition="inside", textinfo="percent+label",
                            textfont=dict(size=12, color="white"),
                            hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Proporsi: %{percent}<extra></extra>",
                            pull=[0.03] * len(acne_counts))
    plotly_layout(fig_donut, "Proporsi Tipe Jerawat", height=380)
    fig_donut.update_layout(showlegend=False)
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("""
<div class="insight-box">
  <strong>Insight:</strong> Setiap kombinasi tipe kulit dan tipe jerawat memiliki jumlah kasus yang
  identik. Model yang dilatih di atasnya bebas dari bias tipe kulit tertentu. Pada data nyata,
  oily skin umumnya lebih rentan terhadap jerawat Comedonal dan Inflammatory.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ==============================================================
# SECTION 5 — KESIMPULAN
# ==============================================================
st.markdown('<p class="section-title">Kesimpulan & Rekomendasi Bisnis</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Ringkasan temuan utama dan saran pengembangan sistem rekomendasi.</p>', unsafe_allow_html=True)

cc1, cc2 = st.columns(2)

with cc1:
    st.markdown("""
    <div class="conclusion-card">
      <h3>Temuan Utama</h3>
      <ul>
        <li>Dataset <strong>240 baris</strong> bersih — tidak ada missing values atau duplikat.</li>
        <li>Distribusi tipe jerawat <strong>seimbang sempurna</strong> di semua segmen usia dan sensitivitas.</li>
        <li><strong>Salicylic Acid</strong> adalah bahan utama untuk jerawat Comedonal.</li>
        <li><strong>Benzoyl Peroxide</strong> paling dominan untuk jerawat Inflammatory.</li>
        <li><strong>Zinc PCA dan Green Tea Extract</strong> bersifat universal untuk semua tipe jerawat.</li>
        <li>Setiap kombinasi kulit–jerawat memiliki jumlah kasus yang <strong>seimbang</strong>.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

with cc2:
    st.markdown("""
    <div class="conclusion-card">
      <h3>Rekomendasi Sistem</h3>
      <ul>
        <li>Gunakan <strong>Skin_Profile</strong> (Tipe Jerawat + Tipe Kulit) sebagai kunci rekomendasi utama.</li>
        <li>Prioritaskan bahan aktif spesifik:
          <br>— Salicylic Acid untuk Comedonal
          <br>— Benzoyl Peroxide untuk Inflammatory
          <br>— Kombinasi keduanya + Niacinamide untuk Cyst</li>
        <li>Tambahkan <strong>Zinc PCA atau Green Tea Extract</strong> sebagai bahan pendukung universal.</li>
        <li>Gunakan <strong>sensitivitas kulit</strong> sebagai filter lapis kedua.</li>
        <li>Kembangkan model dengan data nyata untuk menangani <strong>distribusi tidak seimbang</strong>.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
