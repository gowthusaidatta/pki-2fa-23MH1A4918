Write-Host "Fetching /sign ..."
$res = Invoke-RestMethod "http://127.0.0.1:8000/sign"

$totp = $res.totp
$signature = $res.signature

Write-Host "TOTP =" $totp
Write-Host "Signature =" $signature.Substring(0,20) "... "

# Load PEM and Base64 encode it
$pub_raw = Get-Content "app/student_public.pem" -Raw
$pub = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($pub_raw))

Write-Host "Encoded public key length =" $pub.Length

$body = @{
    roll = "23MH1A4918"
    totp = $totp
    signature = $signature
    public_key = $pub
} | ConvertTo-Json -Depth 10

Write-Host "`nSending JSON:"
Write-Host $body

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/submit" `
        -Method Post `
        -Body $body `
        -ContentType "application/json"

    Write-Host "`nServer Response:"
    $response
}
catch {
    Write-Host "`n--- SERVER ERROR ---"
    Write-Host $_.Exception.Response.StatusCode.Value__
    Write-Host $_.Exception.Message
    Write-Host "`nRaw server output:"
    Write-Host ($_ | Out-String)
}
