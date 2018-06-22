
Sub Count_Volume()

'Declare variables
Dim i As Integer
Dim ws_num As Integer

' Loop over worksheets
Dim starting_ws As Worksheet
Set starting_ws = ActiveSheet 'remember which worksheet is active in the beginning
ws_num = ThisWorkbook.Worksheets.Count

For i = 1 To ws_num
    ThisWorkbook.Worksheets(i).Activate
    
' More variables
Dim tickerFrow As Long
Dim copiedFrow As Long
Dim ticker As String
Dim tickerRange As Range
Dim tickerCopied As Range
Dim volumeFrow As Long

' Get the final row for ticker column A
tickerFrow = ThisWorkbook.Worksheets(i).Range("A1").CurrentRegion.Rows.Count

' Get the final row for volume column G
volumeFrow = ThisWorkbook.Worksheets(i).Range("G1").CurrentRegion.Rows.Count

' Copy unique cells from ticker column to I
ThisWorkbook.Worksheets(i).Range("A1:A" & tickerFrow).AdvancedFilter Action:=xlFilterCopy, CopyToRange:=Range("I1"), Unique:=True

' Set tickerRange from column A
Set tickerRange = ThisWorkbook.Worksheets(i).Range("A2:A" & tickerFrow)

' Set header for Column J
ThisWorkbook.Worksheets(i).Range("J1").Value = "Total Stock Volume"

' Set header for Column I
ThisWorkbook.Worksheets(i).Range("I1").Value = "Ticker"

' Get the final row of unique tickers in column I
copiedFrow = ThisWorkbook.Worksheets(i).Range("I1").CurrentRegion.Rows.Count

' Set tickerCopied range from column I
Set tickerCopied = ThisWorkbook.Worksheets(i).Range("I2:I" & copiedFrow)

' Loop through unique tickers in Column I and set offset cell value to total volume
For Each cell In tickerCopied
'Debug.Print cell
cell.Offset(0, 1).Value = Application.WorksheetFunction.SumIf(Range("A2:A" & tickerFrow), cell.Value, Range("G2:G" & volumeFrow))
Next cell

Next

End Sub