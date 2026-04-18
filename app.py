"""
Dashboard estrategico — Supermercados Mercandina C. A.
Plan de accion basado en Balanced Scorecard.

Ejecucion: streamlit run app.py
Requisitos: streamlit, pandas, plotly, openpyxl, numpy
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# =====================================================================
# CONFIGURACION
# =====================================================================
st.set_page_config(
    page_title="Mercandina | Dashboard estrategico",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# PALETA EJECUTIVA PREMIUM - tema claro, alto contraste
# ---------------------------------------------------------------------
NAVY      = "#0F2A44"
INK       = "#1F2937"
STEEL     = "#2E5C8A"
SLATE     = "#6B7C93"
MIST      = "#C7D2DE"
HAIR      = "#E4E7EB"
PAPER     = "#FFFFFF"
CANVAS    = "#FAFBFC"
MUTED_BG  = "#F5F7FA"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: {INK};
    background-color: {CANVAS};
}}

.main > div {{
    padding-top: 1.2rem;
    padding-left: 2.4rem;
    padding-right: 2.4rem;
    max-width: 1680px;
}}

/* Encabezado */
.brand-header {{
    border-bottom: 1px solid {HAIR};
    padding-bottom: 1.2rem;
    margin-bottom: 1.8rem;
}}
.brand-header h1 {{
    font-size: 1.95rem;
    font-weight: 700;
    color: {NAVY};
    margin: 0;
    letter-spacing: -0.02em;
    line-height: 1.15;
}}
.brand-header .subtitle {{
    color: {SLATE};
    font-size: 0.96rem;
    font-weight: 400;
    margin-top: 0.35rem;
}}

/* Titulo de perspectiva */
.section-title {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.78rem;
    font-weight: 700;
    color: {NAVY};
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin: 2.6rem 0 1.1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid {HAIR};
}}
.section-title::before {{
    content: "";
    width: 4px;
    height: 14px;
    background: {STEEL};
    display: inline-block;
}}

/* KPIs */
[data-testid="stMetric"] {{
    background: {PAPER};
    border: 1px solid {HAIR};
    padding: 1.1rem 1.3rem 1rem 1.3rem;
    border-radius: 4px;
    box-shadow: 0 1px 2px rgba(15, 42, 68, 0.04);
    position: relative;
    overflow: hidden;
}}
[data-testid="stMetric"]::before {{
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 3px;
    background: {STEEL};
}}
[data-testid="stMetricLabel"] {{
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: {SLATE} !important;
    text-transform: uppercase;
    letter-spacing: 0.09em;
}}
[data-testid="stMetricValue"] {{
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: {NAVY} !important;
    line-height: 1.1 !important;
    margin-top: 0.35rem;
}}
[data-testid="stMetricDelta"] {{
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    margin-top: 0.15rem;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: {MUTED_BG};
    border-right: 1px solid {HAIR};
}}
section[data-testid="stSidebar"] > div:first-child {{ padding-top: 2rem; }}
.sidebar-brand {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {NAVY};
    line-height: 1.25;
    margin-bottom: 0.15rem;
}}
.sidebar-sub {{
    font-size: 0.78rem;
    color: {SLATE};
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 1.6rem;
}}
.sidebar-label {{
    font-size: 0.7rem;
    font-weight: 700;
    color: {SLATE};
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 1.2rem 0 0.4rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid {HAIR};
}}
.sidebar-meta {{
    font-size: 0.76rem;
    color: {SLATE};
    line-height: 1.55;
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid {HAIR};
}}
.sidebar-meta b {{ color: {INK}; font-weight: 600; }}

/* Footer */
.footer-note {{
    color: {SLATE};
    font-size: 0.78rem;
    font-style: italic;
    text-align: center;
    padding: 1.2rem 0 0.4rem 0;
    border-top: 1px solid {HAIR};
    margin-top: 2.4rem;
}}

#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Tema Plotly compartido
# FIX: se usan 'title_font', 'title_x' y 'title_xanchor' como props
# escalares para NO chocar con el kwarg 'title=...' que se pasa luego.
# ---------------------------------------------------------------------
PLOT_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color=INK, size=12),
    plot_bgcolor=PAPER,
    paper_bgcolor=PAPER,
    colorway=[STEEL, NAVY, SLATE, MIST, "#9AAAB8"],
    xaxis=dict(gridcolor=HAIR, linecolor=HAIR, zerolinecolor=HAIR,
                title=dict(font=dict(size=11, color=SLATE))),
    yaxis=dict(gridcolor=HAIR, linecolor=HAIR, zerolinecolor=HAIR,
                title=dict(font=dict(size=11, color=SLATE))),
    margin=dict(l=50, r=40, t=60, b=50),
    title_font=dict(size=13, color=NAVY, family="Inter"),
    title_x=0,
    title_xanchor="left",
    hoverlabel=dict(bgcolor=PAPER, bordercolor=STEEL,
                     font=dict(family="Inter", color=INK, size=12)),
)

# =====================================================================
# CARGA Y LIMPIEZA
# =====================================================================
@st.cache_data
def load_data(path: Path | str | None = None) -> pd.DataFrame:
    if path is None:
        path = Path(__file__).resolve().parent / "02_total.xlsx"
    df = pd.read_excel(path, sheet_name="Hoja1")
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={"marcas": "marca", "variable": "fecha", "value": "ingresos"})
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.dropna(subset=["ingresos"])
    df = df[df["ingresos"] > 0].copy()
    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["periodo"] = df["fecha"].dt.to_period("M").astype(str)
    return df

@st.cache_data
def anios_completos(df: pd.DataFrame) -> list:
    """Anios con 12 meses de datos — para la variacion interanual."""
    return sorted(df.groupby("anio")["mes"].nunique()
                    .loc[lambda s: s >= 12].index.tolist())

try:
    df = load_data()
except FileNotFoundError:
    st.error("No se ha encontrado el archivo **02_total.xlsx**. "
              "Ubíquelo en la misma carpeta que `app.py` y reinicie la aplicación.")
    st.stop()
except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")
    st.stop()

ANIOS_COMPLETOS = anios_completos(df)

# =====================================================================
# SIDEBAR
# =====================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">Supermercados Mercandina C. A.</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Panel estratégico</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Rango de años</div>',
                unsafe_allow_html=True)
    min_a, max_a = int(df["anio"].min()), int(df["anio"].max())
    rango = st.slider("Seleccione el periodo",
                       min_a, max_a, (min_a, max_a),
                       label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Top N en rankings</div>',
                unsafe_allow_html=True)
    top_n = st.selectbox("Cantidad de líneas",
                          options=[5, 10, 15, 20], index=1,
                          label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Líneas específicas</div>',
                unsafe_allow_html=True)
    todas = sorted(df["marca"].unique())
    sel_lineas = st.multiselect("Filtro opcional",
                                  options=todas, default=[],
                                  label_visibility="collapsed",
                                  placeholder="Todas las líneas")

    st.markdown(f"""
    <div class="sidebar-meta">
      <b>Fuente:</b> 02_total.xlsx<br>
      <b>Periodo disponible:</b> {min_a} – {max_a}<br>
      <b>Años completos:</b> {ANIOS_COMPLETOS[0]} – {ANIOS_COMPLETOS[-1]}<br>
      <b>Registros válidos:</b> {len(df):,}<br>
      <b>Líneas únicas:</b> {df['marca'].nunique()}
    </div>
    """, unsafe_allow_html=True)

# Filtro
dff = df[(df["anio"] >= rango[0]) & (df["anio"] <= rango[1])].copy()
if sel_lineas:
    dff = dff[dff["marca"].isin(sel_lineas)]

if dff.empty:
    st.warning("La combinación de filtros no devuelve registros. Ajuste los parámetros.")
    st.stop()

# =====================================================================
# ENCABEZADO
# =====================================================================
st.markdown("""
<div class="brand-header">
  <h1>Panel estratégico basado en Balanced Scorecard</h1>
  <div class="subtitle">Supermercados Mercandina C. A. · Categoría de conveniencia · Análisis 2005 – 2022</div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# KPIs GLOBALES
# =====================================================================
completos_en_rango = [a for a in ANIOS_COMPLETOS if rango[0] <= a <= rango[1]]
if len(completos_en_rango) >= 2:
    ult = completos_en_rango[-1]
    prev = completos_en_rango[-2]
    ing_ult = df[df["anio"] == ult]["ingresos"].sum()
    ing_prev = df[df["anio"] == prev]["ingresos"].sum()
    variacion = (ing_ult - ing_prev) / ing_prev * 100
    var_ref = f"{ult} frente a {prev}"
    lineas_ult = df[df["anio"] == ult]["marca"].nunique()
    ing_linea_ult = ing_ult / lineas_ult
    ref_anio = ult
    var_disponible = True
else:
    variacion = 0
    var_ref = "Rango insuficiente"
    ref_anio = rango[1]
    lineas_ult = dff[dff["anio"] == ref_anio]["marca"].nunique() or dff["marca"].nunique()
    ing_linea_ult = dff[dff["anio"] == ref_anio]["ingresos"].sum() / max(lineas_ult, 1)
    var_disponible = False

total = dff["ingresos"].sum()

c1, c2, c3, c4 = st.columns(4, gap="medium")
c1.metric("Ingresos acumulados", f"USD {total/1e9:,.2f} B")
if var_disponible:
    c2.metric("Variación interanual", f"{variacion:+.2f} %",
              delta=f"{var_ref}", delta_color="off")
else:
    c2.metric("Variación interanual", "—",
              delta="Se requieren 2 años completos", delta_color="off")
c3.metric(f"Líneas activas ({ref_anio})", f"{lineas_ult}")
c4.metric(f"Ingreso por línea ({ref_anio})",
          f"USD {ing_linea_ult/1e6:,.2f} M")

# =====================================================================
# PERSPECTIVA FINANCIERA
# =====================================================================
st.markdown('<div class="section-title">Perspectiva financiera</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns([1.4, 1], gap="medium")

with col1:
    ing_mes = dff.groupby("fecha", as_index=False)["ingresos"].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ing_mes["fecha"], y=ing_mes["ingresos"],
        mode="lines", line=dict(color=STEEL, width=1.8),
        fill="tozeroy", fillcolor="rgba(46,92,138,0.10)",
        hovertemplate="<b>%{x|%b %Y}</b><br>USD %{y:,.0f}<extra></extra>",
        name="Ingresos mensuales"
    ))
    fig.update_layout(**PLOT_LAYOUT, height=360,
                      title="Evolución mensual de ingresos",
                      xaxis_title="Periodo", yaxis_title="Ingresos (USD)",
                      yaxis_tickprefix="$", yaxis_tickformat=",.2s",
                      showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    ing_anio = dff.groupby("anio", as_index=False)["ingresos"].sum()
    ing_anio["var"] = ing_anio["ingresos"].pct_change() * 100
    ing_anio = ing_anio[ing_anio["anio"].isin(ANIOS_COMPLETOS)].dropna()
    ing_anio["color"] = ing_anio["var"].apply(
        lambda v: STEEL if v > 0 else (MIST if v > -5 else SLATE))
    fig = go.Figure(go.Bar(
        x=ing_anio["anio"], y=ing_anio["var"],
        marker=dict(color=ing_anio["color"], line=dict(color=PAPER, width=1)),
        text=[f"{v:+.1f}%" for v in ing_anio["var"]],
        textposition="outside",
        textfont=dict(size=9, color=INK),
        hovertemplate="<b>%{x}</b><br>%{y:+.2f}%<extra></extra>"
    ))
    fig.update_layout(**PLOT_LAYOUT, height=360,
                      title="Variación anual de ingresos",
                      xaxis_title="Año", yaxis_title="Variación (%)",
                      yaxis_ticksuffix="%",
                      showlegend=False)
    fig.add_hline(y=0, line=dict(color=INK, width=0.6))
    st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# PERSPECTIVA CLIENTE
# =====================================================================
st.markdown('<div class="section-title">Perspectiva cliente</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1], gap="medium")

with col1:
    top = (dff.groupby("marca")["ingresos"].sum()
              .sort_values(ascending=True).tail(top_n).reset_index())
    shades = [f"rgba(46,92,138,{0.45 + 0.5 * i / max(len(top)-1, 1):.2f})"
              for i in range(len(top))]
    fig = go.Figure(go.Bar(
        x=top["ingresos"], y=top["marca"], orientation="h",
        marker=dict(color=shades, line=dict(color=PAPER, width=1)),
        text=[f"USD {v/1e9:.2f} B" if v >= 1e9 else f"USD {v/1e6:.0f} M"
              for v in top["ingresos"]],
        textposition="outside",
        textfont=dict(size=10, color=INK),
        hovertemplate="<b>%{y}</b><br>USD %{x:,.0f}<extra></extra>"
    ))
    fig.update_layout(**PLOT_LAYOUT, height=460,
                      title=f"Ranking — Top {top_n} líneas por ingresos acumulados",
                      xaxis_title="Ingresos acumulados (USD)", yaxis_title="",
                      xaxis_tickprefix="$", xaxis_tickformat=",.2s",
                      showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    pie_all = dff.groupby("marca")["ingresos"].sum().sort_values(ascending=False)
    top5 = pie_all.head(5)
    resto_label = f"Resto ({len(pie_all)-5} líneas)" if len(pie_all) > 5 else "Resto"
    resto_val = pie_all.iloc[5:].sum() if len(pie_all) > 5 else 0
    if resto_val > 0:
        resto = pd.Series({resto_label: resto_val})
        pie_data = pd.concat([top5, resto])
    else:
        pie_data = top5
    fig = go.Figure(go.Pie(
        labels=pie_data.index, values=pie_data.values,
        hole=0.58,
        marker=dict(colors=[NAVY, "#1E4A6D", STEEL, "#5A7FA8", MIST, "#B8BDC4"],
                    line=dict(color=PAPER, width=2.5)),
        textinfo="percent",
        textfont=dict(size=11, color="white", family="Inter"),
        hovertemplate="<b>%{label}</b><br>USD %{value:,.0f}<br>%{percent}<extra></extra>",
        sort=False
    ))
    fig.update_layout(
        font=dict(family="Inter", color=INK, size=11),
        paper_bgcolor=PAPER, height=460,
        title_text="Concentración del portafolio",
        title_font=dict(size=13, color=NAVY),
        title_x=0,
        legend=dict(orientation="v", yanchor="middle", y=0.5, x=1.02,
                     font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=130, t=60, b=40),
        annotations=[
            dict(text=(f"<b style='color:{NAVY};font-size:18px'>USD {pie_data.sum()/1e9:.1f} B</b>"
                        f"<br><span style='color:{SLATE};font-size:10px;font-style:italic'>total</span>"),
                  x=0.5, y=0.5, font_size=14, showarrow=False)
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# PERSPECTIVA PROCESOS INTERNOS
# =====================================================================
st.markdown('<div class="section-title">Perspectiva de procesos internos</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    amp = dff.groupby("anio", as_index=False)["marca"].nunique()
    amp.columns = ["anio", "n"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=amp["anio"], y=amp["n"], mode="lines+markers+text",
        line=dict(color=STEEL, width=2),
        marker=dict(size=7, color=PAPER, line=dict(color=STEEL, width=1.5)),
        fill="tozeroy", fillcolor="rgba(46,92,138,0.08)",
        text=amp["n"], textposition="top center",
        textfont=dict(size=9, color=INK),
        hovertemplate="<b>%{x}</b><br>%{y} líneas activas<extra></extra>",
        name="Líneas activas"
    ))
    fig.update_layout(**PLOT_LAYOUT, height=400,
                      title="Amplitud del portafolio por año",
                      xaxis_title="Año", yaxis_title="Número de líneas",
                      showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    ef = dff.groupby("anio").agg(total=("ingresos", "sum"),
                                   n=("marca", "nunique")).reset_index()
    ef["ing_linea"] = ef["total"] / ef["n"]
    ef = ef[ef["anio"].isin(ANIOS_COMPLETOS)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ef["anio"], y=ef["ing_linea"], mode="lines+markers",
        line=dict(color=STEEL, width=2),
        marker=dict(size=8, symbol="square", color=PAPER,
                     line=dict(color=STEEL, width=1.5)),
        fill="tozeroy", fillcolor="rgba(46,92,138,0.08)",
        hovertemplate="<b>%{x}</b><br>USD %{y:,.0f}<extra></extra>",
        name="Ingreso por línea"
    ))
    fig.add_hline(y=15e6, line=dict(color=SLATE, width=1, dash="dash"),
                   annotation_text="Meta: USD 15 M",
                   annotation_position="top right",
                   annotation_font=dict(size=10, color=SLATE))
    fig.update_layout(**PLOT_LAYOUT, height=400,
                      title="Ingreso promedio por línea activa",
                      xaxis_title="Año", yaxis_title="Ingreso por línea (USD)",
                      yaxis_tickprefix="$", yaxis_tickformat=",.2s",
                      showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# PERSPECTIVA APRENDIZAJE Y CRECIMIENTO
# =====================================================================
st.markdown('<div class="section-title">Perspectiva de aprendizaje y crecimiento</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    hm = dff.groupby(["anio", "mes"])["ingresos"].sum().reset_index()
    hm_pivot = hm.pivot(index="mes", columns="anio", values="ingresos")
    meses_es = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    fig = go.Figure(go.Heatmap(
        z=hm_pivot.values,
        x=hm_pivot.columns, y=[meses_es[m-1] for m in hm_pivot.index],
        colorscale=[[0, "#F0F4F9"], [0.3, MIST], [0.7, STEEL], [1, NAVY]],
        colorbar=dict(title=dict(text="USD", font=dict(size=10, color=SLATE)),
                       tickprefix="$", tickformat=",.2s",
                       outlinecolor=HAIR, outlinewidth=1,
                       tickfont=dict(size=10, color=INK)),
        hovertemplate="<b>%{y} %{x}</b><br>USD %{z:,.0f}<extra></extra>"
    ))
    fig.update_layout(
        font=dict(family="Inter", color=INK, size=11),
        paper_bgcolor=PAPER, plot_bgcolor=PAPER, height=420,
        title_text="Mapa de calor: ingresos por año y mes",
        title_font=dict(size=13, color=NAVY),
        title_x=0,
        xaxis_title="Año", yaxis_title="Mes",
        margin=dict(l=50, r=40, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    top5_global = (df.groupby("marca")["ingresos"].sum()
                      .sort_values(ascending=False).head(5).index.tolist())
    fig = go.Figure()
    palette = [NAVY, STEEL, "#5A7FA8", SLATE, "#9AAAB8"]
    symbols = ["circle", "square", "diamond", "triangle-up", "triangle-down"]
    cv_medios = {}
    for i, m in enumerate(top5_global):
        s = (df[df["marca"] == m].sort_values("fecha")
                                  .set_index("fecha")["ingresos"]
                                  .resample("MS").sum())
        cv_roll = s.rolling(36, min_periods=24).std() / s.rolling(36, min_periods=24).mean()
        cv_medios[m] = s.std() / s.mean()
        fig.add_trace(go.Scatter(
            x=cv_roll.index, y=cv_roll.values, mode="lines+markers",
            name=f"{m} (CV medio {cv_medios[m]:.2f})",
            line=dict(color=palette[i], width=1.6),
            marker=dict(size=5, symbol=symbols[i],
                         color=PAPER, line=dict(color=palette[i], width=1.2)),
            hovertemplate=f"<b>{m}</b><br>%{{x|%b %Y}}<br>CV: %{{y:.3f}}<extra></extra>"
        ))
    fig.add_hline(y=0.50, line=dict(color=SLATE, width=1, dash="dash"),
                   annotation_text="Meta: CV ≤ 0,50",
                   annotation_position="top right",
                   annotation_font=dict(size=10, color=SLATE))
    fig.update_layout(**PLOT_LAYOUT, height=420,
                      title="Consistencia del Top 5 (CV móvil 36 meses)",
                      xaxis_title="Periodo", yaxis_title="Coeficiente de variación",
                      legend=dict(orientation="h", y=-0.22,
                                   font=dict(size=9.5), bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# MATRIZ DE CUMPLIMIENTO
# =====================================================================
st.markdown('<div class="section-title">Matriz de cumplimiento de indicadores</div>',
            unsafe_allow_html=True)

if len(ANIOS_COMPLETOS) >= 2:
    a_ult, a_prev = ANIOS_COMPLETOS[-1], ANIOS_COMPLETOS[-2]
    ing_a_ult = df[df["anio"] == a_ult]["ingresos"].sum()
    ing_a_prev = df[df["anio"] == a_prev]["ingresos"].sum()
    var_bsc = (ing_a_ult - ing_a_prev) / ing_a_prev * 100
else:
    a_ult = int(df["anio"].max())
    a_prev = a_ult - 1
    var_bsc = 0

top5_bsc = df.groupby("marca")["ingresos"].sum().sort_values(ascending=False).head(5)
part_top5 = top5_bsc.sum() / df["ingresos"].sum() * 100

n_lineas_ult = df[df["anio"] == a_ult]["marca"].nunique()
ing_linea_bsc = df[df["anio"] == a_ult]["ingresos"].sum() / max(n_lineas_ult, 1)

cv_vals = []
for m in top5_bsc.index:
    s = df[df["marca"] == m]["ingresos"]
    cv_vals.append(s.std() / s.mean())
cv_prom = float(np.mean(cv_vals))

def estado_mayor(v, meta):
    return "Cumplido" if v >= meta else "Parcial"
def estado_menor(v, meta):
    return "Cumplido" if v <= meta else "Parcial"

matriz = pd.DataFrame([
    {"Perspectiva": "Financiera",
     "Indicador": f"Variación anual de ingresos ({a_ult} vs {a_prev})",
     "Meta": "≥ +3,0 %",
     "Valor observado": f"{var_bsc:+.2f} %",
     "Estado": estado_mayor(var_bsc, 3.0)},
    {"Perspectiva": "Cliente",
     "Indicador": "Participación del Top 5 sobre ingresos totales",
     "Meta": "≥ 50,0 %",
     "Valor observado": f"{part_top5:.2f} %",
     "Estado": estado_mayor(part_top5, 50.0)},
    {"Perspectiva": "Procesos internos",
     "Indicador": f"Ingreso promedio por línea activa ({a_ult})",
     "Meta": "≥ USD 15,0 M",
     "Valor observado": f"USD {ing_linea_bsc/1e6:,.2f} M",
     "Estado": estado_mayor(ing_linea_bsc, 15e6)},
    {"Perspectiva": "Aprendizaje y crecimiento",
     "Indicador": "Coeficiente de variación promedio del Top 5",
     "Meta": "≤ 0,50",
     "Valor observado": f"{cv_prom:.2f}",
     "Estado": estado_menor(cv_prom, 0.50)},
])

st.dataframe(matriz, use_container_width=True, hide_index=True,
              column_config={
                  "Perspectiva": st.column_config.TextColumn(width="medium"),
                  "Indicador": st.column_config.TextColumn(width="large"),
                  "Meta": st.column_config.TextColumn(width="small"),
                  "Valor observado": st.column_config.TextColumn(width="small"),
                  "Estado": st.column_config.TextColumn(width="small"),
              })

# =====================================================================
# FOOTER
# =====================================================================
st.markdown("""
<div class="footer-note">
Fuente: archivo 02_total.xlsx · Metodología: Balanced Scorecard (Kaplan &amp; Norton, 1996) ·
Supermercados Mercandina C. A. — Panel estratégico
</div>
""", unsafe_allow_html=True)
