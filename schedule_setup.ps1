# ===== LMS AutoSaver 자동 실행 스케줄러 등록 =====
param(
    [string]$Time = "08:00AM"
)

Write-Host "LMS AutoSaver 자동 실행 스케줄러를 등록합니다..." -ForegroundColor Cyan
Write-Host "실행 시간: 매일 $Time" -ForegroundColor Yellow

# 현재 스크립트 위치 기준으로 경로 설정
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$batPath = Join-Path $scriptPath "run.bat"

if (-not (Test-Path $batPath)) {
    Write-Host "오류: run.bat 파일을 찾을 수 없습니다." -ForegroundColor Red
    exit 1
}

try {
    $action = New-ScheduledTaskAction -Execute $batPath
    $trigger = New-ScheduledTaskTrigger -Daily -At $Time
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
    Register-ScheduledTask -TaskName "LMS AutoSaver" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force
    Write-Host "✅ 스케줄러 등록 완료! 매일 $Time 에 자동 실행됩니다." -ForegroundColor Green
} catch {
    Write-Host "❌ 오류: 관리자 권한으로 실행해주세요." -ForegroundColor Red
    Write-Host "PowerShell을 관리자 권한으로 열고 다시 실행하세요." -ForegroundColor Yellow
}