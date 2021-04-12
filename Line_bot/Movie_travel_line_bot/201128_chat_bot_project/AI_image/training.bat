echo off
set /p lang="請輸入這個新語言包的名稱："
set /p file="請輸入要學習的圖檔名稱："
%~d0
cd %~p0
copy %file% %lang%.src
tesseract %lang%.src %lang% batch.nochop makebox
echo 請先確認%lang.box檔案內容是否正確
pause
tesseract %lang%.src %lang% nobatch box.train
unicharset_extractor %lang%.box
echo %lang% 0 0 0 0 0 > font_properties
shapeclustering -F font_properties -U unicharset %lang%.tr
mftraining -F font_properties -U unicharset -O unicharset %lang%.tr
cntraining %lang%.tr
rename unicharset %lang%.unicharset
rename normproto %lang%.normproto
rename pffmtable %lang%.pffmtable
rename shapetable %lang%.shapetable
rename inttemp %lang%.inttemp
del %lang%.src
del %lang%.box
del %lang%.tr
del font_properties
combine_tessdata %lang%.
del %lang%.unicharset
del %lang%.normproto
del %lang%.pffmtable
del %lang%.shapetable
del %lang%.inttemp
pause