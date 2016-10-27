Function Remove-InvalidFileNameChars {
  param(
    [Parameter(Mandatory=$true,
      Position=0,
      ValueFromPipeline=$true,
      ValueFromPipelineByPropertyName=$true)]
    [String]$Name
  )

  $invalidChars = [IO.Path]::GetInvalidFileNameChars() -join ''
  $invalidChars += "%"
  $re = "[{0}]" -f [RegEx]::Escape($invalidChars)
  return ($Name -replace $re)
}

$BasePath = "D:\Repositories\GitHub\gischem_scraper"

$Substances = Get-Content -Encoding UTF8 "gischem.json" | ConvertFrom-Json | Sort-Object -Property substance -Unique

ForEach($Substance in $Substances) {
    $Filename = Remove-InvalidFileNameChars $Substance.substance
    
    Write-Host $Substance.substance, $Filename


    $Source = $BasePath + "\docs\" + $Substance.files[0].path.Replace('/', '\')
    $Target = $BasePath + "\export\$Filename.doc"
    
    Copy-Item $Source $Target
}
