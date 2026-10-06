$hadoopDir = "$PSScriptRoot\hadoop"
$env:HADOOP_HOME = $hadoopDir
$env:Path = "$env:Path;$hadoopDir\bin"
$env:PYTHONPATH = "$PSScriptRoot\src"

. .\.venv\Scripts\Activate.ps1

Write-Host "Running generation..."
python -m fraud_detection.generation.run_generation
if ($LASTEXITCODE -ne 0) { throw "Generation failed" }

Write-Host "Running bronze..."
python -m fraud_detection.ingestion.batch_ingest
if ($LASTEXITCODE -ne 0) { throw "Bronze failed" }

Write-Host "Running silver..."
python -m fraud_detection.processing.build_silver
if ($LASTEXITCODE -ne 0) { throw "Silver failed" }

Write-Host "Running gold..."
python -m fraud_detection.features.build_gold
if ($LASTEXITCODE -ne 0) { throw "Gold failed" }

Write-Host "Running training..."
python -m fraud_detection.models.train
if ($LASTEXITCODE -ne 0) { throw "Training failed" }

Write-Host "Pipeline completed successfully."
