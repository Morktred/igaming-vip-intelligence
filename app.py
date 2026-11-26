import json
from pathlib import Path
import html
import streamlit as st
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
.footer {color:#aab5a8;font-size:11px;border-top:1px solid #3c493e;margin-top:32px;padding-top:14px;letter-spacing:.4px;}
</style>''',unsafe_allow_html=True)

@st.cache_resource
def bundle_for(kind): return load_bundle(kind)

def tile(label,value,note):
    st.markdown(f'<div class="tile"><small>{html.escape(label)}</small><div class="value">{html.escape(str(value))}</div><p>{html.escape(note)}</p></div>',unsafe_allow_html=True)

def hero(section):
    st.markdown(f'''<div class="hero"><div class="suits">♠ ♥ ♣ ♦</div><div class="eyebrow">IGAMING · PREDICTIVE ANALYTICS</div><h1>VIP Intelligence</h1><p>{html.escape(section)} · Modelos predictivos para el estudio de transiciones del segmento VIP en iGaming.</p></div>''',unsafe_allow_html=True)

with st.sidebar:
    st.markdown('### ♠ VIP INTELLIGENCE')
    st.caption('MACHINE LEARNING / VIP ANALYTICS')
    section=st.radio('Navegación',['Inicio','Churn VIP','Reactivación VIP','Ranking de reactivación','Metodología y métricas'],label_visibility='collapsed')
    st.divider()
    st.caption('EQUIPO DE DESARROLLO')
    st.markdown('**Daniel Holguin** · Reactivación VIP')
    st.markdown('**Julián Vega** · Churn VIP')
    st.divider()
    st.caption('Demostración técnica · perfiles ficticios. No ingresar datos personales ni información confidencial.')

hero(section)

# Presentation groups; all variables required by the serialized estimators are present.
GROUPS={
'churn': [('Perfil VIP y contexto',['nivel_vip','antiguedad_meses','venia_prev','cambio_nivel','mes_mundial','perfilado']),('Actividad del mes',['dias_activos_mes','recencia_fin_mes','tickets_mes','spins_mes','apuesta_dep_mes','apuesta_casino_mes']),('Valor económico y bonos',['deposito_mes','retiro_mes','ggr_dep_mes','ggr_slot_mes','ggr_live_mes','ggr_virt_mes','bono_total_mes','usa_bono_mes']),('Cambios frente al mes anterior',['delta_dias_activos','delta_deposito','delta_ggr'])],
'reactivacion':[('Historial y ausencia VIP',['meses_fuera_vip','ultimo_nivel_vip','nivel_vip_max_historico','meses_vip_historicos','racha_vip_previa','reactivaciones_previas','cambio_nivel_ultimo_mes']),('Actividad del último mes VIP',['dias_activos_ultimo_mes','recencia_fin_ultimo_mes','tickets_ultimo_mes','spins_ultimo_mes','apuesta_total_ultimo_mes']),('Valor económico del último mes VIP',['deposito_ultimo_mes','retiro_ultimo_mes','ggr_general_ultimo_mes','bono_total_ultimo_mes']),('Historial agregado',['deposito_promedio_historico','ggr_promedio_historico','apuesta_promedio_historico','bono_promedio_historico','dias_activos_promedio_historico']),('Cambios antes de la salida',['delta_dias_activos_ultimo_mes','delta_deposito_ultimo_mes','delta_ggr_ultimo_mes'])]}
LABELS={'venia_prev':'¿Era VIP el mes anterior?','mes_mundial':'¿Mes de Mundial (junio/julio 2026)?','perfilado':'Perfil histórico de producto','usa_bono_mes':'¿Uso de bono?','recencia_fin_mes':'Días desde la última actividad al cierre','recencia_fin_ultimo_mes':'Recencia al cierre del último mes VIP','antiguedad_meses':'Antigüedad VIP (meses)','nivel_vip_max_historico':'Nivel VIP máximo observado','meses_vip_historicos':'Meses observados como VIP','racha_vip_previa':'Racha VIP consecutiva previa','reactivaciones_previas':'Reingresos VIP previos','cambio_nivel_ultimo_mes':'Cambio de nivel en el último mes VIP','ggr_dep_mes':'GGR deportivas','ggr_slot_mes':'GGR slots','ggr_live_mes':'GGR casino en vivo','ggr_virt_mes':'GGR virtuales','apuesta_dep_mes':'Apuesta deportivas','apuesta_casino_mes':'Apuesta casino'}
COUNTS={'antiguedad_meses','dias_activos_mes','recencia_fin_mes','tickets_mes','spins_mes','delta_dias_activos','meses_fuera_vip','meses_vip_historicos','racha_vip_previa','reactivaciones_previas','dias_activos_ultimo_mes','recencia_fin_ultimo_mes','tickets_ultimo_mes','spins_ultimo_mes','delta_dias_activos_ultimo_mes'}

def field(kind,name,bundle):
    d=DEFAULTS[kind][name]; key=f'{kind}_{name}'; label=LABELS.get(name,name.replace('_',' ').capitalize()); cats=get_categories(kind,bundle)
    if name in cats:
        opts=cats[name]; return st.selectbox(label,opts,index=opts.index(d),key=key)
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

def page_model(kind):
    bundle=bundle_for(kind)
    is_churn=kind=='churn'
    st.markdown('#### '+('♠ Análisis 01 · Pérdida de calificación VIP' if is_churn else '♦ Análisis 02 · Reingreso al segmento VIP'))
    st.caption('Mes de referencia M cerrado → resultado en M+1. No se predice abandono total ni retorno al juego.')
    c1,c2,c3=st.columns(3)
    with c1: tile('Algoritmo','Votación soft' if is_churn else 'Regresión logística','Ensamble de tres estimadores' if is_churn else 'Clasificador lineal')
    with c2: tile('Atributos',len(bundle['features']),'Entrada sintética editable')
    with c3: tile('Umbral de decisión',f"{bundle['umbral']*100:.2f}%",'Determinado con datos de desarrollo')
    if st.button('Restablecer ejemplo sintético',key=f'reset_{kind}'):
        for f in bundle['features']: st.session_state.pop(f'{kind}_{f}',None)
        st.session_state.pop(f'result_{kind}',None); st.rerun()
    st.caption('Los valores son ficticios; los importes usan las unidades de la fuente. Los campos se mantienen en su escala original: el modelo aplica sus propias transformaciones.')
    if is_churn: st.caption('Si no venía del mes anterior, se asigna cambio de nivel no aplicable y los deltas se codifican en cero según el preprocesamiento del modelo.')
    if is_churn: st.caption('El origen temporal de perfilado está pendiente de verificación; resultado exclusivamente demostrativo.')
    else: st.caption('Si la racha previa es de un mes, los tres deltas se tratan como faltantes estructurales. No se simula actividad durante la ausencia.')
    with st.form(f'form_{kind}'):
        values={}
        for i,(name,fields) in enumerate(GROUPS[kind]):
            with st.expander(name,expanded=i==0):
                cols=st.columns(3)
                for j,f in enumerate(fields):
                    with cols[j%3]: values[f]=field(kind,f,bundle)
        submitted=st.form_submit_button('Calcular score del modelo',use_container_width=True)
    if submitted:
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

def metrics_page():
    c=json.loads((ROOT/'metricas_churn.json').read_text()); r=json.loads((ROOT/'metricas_reactivacion.json').read_text())['test_retrospectivo']
    st.markdown('#### Evidencia de evaluación')
    left,right=st.columns(2)
    for col,title,roc,ap,prec,rec,f1,note in [(left,'Churn VIP',c['roc_auc'],c['ap'],c['precision'],c['recall'],c['f1'],'Septiembre · reproducción compatible; evaluación retrospectiva'),(right,'Reactivación VIP',r['ROC-AUC'],r['AP'],r['Precisión'],r['Recall'],r['F1'],'Agosto · evaluación retrospectiva')]:
        with col:
            st.subheader(title); st.caption(note)
            a,b=st.columns(2)
            with a: tile('ROC-AUC',f'{roc:.3f}','Discriminación')
            with b: tile('Average Precision',f'{ap:.3f}','Resumen precisión-recall')
            a,b,d=st.columns(3)
            with a: st.metric('Precisión',f'{prec:.1%}')
            with b: st.metric('Recall',f'{rec:.1%}')
            with d: st.metric('F1',f'{f1:.3f}')
    st.divider()
    ranking_page()
    st.divider()
    st.markdown('#### Alcance metodológico')
    st.write('Churn: clasificación a nivel usuario–mes. Votación soft con LR, MLP y Gradient Boosting; SMOTENC durante el entrenamiento. Reactivación: regresión logística sin sobremuestreo; la población son antiguos VIP ausentes en M. Los modelos no comparten población ni etiqueta.')
    st.write('El modelo de churn se reentrenó con los hiperparámetros y el umbral originales en scikit-learn 1.8.0 para compatibilidad con el modelo de reactivación. El artefacto de inferencia no conserva el remuestreador SMOTENC ajustado. Las métricas de churn corresponden a la reproducción con enero–agosto y evaluación en septiembre; la versión de despliegue se ajustó con enero–septiembre.')
    st.write('Reactivación se conserva como se exportó en su notebook: entrenamiento febrero–junio, validación julio, prueba retrospectiva agosto. Las métricas no son directamente comparables porque las prevalencias difieren.')
    st.warning('Limitaciones: origen temporal de perfilado pendiente de confirmar en churn; evaluación de agosto ya consultada; calibración no demostrada; histórico limitado; poca evidencia en niveles Oro y Diamante. Demostración técnica, no sistema operativo validado.')
    st.markdown('**Privacidad y juego responsable:** no contiene registros de jugadores ni identificadores; no ofrece apuestas, incentivos personalizados ni recomendaciones de contacto. Los modelos requieren autorización del titular de los datos antes de publicarse.')

if section=='Inicio':
    a,b=st.columns(2)
    with a: tile('♠ Análisis 01','Churn VIP','Estima pérdida de calificación VIP al mes siguiente.')
    with b: tile('♦ Análisis 02','Reactivación VIP','Estudia el reingreso al segmento VIP y su ordenamiento retrospectivo.')
    st.markdown('#### Dos poblaciones, dos preguntas analíticas')
    st.write('Elige un análisis en el menú lateral. Cada módulo presenta los atributos del modelo y un ejemplo sintético editable; calcula el score con el estimador entrenado. La sección de ranking permite explorar la concentración retrospectiva de reingresos. La metodología conserva las métricas completas y sus limitaciones.')
    st.markdown('#### Ciclo del análisis')
    st.markdown('**Histórico VIP**  →  **Preparación usuario–mes**  →  **Modelo de clasificación**  →  **Score y umbral**  →  **Evaluación del modelo**')
    st.info('Este prototipo no es una plataforma de apuestas y no contiene datos de usuarios reales.')
elif section=='Churn VIP': page_model('churn')
elif section=='Reactivación VIP': page_model('reactivacion')
elif section=='Ranking de reactivación': ranking_page()
else: metrics_page()
st.markdown('<div class="footer">VIP INTELLIGENCE · DANIEL HOLGUIN &amp; JULIÁN VEGA · MACHINE LEARNING</div>',unsafe_allow_html=True)
