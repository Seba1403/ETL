# 🧪 Proceso ETL – Evaluación de Riesgo Crediticio

Este documento detalla el flujo de trabajo ETL aplicado a tres datasets relacionados con riesgo crediticio, integrando múltiples fuentes, limpiando inconsistencias y generando variables derivadas útiles para análisis en inteligencia de negocios.

---

## 🎯 Objetivo

Consolidar datos financieros relevantes desde distintas fuentes públicas, aplicando un proceso ETL completo con enfoque en limpieza, estandarización, transformación y preparación para su análisis.

---

## 📂 Fuentes de Datos Utilizadas

1. **bankloans.csv**: Contiene información de edad, ingresos, años de empleo, deudas y si hubo incumplimiento.
2. **credit_risk_dataset.csv**: Contiene variables similares con nombres distintos, incluyendo historial crediticio.
3. **german_credit_data.csv**: Incluye monto y duración del crédito, pero no tiene ingresos ni la variable objetivo.

---

## ✅ Transformaciones Aplicadas

| Nº | Transformación                              | Descripción                                                                 |
|----|----------------------------------------------|-----------------------------------------------------------------------------|
| 1️⃣ | **Selección y renombrado de columnas clave** | Se extrajeron atributos esenciales como edad, ingresos, años de experiencia, tipo de deuda, cumplimiento y antigüedad crediticia. |
| 2️⃣ | **Unificación estructural y combinación**     | Se estandarizaron las columnas y se unificaron los tres datasets en una única tabla. Se añadieron columnas faltantes con `NaN`. |
| 3️⃣ | **Limpieza de valores nulos**                | Se eliminaron registros sin valor en `incumplimiento` y se imputaron los demás atributos numéricos faltantes con la mediana. |
| 4️⃣ | **Conversión de tipos de datos**             | Las columnas se tipificaron como `int64` o `float64` según su naturaleza para evitar errores y asegurar consistencia. |
| 5️⃣ | **Creación de variables derivadas**          | Se añadieron:
   - `deuda_total`: suma de deuda de crédito y otras deudas  
   - `log_ingresos`: log10(ingresos + 1) para estabilizar escalas  
   - `ratio_deuda_total_ingreso`: carga financiera en relación al ingreso |
| 6️⃣ | **Eliminación de valores atípicos**          | Se filtraron registros con valores mayores al percentil 99.5 en `ingresos`, `deuda_total` y `ratio_deuda_total_ingreso` para evitar distorsión analítica. |

---

## 📁 Variables Finales del Dataset

| Variable                    | Descripción                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| `edad`                      | Edad del solicitante                                                        |
| `ingresos`                  | Ingresos mensuales estimados                                                |
| `años_experiencia`          | Años de experiencia laboral                                                 |
| `ratio_deuda_ingresos`      | Porcentaje del ingreso comprometido en deuda                               |
| `deuda_credito`             | Monto adeudado a entidades financieras                                      |
| `otra_deuda`                | Otras deudas del solicitante                                               |
| `incumplimiento`            | Variable objetivo: 1 si hubo mora, 0 si no                                  |
| `antiguedad_crediticia`     | Duración del historial crediticio                                           |
| `deuda_total`               | Suma total de deudas                                                        |
| `log_ingresos`              | Escalado logarítmico de ingresos para visualización y modelos              |
| `ratio_deuda_total_ingreso` | Relación entre deuda total e ingresos, útil para evaluación de riesgo       |

---

## 📦 Archivo Final Generado

- **Nombre:** `datos_etl_final.csv`
- **Ubicación:** `./csv/`
- **Formato:** CSV delimitado por comas
- **Observaciones:**  
  - Dataset homogéneo y sin valores nulos  
  - Se eliminaron registros extremos que podrían distorsionar modelos  
  - Apto para análisis en herramientas como Power BI, Tableau, Python o ML

---

## 🧾 Ejemplo de Registro Transformado

| Variable                    | Valor   | Descripción                                                                 |
|-----------------------------|---------|-----------------------------------------------------------------------------|
| edad                        | 41      | Edad del solicitante                                                       |
| ingresos                    | 25.0    | Ingreso mensual (en miles)                                                 |
| deuda_credito               | 0.3927  | Monto en deudas de crédito                                                 |
| otra_deuda                  | 2.1573  | Otras deudas acumuladas                                                    |
| deuda_total                 | 2.55    | Suma total de deudas                                                       |
| log_ingresos                | 1.4149  | Ingresos transformados logarítmicamente                                    |
| ratio_deuda_total_ingreso   | 0.102   | 10.2% de los ingresos están comprometidos en deuda                         |
| incumplimiento              | 0       | El solicitante **no presenta incumplimiento de pago**                                     |

📌 **Interpretación**: Este solicitante tiene un nivel de deuda moderado y un ingreso bajo. Su ratio de carga financiera es bajo (10.2%), y no ha incumplido, por lo que sería considerado de bajo riesgo crediticio.

---

## 📌 Conclusión

El proceso ETL desarrollado permitió consolidar tres fuentes de datos heterogéneas en un único dataset limpio, estructurado y enriquecido con variables clave para análisis de riesgo crediticio. El resultado final es una base confiable para visualizaciones, segmentaciones o modelos predictivos.
