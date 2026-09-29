import sys
import subprocess
import os

# ==========================================
# 1. AUTO-LANZADOR PARA DOBLE CLIC EN WINDOWS
# ==========================================
if __name__ == "__main__":
    import streamlit as st
    if not st.runtime.exists():
        file_path = os.path.abspath(__file__)
        subprocess.run([sys.executable, "-m", "streamlit", "run", file_path])
        sys.exit(0)

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 2. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Calculadora de Sueldo Ecuador",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 3. MANEJO DE ESTADO (RESET / VALORES INICIALES)
# ==========================================
def init_states():
    defaults = {
        "sueldo_mensual": 900.0,
        "dias_trabajados": 30,
        "hrs_50": 0.0,
        "hrs_100": 0.0,
        "bonos": 0.0,
        "comisiones": 0.0,
        "prestamo_quiro": 0.0,
        "prestamo_hipo": 0.0,
        "hrs_descontar": 0.0,
        "multas": 0.0,
        "atrasos": 0.0,
        "imp_renta": 0.0,
        "cesantia_manual": 0.0,
        "anticipos": 0.0,
        "consumos": 0.0,
        "pension_alim": 0.0,
        "ext_salud": 0.0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def reset_fields():
    st.session_state["sueldo_mensual"] = 900.0
    st.session_state["dias_trabajados"] = 30
    st.session_state["hrs_50"] = 0.0
    st.session_state["hrs_100"] = 0.0
    st.session_state["bonos"] = 0.0
    st.session_state["comisiones"] = 0.0
    st.session_state["prestamo_quiro"] = 0.0
    st.session_state["prestamo_hipo"] = 0.0
    st.session_state["hrs_descontar"] = 0.0
    st.session_state["multas"] = 0.0
    st.session_state["atrasos"] = 0.0
    st.session_state["imp_renta"] = 0.0
    st.session_state["cesantia_manual"] = 0.0
    st.session_state["anticipos"] = 0.0
    st.session_state["consumos"] = 0.0
    st.session_state["pension_alim"] = 0.0
    st.session_state["ext_salud"] = 0.0

init_states()

# ==========================================
# 4. INYECCIÓN DE CSS (AJUSTE ESTRICTO DE 2 COLUMNAS Y CERO SCROLL HORIZONTAL)
# ==========================================
st.markdown("""
<style>
    /* Reset de box-sizing global */
    *, *:before, *:after {
        box-sizing: border-box !important;
    }

    /* Ocultar header nativo y evitar bloqueos */
    [data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 100 !important;
    }
    
    /* Bloqueo absoluto de scroll horizontal */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        overflow-x: hidden !important;
        width: 100% !important;
        max-width: 100vw !important;
    }

    /* Ajustar área principal */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.1rem !important;
        padding-right: 0.1rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }

    /* OCULTAR BOTONES (+ / -) Y FLECHAS DE INPUTS NUMÉRICOS */
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        display: none !important;
    }
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { 
        -webkit-appearance: none !important;
        margin: 0 !important;
    }
    input[type=number] {
        -moz-appearance: textfield !important;
        text-align: center !important;
        padding: 4px 2px !important;
        font-size: 0.85rem !important;
        width: 100% !important;
    }

    /* COMPRIMIR CONTENEDORES DE INPUTS */
    div[data-testid="stNumberInput"], 
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        background-color: #0F172A !important;
        border-color: #334155 !important;
        border-radius: 6px !important;
    }

    /* FORZAR 2 COLUMNAS ESTRICTAS DEL 48.5% CADA UNA (TOTAL 100% CON GAP DE 3%) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
        gap: 3% !important;
        width: 100% !important;
        max-width: 100% !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    [data-testid="column"] {
        flex: 0 0 48.5% !important;
        width: 48.5% !important;
        max-width: 48.5% !important;
        min-width: 0 !important;
        overflow: hidden !important;
        padding: 0 !important;
    }

    /* LABELS COMPACTAS CON RECORTES LIMPIOS SI EXCEDEN */
    div[data-testid="stWidgetLabel"] label p {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        margin-bottom: 2px !important;
    }

    /* BOTONES DE CABECERA COMPACTOS */
    .stButton > button {
        padding: 0.3rem 0.1rem !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
    }

    /* Fondo oscuro principal */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* Títulos de sección */
    .section-title-ingresos {
        color: #00E676;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
        border-bottom: 1px solid #334155;
        padding-bottom: 4px;
    }

    .section-title-egresos {
        color: #F472B6;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
        border-bottom: 1px solid #334155;
        padding-bottom: 4px;
    }

    .section-title-kpis {
        color: #38BDF8;
        font-size: 0.85rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
        border-bottom: 1px solid #334155;
        padding-bottom: 4px;
    }

    /* Tarjetas de Métricas Secundarias / KPIs Grid */
    .kpi-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 6px 2px;
        margin-bottom: 6px;
        text-align: center;
        min-height: 58px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;
    }
    
    .kpi-card-centered {
        background: linear-gradient(135deg, #0F2744 0%, #0F172A 100%);
        border: 1.5px solid #38BDF8;
        border-radius: 8px;
        padding: 8px 4px;
        margin: 4px auto 6px auto;
        text-align: center;
        width: 100%;
    }

    /* TÍTULOS DE KPIS: Blanco claro (#CBD5E1) */
    .kpi-card .title, .kpi-card-centered .title {
        font-size: 0.62rem;
        color: #CBD5E1 !important;
        font-weight: 700;
        text-transform: uppercase;
        line-height: 1.1;
        letter-spacing: 0.01em;
    }
    .kpi-card .value, .kpi-card-centered .value {
        font-size: 1.05rem;
        font-weight: 800;
        margin-top: 2px;
        line-height: 1.15;
    }

    /* Colores para KPIs */
    .text-green { color: #00E676 !important; }
    .text-blue { color: #38BDF8 !important; }
    .text-amber { color: #FBBF24 !important; }
    .text-rose { color: #F472B6 !important; }
    .text-teal { color: #2DD4BF !important; }
    .text-purple { color: #C084FC !important; }

    /* Tarjeta Destacada TOTAL A PAGAR */
    .kpi-highlight {
        background: linear-gradient(135deg, #064E3B 0%, #022C22 100%);
        border: 2px solid #00E676;
        border-radius: 12px;
        padding: 10px 6px;
        margin-top: 10px;
        margin-bottom: 12px;
        text-align: center;
        box-shadow: 0 6px 14px rgba(0, 230, 118, 0.2);
    }
    .kpi-highlight .kpi-title {
        color: #A7F3D0;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    .kpi-highlight .kpi-value {
        color: #00E676;
        font-size: 1.7rem;
        font-weight: 900;
        line-height: 1.2;
    }
    .kpi-highlight .kpi-sub {
        color: #FFFFFF !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        margin-top: 3px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. FIX PARCHE MÓVIL (POPOVER / DROPDOWNS)
# ==========================================
components.html("""
<script>
document.addEventListener('click', function(e) {
    var target = e.target;
    if (target.closest('[data-testid="stPopover"]') || target.closest('.stSelectbox')) {
        setTimeout(function() {
            var event = new KeyboardEvent('keydown', {
                key: 'Escape',
                keyCode: 27,
                which: 27,
                bubbles: true,
                cancelable: true
            });
            document.dispatchEvent(event);
        }, 120);
    }
});
</script>
""", height=0, width=0)

# ==========================================
# 6. ENCABEZADO Y BOTONES SUPERIORES (REFRESCAR / RESET)
# ==========================================
st.markdown("<h3 style='text-align: center; color: #38BDF8; font-weight: 800; margin-bottom: 2px; font-size: 1.2rem;'>🧮 Calculadora de Sueldo</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.72rem; margin-bottom: 8px;'>Simulador Interactivo (Normativa Ecuador)</p>", unsafe_allow_html=True)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🔄 Refrescar", use_container_width=True):
        st.rerun()

with col_btn2:
    if st.button("🧹 Reset / Limpiar", use_container_width=True):
        reset_fields()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 7. SECCIÓN 1: RECUADRO DE INGRESOS
# ==========================================
st.markdown('<div class="section-title-ingresos">🟢 1. RECUADRO DE INGRESOS</div>', unsafe_allow_html=True)

col_i1, col_i2 = st.columns(2)
with col_i1:
    sueldo_mensual = st.number_input("Sueldo Base ($)", min_value=0.0, key="sueldo_mensual", step=50.0, format="%.2f")
    hrs_50 = st.number_input("Horas Sup. (50%)", min_value=0.0, key="hrs_50", step=1.0, format="%.1f")
    bonos = st.number_input("Bonos ($)", min_value=0.0, key="bonos", step=5.0, format="%.2f")

with col_i2:
    dias_trabajados = st.number_input("Días Trab.", min_value=1, max_value=30, key="dias_trabajados", step=1)
    hrs_100 = st.number_input("Horas Ext. (100%)", min_value=0.0, key="hrs_100", step=1.0, format="%.1f")
    comisiones = st.number_input("Comisiones ($)", min_value=0.0, key="comisiones", step=5.0, format="%.2f")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 8. SECCIÓN 2: RECUADRO DE EGRESOS Y DESCUENTOS
# ==========================================
st.markdown('<div class="section-title-egresos">🔴 2. RECUADRO DE EGRESOS Y DESCUENTOS</div>', unsafe_allow_html=True)

col_e1, col_e2 = st.columns(2)
with col_e1:
    prestamo_quiro = st.number_input("Prést. Quirografario ($)", min_value=0.0, key="prestamo_quiro", step=10.0, format="%.2f")
    prestamo_hipo = st.number_input("Prést. Hipotecario ($)", min_value=0.0, key="prestamo_hipo", step=10.0, format="%.2f")
    hrs_descontar = st.number_input("Horas Descontar (#)", min_value=0.0, key="hrs_descontar", step=1.0, format="%.1f")

with col_e2:
    multas = st.number_input("Multas ($)", min_value=0.0, key="multas", step=5.0, format="%.2f")
    atrasos = st.number_input("Atrasos ($)", min_value=0.0, key="atrasos", step=5.0, format="%.2f")
    imp_renta = st.number_input("Imp. Renta ($)", min_value=0.0, key="imp_renta", step=5.0, format="%.2f")

# Opcionales de Egresos adicionales
with st.expander("➕ Otros Descuentos Opcionales (Cesantía, Anticipos, Consumos)"):
    col_e3, col_e4 = st.columns(2)
    with col_e3:
        usar_cesantia_auto = st.checkbox("Cesantía IESS (2%) Auto.", value=True)
        cesantia_manual = st.number_input("Cesantía ($)", min_value=0.0, key="cesantia_manual", step=5.0, format="%.2f")
        anticipos = st.number_input("Anticipos ($)", min_value=0.0, key="anticipos", step=5.0)
    with col_e4:
        consumos = st.number_input("Consumos ($)", min_value=0.0, key="consumos", step=5.0)
        pension_alim = st.number_input("Pensión Alim. ($)", min_value=0.0, key="pension_alim", step=10.0)
        ext_salud = st.number_input("Ext. Salud ($)", min_value=0.0, key="ext_salud", step=5.0)

# Beneficios opcionales (Décimos)
with st.expander("🎁 Beneficios de Ley (Mensualización de Décimos y F. Reserva)"):
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        mensualizar_13 = st.checkbox("XIII Mensual", value=True)
        mensualizar_fr = st.checkbox("F. Reserva (8.33%)", value=True)
    with col_b2:
        mensualizar_14 = st.checkbox("XIV Mensual", value=True)
        sbu_valor = st.number_input("SBU ($)", value=482.0, step=1.0)

# ==========================================
# 9. MOTOR DE CÁLCULO FINANCIERO Y FÓRMULAS
# ==========================================
val_hora_norm = sueldo_mensual / 240.0 if sueldo_mensual > 0 else 0.0
val_hora_50 = val_hora_norm * 1.5
val_hora_100 = val_hora_norm * 2.0

val_sup = hrs_50 * val_hora_50
val_ext = hrs_100 * val_hora_100
total_he = val_sup + val_ext

sueldo_ganado = (sueldo_mensual / 30.0) * dias_trabajados
val_descuento_horas = hrs_descontar * val_hora_norm

ingresos_gravables = max(0.0, (sueldo_ganado + total_he + bonos + comisiones) - val_descuento_horas)

# Aporte IESS Personal 9.45%
iess_945 = ingresos_gravables * 0.0945

# CÁLCULO AUTOMÁTICO DE CESANTÍA (2% de los ingresos gravables)
cesantia = (ingresos_gravables * 0.02) if usar_cesantia_auto else cesantia_manual

# Beneficios de Ley
val_xiii = (ingresos_gravables / 12.0) if mensualizar_13 else 0.0
val_xiv = (sbu_valor / 12.0) if mensualizar_14 else 0.0
val_fr = (ingresos_gravables * (1.0 / 12.0)) if mensualizar_fr else 0.0

total_beneficios = val_xiii + val_xiv + val_fr
total_ingresos = ingresos_gravables + total_beneficios

otros_egresos_sum = (
    prestamo_quiro + prestamo_hipo + multas + atrasos + 
    imp_renta + anticipos + consumos + pension_alim + ext_salud
)
total_egresos = iess_945 + cesantia + otros_egresos_sum
total_a_pagar = total_ingresos - total_egresos

# ==========================================
# 10. RESUMEN DE KPIS ORGANIZADOS EN 2 COLUMNAS EN MÓVIL
# ==========================================
st.markdown("---")

# --- BLOQUE 1: INGRESOS Y HORAS EXTRAS ---
st.markdown('<div class="section-title-kpis">💵 1. INGRESOS BASE Y HORAS EXTRAS</div>', unsafe_allow_html=True)

k_col1, k_col2 = st.columns(2)
with k_col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Sueldo Base (Ganado)</div>
        <div class="value text-blue">${sueldo_ganado:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with k_col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Bonos</div>
        <div class="value text-amber">${bonos:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

k_col3, k_col4 = st.columns(2)
with k_col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Suplementarias (50%)</div>
        <div class="value text-teal">${val_sup:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with k_col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Extraordinarias (100%)</div>
        <div class="value text-teal">${val_ext:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-card-centered">
    <div class="title">Valor Total Horas Extras: <span class="text-blue">${total_he:,.2f}</span></div>
    <div class="title" style="margin-top:6px;">Total Ingresos Gravables (Sueldo + HE + Bonos + Comisiones)</div>
    <div class="value text-blue">${ingresos_gravables:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# --- BLOQUE 2: BENEFICIOS DE LEY ---
st.markdown('<div class="section-title-kpis">🎁 2. BENEFICIOS DE LEY</div>', unsafe_allow_html=True)

k_col5, k_col6 = st.columns(2)
with k_col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">F. Reserva (8.33%)</div>
        <div class="value text-purple">${val_fr:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with k_col6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">XIII Mensual</div>
        <div class="value text-amber">${val_xiii:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

k_col7, k_col8 = st.columns(2)
with k_col7:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">XIV Mensual</div>
        <div class="value text-amber">${val_xiv:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with k_col8:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Total Beneficios</div>
        <div class="value text-green">${total_beneficios:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-card-centered" style="border-color: #00E676;">
    <div class="title">Total Ingresos (Gravables + Beneficios de Ley)</div>
    <div class="value text-green">${total_ingresos:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# --- BLOQUE 3: APORTACIONES Y EGRESOS ---
st.markdown('<div class="section-title-kpis">🔻 3. APORTACIONES Y EGRESOS</div>', unsafe_allow_html=True)

k_col9, k_col10 = st.columns(2)
with k_col9:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Aporte IESS 9.45%</div>
        <div class="value text-rose">${iess_945:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with k_col10:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Cesantía (2%)</div>
        <div class="value text-rose">${cesantia:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

if otros_egresos_sum > 0:
    st.markdown(f"""
    <div class="kpi-card-centered" style="border-color: #F472B6;">
        <div class="title">Otros Egresos y Descuentos</div>
        <div class="value text-rose">${otros_egresos_sum:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# --- BLOQUE 4: KPI GRANDE TOTAL NETO A RECIBIR ---
st.markdown(f"""
<div class="kpi-highlight">
    <div class="kpi-title">💵 TOTAL NETO A RECIBIR</div>
    <div class="kpi-value">${total_a_pagar:,.2f}</div>
    <div class="kpi-sub">Ingresos: ${total_ingresos:,.2f} | Egresos: ${total_egresos:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 11. GRÁFICO Y TABLA DETALLADA
# ==========================================
tab1, tab2 = st.tabs(["📊 Distribución", "📄 Detalle Rol"])

with tab1:
    labels_chart = ["Neto a Recibir", "IESS (9.45%)"]
    values_chart = [max(0.0, total_a_pagar), iess_945]
    colors_chart = ["#00E676", "#F472B6"]
    
    if (cesantia + otros_egresos_sum) > 0:
        labels_chart.append("Otros Egresos")
        values_chart.append(cesantia + otros_egresos_sum)
        colors_chart.append("#FBBF24")

    pct_iess_real = (iess_945 / total_ingresos * 100) if total_ingresos > 0 else 0.0

    fig = px.pie(
        names=labels_chart,
        values=values_chart,
        hole=0.55,
        color_discrete_sequence=colors_chart
    )
    
    fig.update_traces(
        textinfo="percent+value",
        texttemplate="%{percent:.1%}<br>$%{value:,.2f}",
        marker=dict(line=dict(color="#0E1117", width=2))
    )
    
    fig.update_layout(
        title=dict(
            text=f"<b>📊 Retención IESS: {pct_iess_real:.2f}%</b><br><span style='font-size:0.75rem; color:#94A3B8;'>${iess_945:,.2f} de ${total_ingresos:,.2f}</span>",
            font=dict(color="#38BDF8", size=13),
            x=0.5,
            xanchor="center"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=30, l=5, r=5),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(color="#FAFAFA", size=9)
        ),
        font=dict(color="#FAFAFA")
    )
    
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with tab2:
    st.markdown("<h5 style='color: #00E676;'>🟢 Ingresos</h5>", unsafe_allow_html=True)
    df_i = pd.DataFrame([
        {"Concepto": f"Sueldo Ganado ({dias_trabajados}d)", "Valor ($)": sueldo_ganado},
        {"Concepto": f"Horas Sup. 50% ({hrs_50}h)", "Valor ($)": val_sup},
        {"Concepto": f"Horas Ext. 100% ({hrs_100}h)", "Valor ($)": val_ext},
        {"Concepto": "Bonos / Bonificaciones", "Valor ($)": bonos},
        {"Concepto": "Comisiones", "Valor ($)": comisiones},
        {"Concepto": "(-) Descuento Horas", "Valor ($)": -val_descuento_horas},
        {"Concepto": "TOTAL INGRESOS GRAVABLES", "Valor ($)": ingresos_gravables},
        {"Concepto": "XIII Mensual", "Valor ($)": val_xiii},
        {"Concepto": "XIV Mensual", "Valor ($)": val_xiv},
        {"Concepto": "Fondos de Reserva (8.33%)", "Valor ($)": val_fr},
        {"Concepto": "TOTAL INGRESOS", "Valor ($)": total_ingresos},
    ])
    st.dataframe(df_i.style.format({"Valor ($)": "${:,.2f}"}), use_container_width=True, hide_index=True)

    st.markdown("<h5 style='color: #F472B6;'>🔴 Egresos</h5>", unsafe_allow_html=True)
    df_e = pd.DataFrame([
        {"Concepto": "Aporte IESS 9.45%", "Valor ($)": iess_945},
        {"Concepto": "Cesantía (2%)", "Valor ($)": cesantia},
        {"Concepto": "Préstamo Quirografario", "Valor ($)": prestamo_quiro},
        {"Concepto": "Préstamo Hipotecario", "Valor ($)": prestamo_hipo},
        {"Concepto": "Multas", "Valor ($)": multas},
        {"Concepto": "Atrasos", "Valor ($)": atrasos},
        {"Concepto": "Impuesto a la Renta", "Valor ($)": imp_renta},
        {"Concepto": "Otros (Anticipos/Consumos/Salud)", "Valor ($)": anticipos + consumos + pension_alim + ext_salud},
        {"Concepto": "TOTAL EGRESOS", "Valor ($)": total_egresos},
    ])
    st.dataframe(df_e.style.format({"Valor ($)": "${:,.2f}"}), use_container_width=True, hide_index=True)