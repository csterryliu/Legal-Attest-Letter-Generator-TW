# How To Start #
本章介紹使用本工具前的必要準備。
## Install Python 2.7 ##
### Windows ###
下載並安裝 [Python 2.7](https://www.python.org/downloads/)。使用安裝精靈的預設值即可，一直按「下一步」，直到安裝結束。  
### macOS / Ubuntu Linux ###
通常系統已預設安裝一套。請打開終端機，鍵入`python --version`看是否可執行。若失敗：  
- macOS 使用者，請依連結說明安裝 [Homebrew](http://brew.sh/index_zh-tw.html)。安裝後，使用以下指令安裝 Python：  
  ```
  brew install python
  ```
- Ubuntu 使用者，直接輸入：  
  ```
  sudo apt-get install python
  ```

## Set Environment Variables ##
使用前，需設定環境變數 (PYTHONPATH)。  
### Windows ###
下載並解壓縮本專案之後，用檔案總管開啟專案目錄。直接點擊 ***set_pythonpath_win.bat*** 即可。  
### macOS / Ubuntu Linux ###
下載並解壓縮之後，開啟終端機，使用```cd```指令移動到專案目錄下。接著直接執行以下指令即可：  
 ```
 source ./set_pythonpath_unix.sh
 ```
但若開啟新的終端機，就須重新執行以上指令。若希望不要重複此動作，請用文字編輯器開啟 ***~/.bash_profile*** (若無請自行建立)。在檔案的最後加入以下指令並存檔：  
```
PYTHONPATH=$(your_project_path)/dep/pyPDF2:$(your_project_path)/dep/reportlab/src
export PYTHONPATH
```
$(your_project_path) 是您解壓縮後的專案目錄路徑。  

存檔後，在終端機下輸入：
```
source ~/.bash_profile
```
如此一來環境變數便會保存，不必重複執行腳本。

### Test Your Program ###
- Windows 使用者，請用檔案總管進入專案目錄下。將滑鼠移到空白處，壓住 shift 並按下滑鼠右鍵，會在功能表上看到「在此處開啟命令提示字元」，點擊他以打開終端機。最後輸入 ```tw-lal-generator.py --help```。



- macOS / Linux 使用者，請直接打開終端機，並 ```cd``` 至專案目錄下，輸入 ```./tw-lal-generator.py --help```

若看到以下畫面，表示變數設定成功，可開始使用。
