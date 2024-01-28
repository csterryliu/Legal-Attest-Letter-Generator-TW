# Legal Attest Letter Generator - Taiwan #
台灣郵局存證信函產生器 (PDF 格式)。  
A tool for creating a legal attest letter of Taiwan - in PDF format.

![](./img/sample.png)

## Feature ##
- 輸出整齊、美觀的信函  
  The output is neat and beautiful.  

- 可指定任意數目之姓名、地址  
  You can specify any number of names or addresses.  

- 可排版：只需用純文字編輯器打好內容並排版，便會反應至信函上，使內容不至於擁擠  
  Support indentation: The only thing you have to do is typing your main article and indenting them on a text editor. The output will reflect your indentation so that the main article won't look crowded.  

- 可免費離線使用 (目前尚未提供圖形介面)  
  You can use it offline for free (No GUI currently).

- 開源：程式實作完全開放閱覽，無隱私問題，過程完全透明  
  Open source: You are free to read the code. No privacy issue. The process is totally transparent.

## Download The Latest Version ##
Please click [here](https://github.com/csterryliu/Legal-Attest-Letter-Generator-TW/releases/download/v2.1.1/Legal-Attest-Letter-Generator-TW-v2.1.1.zip). For more detail, please head to [Releases](https://github.com/csterryliu/Legal-Attest-Letter-Generator-TW/releases).

## How To Use It ##
Please read [Wiki](https://github.com/csterryliu/Legal-Attest-Letter-Generator-TW/wiki/).

## Dependencies ##
- [PyPDF2 3.0.1](https://pypi.org/project/PyPDF2/)
- [reportlab 4.0.9](https://pypi.org/project/reportlab/)
- [Letter sample provided by Post Office of Taiwan](http://www.post.gov.tw/post/internet/Download/index.jsp?ID=220301)
- [Traditional Chinese font provided by National Development Council, Taiwan ](http://data.gov.tw/node/5961)

### Install Dependencies ###
```shell
% pip install -r requirements.txt
```

## Roadmap ##
- Provide online web service
- Provide offline application GUI
- Compatible with Python 2.7
- Keep matching PEP8

## License ##
MIT
