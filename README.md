# AWS AI Practitioner (AIF-C01) 增強版模擬測驗
# AWS AI Practitioner (AIF-C01) Enhanced Mock Test

這是一個開源的 AWS Certified AI Practitioner (AIF-C01) 模擬測驗工具。它被設計為一個**單一、自包含的 HTML 檔案**，讓使用者可以輕鬆下載、離線使用或分享。

This is an open-source mock test tool for the AWS AI Practitioner (AIF-C01) exam. It is designed as a **single, self-contained HTML file**, making it easy to download, use offline, and share.

---

## 💡 主要功能 (Features)

* **整合式體驗 (All-in-One):** 所有功能（HTML/CSS/JS）都在一個檔案中，無需安裝、無需伺服器。
* **隨機化題庫 (Randomized):** 每次重新載入頁面時，都會自動打亂所有題目順序，非常適合重複練習。
* **完整測驗功能 (Full-Featured):** 包含測驗計時器、進度條和快速題目導航格。
* **進階學習工具 (Advanced Study Tools):**
    * **⭐ 收藏題目 (Bookmark Questions):** 標記困難或需要複習的題目。
    * **🔄 收藏篩選 (Filter Bookmarks):** 可一鍵切換，僅顯示您收藏的題目。
* **進度保存 (Progress Saving):**
    * **💾 自動保存 (Auto-Save):** 您的答題進度會自動保存到瀏覽器的 `localStorage` 中。
    * **📂 手動保存/載入 (Manual Save/Load):** 您也可以手動點擊「保存進度」和「載入進度」。
* **易於擴充 (Easy to Expand):** 程式碼結構清晰，您可以輕鬆地將自己的題庫粘貼到 `<script>` 區域中。

---

## 🚀 如何使用 (How to Use)

1.  **下載 (Download):** 從本專案下載 `AIF-C01.html` 檔案 (或您命名的 HTML 檔案)。
2.  **開啟 (Open):** 在您的任何現代網頁瀏覽器（如 Chrome, Firefox, Edge）中直接開啟這個檔案。
3.  **開始練習 (Practice)!**

---

## 🧩 如何添加您自己的題庫 (How to Add Your Own Questions)

此工具的題庫是模組化的。

1.  使用文字編輯器（如 VS Code）開啟 `.html` 檔案。
2.  找到 `<script>` 標籤內的「**⬇️ 題庫粘貼區**」。
3.  將您格式化好的題庫陣列（JSON 格式）貼入 `const questionSet1 = [...]` 或 `const questionSet2 = [...]` 變數中。
4.  保存檔案並在瀏覽器中刷新即可。

---

## ⚠️ 免責聲明 (Disclaimer)

* 本專案提供的題庫來源於網路，僅供學術交流和備考學習使用。
* 題目的答案僅供參考，不保證 100% 準確。
* AWS 考試內容會隨時更新，請務必以 AWS 官方文件和最新考綱為準。

* The question banks provided in this project are sourced from online resources, intended for academic exchange and exam preparation only.
* The answers provided are for reference and are not guaranteed to be 100% accurate.
* AWS exam content is subject to change. Please always refer to the official AWS documentation and the latest exam guide.

---

## 📄 授權協議 (License)
MIT License
