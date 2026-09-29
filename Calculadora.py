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

# Importaciones principales
import pandas as pd
import plotly.express as px
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
# 3. INYECCIÓN DE CSS (DARK MODE & MÓVIL)
# ==========================================
st.markdown("""
<style>
    /* Ocultar header nativo de Streamlit */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Maximizar área táctil en teléfonos */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 740px !important;
    }

    /* Fondo oscuro principal */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* Títulos de sección */
    .section-title-ingresos {
        color: #00E676;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #334155;
        padding-bottom: 6px;
    }

    .section-title-egresos {
        color: #F472B6;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #334155;
        padding-bottom: 6px;
    }

    .section-title-kpis {
        color: #38BDF8;
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 14px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #334155;
        padding-bottom: 4px;
    }

    /* Tarjetas de Métricas Secundarias / KPIs Grid */
    .kpi-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 10px;
        text-align: center;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .kpi-card-centered {
        background: linear-gradient(135deg, #0F2744 0%, #0F172A 100%);
        border: 1.5px solid #38BDF8;
        border-radius: 12px;
        padding: 12px 14px;
        margin: 4px auto 14px auto;
        text-align: center;
        max-width: 420px;
    }

    .kpi-card .title, .kpi-card-centered .title {
        font-size: 0.72rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        line-height: 1.1;
    }
    .kpi-card .value, .kpi-card-centered .value {
        font-size: 1.28rem;
        font-weight: 800;
        margin-top: 4px;
        line-height: 1.2;
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
        border-radius: 16px;
        padding: 18px 20px;
        margin-top: 16px;
        margin-bottom: 18px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0, 230, 118, 0.2);
    }
    .kpi-highlight .kpi-title {
        color: #A7F3D0;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    .kpi-highlight .kpi-value {
        color: #00E676;
        font-size: 2.3rem;
        font-weight: 900;
        line-height: 1.2;
    }
    .kpi-highlight .kpi-sub {
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin-top: 6px;
        letter-spacing: 0.02em;
    }

    /* Estilo de inputs en Streamlit */
    div[data-baseweb="input"] {
        background-color: #0F172A !important;
        border-color: #334155 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }

    /* Media query para móviles pequeños */
    @media (max-width: 480px) {
        .kpi-highlight .kpi-value {
            font-size: 1.8rem;
        }
        .kpi-highlight .kpi-sub {
            font-size: 0.82rem !important;
        }
        .kpi-card .value, .kpi-card-centered .value {
            font-size: 1.1rem;
        }
        .kpi-card .title, .kpi-card-centered .title {
            font-size: 0.68rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. FIX PARCHE MÓVIL (POPOVER / DROPDOWNS)
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
# 5. ENCABEZADO
# ==========================================
st.markdown("<h2 style='text-align: center; color: #38BDF8; font-weight: 800; margin-bottom: 2px;'>🧮 Calculadora de Sueldo</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem; margin-bottom: 20px;'>Simulador Interactivo de Rol de Pagos (Normativa Ecuador)</p>", unsafe_allow_html=True)

# ==========================================
# 6. SECCIÓN 1: RECUADRO DE INGRESOS
# ==========================================
st.markdown('<div class="section-title-ingresos">🟢 1. RECUADRO DE INGRESOS</div>', unsafe_allow_html=True)

col_i1, col_i2 = st.columns(2)
with col_i1:
    sueldo_mensual = st.number_input("Sueldo Mensual Base ($)", min_value=0.0, value=900.0, step=50.0, format="%.2f")
    hrs_50 = st.number_input("Horas Suplementarias (50%)", min_value=0.0, value=10.0, step=1.0, format="%.1f")
    bonos = st.number_input("Bonos / Bonificaciones ($)", min_value=0.0, value=85.73, step=5.0, format="%.2f")

with col_i2:
    dias_trabajados = st.number_input("Días Trabajados", min_value=1, max_value=30, value=30, step=1)
    hrs_100 = st.number_input("Horas Extraordinarias (100%)", min_value=0.0, value=0.0, step=1.0, format="%.1f")
    comisiones = st.number_input("Comisiones ($)", min_value=0.0, value=0.0, step=5.0, format="%.2f")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 7. SECCIÓN 2: RECUADRO DE EGRESOS Y DESCUENTOS
# ==========================================
st.markdown('<div class="section-title-egresos">🔴 2. RECUADRO DE EGRESOS Y DESCUENTOS</div>', unsafe_allow_html=True)

col_e1, col_e2 = st.columns(2)
with col_e1:
    prestamo_quiro = st.number_input("Préstamo Quirografario ($)", min_value=0.0, value=0.0, step=10.0, format="%.2f")
    prestamo_hipo = st.number_input("Préstamo Hipotecario ($)", min_value=0.0, value=0.0, step=10.0, format="%.2f")
    hrs_descontar = st.number_input("Horas a Descontar (#)", min_value=0.0, value=0.0, step=1.0, format="%.1f")

with col_e2:
    multas = st.number_input("Multas ($)", min_value=0.0, value=0.0, step=5.0, format="%.2f")
    atrasos = st.number_input("Atrasos ($)", min_value=0.0, value=0.0, step=5.0, format="%.2f")
    imp_renta = st.number_input("Impuesto a la Renta ($)", min_value=0.0, value=0.0, step=5.0, format="%.2f")

# Opcionales de Egresos adicionales
with st.expander("➕ Otros Descuentos Opcionales (Cesantía, Anticipos, Consumos)"):
    col_e3, col_e4 = st.columns(2)
    with col_e3:
        usar_cesantia_auto = st.checkbox("Calcular Cesantía IESS (2%) Automática", value=True)
        cesantia_manual = st.number_input("Cesantía ($) (Si no es automática)", min_value=0.0, value=0.0, step=5.0, format="%.2f")
        anticipos = st.number_input("Anticipos de Bono / Sueldo ($)", min_value=0.0, value=0.0, step=5.0)
    with col_e4:
        consumos = st.number_input("Consumo de Empleados ($)", min_value=0.0, value=0.0, step=5.0)
        pension_alim = st.number_input("Pensión Alimenticia ($)", min_value=0.0, value=0.0, step=10.0)
        ext_salud = st.number_input("Extensión de Salud IESS ($)", min_value=0.0, value=0.0, step=5.0)

# Beneficios opcionales (Décimos)
with st.expander("🎁 Beneficios de Ley (Mensualización de Décimos y F. Reserva)"):
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        mensualizar_13 = st.checkbox("XIII Mensual", value=True)
    with col_b2:
        mensualizar_14 = st.checkbox("XIV Mensual", value=True)
    with col_b3:
        mensualizar_fr = st.checkbox("Fondos Reserva (8.33%)", value=True)
    sbu_valor = st.number_input("Salario Básico Unificado (SBU)", value=482.0, step=1.0)

# ==========================================
# 8. MOTOR DE CÁLCULO FINANCIERO Y FÓRMULAS
# ==========================================
val_hora_norm = sueldo_mensual / 240.0 if sueldo_mensual > 0 else 0.0
val_hora_50 = val_hora_norm * 1.5   # 50% recargo suplementario
val_hora_100 = val_hora_norm * 2.0  # 100% recargo extraordinario

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

# Beneficios de Ley (Décimos y Fondos de Reserva)
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
# 9. RESUMEN DE KPIS REORGANIZADOS
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

k_col3, k_col4, k_col5 = st.columns(3)
with k_col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Valor Suplementarias (50%)</div>
        <div class="value text-teal">${val_sup:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with k_col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Valor Extraordinarias (100%)</div>
        <div class="value text-teal">${val_ext:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with k_col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Valor Total Horas</div>
        <div class="value text-blue">${total_he:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-card-centered">
    <div class="title">Total Ingresos Gravables (Sueldo + HE + Bonos + Comisiones)</div>
    <div class="value text-blue">${ingresos_gravables:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# --- BLOQUE 2: BENEFICIOS DE LEY ---
st.markdown('<div class="section-title-kpis">🎁 2. BENEFICIOS DE LEY</div>', unsafe_allow_html=True)

k_col6, k_col7, k_col8 = st.columns(3)
with k_col6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">F. Reserva Mensual (8.33%)</div>
        <div class="value text-purple">${val_fr:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with k_col7:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">XIII Mensual</div>
        <div class="value text-amber">${val_xiii:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
with k_col8:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">XIV Mensual</div>
        <div class="value text-amber">${val_xiv:,.2f}</div>
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

k_col9, k_col10, k_col11 = st.columns(3)
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
with k_col11:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="title">Otros Egresos</div>
        <div class="value text-rose">${otros_egresos_sum:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# --- BLOQUE 4: KPI GRANDE TOTAL NETO A RECIBIR ---
st.markdown(f"""
<div class="kpi-highlight">
    <div class="kpi-title">💵 TOTAL NETO A RECIBIR</div>
    <div class="kpi-value">${total_a_pagar:,.2f}</div>
    <div class="kpi-sub">Total Ingresos: ${total_ingresos:,.2f} | Total Egresos: ${total_egresos:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 10. GRÁFICO Y TABLA DETALLADA
# ==========================================
tab1, tab2 = st.tabs(["📊 Distribución de Ingresos y Descuentos", "📄 Detalle Rol de Pagos"])

with tab1:
    labels_chart = ["Total Neto a Recibir", "Aporte IESS (9.45%)"]
    values_chart = [max(0.0, total_a_pagar), iess_945]
    colors_chart = ["#00E676", "#F472B6"]
    
    if (cesantia + otros_egresos_sum) > 0:
        labels_chart.append("Otros Egresos / Descuentos")
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
            text=f"<b>📊 Porcentaje de Ingresos Retenido por el IESS</b><br><span style='font-size:0.78rem; color:#94A3B8;'>El IESS 9.45% se lleva el <b>{pct_iess_real:.2f}%</b> de tus ingresos totales (${iess_945:,.2f} de ${total_ingresos:,.2f})</span>",
            font=dict(color="#38BDF8", size=14),
            x=0.5,
            xanchor="center"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=65, b=40, l=10, r=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center",
            x=0.5,
            title=dict(text="💡 Leyenda (Clic para ocultar/filtrar):", font=dict(color="#FAFAFA", size=11)),
            font=dict(color="#FAFAFA", size=10)
        ),
        font=dict(color="#FAFAFA")
    )
    
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with tab2:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("<h4 style='color: #00E676;'>🟢 Ingresos</h4>", unsafe_allow_html=True)
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

    with col_t2:
        st.markdown("<h4 style='color: #F472B6;'>🔴 Egresos</h4>", unsafe_allow_html=True)
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