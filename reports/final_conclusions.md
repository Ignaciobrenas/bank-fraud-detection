# Conclusiones Finales

## 1. Resultado Principal
- **Escenario A (Batch)**: 0% detectado en tiempo real.
- **Escenario B (Reglas Stream)**: Detecta fraude obvio pero con alta tasa de falsos positivos.
- **Escenario C (ML Stream)**: Detecta el fraude en menos de 2s con alta precisión y balance.

## 2. Streaming vs Batch
El streaming aporta la inmediatez necesaria para bloquear transacciones antes de que el dinero salga, reduciendo pérdidas directas.

## 3. ML vs Reglas
Machine Learning (LightGBM) se adapta mejor a patrones solapados y reduce los falsos positivos (clientes bloqueados injustamente).

## 4. Limitaciones
Datos generados sintéticamente; en la vida real, el data drift requiere reentrenamiento constante.
