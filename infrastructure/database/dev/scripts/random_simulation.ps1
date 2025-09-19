$params = @{
    x = (Get-Random -Minimum 1 -Maximum 10).ToString()
    y = (Get-Random -Minimum 20 -Maximum 30).ToString()
    z = (Get-Random -Minimum 100 -Maximum 200).ToString()
}

$result = "result_$((Get-Random -Minimum 1 -Maximum 5).ToString())"

$output = @{
    result = $result
    parameters = $params
}

$output | ConvertTo-Json -Compress
