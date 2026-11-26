# Responsables de análisis: Julián Vega Castellón (churn) y Edwin Daniel Holguín Ángel (reactivación).
# Coordinación del despliegue: Daniel Holguin. Integración con asistencia de IA.
"""Inference on synthetic examples. No dataset or identifiers needed."""
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
FILES = {'churn':'modelo_churn_vip.pkl','reactivacion':'modelo_reactivacion_vip.pkl'}
# Examples are invented, not selected from the source records. Monetary inputs use source units.
DEFAULTS = {
'churn': {'antiguedad_meses':3,'dias_activos_mes':18,'recencia_fin_mes':5,'delta_dias_activos':-3,
'deposito_mes':3500.,'retiro_mes':1200.,'tickets_mes':90,'apuesta_dep_mes':11500.,'apuesta_casino_mes':8500.,'spins_mes':250,'ggr_dep_mes':300.,'ggr_slot_mes':180.,'ggr_live_mes':-80.,'ggr_virt_mes':0.,'bono_total_mes':100.,'delta_deposito':-500.,'delta_ggr':-120.,'nivel_vip':'bronce','venia_prev':'si','cambio_nivel':'se_mantuvo','mes_mundial':'no','perfilado':'Doble Apostador Deportivas y Casino Slot','usa_bono_mes':'si'},
'reactivacion': {'meses_fuera_vip':2,'ultimo_nivel_vip':'bronce','nivel_vip_max_historico':'plata','meses_vip_historicos':3,'racha_vip_previa':2,'reactivaciones_previas':1,'dias_activos_ultimo_mes':18,'recencia_fin_ultimo_mes':5,'deposito_ultimo_mes':3500.,'retiro_ultimo_mes':1200.,'tickets_ultimo_mes':90,'apuesta_total_ultimo_mes':20000.,'spins_ultimo_mes':250,'ggr_general_ultimo_mes':400.,'bono_total_ultimo_mes':100.,'cambio_nivel_ultimo_mes':'descendio','delta_dias_activos_ultimo_mes':-3,'delta_deposito_ultimo_mes':-500.,'delta_ggr_ultimo_mes':-120.,'deposito_promedio_historico':4200.,'ggr_promedio_historico':520.,'apuesta_promedio_historico':24000.,'bono_promedio_historico':130.,'dias_activos_promedio_historico':21.}}

def load_bundle(kind):
    # Only load the files shipped with this app; never accept uploaded pickle files.
    return joblib.load(ROOT / FILES[kind])

def get_categories(kind,bundle):
    if kind=='churn': return bundle['categorias']
    cat=bundle['pipeline'].named_steps['prep'].named_transformers_['cat'].named_steps['ohe']
    return dict(zip(['ultimo_nivel_vip','nivel_vip_max_historico','cambio_nivel_ultimo_mes'],[list(x) for x in cat.categories_]))

def predict(kind,bundle,values):
    features=bundle['features']
    if set(values)!=set(features): raise ValueError('La entrada no coincide con los atributos del modelo.')
    row=dict(values)
    cats=get_categories(kind,bundle)
    for c,opts in cats.items():
        if row[c] not in opts: raise ValueError(f'Categoría inválida: {c}')
    if kind=='churn':
        if row['venia_prev']=='no':
            row['cambio_nivel']='no_aplica'
            for c in ['delta_dias_activos','delta_deposito','delta_ggr']: row[c]=0.
        elif row['cambio_nivel']=='no_aplica': raise ValueError('Si venía del mes anterior, selecciona un cambio de nivel válido.')
        if row['dias_activos_mes']+row['recencia_fin_mes']>31: raise ValueError('Días activos + recencia no pueden superar 31.')
        if (row['bono_total_mes']>0)!=(row['usa_bono_mes']=='si'): raise ValueError('El uso de bono debe coincidir con su importe.')
    else:
        if row['racha_vip_previa']>row['meses_vip_historicos']: raise ValueError('La racha VIP no puede superar el histórico VIP.')
        if row['reactivaciones_previas']>=row['meses_vip_historicos']: raise ValueError('Las reactivaciones anteriores deben ser menores que los meses VIP históricos.')
        ranks={'bronce':1,'plata':2,'oro':3,'diamante':4}
        if ranks[row['nivel_vip_max_historico']]<ranks[row['ultimo_nivel_vip']]: raise ValueError('El nivel máximo no puede ser menor que el último nivel.')
        if row['dias_activos_ultimo_mes']+row['recencia_fin_ultimo_mes']>31: raise ValueError('Días activos + recencia no pueden superar 31.')
        if row['racha_vip_previa']==1:
            row['cambio_nivel_ultimo_mes']='no_aplica'
            for c in ['delta_dias_activos_ultimo_mes','delta_deposito_ultimo_mes','delta_ggr_ultimo_mes']: row[c]=np.nan
        elif row['cambio_nivel_ultimo_mes']=='no_aplica': raise ValueError('Con racha de dos o más meses, selecciona un cambio de nivel válido.')
    for c in features:
        if c not in cats and not (np.isfinite(float(row[c])) or (kind=='reactivacion' and c.startswith('delta_') and pd.isna(row[c]))): raise ValueError(f'Valor numérico inválido: {c}')
    X=pd.DataFrame([row],columns=features)
    for c,opts in cats.items():
        if kind=='churn': X[c]=pd.Categorical(X[c],categories=opts)
    model=bundle['pipeline']; idx=list(model.classes_).index(1)
    score=float(model.predict_proba(X)[0,idx]); threshold=float(bundle['umbral'])
    return {'score':score,'umbral':threshold,'clase':int(score>=threshold),'entrada':X}
