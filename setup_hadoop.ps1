$hadoopDir = "$PSScriptRoot\hadoop"
$binDir = "$hadoopDir\bin"
if (-not (Test-Path $binDir)) {
    New-Item -ItemType Directory -Path $binDir | Out-Null
}

$winutilsUrl = "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.3.5/bin/winutils.exe"
$hadoopDllUrl = "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.3.5/bin/hadoop.dll"

Invoke-WebRequest -Uri $winutilsUrl -OutFile "$binDir\winutils.exe"
Invoke-WebRequest -Uri $hadoopDllUrl -OutFile "$binDir\hadoop.dll"

[System.Environment]::SetEnvironmentVariable("HADOOP_HOME", $hadoopDir, "User")
[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";$binDir", "User")

Write-Host "Hadoop setup complete. HADOOP_HOME set to $hadoopDir"
