# VIP Intelligence | Responsables de los análisis: Julián Vega Castellón (churn) y Edwin Daniel Holguín Ángel (reactivación).
# Coordinación del despliegue: Daniel Holguin. Interfaz con asistencia de IA.
import json
from pathlib import Path
import html
import math
import streamlit as st
import pandas as pd
from inference import load_bundle, get_categories, predict, DEFAULTS

st.set_page_config(page_title='VIP Intelligence',page_icon='♠',layout='wide',initial_sidebar_state='expanded')
ROOT=Path(__file__).resolve().parent
st.markdown('''<style>
.stApp {background:radial-gradient(ellipse at 86% 0%,#182d25 0%,#101816 32%,#0b1010 75%); color:#f1eee4;}
[data-testid="stSidebar"] {background:#101917;border-right:1px solid #3e4435;}
.block-container {max-width:1240px;padding-top:2.2rem;padding-bottom:3rem;}
[data-testid="stHeader"] {background:transparent;}
.hero {position:relative;overflow:hidden;border:1px solid #74613a;border-radius:18px;padding:32px 34px;background:linear-gradient(115deg,#172e24 0%,#101e19 55%,#191b14 100%);margin:0 0 24px;}
.hero .suits {position:absolute;right:25px;top:0px;opacity:.18;font-family:Georgia,serif;font-size:100px;color:#c4a56b;letter-spacing:-12px;transform:rotate(-11deg);pointer-events:none;}
.hero .eyebrow,.eyebrow {font-size:11px;font-weight:700;letter-spacing:2.6px;text-transform:uppercase;color:#d8b974;}
.hero h1 {font-family:Georgia,serif;color:#f5e5ba;font-weight:500;font-size:clamp(28px,4vw,47px);margin:.3rem 0 .45rem;line-height:1.15;}
.hero p {color:#bbc7b9;max-width:680px;font-size:15px;margin:0;}
.tile {min-height:136px;border:1px solid #39473d;background:#121d19;border-radius:14px;padding:18px 20px;margin-bottom:12px;}
.tile small {color:#b6bdac;text-transform:uppercase;letter-spacing:1.3px;font-size:10px;}
.tile .value {font-family:Georgia,serif;font-size:29px;color:#e7c67f;line-height:1.2;margin:9px 0;}
.tile p {color:#b6bdac;font-size:12px;margin:0;}
.score {border:1px solid #76633d;background:linear-gradient(150deg,#182c22,#131b17);border-radius:16px;padding:24px;margin:10px 0 16px;}
.score .big {font-family:Georgia,serif;font-size:54px;line-height:1.2;color:#f1d99b;}
.score .rail {height:12px;background:#29382f;border-radius:20px;position:relative;margin:26px 0 9px;}
.score .fill {height:12px;border-radius:20px;background:linear-gradient(90deg,#659687,#d8b974);}
.score .marker {position:absolute;top:-7px;height:26px;width:2px;background:#fff3d0;}
.score .range {display:flex;justify-content:space-between;font-size:11px;color:#b9c0b2;}
.score .class {margin-top:17px;padding:13px;border-left:3px solid #d8b974;background:#1d2c24;color:#efdfb9;font-weight:600;}
[data-testid="stForm"] {border:1px solid #39473d;border-radius:15px;padding:16px;}
[data-testid="stExpander"] {border-color:#3b493d;}
.stButton>button,.stFormSubmitButton>button {border:1px solid #d7b66f!important;background:#d7b66f!important;color:#101710!important;font-weight:700!important;border-radius:9px!important;}
hr {border-color:#344237!important;}
.life {display:flex;align-items:stretch;gap:12px;flex-wrap:wrap;margin:14px 0;} .node {flex:1;min-width:140px;border:1px solid #74613a;background:#172820;border-radius:14px;padding:20px;text-align:center;} .node strong {font-family:Georgia,serif;font-size:24px;color:#e7c67f;} .node p {font-size:12px;color:#bbc7b9;margin:8px 0 0;} .arrow {align-self:center;color:#d8b974;font-size:20px;text-align:center;} .arrow small {display:block;font-size:10px;} .research {border:1px solid #74613a;border-radius:14px;padding:22px;background:linear-gradient(110deg,#172e24,#1e251a);margin:12px 0 20px;} .research h3 {color:#e7c67f;margin:4px 0;} .research p {color:#bbc7b9;margin:8px 0;} .footer {color:#aab5a8;font-size:11px;border-top:1px solid #3c493e;margin-top:32px;padding-top:14px;letter-spacing:.4px;}
.profile-head {display:flex;align-items:center;gap:22px;flex-wrap:wrap;border:1px solid #74613a;border-radius:18px;padding:30px;background:linear-gradient(120deg,#172e24,#121d19);margin:8px 0 22px;}
.profile-initials {width:88px;height:88px;flex:0 0 88px;display:grid;place-items:center;border-radius:50%;border:1px solid #b49a61;background:#202c23;color:#e7c67f;font-family:Georgia,serif;font-size:31px;letter-spacing:1px;}
.profile-head h2 {color:#f5e5ba;font-family:Georgia,serif;font-weight:500;font-size:clamp(24px,3vw,37px);margin:5px 0;}
.profile-head p {color:#bbc7b9;margin:5px 0;font-size:15px;}
.profile-interest {display:flex;align-items:center;gap:12px;border:1px solid #435044;background:linear-gradient(90deg,#172820 0%,#183127 100%);padding:13px 16px;border-radius:10px;color:#f5e5ba;margin:6px 0;font-size:15px;}
.profile-interest .icon {display:grid;place-items:center;width:24px;height:24px;border-radius:8px;background:#1f3228;color:#d8b974;font-size:14px;flex:0 0 24px;}
.profile-interest .text {line-height:1.2;}
/* Sidebar navigation: button cards with icon and descriptor. */
[data-testid="stSidebar"] .st-key-nav_home button,
[data-testid="stSidebar"] .st-key-nav_churn button,
[data-testid="stSidebar"] .st-key-nav_reactivation button,
[data-testid="stSidebar"] .st-key-nav_research button,
[data-testid="stSidebar"] .st-key-nav_metrics button,
[data-testid="stSidebar"] .st-key-nav_roadmap button {
    display:flex!important;align-items:center!important;justify-content:flex-start!important;gap:10px!important;
    background:transparent!important;border:1px solid transparent!important;border-radius:12px!important;
    padding:10px 10px!important;min-height:64px!important;width:100%!important;
    color:#f5e5ba!important;text-align:left!important;box-shadow:none!important;
}
[data-testid="stSidebar"] .st-key-nav_home button:hover,
[data-testid="stSidebar"] .st-key-nav_churn button:hover,
[data-testid="stSidebar"] .st-key-nav_reactivation button:hover,
[data-testid="stSidebar"] .st-key-nav_research button:hover,
[data-testid="stSidebar"] .st-key-nav_metrics button:hover,
[data-testid="stSidebar"] .st-key-nav_roadmap button:hover {background:#172820!important;border-color:#74613a!important;}
[data-testid="stSidebar"] .st-key-nav_home button::before,
[data-testid="stSidebar"] .st-key-nav_churn button::before,
[data-testid="stSidebar"] .st-key-nav_reactivation button::before,
[data-testid="stSidebar"] .st-key-nav_research button::before,
[data-testid="stSidebar"] .st-key-nav_metrics button::before,
[data-testid="stSidebar"] .st-key-nav_roadmap button::before {
    display:grid;place-items:center;width:34px;height:34px;flex:0 0 34px;border-radius:10px;
    border:1px solid #74613a;background:#203127;color:#e7c67f;font-size:15px;font-weight:600;
}
[data-testid="stSidebar"] .st-key-nav_home button::before {content:"✦";}
[data-testid="stSidebar"] .st-key-nav_churn button::before {content:"🛡️";}
[data-testid="stSidebar"] .st-key-nav_reactivation button::before {content:"↺";}
[data-testid="stSidebar"] .st-key-nav_research button::before {content:"🔬";}
[data-testid="stSidebar"] .st-key-nav_metrics button::before {content:"📊";}
[data-testid="stSidebar"] .st-key-nav_roadmap button::before {content:"🗺️";}
[data-testid="stSidebar"] .st-key-nav_home button::after,
[data-testid="stSidebar"] .st-key-nav_churn button::after,
[data-testid="stSidebar"] .st-key-nav_reactivation button::after,
[data-testid="stSidebar"] .st-key-nav_research button::after,
[data-testid="stSidebar"] .st-key-nav_metrics button::after,
[data-testid="stSidebar"] .st-key-nav_roadmap button::after {content:"›";color:#d8b974;font-size:22px;line-height:1;margin-left:auto;flex:0 0 12px;}
[data-testid="stSidebar"] .st-key-nav_home button [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] .st-key-nav_churn button [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] .st-key-nav_reactivation button [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] .st-key-nav_research button [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] .st-key-nav_metrics button [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] .st-key-nav_roadmap button [data-testid="stMarkdownContainer"] {flex:1;min-width:0;text-align:left;}
[data-testid="stSidebar"] .st-key-nav_home button p,
[data-testid="stSidebar"] .st-key-nav_churn button p,
[data-testid="stSidebar"] .st-key-nav_reactivation button p,
[data-testid="stSidebar"] .st-key-nav_research button p,
[data-testid="stSidebar"] .st-key-nav_metrics button p,
[data-testid="stSidebar"] .st-key-nav_roadmap button p {margin:0!important;text-align:left!important;font-size:14px!important;font-weight:600!important;line-height:1.2!important;color:#f5e5ba!important;}
[data-testid="stSidebar"] .st-key-nav_home button p::after,
[data-testid="stSidebar"] .st-key-nav_churn button p::after,
[data-testid="stSidebar"] .st-key-nav_reactivation button p::after,
[data-testid="stSidebar"] .st-key-nav_research button p::after,
[data-testid="stSidebar"] .st-key-nav_metrics button p::after,
[data-testid="stSidebar"] .st-key-nav_roadmap button p::after {display:block;color:#aab5a8;font-size:11px;font-weight:400;margin-top:3px;}
[data-testid="stSidebar"] .st-key-nav_home button p::after {content:"Vista general del ciclo VIP";}
[data-testid="stSidebar"] .st-key-nav_churn button p::after {content:"Retención y pérdida de nivel";}
[data-testid="stSidebar"] .st-key-nav_reactivation button p::after {content:"Reingreso y oportunidad futura";}
[data-testid="stSidebar"] .st-key-nav_research button p::after {content:"Perfiles y sensibilidad";}
[data-testid="stSidebar"] .st-key-nav_metrics button p::after {content:"Métricas, límites y evidencia";}
[data-testid="stSidebar"] .st-key-nav_roadmap button p::after {content:"Siguientes pasos del proyecto";}
/* Team navigation: native buttons, styled as compact professional profile cards. */
.st-key-team_footer .stButton>button {background:transparent!important;border:0!important;color:#e7c67f!important;box-shadow:none!important;text-decoration:underline;text-underline-offset:4px;padding:0!important;min-height:30px;justify-content:flex-start!important;font-weight:600!important;}
.st-key-team_footer .stButton>button:hover {color:#fff3d0!important;}
[data-testid="stSidebar"] .st-key-team_card_daniel button,
[data-testid="stSidebar"] .st-key-team_card_julian button {
    display:flex!important;align-items:center!important;justify-content:flex-start!important;gap:10px!important;
    background:transparent!important;border:1px solid transparent!important;border-radius:11px!important;
    padding:10px 8px!important;min-height:66px!important;width:100%!important;
    color:#f5e5ba!important;text-align:left!important;box-shadow:none!important;
}
[data-testid="stSidebar"] .st-key-team_card_daniel button:hover,
[data-testid="stSidebar"] .st-key-team_card_julian button:hover {background:#172820!important;border-color:#74613a!important;}
[data-testid="stSidebar"] .st-key-team_card_daniel button:focus-visible,
[data-testid="stSidebar"] .st-key-team_card_julian button:focus-visible {outline:2px solid #d8b974!important;outline-offset:2px!important;}
[data-testid="stSidebar"] .st-key-team_card_daniel button::before,
[data-testid="stSidebar"] .st-key-team_card_julian button::before {
    display:grid;place-items:center;width:40px;height:40px;flex:0 0 40px;border-radius:50%;
    border:1px solid #74613a;background:#26382b;color:#e7c67f;font-size:13px;font-weight:600;
}
[data-testid="stSidebar"] .st-key-team_card_daniel button::before {content:"DH";}
[data-testid="stSidebar"] .st-key-team_card_julian button::before {content:"JV";}
[data-testid="stSidebar"] .st-key-team_card_daniel button::after,
[data-testid="stSidebar"] .st-key-team_card_julian button::after {content:"›";color:#d8b974;font-size:22px;line-height:1;margin-left:auto;flex:0 0 12px;}
[data-testid="stSidebar"] .st-key-team_card_daniel button [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] .st-key-team_card_julian button [data-testid="stMarkdownContainer"] {flex:1;min-width:0;text-align:left;}
[data-testid="stSidebar"] .st-key-team_card_daniel button p,
[data-testid="stSidebar"] .st-key-team_card_julian button p {margin:0!important;text-align:left!important;font-size:14px!important;font-weight:600!important;line-height:1.35!important;color:#f5e5ba!important;}
[data-testid="stSidebar"] .st-key-team_card_daniel button p::after,
[data-testid="stSidebar"] .st-key-team_card_julian button p::after {display:block;color:#aab5a8;font-size:12px;font-weight:400;margin-top:3px;}
[data-testid="stSidebar"] .st-key-team_card_daniel button p::after {content:"Economista";}
[data-testid="stSidebar"] .st-key-team_card_julian button p::after {content:"Estadístico";}
</style>''',unsafe_allow_html=True)

@st.cache_resource
def bundle_for(kind): return load_bundle(kind)

def tile(label,value,note):
    st.markdown(f'<div class="tile"><small>{html.escape(label)}</small><div class="value">{html.escape(str(value))}</div><p>{html.escape(note)}</p></div>',unsafe_allow_html=True)

def hero(section):
    st.markdown(f'''<div class="hero"><div class="suits">♠ ♥ ♣ ♦</div><div class="eyebrow">IGAMING · PREDICTIVE ANALYTICS</div><h1>VIP Intelligence</h1><p>{html.escape(section)} · Modelos predictivos para el estudio de transiciones del segmento VIP en iGaming.</p></div>''',unsafe_allow_html=True)

# Professional profile pages are separate from the analytical navigation.
TEAM_PROFILES = {
    'daniel': {
        'name': 'Edwin Daniel Holguín Ángel', 'short': 'Daniel Holguín', 'initials': 'DH',
        'profession': 'Economista', 'university': 'Universidad de Antioquia',
        'interests': ['Macroeconomía', 'Econometría', 'Análisis de mercado'],
        'bio': 'Economista de la Universidad de Antioquia, con intereses en el estudio de la economía agregada, la aplicación de métodos econométricos y el análisis de mercados.',
        'role': 'Co-desarrollador de VIP Intelligence'
    },
    'julian': {
        'name': 'Julián Vega Castellón', 'short': 'Julián Vega', 'initials': 'JV',
        'profession': 'Estadístico', 'university': 'Universidad de Antioquia',
        'interests': ['Estadística aplicada', 'Análisis de mercado'],
        'bio': 'Estadístico de la Universidad de Antioquia, con intereses en la aplicación de métodos estadísticos al estudio de datos y al análisis de mercados.',
        'role': 'Co-desarrollador de VIP Intelligence'
    }
}

INTEREST_ICONS = {
    'Macroeconomía': '📈',
    'Econometría': '🧮',
    'Análisis de mercado': '🖼️',
    'Estadística aplicada': '📊',
}

def open_team_profile(person):
    st.session_state['team_profile_active'] = person


def close_team_profile():
    st.session_state.pop('team_profile_active', None)


NAV_ITEMS = [
    ('Inicio · Ciclo de vida', 'nav_home'),
    ('Churn Intelligence', 'nav_churn'),
    ('Reactivation Intelligence', 'nav_reactivation'),
    ('Research Lab · Ciclo VIP', 'nav_research'),
    ('Evaluación y metodología', 'nav_metrics'),
    ('Development Roadmap', 'nav_roadmap'),
]
if 'vip_main_navigation' not in st.session_state:
    st.session_state['vip_main_navigation'] = NAV_ITEMS[0][0]

active_nav_key = dict(NAV_ITEMS).get(st.session_state['vip_main_navigation'], 'nav_home')
st.markdown(f'''<style>
[data-testid="stSidebar"] .st-key-{active_nav_key} button {{background:linear-gradient(90deg,#1a3227 0%,#1a2d24 100%)!important;border-color:#74613a!important;box-shadow:0 0 0 1px rgba(216,185,116,.15) inset!important;}}
[data-testid="stSidebar"] .st-key-{active_nav_key} button::before {{background:#2a3e31!important;}}
</style>''',unsafe_allow_html=True)

with st.sidebar:
    st.markdown('### ♠ VIP INTELLIGENCE')
    st.caption('MACHINE LEARNING / VIP LIFECYCLE')
    for label, nav_key in NAV_ITEMS:
        with st.container(key=nav_key):
            if st.button(label, key=f'btn_{nav_key}', use_container_width=True):
                st.session_state['vip_main_navigation'] = label
                close_team_profile()
    section = st.session_state['vip_main_navigation']
    st.divider()
    st.caption('EQUIPO DE DESARROLLO')
    for person in ('daniel', 'julian'):
        member = TEAM_PROFILES[person]
        with st.container(key=f'team_card_{person}'):
            st.button(member['short'],key=f'team_sidebar_{person}',on_click=open_team_profile,
                      args=(person,),use_container_width=True,
                      help=f"{member['profession']} · Ver perfil profesional")
    st.caption('Economía · Estadística · Ciencia de Datos')
    st.divider()
    st.caption('Demostración técnica · perfiles ficticios. No ingresar datos personales ni información confidencial.')

active_person = st.session_state.get('team_profile_active')
if active_person in TEAM_PROFILES:
    hero('Equipo de desarrollo · Perfil profesional')
else:
    hero(section)

# Presentation groups; all variables required by the serialized estimators are present.
GROUPS={
'churn': [('Perfil VIP y contexto',['nivel_vip','antiguedad_meses','venia_prev','cambio_nivel','mes_mundial','perfilado']),('Actividad del mes',['dias_activos_mes','recencia_fin_mes','tickets_mes','spins_mes','apuesta_dep_mes','apuesta_casino_mes']),('Valor económico y bonos',['deposito_mes','retiro_mes','ggr_dep_mes','ggr_slot_mes','ggr_live_mes','ggr_virt_mes','bono_total_mes','usa_bono_mes']),('Cambios frente al mes anterior',['delta_dias_activos','delta_deposito','delta_ggr'])],
'reactivacion':[('Historial y ausencia VIP',['meses_fuera_vip','ultimo_nivel_vip','nivel_vip_max_historico','meses_vip_historicos','racha_vip_previa','reactivaciones_previas','cambio_nivel_ultimo_mes']),('Actividad del último mes VIP',['dias_activos_ultimo_mes','recencia_fin_ultimo_mes','tickets_ultimo_mes','spins_ultimo_mes','apuesta_total_ultimo_mes']),('Valor económico del último mes VIP',['deposito_ultimo_mes','retiro_ultimo_mes','ggr_general_ultimo_mes','bono_total_ultimo_mes']),('Historial agregado',['deposito_promedio_historico','ggr_promedio_historico','apuesta_promedio_historico','bono_promedio_historico','dias_activos_promedio_historico']),('Cambios antes de la salida',['delta_dias_activos_ultimo_mes','delta_deposito_ultimo_mes','delta_ggr_ultimo_mes'])]}
LABELS = {
    'nivel_vip': 'Nivel VIP',
    'antiguedad_meses': 'Antigüedad VIP (meses)',
    'venia_prev': '¿Era VIP el mes anterior?',
    'cambio_nivel': 'Cambio de nivel VIP',
    'mes_mundial': '¿Mes del Mundial (junio/julio de 2026)?',
    'perfilado': 'Perfil histórico de producto',
    'dias_activos_mes': 'Días activos del mes',
    'recencia_fin_mes': 'Días desde la última actividad al cierre',
    'tickets_mes': 'Tickets del mes',
    'spins_mes': 'Spins del mes',
    'apuesta_dep_mes': 'Apuestas deportivas del mes',
    'apuesta_casino_mes': 'Apuestas de casino del mes',
    'deposito_mes': 'Depósitos del mes',
    'retiro_mes': 'Retiros del mes',
    'ggr_dep_mes': 'GGR deportivas',
    'ggr_slot_mes': 'GGR slots',
    'ggr_live_mes': 'GGR casino en vivo',
    'ggr_virt_mes': 'GGR virtuales',
    'bono_total_mes': 'Bonos del mes',
    'usa_bono_mes': '¿Usó bonos en el mes?',
    'delta_dias_activos': 'Variación de días activos',
    'delta_deposito': 'Variación de depósitos',
    'delta_ggr': 'Variación de GGR',
    'meses_fuera_vip': 'Meses fuera del segmento VIP',
    'ultimo_nivel_vip': 'Último nivel VIP',
    'nivel_vip_max_historico': 'Nivel VIP máximo observado',
    'meses_vip_historicos': 'Meses observados como VIP',
    'racha_vip_previa': 'Racha VIP consecutiva previa',
    'reactivaciones_previas': 'Reingresos VIP previos',
    'cambio_nivel_ultimo_mes': 'Cambio de nivel en el último mes VIP',
    'dias_activos_ultimo_mes': 'Días activos del último mes VIP',
    'recencia_fin_ultimo_mes': 'Recencia al cierre del último mes VIP',
    'tickets_ultimo_mes': 'Tickets del último mes VIP',
    'spins_ultimo_mes': 'Spins del último mes VIP',
    'apuesta_total_ultimo_mes': 'Apuestas del último mes VIP',
    'deposito_ultimo_mes': 'Depósitos del último mes VIP',
    'retiro_ultimo_mes': 'Retiros del último mes VIP',
    'ggr_general_ultimo_mes': 'GGR del último mes VIP',
    'bono_total_ultimo_mes': 'Bonos del último mes VIP',
    'deposito_promedio_historico': 'Promedio histórico de depósitos',
    'ggr_promedio_historico': 'Promedio histórico de GGR',
    'apuesta_promedio_historico': 'Promedio histórico de apuestas',
    'bono_promedio_historico': 'Promedio histórico de bonos',
    'dias_activos_promedio_historico': 'Promedio histórico de días activos',
    'delta_dias_activos_ultimo_mes': 'Variación previa de días activos',
    'delta_deposito_ultimo_mes': 'Variación previa de depósitos',
    'delta_ggr_ultimo_mes': 'Variación previa de GGR',
}

# Display order and captions only; inference retains the original category values.
VIP_FIELDS = {'nivel_vip', 'ultimo_nivel_vip', 'nivel_vip_max_historico'}
VIP_ORDER = ('bronce', 'plata', 'oro', 'diamante')
CATEGORY_LABELS = {
    'bronce': '🥉 Bronce', 'plata': '🥈 Plata', 'oro': '🥇 Oro', 'diamante': '💎 Diamante',
    'si': 'Sí', 'no': 'No', 'ascendio': 'Ascendió', 'descendio': 'Descendió',
    'se_mantuvo': 'Se mantuvo', 'no_aplica': 'No aplica',
}

def display_category(value):
    return CATEGORY_LABELS.get(value, str(value))

def display_options(name, categories):
    options = list(categories)
    if name in VIP_FIELDS:
        # Preserve the estimator's available categories, even if new ones appear.
        return [v for v in VIP_ORDER if v in options] + [v for v in options if v not in VIP_ORDER]
    return options

COUNTS={'antiguedad_meses','dias_activos_mes','recencia_fin_mes','tickets_mes','spins_mes','delta_dias_activos','meses_fuera_vip','meses_vip_historicos','racha_vip_previa','reactivaciones_previas','dias_activos_ultimo_mes','recencia_fin_ultimo_mes','tickets_ultimo_mes','spins_ultimo_mes','delta_dias_activos_ultimo_mes'}

def field(kind,name,bundle,revision,defaults=None):
    d=(DEFAULTS[kind] if defaults is None else defaults)[name]; key=f'{kind}_{revision}_{name}'; label=LABELS.get(name,name.replace('_',' ').capitalize()); cats=get_categories(kind,bundle)
    if name in cats:
        opts = display_options(name, cats[name])
        return st.selectbox(label, opts, index=opts.index(d), key=key, format_func=display_category)
    if name in COUNTS:
        low=-31 if name.startswith('delta_') else (1 if name in {'antiguedad_meses','meses_fuera_vip','meses_vip_historicos','racha_vip_previa','dias_activos_mes','dias_activos_ultimo_mes'} else 0)
        upper=31 if 'dias_activos' in name or 'recencia' in name else (9 if name in {'antiguedad_meses','meses_vip_historicos','racha_vip_previa','reactivaciones_previas'} else (7 if name=='meses_fuera_vip' else None))
        return st.number_input(label,min_value=low,max_value=upper,value=int(d),step=1,key=key)
    low=None if name.startswith(('ggr_','delta_')) else 0.
    upper=31. if name=='dias_activos_promedio_historico' else None
    return st.number_input(label,min_value=low,max_value=upper,value=float(d),step=1.,format='%.2f',key=key)

def score_panel(kind,result):
    s=result['score']*100; u=result['umbral']*100
    positive='Clase 1 · Pérdida de calificación VIP' if kind=='churn' else 'Clase 1 · Reingreso al segmento VIP'
    negative='Clase 0 · No se anticipa pérdida de calificación' if kind=='churn' else 'Clase 0 · No se anticipa reingreso'
    label=positive if result['clase'] else negative
    st.markdown(f'''<div class="score"><div class="eyebrow">Score del modelo</div><div class="big">{s:.2f}%</div><div class="rail"><div class="fill" style="width:{s:.6f}%"></div><div class="marker" style="left:{u:.6f}%"></div></div><div class="range"><span>0%</span><span>Umbral {u:.2f}%</span><span>100%</span></div><div class="class">{html.escape(label)}</div></div>''',unsafe_allow_html=True)
    st.caption('Score de clasificación sin calibración demostrada. No es una probabilidad garantizada. La línea indica el umbral fijado en el desarrollo del modelo.')
    st.info('Resultado para un caso hipotético. No autoriza decisiones automatizadas sobre personas. En una aplicación real se requerirían validación adicional, consentimiento, controles de juego responsable y exclusiones pertinentes.')
    with st.expander('Ver entrada que recibió el modelo'):
        st.dataframe(result['entrada'],hide_index=True)

def reset_synthetic_example(kind):
    # A new form and widget identity discards even unsubmitted browser edits.
    revision_key = f'form_revision_{kind}'
    st.session_state[revision_key] = st.session_state.get(revision_key, 0) + 1
    st.session_state.pop(f'manual_defaults_{kind}', None)
    st.session_state.pop(f'result_{kind}', None)
    st.session_state[f'reset_notice_{kind}'] = True

# Complete fictional scenarios, not sampled from the source dataset.
# Names describe inputs, not a promised or optimized outcome.
def synthetic_profiles(kind):
    d=DEFAULTS[kind]
    if kind=='churn':
        return {
            'A · Actividad sostenida': ( 'Perfil con actividad frecuente y variaciones moderadas.', dict(d,
                nivel_vip='oro', antiguedad_meses=6, dias_activos_mes=25, recencia_fin_mes=1,
                tickets_mes=160, spins_mes=800, apuesta_dep_mes=16000., apuesta_casino_mes=14000.,
                deposito_mes=5500., retiro_mes=2000., ggr_dep_mes=420., ggr_slot_mes=300.,
                ggr_live_mes=0., ggr_virt_mes=0., bono_total_mes=120., delta_dias_activos=2,
                delta_deposito=400., delta_ggr=80., cambio_nivel='se_mantuvo')),
            'B · Actividad intermedia': ('Perfil con menor frecuencia y descenso moderado de actividad.', dict(d)),
            'C · Actividad decreciente': ('Perfil con menor actividad reciente y disminución del valor histórico.', dict(d,
                nivel_vip='bronce', antiguedad_meses=4, dias_activos_mes=6, recencia_fin_mes=18,
                tickets_mes=20, spins_mes=90, apuesta_dep_mes=2600., apuesta_casino_mes=1800.,
                deposito_mes=800., retiro_mes=400., ggr_dep_mes=60., ggr_slot_mes=40.,
                ggr_live_mes=0., ggr_virt_mes=0., bono_total_mes=20., delta_dias_activos=-12,
                delta_deposito=-1800., delta_ggr=-320., cambio_nivel='descendio')),
        }
    return {
        'A · Ausencia prolongada': ('Dos meses VIP consecutivos observados antes de una ausencia de cuatro meses.', dict(d,
            meses_fuera_vip=4, ultimo_nivel_vip='bronce', nivel_vip_max_historico='plata',
            meses_vip_historicos=2, racha_vip_previa=2, reactivaciones_previas=0,
            dias_activos_ultimo_mes=7, recencia_fin_ultimo_mes=15, tickets_ultimo_mes=20,
            spins_ultimo_mes=100, apuesta_total_ultimo_mes=4200., deposito_ultimo_mes=900.,
            retiro_ultimo_mes=350., ggr_general_ultimo_mes=100., bono_total_ultimo_mes=20.,
            cambio_nivel_ultimo_mes='descendio', delta_dias_activos_ultimo_mes=-10,
            delta_deposito_ultimo_mes=-1500., delta_ggr_ultimo_mes=-240.,
            deposito_promedio_historico=1650., ggr_promedio_historico=220.,
            apuesta_promedio_historico=8100., bono_promedio_historico=60., dias_activos_promedio_historico=12.)),
        'B · Historial continuo': ('Tres meses VIP consecutivos, con actividad histórica regular y ausencia de dos meses.', dict(d,
            meses_fuera_vip=2, ultimo_nivel_vip='plata', nivel_vip_max_historico='plata',
            meses_vip_historicos=3, racha_vip_previa=3, reactivaciones_previas=0,
            dias_activos_ultimo_mes=18, recencia_fin_ultimo_mes=5, tickets_ultimo_mes=90,
            spins_ultimo_mes=250, apuesta_total_ultimo_mes=20000., deposito_ultimo_mes=3500.,
            retiro_ultimo_mes=1200., ggr_general_ultimo_mes=400., bono_total_ultimo_mes=100.,
            cambio_nivel_ultimo_mes='se_mantuvo', delta_dias_activos_ultimo_mes=-3,
            delta_deposito_ultimo_mes=-500., delta_ggr_ultimo_mes=-120.,
            deposito_promedio_historico=4200., ggr_promedio_historico=520.,
            apuesta_promedio_historico=24000., bono_promedio_historico=130., dias_activos_promedio_historico=21.)),
        'C · Reingreso previo': ('Cuatro meses VIP observados, un reingreso previo y una ausencia reciente.', dict(d,
            meses_fuera_vip=1, ultimo_nivel_vip='plata', nivel_vip_max_historico='plata',
            meses_vip_historicos=4, racha_vip_previa=2, reactivaciones_previas=1,
            cambio_nivel_ultimo_mes='se_mantuvo')),
    }

def load_manual_profile(kind,profile):
    st.session_state[f'manual_defaults_{kind}']=dict(profile)
    revision_key=f'form_revision_{kind}'
    st.session_state[revision_key]=st.session_state.get(revision_key,0)+1
    st.session_state.pop(f'result_{kind}',None)
    st.session_state[f'mode_{kind}']='Predicción manual'
    st.session_state[f'profile_notice_{kind}']=True

def profile_table(kind,bundle,profiles):
    cats=get_categories(kind,bundle)
    rows=[]
    for group,fields in GROUPS[kind]:
        for f in fields:
            row={'Grupo':group,'Variable':LABELS.get(f,f)}
            for name,values in profiles.items():
                v=values[f]
                row[name]=display_category(v) if f in cats else ('No aplica' if pd.isna(v) else str(v))
            rows.append(row)
    return pd.DataFrame(rows)

def profiles_page(kind,bundle):
    st.subheader('Comparación de perfiles sintéticos')
    st.write('Cada perfil contiene todos los atributos del modelo. Los scores se calculan al abrir esta sección con el estimador entrenado; no son valores prefijados. Los casos son ilustrativos, no representan jugadores reales.')
    profiles=synthetic_profiles(kind)
    results={name:predict(kind,bundle,values) for name,(_,values) in profiles.items()}
    for col,(name,(description,values)) in zip(st.columns(3),profiles.items()):
        with col:
            r=results[name]
            tile(name,f"{r['score']:.2%}",description)
            st.caption(f"Clase {r['clase']} · umbral {r['umbral']:.2%}")
    comparison=pd.DataFrame([{'Perfil':name,'Score (%)':r['score']*100,'Umbral (%)':r['umbral']*100} for name,r in results.items()])
    st.bar_chart(comparison,x='Perfil',y='Score (%)',color='#D8B974',use_container_width=True)
    st.dataframe(comparison.round(2),hide_index=True,use_container_width=True)
    with st.expander('Ver todos los atributos de los tres perfiles'):
        st.dataframe(profile_table(kind,bundle,{name:r['entrada'].iloc[0].to_dict() for name,r in results.items()}),hide_index=True,use_container_width=True)
    name=st.selectbox('Selecciona un perfil para consultar su resultado completo',list(profiles),key=f'profile_detail_{kind}')
    score_panel(kind,results[name])
    st.button('Cargar este perfil en predicción manual',key=f'load_profile_{kind}',on_click=load_manual_profile,args=(kind,profiles[name][1]))
    st.caption('Los escenarios no son una evaluación de desempeño ni una recomendación de intervención. Solo comprueban la inferencia con entradas ficticias.')

# One-at-a-time sensitivity: intentionally restrict to numeric variables that
# can vary independently under simple domain and calendar constraints.
def sensitivity_ranges(kind,base):
    if kind=='churn':
        return {
            'recencia_fin_mes': list(range(0,min(21,31-base['dias_activos_mes'])+1)),
            'dias_activos_mes': list(range(max(1,1+base['delta_dias_activos']),min(31-base['recencia_fin_mes'],31+base['delta_dias_activos'])+1)),
            'deposito_mes': sorted(set([max(0.,base['delta_deposito'],base['deposito_mes']*factor) for factor in (0.5,.75,1.,1.25,1.5)])),
            'ggr_slot_mes': sorted(set([base['ggr_slot_mes']+shift for shift in (-200.,-100.,0.,100.,200.)])),
        }
    max_absence=min(5,8-base['meses_vip_historicos']-base['reactivaciones_previas'])
    # For the historical averages, keep the other observed months nonnegative.
    dep_min=max(0.,base['delta_deposito_ultimo_mes'])
    dep_max=(base['meses_vip_historicos']*base['deposito_promedio_historico']+base['delta_deposito_ultimo_mes'])/2
    days_min=max(1,1+base['delta_dias_activos_ultimo_mes'],math.ceil((base['meses_vip_historicos']*base['dias_activos_promedio_historico']+base['delta_dias_activos_ultimo_mes']-(base['meses_vip_historicos']-2)*31)/2))
    days_max=min(31-base['recencia_fin_ultimo_mes'],31+base['delta_dias_activos_ultimo_mes'],int((base['meses_vip_historicos']*base['dias_activos_promedio_historico']+base['delta_dias_activos_ultimo_mes']-(base['meses_vip_historicos']-2))/2))
    options = {
        'meses_fuera_vip': list(range(1,max_absence+1)),
        'recencia_fin_ultimo_mes': list(range(0,min(21,31-base['dias_activos_ultimo_mes'])+1)),
        'dias_activos_ultimo_mes': list(range(days_min,days_max+1)),
        'deposito_ultimo_mes': sorted(set([min(dep_max,max(dep_min,base['deposito_ultimo_mes']*factor)) for factor in (.5,.75,1.,1.25,1.5)])),
        'ggr_general_ultimo_mes': sorted(set([base['ggr_general_ultimo_mes']+shift for shift in (-200.,-100.,0.,100.,200.)])),
    }
    # A two-month history fixes last-month quantities when both mean and delta are held fixed.
    if base['meses_vip_historicos']==2:
        for f in ('dias_activos_ultimo_mes','deposito_ultimo_mes','ggr_general_ultimo_mes'):
            options.pop(f,None)
    return {f:vals for f,vals in options.items() if len(set(vals+[base[f]]))>1}

def sensitivity_results(kind,bundle,base,variable,values):
    original=predict(kind,bundle,base)
    rows=[]
    for value in sorted(set(values+[base[variable]])):
        result=predict(kind,bundle,dict(base,**{variable:value}))
        before=original['entrada'].iloc[0]; after=result['entrada'].iloc[0]
        # Confirm that preprocessing at inference did not alter other inputs.
        for f in bundle['features']:
            if f!=variable:
                assert (pd.isna(before[f]) and pd.isna(after[f])) or before[f]==after[f]
        rows.append({'Valor':value,'Score (%)':result['score']*100,'Umbral (%)':result['umbral']*100,'Cambio (pp)':(result['score']-original['score'])*100,'Clase':result['clase']})
    return original,pd.DataFrame(rows)

def sensitivity_page(kind,bundle):
    st.subheader('Análisis de sensibilidad · una variable a la vez')
    st.write('Selecciona un perfil ficticio y una variable. El modelo vuelve a calcular el score para cada valor del eje horizontal; todas las demás entradas permanecen constantes. Es una exploración local del modelo, no una estimación causal.')
    profiles=synthetic_profiles(kind)
    name=st.selectbox('Perfil sintético de referencia',list(profiles),key=f'sensitivity_profile_{kind}')
    description,base=profiles[name]
    st.caption(description)
    ranges=sensitivity_ranges(kind,base)
    variable=st.selectbox('Variable que se modifica',list(ranges),format_func=lambda f:LABELS[f],key=f'sensitivity_variable_{kind}_{name}')
    original,table=sensitivity_results(kind,bundle,base,variable,ranges[variable])
    a,b,c=st.columns(3)
    with a: tile('Score base',f"{original['score']:.2%}",'Perfil de referencia')
    with b: tile('Atributos fijos',len(bundle['features'])-1,'Sin modificación')
    with c: tile('Umbral',f"{original['umbral']:.2%}",'Umbral original')
    st.caption(f"Valor base: {base[variable]:g} · Variable analizada: {LABELS[variable]}")
    # Plot with an explicit linear numeric axis, not equally spaced categories.
    import altair as alt
    long=table.melt(id_vars=['Valor'],value_vars=['Score (%)','Umbral (%)'],var_name='Serie',value_name='Porcentaje')
    plot=alt.Chart(long).mark_line(point=True).encode(
        x=alt.X('Valor:Q',title=LABELS[variable],scale=alt.Scale(zero=False)),
        y=alt.Y('Porcentaje:Q',title='Score (%)',scale=alt.Scale(domain=[0,100])),
        color=alt.Color('Serie:N',scale=alt.Scale(domain=['Score (%)','Umbral (%)'],range=['#D8B974','#CF806B'])),
        tooltip=['Serie:N',alt.Tooltip('Valor:Q'),alt.Tooltip('Porcentaje:Q',format='.2f')]
    ).properties(height=320)
    st.altair_chart(plot,use_container_width=True)
    st.dataframe(table.round(3),hide_index=True,use_container_width=True)
    with st.expander('Ver atributos fijos del perfil base'):
        st.dataframe(profile_table(kind,bundle,{'Perfil base':original['entrada'].iloc[0].to_dict()}),hide_index=True,use_container_width=True)
    st.info('Los rangos son escenarios ficticios restringidos mediante controles simples de coherencia; no garantizan que todas las combinaciones estén representadas en entrenamiento. Las diferencias son cambios en la salida del estimador, no efectos reales ni probabilidades calibradas.')

def page_model(kind):
    bundle=bundle_for(kind)
    is_churn=kind=='churn'
    st.markdown('#### '+('♠ Análisis 01 · Pérdida de calificación VIP' if is_churn else '♦ Análisis 02 · Reingreso al segmento VIP'))
    st.caption('Mes de referencia M cerrado → resultado en M+1. No se predice abandono total ni retorno al juego.')
    c1,c2,c3=st.columns(3)
    with c1: tile('Algoritmo','Votación soft' if is_churn else 'Regresión logística','Ensamble de tres estimadores' if is_churn else 'Clasificador lineal')
    with c2: tile('Atributos',len(bundle['features']),'Variables de entrada')
    with c3: tile('Umbral de decisión',f"{bundle['umbral']*100:.2f}%",'Determinado con datos de desarrollo')
    mode=st.radio('Modalidad de análisis',['Predicción manual','Perfiles sintéticos','Análisis de sensibilidad'],horizontal=True,key=f'mode_{kind}')
    if mode=='Predicción manual':
        if st.session_state.pop(f'profile_notice_{kind}',False): st.success('Perfil completo cargado. Puedes modificar sus atributos y calcular el score.')
        manual_page(kind,bundle)
    elif mode=='Perfiles sintéticos': profiles_page(kind,bundle)
    else: sensitivity_page(kind,bundle)

def manual_page(kind,bundle):
    is_churn=kind=='churn'
    st.button('Restablecer ejemplo sintético', key=f'reset_{kind}',
              on_click=reset_synthetic_example, args=(kind,))
    revision = st.session_state.get(f'form_revision_{kind}', 0)
    if st.session_state.pop(f'reset_notice_{kind}', False):
        st.success('Ejemplo sintético restablecido. Pulsa Calcular score del modelo para generar un nuevo resultado.')
    defaults = st.session_state.get(f'manual_defaults_{kind}', DEFAULTS[kind])
    st.caption('El cálculo usa todos los atributos, incluso los grupos cerrados. Los valores son ficticios; los importes usan las unidades de la fuente. Los campos se mantienen en su escala original: el modelo aplica sus propias transformaciones.')
    if is_churn: st.caption('Si no venía del mes anterior, se asigna cambio de nivel no aplicable y los deltas se codifican en cero según el preprocesamiento del modelo.')
    if is_churn: st.caption('El origen temporal de perfilado está pendiente de verificación; resultado exclusivamente demostrativo.')
    else: st.caption('Si la racha previa es de un mes, los tres deltas se tratan como faltantes estructurales. No se simula actividad durante la ausencia.')
    with st.form(f'form_{kind}_{revision}'):
        values={}
        for i,(name,fields) in enumerate(GROUPS[kind]):
            with st.expander(name,expanded=i==0):
                cols=st.columns(3)
                for j,f in enumerate(fields):
                    with cols[j%3]: values[f]=field(kind,f,bundle,revision,defaults)
        submitted=st.form_submit_button('Calcular score del modelo',use_container_width=True)
    if submitted:
        st.session_state[f'manual_defaults_{kind}']=dict(values)
        try: st.session_state[f'result_{kind}']=predict(kind,bundle,values)
        except ValueError as e: st.session_state.pop(f'result_{kind}',None); st.error(str(e))
        except Exception as e: st.session_state.pop(f'result_{kind}',None); st.error(f'No se pudo ejecutar el modelo: {type(e).__name__}. Revisa las dependencias y la entrada.')
    if f'result_{kind}' in st.session_state:
        result=st.session_state[f'result_{kind}']
        if not is_churn and result['entrada']['meses_fuera_vip'].iloc[0] >= 6:
            st.warning('Duración de ausencia fuera del rango observado en entrenamiento. Este score es una extrapolación y no está validado para ese caso.')
        score_panel(kind,result)
    else: st.caption('Completa los parámetros o utiliza el ejemplo ficticio precargado y pulsa Calcular score del modelo.')


def ranking_page():
    st.markdown('### Reactivación VIP · evaluación por ranking')
    st.caption('Agosto de 2026 · evaluación retrospectiva · resultados agregados del notebook')
    n, positives = 2323, 214
    baseline = positives / n
    evidence = {5: (117, 33), 10: (233, 58), 20: (465, 85), 30: (697, 116), 50: (1162, 155), 100: (2323, 214)}
    st.write('Explora cómo se concentran los reingresos VIP observados al ordenar retrospectivamente los registros por su score. No se simula una intervención ni se generan recomendaciones individuales.')
    pct = st.select_slider('Fracción superior del ranking histórico (%)', options=list(evidence), value=10, key='react_ranking_pct')
    k, tp = evidence[pct]
    precision, recall = tp / k, tp / positives
    expected = k * baseline
    a,b,c,d = st.columns(4)
    with a: tile('Lift observado', f'{precision / baseline:.2f}x', 'Respecto de la tasa general')
    with b: tile('Precisión@K', f'{precision:.1%}', f'{tp} reingresos de {k} registros')
    with c: tile('Recall@K', f'{recall:.1%}', f'{tp} de {positives} eventos observados')
    with d: tile('Referencia aleatoria', f'{expected:.1f}', 'Eventos esperados en igual tamaño de muestra')
    st.markdown('**Tasa de reingreso observada**')
    for label, value, color in [('Ranking histórico',precision,'#d8b974'),('Referencia aleatoria',baseline,'#659687')]:
        st.markdown(f'<div style="margin:10px 0 4px;display:flex;justify-content:space-between"><span>{label}</span><strong>{value:.2%}</strong></div><div style="height:14px;background:#29382f;border-radius:8px;overflow:hidden"><div style="width:{value*100:.3f}%;height:100%;background:{color}"></div></div>',unsafe_allow_html=True)
    st.caption('Barras sobre escala 0–100 %. La referencia es la prevalencia del evento en agosto (9,21 %).')
    with st.expander('Ver tabla completa de evaluación retrospectiva'):
        st.dataframe([{'Fracción superior':f'{f}%', 'Registros':k0, 'Reingresos':t0, 'Precisión':f'{t0/k0:.2%}', 'Recall':f'{t0/positives:.2%}', 'Lift':f'{(t0/k0)/baseline:.2f}x'} for f,(k0,t0) in evidence.items()],hide_index=True,use_container_width=True)
    st.info('AP = 0,193 frente a prevalencia 0,0921 (2,09 veces). Brier = 0,0864 frente a referencia constante 0,0842: la calibración no está demostrada. El ranking describe asociación retrospectiva; no prueba causalidad, incremento de ingresos ni utilidad prospectiva.')
    st.caption('Fuente: resultados agregados de la evaluación de agosto. No se incluyen registros, scores individuales ni identificadores.')

def research_page():
    st.subheader('Research Lab · Ciclo VIP')
    st.write('Dos líneas de investigación complementarias, con la misma importancia dentro del ciclo de vida. La evidencia actual y las oportunidades de mejora se interpretan por separado.')
    tc,tr=st.tabs(['♠ Churn Intelligence','♦ Reactivation Intelligence'])
    with tc:
        st.markdown('''<div class="research"><div class="eyebrow">EVIDENCIA ACTUAL</div><h3>♠ Pérdida de calificación VIP</h3><p>La fuente registra directamente el comportamiento durante los meses VIP. Esta mayor disponibilidad de información y una clase positiva más frecuente favorecen el estudio de la pérdida de calificación.</p></div>''',unsafe_allow_html=True)
        c=json.loads((ROOT/'metricas_churn.json').read_text())
        a,b,d=st.columns(3)
        with a: tile('Recall',f"{c['recall']:.1%}",'Cobertura de pérdidas observadas')
        with b: tile('ROC-AUC',f"{c['roc_auc']:.3f}",'Discriminación retrospectiva')
        with d: tile('Prevalencia','41,07 %','Septiembre · 414 de 1.008 registros')
        st.write('Churn presenta mayor capacidad de discriminación y clasificación con los datos actuales. Esto no demuestra que una intervención evite una pérdida de calificación. Persisten falsos positivos, falta verificar la disponibilidad temporal de perfilado y se requiere validación prospectiva.')
        st.subheader('Próximas líneas de estudio')
        st.write('Ampliar el horizonte temporal, estudiar estabilidad por nivel VIP, verificar la procedencia temporal de los atributos y evaluar calibración y cambios en la distribución de los datos.')
    with tr:
        st.markdown('''<div class="research"><div class="eyebrow">POTENCIAL DE INVESTIGACIÓN</div><h3>♦ Reingreso al segmento VIP</h3><p>El retorno es menos frecuente y durante la ausencia no se observa el comportamiento del usuario. La señal de ordenamiento encontrada permite plantear nuevas preguntas y ampliar la investigación, sin afirmar que el modelo esté listo para producción.</p></div>''',unsafe_allow_html=True)
        a,b,c,d=st.columns(4)
        with a: tile('Lift · Top 5 %','3,06x','Concentración retrospectiva')
        with b: tile('AP frente a referencia','2,09x','0,193 frente a 0,0921')
        with c: tile('Base analítica','9.331','Observaciones usuario–mes')
        with d: tile('Experimentación','15','Configuraciones evaluadas')
        st.write('En agosto, el reingreso tuvo una prevalencia de 9,21 %. El 5 % superior contiene 33 eventos de 117 registros (28,21 %), frente a 10,8 esperados al azar. Se muestran todas las fracciones, no solo la de mayor lift.')
        ranking_page()
        st.subheader('Qué sabemos y qué falta demostrar')
        st.write('El modelo presenta una señal retrospectiva de ordenamiento, pero su precisión individual es 17,32 %, su recall 43,46 % y su ROC-AUC 0,675. El Brier de 0,0864 no mejora la referencia constante de 0,0842. El ranking no implica calibración ni eficacia de intervenciones.')
        st.subheader('Próximas líneas de estudio')
        st.write('Ampliar el histórico, evaluar nuevas fuentes autorizadas, estudiar el tiempo hasta reingreso con métodos de supervivencia, comprobar disponibilidad temporal de variables y validar en meses nuevos. El mayor margen de investigación se relaciona con las limitaciones de información y la menor frecuencia del evento.')
    st.caption('Toda ampliación requiere controles de privacidad y juego responsable. Las líneas futuras no representan resultados ya demostrados.')


def metrics_page():
    c=json.loads((ROOT/'metricas_churn.json').read_text()); r=json.loads((ROOT/'metricas_reactivacion.json').read_text())['test_retrospectivo']
    st.subheader('Evaluación de dos transiciones complementarias')
    st.write('Ambos modelos tienen la misma importancia en el proyecto. Churn muestra mayor discriminación con los datos disponibles; reingreso estudia un evento menos frecuente con menor observabilidad durante la ausencia. La evaluación conserva todas las métricas y considera la prevalencia de cada población.')
    tc,tr=st.tabs(['♠ Churn Intelligence','♦ Reactivation Intelligence'])
    with tc:
        st.caption('Septiembre · reproducción compatible · evaluación retrospectiva · prevalencia 41,07 %')
        a,b,d=st.columns(3)
        with a: tile('Recall',f"{c['recall']:.1%}",'Cobertura de pérdidas VIP observadas')
        with b: tile('ROC-AUC',f"{c['roc_auc']:.3f}",'Discriminación')
        with d: tile('Average Precision',f"{c['ap']:.3f}",'Referencia aleatoria: 0,4107')
        a,b=st.columns(2)
        with a: st.metric('Precisión',f"{c['precision']:.1%}")
        with b: st.metric('F1',f"{c['f1']:.3f}")
        st.write('La cobertura es alta en esta evaluación, pero existen falsos positivos y falta confirmar la disponibilidad temporal de perfilado.')
    with tr:
        st.caption('Agosto · evaluación retrospectiva · prevalencia 9,21 %')
        a,b,d=st.columns(3)
        with a: tile('Lift · Top 10 %','2,70x','Concentración de reingresos observados')
        with b: tile('ROC-AUC',f"{r['ROC-AUC']:.3f}",'Discriminación')
        with d: tile('Average Precision',f"{r['AP']:.3f}",'Referencia aleatoria: 0,0921')
        a,b,d=st.columns(3)
        with a: st.metric('Precisión',f"{r['Precisión']:.1%}")
        with b: st.metric('Recall',f"{r['Recall']:.1%}")
        with d: st.metric('F1',f"{r['F1']:.3f}")
        st.write('El ranking complementa la clasificación binaria, no la reemplaza. La calibración no está demostrada. Research Lab · Ciclo VIP desarrolla la evidencia completa.')
    st.divider()
    st.subheader('Alcance metodológico')
    st.write('Churn: votación soft con LR, MLP y Gradient Boosting; SMOTENC durante entrenamiento. Reactivación: regresión logística sin sobremuestreo; antiguos VIP ausentes en M. Ambos estudian calificación VIP en M+1, no abandono o retorno al juego.')
    st.write('Churn se reprodujo con hiperparámetros y umbral originales en scikit-learn 1.8.0. Las métricas corresponden a entrenamiento enero–agosto y evaluación septiembre; el artefacto desplegado se ajustó con enero–septiembre y no conserva el remuestreador ajustado. Reactivación conserva el modelo del notebook: entrenamiento febrero–junio, validación julio y evaluación retrospectiva agosto.')
    st.warning('Limitaciones: origen temporal de perfilado pendiente en churn; agosto ya consultado; calibración no demostrada; histórico limitado; poca evidencia en Oro y Diamante. No es un sistema operativo validado.')
    st.markdown('**Privacidad y juego responsable:** perfiles ficticios, sin registros individuales ni recomendaciones de contacto o incentivos. Los artefactos requieren autorización del titular de los datos.')


def roadmap_page():
    st.subheader('Development Roadmap')
    st.caption('Propuestas de evolución, no compromisos ni funcionalidades productivas.')
    stages=[('V1.0 · Fundamentos predictivos','Implementado en código','Dos análisis supervisados, validación temporal y prototipo web.'),('V1.1 · Experimentación y explicabilidad','Implementado en código','Predicción manual, perfiles sintéticos, sensibilidad local y ranking histórico.'),('V2.0 · Evolución de ambos modelos','Investigación propuesta','Churn: verificar atributos temporales, estabilidad y calibración. Reingreso: ampliar el histórico y la información autorizada disponible durante la ausencia; estudiar la señal de retorno.'),('V2.1 · Time-to-event Analytics','Investigación propuesta','Analizar tiempo hasta pérdida o reingreso VIP mediante métodos de supervivencia y censura.'),('V3.0 · Model Reliability','Investigación propuesta','Validación prospectiva, calibración, drift, privacidad y juego responsable.')]
    for title,status,desc in stages:
        st.markdown(f'<div class="tile"><small>{html.escape(status)}</small><div class="value" style="font-size:23px">{html.escape(title)}</div><p>{html.escape(desc)}</p></div>',unsafe_allow_html=True)
    st.caption('La agenda de investigación es futura; el módulo informativo está incluido en esta versión. La última interfaz requiere verificación en Streamlit Cloud.')


def home_page():
    st.subheader('VIP Lifecycle Intelligence')
    st.write('Dos modelos, una visión integral: comprender tanto la pérdida de calificación VIP como el reingreso al segmento. Ambas transiciones tienen la misma importancia en la plataforma, aunque presentan desafíos predictivos diferentes.')
    st.markdown('''<div class="life"><div class="node"><strong>♠ VIP activo</strong><p>Calificación observada en M</p></div><div class="arrow">→<small>Churn</small></div><div class="node"><strong>◇ Fuera del segmento</strong><p>Ausencia de calificación VIP</p></div><div class="arrow">→<small>Reactivación</small></div><div class="node"><strong>♦ Reingreso VIP</strong><p>Recalificación observada</p></div></div>''',unsafe_allow_html=True)
    st.caption('Esquema conceptual de estados observables. Estar fuera del segmento no significa haber dejado de jugar.')
    a,b=st.columns(2)
    with a:
        tile('♠ Línea analítica 01','Churn Intelligence','Votación soft · pérdida de calificación VIP')
        st.markdown('**Mayor capacidad predictiva actual**')
        st.write('La actividad del mes VIP es observable: frecuencia, recencia, variables económicas y evolución histórica. Esto favorece el aprendizaje de patrones asociados a la pérdida de calificación.')
        tile('Recall · evaluación retrospectiva','79,7 %','Cobertura de pérdidas VIP observadas')
        st.caption('Prevalencia: 41,07 % · 414 eventos de 1.008 registros evaluados.')
    with b:
        tile('♦ Línea analítica 02','Reactivation Intelligence','Regresión logística · reingreso VIP')
        st.markdown('**Mayor margen de investigación futura**')
        st.write('El retorno es menos frecuente y la actividad durante la ausencia no es observable. Aun con esta restricción, el modelo encuentra una señal de ordenamiento que merece mayor investigación.')
        tile('Lift · Top 5 % retrospectivo','3,06x','Concentración de reingresos frente a la referencia')
        st.caption('Prevalencia: 9,21 % · 214 eventos de 2.323 registros evaluados.')
    st.subheader('Dos desafíos complementarios')
    st.write('Anticipar la pérdida de calificación mientras el usuario aún pertenece al segmento es conceptualmente distinto de estudiar su retorno tras una ausencia. La hipótesis de que conservar una relación existente es más sencillo que recuperarla es razonable como contexto de negocio, pero este estudio no mide la eficacia ni el costo de intervenciones. Los resultados muestran diferencias de observabilidad, prevalencia y desempeño predictivo; no una comparación causal de retención y reingreso.')
    st.subheader('Evolución del ciclo VIP')
    a,b=st.columns(2)
    with a: tile('Churn · continuidad','Validación y fiabilidad','Verificar atributos temporales, estabilidad, calibración y generalización.')
    with b: tile('Reingreso · continuidad','Ampliación del conocimiento','Profundizar en el histórico y la ausencia, con fuentes autorizadas y validación futura.')
    st.write('Explora ambos modelos mediante predicción manual, perfiles ficticios completos y sensibilidad. Research Lab reúne las evidencias y las líneas futuras; Evaluación y metodología conserva todas las métricas y limitaciones.')
    st.info('Prototipo de investigación, no plataforma de apuestas. Scores no calibrados; no ingresar información confidencial ni utilizar para decisiones sobre personas.')

def team_profile_page(person):
    profile = TEAM_PROFILES[person]
    st.button('← Volver a la plataforma',key='team_back',on_click=close_team_profile)
    st.markdown(f'''<div class="profile-head">
      <div class="profile-initials">{html.escape(profile['initials'])}</div>
      <div><div class="eyebrow">EQUIPO DE DESARROLLO · PERFIL PROFESIONAL</div>
      <h2>{html.escape(profile['name'])}</h2>
      <p>{html.escape(profile['profession'])} · {html.escape(profile['university'])}</p></div>
      </div>''',unsafe_allow_html=True)
    a,b=st.columns([3,2])
    with a:
        st.subheader('Perfil profesional')
        st.write(profile['bio'])
        st.subheader('Participación en VIP Intelligence')
        tile('Equipo de desarrollo',profile['role'],'Iniciativa colaborativa que integra economía, estadística y ciencia de datos para estudiar el ciclo de vida VIP mediante aprendizaje automático.')
    with b:
        st.subheader('Formación')
        tile('Título profesional',profile['profession'],profile['university'])
        st.subheader('Áreas de interés')
        for interest in profile['interests']:
            icon = INTEREST_ICONS.get(interest, '•')
            st.markdown(f'<div class="profile-interest"><span class="icon">{html.escape(icon)}</span><span class="text">{html.escape(interest)}</span></div>',unsafe_allow_html=True)
    st.divider()
    st.caption('VIP Intelligence integra perspectivas de economía, estadística y ciencia de datos para estudiar el ciclo de vida del segmento VIP.')
    other = 'julian' if person == 'daniel' else 'daniel'
    st.button('Ver perfil de '+TEAM_PROFILES[other]['short'],key='team_other',on_click=open_team_profile,args=(other,))


if active_person in TEAM_PROFILES: team_profile_page(active_person)
elif section=='Inicio · Ciclo de vida': home_page()
elif section=='Churn Intelligence': page_model('churn')
elif section=='Reactivation Intelligence': page_model('reactivacion')
elif section=='Research Lab · Ciclo VIP': research_page()
elif section=='Development Roadmap': roadmap_page()
else: metrics_page()
with st.container(key='team_footer'):
    st.markdown('<div class="footer">VIP INTELLIGENCE · EQUIPO DE DESARROLLO · MACHINE LEARNING</div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        st.button('Daniel Holguín',key='team_footer_daniel',on_click=open_team_profile,args=('daniel',))
    with b:
        st.button('Julián Vega',key='team_footer_julian',on_click=open_team_profile,args=('julian',))
