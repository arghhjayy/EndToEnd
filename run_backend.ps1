# setup prefect api pointer to local
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
# start the mlflow server for logging performance/registering models
# and start the prefect api server
# Define the script blocks for your commands
$mlflowserver = {
    mlflow server
    Write-Output "Started mlflow server"
}

$prefectserver = {
    prefect server start
    Write-Output "Start prefect server"
}

$mlflowJob = Start-Job -ScriptBlock $mlflowserver

$prefectJob = Start-Job -ScriptBlock $prefectserver

try {
    Wait-Event -SourceIdentifier PowerShell.Exiting
}
finally {
    # Cleanup and stop both servers
    Stop-Job $mlflowJob
    Stop-Job $prefectJob

    # Remove the jobs (optional)
    Remove-Job $mlflowJob
    Remove-Job $prefectJob
}