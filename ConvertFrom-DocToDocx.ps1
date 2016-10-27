$word = new-object -comobject word.application
$word.Visible = $False

$saveFormat = [Enum]::Parse([Microsoft.Office.Interop.Word.WdSaveFormat],”wdFormatDocumentDefault”);

#Get the files
$folderpath = "D:\Repositories\GitHub\gischem_scraper\export\*"
$fileType = "*doc"

Get-ChildItem -path $folderpath -include $fileType | foreach-object {

    if (-not (Test-Path ($_.FullName+"x"))) { 

        $opendoc = $word.documents.open($_.FullName)
        $savename = ($_.fullname).substring(0,($_.FullName).lastindexOf(“.”))
        $opendoc.Convert()
    
        $opendoc.saveas([ref]”$savename”, [ref]$saveFormat);
        $opendoc.close();
    }
}

#Clean up
$word.quit()