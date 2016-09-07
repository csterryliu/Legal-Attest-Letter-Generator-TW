# Legal Attest Letter Generator - Taiwan #
台灣郵局存證信函產生器 (PDF 格式)。A tool for creating a legal attest letter of Taiwan - in PDF format.

![](./doc/sample.png)

## Feature ##
- 輸出整齊、美觀的信函  
  The output is neat and beautiful.  

- 可指定任意數目之姓名、地址  
  You can specify any number of names or addresses.  

- 可排版：只需用純文字編輯器打好內容並排版，便會反應至信函上，使內容不至於擁擠  
  Support indentation: The only thing you have to do is typing your main article and indenting them on a text editor. The output will reflect your indentation so that the main article won't look crowded.  

- 可免費離線使用  
  You can use it offline for free.

- 開源：程式實作完全開放閱覽，無隱私問題，過程完全透明  
  Open source: You are free to read the code. No privacy issue. The process is totally transparent.

## Prerequisite ##
Download and install [Python 2.7](https://www.python.org/downloads/) to your computer

## Usage ##
```
tw-lal-generator.py 信函正文純文字檔路徑 [--senderName 寄件人姓名 [寄件人姓名 ...]] [--senderAddr 寄件人詳細地址] [--receiverName 收件人姓名 [收件人姓名 ...]] [--receiverAddr 收件人詳細地址] [--ccName 副本收件人姓名 [副本收件人姓名 ...]] [--ccAddr 副本收件人詳細地址] [--outputFileName 輸出之檔案名稱] [--help]
```
For example:  
```
# 只有內文，無收件人等資訊
tw-lal-generator.py 信函正文.txt

# 含正文、寄件人姓名地址、收件人姓名地址、副本收件人姓名地址
tw-lal-generator.py 信函正文.txt --senderName 王大明 --senderAddr 某某縣某某鎮某某路100號 --receiverName 林小英 --receiverAddr 某某市某某街71號 --ccName 許大年 --ccAddr 某某縣某某鄉某某路90號
```

## Dependency ##
- [PyPDF2 1.26](https://github.com/mstamy2/PyPDF2)  
- [reportlab 3.3.0](https://bitbucket.org/rptlab/reportlab)
- [Letter sample provided by Post Office of Taiwan](http://www.post.gov.tw/post/internet/Download/index.jsp?ID=220301)
- [Traditional Chinese font provided by National Development Council, Taiwan ](http://data.gov.tw/node/5961)

## Roadmap ##
- Match PEP8  
- Provide application GUI
- Turn it into a cloud service (Maybe)

## License ##
MIT
