# Changelog

所有重要變更都記錄於此。格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

---

## [v2.3.0] — 2026-09-08

### 新增
- 新增 Web UI 介面（`tw-lal-generator-webui.py` + `lal_modules/webui.py`）：可在瀏覽器中填寫寄件人／收件人／副本收件人資訊與內文，並即時預覽排版後的信紙格網樣式（斷行、分頁邏輯與正式 PDF 輸出一致）。伺服器端僅使用 Python 標準函式庫（`http.server`），不需額外安裝套件。
- 新增 `start_webui.bat`：Windows 快速啟動捷徑，雙擊即可開啟 Web UI；若內建 reportlab 因 Python 3.12+ 相容性問題載入失敗，會自動改用系統已安裝的 reportlab 重試。

### 修正
- 修正 `lal_modules/core.py` 的 `_fill_info_if_empty()` 參照未定義的區域變數 `painter` 而非 `kwargs['painter']`，導致多頁信函（需要輸出資訊框）且寄件人／收件人／副本收件人任一欄位為空時，匯出 PDF 會直接拋出 `NameError` 而失敗。此問題原本就存在於 CLI 與桌面 GUI，此次一併修正。

---

## [v2.2.2] — 2026-09-08

以此日期回溯建立 CHANGELOG，記錄建立當時既有的功能集（實際版本歷史請見 git log / GitHub Releases）：

### 新增（既有功能）
- 命令列工具（`tw-lal-generator.py`）：指定任意數目之寄件人、收件人、副本收件人姓名與地址，讀取純文字內文檔案，輸出符合郵局存證信函格式的 PDF。
- 桌面圖形介面（`tw-lal-generator-gui.py` + `lal_modules/gui.py`，Tkinter）：填寫資訊、開啟／存檔純文字內文、匯出 PDF（背景執行緒，不卡住介面）。
- 排版引擎（`lal_modules/core.py`、`pdfpainter.py`、`pdfpage.py`）：依 `CONTENT_MAX_CHARACTER_PER_LINE`／`CONTENT_MAX_LINE_PER_PAGE` 自動斷行、分頁，並合併郵局提供的信紙底圖。
