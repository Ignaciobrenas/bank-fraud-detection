.PHONY: setup generate bronze silver gold train stream kpi dashboard test

setup:
	python -m venv .venv
	.venv/Scripts/pip install -r requirements.txt

generate:
	python -m src.fraud_detection.generation.run_generation

bronze:
	python -m src.fraud_detection.ingestion.batch_ingest

silver:
	python -m src.fraud_detection.processing.build_silver

gold:
	python -m src.fraud_detection.features.build_gold

train:
	python -m src.fraud_detection.models.train

stream:
	python -m src.fraud_detection.streaming.consumer

kpi:
	python -m src.fraud_detection.analysis.kpi

dashboard:
	streamlit run src/fraud_detection/dashboard/app.py

test:
	pytest -q
