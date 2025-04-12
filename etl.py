# ============================================
# Grupo 3: Evaluación de Riesgo Crediticio
# ICI6642 - Inteligencia de Negocios
# ============================================

import pandas as pd
import numpy as np

# Carga de datasets originales
bankloans = pd.read_csv('./csv/bankloans.csv')
credit_risk = pd.read_csv('./csv/credit_risk_dataset.csv')
german_credit = pd.read_csv('./csv/german_credit_data.csv')

# ============================================
# Transformación 1: Seleccion y extracción de columnas clave para analisis de riesgo crediticio
# ============================================

# --- Primer Dataset: bankloans ---
# Columnas seleccionadas: edad, ingresos, años de experiencia laboral, ratio deuda/ingreso, deuda de crédito, otra deuda, y si hubo incumplimiento
bankloans_clean = bankloans[['age', 'income', 'employ', 'debtinc', 'creddebt', 'othdebt', 'default']].copy()
bankloans_clean.rename(columns={
    'age': 'edad',
    'income': 'ingresos',
    'employ': 'años_experiencia',
    'debtinc': 'ratio_deuda_ingresos',
    'creddebt': 'deuda_credito',
    'othdebt': 'otra_deuda',
    'default': 'incumplimiento'
}, inplace=True)
bankloans_clean['antiguedad_crediticia'] = np.nan  # Columna extra que otros datasets sí tienen

# --- Segundo Dataset: credit_risk_dataset ---
# Aqui hay columnas claves similares al otro dataset pero con otros nombres. Se renombran para unificar datos.
credit_risk_clean = credit_risk[['person_age', 'person_income', 'person_emp_length',
                                 'loan_percent_income', 'loan_status', 'cb_person_cred_hist_length']].copy()
credit_risk_clean.rename(columns={
    'person_age': 'edad',
    'person_income': 'ingresos',
    'person_emp_length': 'años_experiencia',
    'loan_percent_income': 'ratio_deuda_ingresos',
    'loan_status': 'incumplimiento',
    'cb_person_cred_hist_length': 'antiguedad_crediticia'
}, inplace=True)
# Estas columnas no existen en este dataset, asi que se agregan con NaN
credit_risk_clean['deuda_credito'] = np.nan
credit_risk_clean['otra_deuda'] = np.nan

# --- Dataset: german_credit_data ---
# Este dataset no tiene ingresos ni cumplimiento, pero se puede rescatar edad, duración crediticia y monto de crédito
german_credit_clean = german_credit[['Age', 'Credit amount', 'Duration']].copy()
german_credit_clean.rename(columns={
    'Age': 'edad',
    'Credit amount': 'deuda_credito',
    'Duration': 'antiguedad_crediticia'
}, inplace=True)
# Agregamos las columnas faltantes para emparejar estructura con los otros datasets
german_credit_clean['ingresos'] = np.nan
german_credit_clean['años_experiencia'] = np.nan
german_credit_clean['ratio_deuda_ingresos'] = np.nan
german_credit_clean['otra_deuda'] = np.nan
german_credit_clean['incumplimiento'] = np.nan

# ============================================
# Transformación 2: Unificación y combinación de datasets 
# ============================================

columnas_finales = [
    'edad', 'ingresos', 'años_experiencia', 'ratio_deuda_ingresos',
    'deuda_credito', 'otra_deuda', 'incumplimiento', 'antiguedad_crediticia'
]

# Ordenamos y combinamos todos los datasets en un solo DataFrame
bankloans_clean = bankloans_clean[columnas_finales]
credit_risk_clean = credit_risk_clean[columnas_finales]
german_credit_clean = german_credit_clean[columnas_finales]

df_combinado = pd.concat([bankloans_clean, credit_risk_clean, german_credit_clean], ignore_index=True)

# ============================================
# Transformación 3: Limpieza de valores nulos (NaN en este caso)
# ============================================

# Eliminación de registros sin información en columna 'incumplimiento'
df_limpio = df_combinado.dropna(subset=['incumplimiento']).copy()
# El resto de valores faltantes lo tomaremos con la mediana, para asi no tener que perder exceso de datos
# y al usar la mediana, no alteramos resultados en el análisis
for col in ['edad', 'ingresos', 'años_experiencia', 'ratio_deuda_ingresos',
            'deuda_credito', 'otra_deuda', 'antiguedad_crediticia']:
    df_limpio[col] = df_limpio[col].fillna(df_limpio[col].median())

# ============================================
# Transformación 4: Conversión de tipos de datos para mayor coherencia
# ============================================

df_limpio = df_limpio.astype({
    'edad': 'int64',
    'años_experiencia': 'int64',
    'antiguedad_crediticia': 'int64',
    'ingresos': 'float64',
    'deuda_credito': 'float64',
    'otra_deuda': 'float64',
    'ratio_deuda_ingresos': 'float64',
    'incumplimiento': 'int64'
})

# ============================================
# Transformación 5: Creación de variables derivadas de otras (esto ayuda a enriquecer la información para el análisis)
# ============================================

# deuda_total: suma de deudas existentes
df_limpio['deuda_total'] = df_limpio['deuda_credito'] + df_limpio['otra_deuda']

# log_ingresos: sirve para analizar datos en gráficos, sin romper el eje X con ingresos demasiados altos (los valores 
# suelen moverse entre numeros muchisimo menores (en vez de 100mil a 10 millones, se va desde el 0 al 10 por ejemplo))
df_limpio['log_ingresos'] = np.log10(df_limpio['ingresos'] + 1)

# ratio_deuda_total_ingreso: indicador que mide qué parte del ingreso está comprometida en deudas, preciso para evaluar riesgo financiero.
df_limpio['ratio_deuda_total_ingreso'] = df_limpio['deuda_total'] / df_limpio['ingresos']

# ============================================
# Transformación 6: Eliminación de datos extremos (valores atípicos)
# ============================================

# Utilizamos 99.5 como umbral para definir datos extremos (valores atípicos)
percentiles = {
    'ingresos': df_limpio['ingresos'].quantile(0.995),
    'deuda_total': df_limpio['deuda_total'].quantile(0.995),
    'ratio_deuda_total_ingreso': df_limpio['ratio_deuda_total_ingreso'].quantile(0.995)
}

# Limpiamos los datos que superen el umbral del 99.5
df_limpio = df_limpio[
    (df_limpio['ingresos'] <= percentiles['ingresos']) &
    (df_limpio['deuda_total'] <= percentiles['deuda_total']) &
    (df_limpio['ratio_deuda_total_ingreso'] <= percentiles['ratio_deuda_total_ingreso'])
]

# ============================================
# Exportación a formato csv
# ============================================

df_limpio.to_csv("datos_etl_final.csv", index=False)
