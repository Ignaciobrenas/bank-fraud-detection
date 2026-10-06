# 🛡️ Bank Fraud Detection Pipeline (End-to-End)

Este repositorio contiene una solución completa y robusta para la detección de fraude bancario en tiempo real. Aborda todo el ciclo de vida del dato (Data Lifecycle), desde la generación de datos sintéticos masivos hasta la puntuación predictiva en streaming y su visualización en un Dashboard financiero.

---

## 🏗️ Arquitectura y Decisiones de Diseño

El sistema está diseñado bajo el patrón **Medallion Architecture** (Bronze, Silver, Gold), utilizando herramientas de **Big Data** para asegurar la escalabilidad horizontal.

### 1. Data Generation (Faker / Numpy)
Dado que los datos bancarios reales están protegidos por leyes de privacidad (GDPR, PCI-DSS), hemos optado por construir un generador sintético determinista.
- **Decisión:** Usar `Faker` y `numpy` para generar 7 datasets relacionales (perfiles, transacciones, dispositivos, logs).
- **Por qué:** Permite inyectar casos de uso de fraude específicos (`impossible_travel`, `account_takeover`, `velocity_burst`) controlando la tasa de fraude, lo cual es vital para entrenar modelos de Machine Learning.
- **Alternativa Masiva:** Para pruebas de estrés, hemos integrado un script (`kaggle_seed.py`) preparado para descargar el dataset **PaySim** (6.3 millones de transacciones) de Kaggle.

### 2. Ingestion (Bronze Layer)
- **Decisión:** Almacenar los datos crudos añadiendo metadata de gobierno (`source_system`, `ingestion_timestamp`, `schema_version`) en formato **Parquet** particionado por fecha.
- **Por qué:** Parquet es un formato columnar que reduce drásticamente los costes de almacenamiento y acelera las consultas analíticas posteriores. Particionar por fecha facilita la simulación de ventanas temporales.
- **Herramienta:** **PySpark**, porque permite escalar la ingesta a clústeres si el volumen de datos crudos crece de megabytes a terabytes.

### 3. Processing & Quality (Silver Layer)
- **Decisión:** Castear tipos de datos, aplanar estructuras JSON anidadas (geolocalización, datos del dispositivo) y deduplicar (`transaction_id`).
- **Por qué:** El modelo de Machine Learning necesita tensores y tablas planas sin valores nulos ni duplicados que puedan desvirtuar el entrenamiento.

### 4. Feature Engineering (Gold Layer)
- **Decisión:** Calcular métricas derivadas complejas como el `amount_zscore_customer` (cuántas desviaciones estándar se aleja la transacción actual del comportamiento habitual del cliente).
- **Por qué:** Los algoritmos aprenden mejor de features relativas (Z-Score) que de absolutas (Amount), ya que un gasto de 500€ es normal para un cliente de banca privada, pero anómalo para un estudiante.

### 5. Machine Learning (LightGBM)
- **Decisión:** Se ha elegido **LightGBM** con `class_weight="balanced"`.
- **Por qué:** El fraude bancario es un problema clásico de **Clases Extremadamente Desbalanceadas** (usualmente < 1% de fraude). LightGBM maneja el desbalanceo eficientemente mediante la construcción de árboles asimétricos y es ultrarrápido tanto en entrenamiento como en inferencia (crucial para streaming).

### 6. Streaming Simulation & Financial KPIs
- **Decisión:** Pasar de medir solo el `% de detección` a medir el **Impacto Financiero** (Dinero Salvado vs Dinero Retenido por Error).
- **Por qué:** A nivel de negocio, un modelo con un 99% de detección pero un 20% de Falsos Positivos (FPR) arruinaría la experiencia del cliente (bloqueando tarjetas legítimas constantemente). El KPI real de un banco busca el equilibrio entre la precisión (minimizar la fricción al cliente) y el recall (detectar el fraude).

---

## 📊 Modelo DIKW

Este proyecto aplica el modelo DIKW (Data, Information, Knowledge, Wisdom) al flujo de transacciones:

*   **Data (Dato):** `amount=4800, country=RU, device=new, ip_country=RU` (Registros crudos en `data/raw`).
*   **Information (Información):** "El importe es 12 veces superior a la media histórica del cliente, el dispositivo nunca ha sido visto, y hay un inicio de sesión fallido previo." (Capa Gold: Features Z-Score).
*   **Knowledge (Conocimiento):** El modelo LightGBM asocia este patrón con una probabilidad del 94% de ser un `account_takeover` (Toma de control de cuenta).
*   **Wisdom / Action (Sabiduría):** El Consumer bloquea la transacción automáticamente en menos de 2 segundos y emite una alerta temprana en el Dashboard para el equipo de analistas.

---

## 🚀 Cómo ejecutar el proyecto

### 1. Instalación automatizada
Hemos preparado un script que levantará el entorno virtual y comprobará las dependencias de Java (requerido para PySpark local).

**En Windows (PowerShell):**
```powershell
.\install.ps1
```
**En Linux / Mac / WSL:**
```bash
chmod +x install.sh
./install.sh
```

### 2. Ejecutar el Pipeline (End-to-End)
Asegúrate de tener el entorno activado (`.venv\Scripts\Activate.ps1` o `source .venv/bin/activate`). Usa los comandos del `Makefile`:

```bash
make generate    # 1. Crea los 7 datasets sintéticos (Raw)
make bronze      # 2. Ingesta a Parquet con metadatos (PySpark)
make silver      # 3. Limpieza y deduplicación (PySpark)
make gold        # 4. Feature Engineering y cruces (PySpark)
make train       # 5. Entrena el modelo LightGBM y lo guarda
```

### 3. Simular el Streaming y Analizar KPIs
Una vez entrenado el modelo, ejecutamos el consumidor que simulará la entrada de transacciones en tiempo real:

```bash
python -m src.fraud_detection.streaming.consumer
```

Para levantar el **Dashboard Interactivo** donde se visualizan los KPIs financieros:
```bash
make dashboard
```

### 4. Tests
El repositorio incluye una batería de tests (KPIs, Generación, Features) usando `pytest`:
```bash
make test
```

---

## 📂 Data Lineage

El flujo de vida del dato desde su origen hasta el panel de negocio es el siguiente:
`data/raw/*.csv` ➔ `batch_ingest` ➔ `data/bronze/` ➔ `build_silver` ➔ `data/silver/` ➔ `build_gold` ➔ `data/gold/features` ➔ `train` ➔ `models/lgbm_model.pkl` ➔ `consumer` ➔ `alerts.parquet` ➔ `dashboard`.

## 🐳 Dockerization & CI/CD
Para garantizar que el entorno sea completamente reproducible y robusto (Enterprise-Ready):
- **Docker & Docker Compose**: Se ha añadido un \Dockerfile\ y un \docker-compose.yml\ que levantan tanto el pipeline de datos (\main.py\) como el Dashboard de Streamlit sin tener que instalar Java ni dependencias localmente.
  - Comando: \docker-compose up --build\
- **GitHub Actions**: Se ha añadido un flujo de Integración Continua (CI) en \.github/workflows/ci.yml\ que ejecuta comprobaciones y los tests unitarios automáticamente en cada _Push_ o _Pull Request_.
- **Pre-commit**: Se usan ganchos (hooks) automáticos configurados en \.pre-commit-config.yaml\ para bloquear subidas de archivos masivos o código mal formateado (integrando _Ruff_).
- **Quality Checks & Logs**: Hay un sistema robusto de aserciones en \quality_checks.py\ (que aborta si hay nulos en variables clave de negocio) y se exportan _Logs_ centralizados en la carpeta \logs/\ para total observabilidad y trazabilidad.

