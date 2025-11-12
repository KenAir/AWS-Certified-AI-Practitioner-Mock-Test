import requests
from bs4 import BeautifulSoup
import json
import time
import re

# --- 設定 (Configuration) ---
BASE_URL = "https://www.examtopics.com"
DISCUSSION_LIST_URL = "https://www.examtopics.com/discussions/amazon/"
KEYWORDS = ["aif-c01", "aws certified ai practitioner"]
OUTPUT_FILE = "aws_aif_c01_questions.json"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

# --- Phase 1: 尋找討論串 URL (已更正分頁邏輯) ---

def find_discussion_links():
    """
    遍歷討論區的所有分頁，找出包含關鍵字的討論串 URL。
    現在只依賴 404 或真正的空頁面來停止。
    """
    print("Phase 1: Starting discussion link discovery...")
    discussion_links = []
    page = 1
    
    while True:
        # 組合正確的分頁 URL 結構
        if page == 1:
            current_url = DISCUSSION_LIST_URL
        else:
            current_url = f"{DISCUSSION_LIST_URL.rstrip('/')}/{page}/" 
        
        print(f"Checking page: {current_url}")
        
        try:
            response = requests.get(current_url, headers=HEADERS)
            
            # --- 停止條件 1：遇到 404 ---
            if response.status_code == 404:
                print(f"Received 404 Not Found for page {page}. Assuming this is the last page and stopping.")
                break
                
            response.raise_for_status() 
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links_on_page = soup.select('a.discussion-link') 

            # --- 停止條件 2：頁面上沒有任何討論連結 ---
            if not links_on_page:
                print(f"No discussion links found on page {page}. Ending discovery.")
                break 

            for link in links_on_page:
                # ... (關鍵字過濾邏輯不變) ...
                title = link.text.lower()
                href = link.get('href')
                
                if not href:
                    continue
                    
                if any(keyword in title for keyword in KEYWORDS):
                    full_url = BASE_URL + href
                    if full_url not in discussion_links:
                        print(f"  [Found Match]: {link.text.strip()}")
                        discussion_links.append(full_url)
            
            page += 1
            time.sleep(1) # 禮貌性延遲

        except requests.exceptions.RequestException as e:
            print(f"Error fetching discussion list (Page {page}): {e}. Stopping process.")
            break
            
    print(f"Phase 1: Found {len(discussion_links)} matching discussion links.\n")
    return discussion_links

# --- Phase 2: 擷取單一問題資料 ---

def scrape_question(url):
    """
    從指定的 URL 擷取單一問題的詳細資訊。
    這假設了網站內容是靜態載入的，如果答案抓不到，則需要使用 Selenium。
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        question_data = {}
        
        # 1. 取得 ID (Question #)
        # 尋找包含 "Question #:" 的 div
        question_header = soup.select_one('div.question-discussion-header div')
        if question_header:
            # 使用正則表達式或直接文字解析來提取 Question #: 50
            match_id = re.search(r'Question\s*#:\s*(\d+)', question_header.text)
            if match_id:
                # 將 ID 儲存為整數
                question_data['id'] = int(match_id.group(1))
            else:
                 # 備用方案：從 URL 解析 ID
                id_match_url = re.search(r'question-(\d+)', url)
                question_data['id'] = int(id_match_url.group(1)) if id_match_url else None
        else:
             question_data['id'] = None
        
        # 2. 取得問題內文 (Question Body)
        # 選擇器：'div.question-body p.card-text'
        text_element = soup.select_one('div.question-body p.card-text')
        # 移除內文中的換行符號，並清理空白
        text_content = text_element.text.strip().replace('\n', ' ').replace('\t', ' ') if text_element else None
        # 使用正則表達式清理多餘的空格
        question_data['text'] = re.sub(r'\s+', ' ', text_content) if text_content else None
        
        # 3. 取得選項 (Question Options)
        options = {}
        # 選擇器：'li.multi-choice-item'
        option_elements = soup.select('li.multi-choice-item')
        
        for item in option_elements:
            # 取得選項字母 A., B., C., D.
            letter_span = item.select_one('span.multi-choice-letter')
            
            if letter_span:
                # 取得選項字母 (A, B, C, D)
                key = letter_span.get('data-choice-letter')
                
                # 取得整個選項的文字內容
                # item.text 包含 letter_span 的文字，但它也會包含選項內容和 'Most Voted' 徽章
                # 為了取得純文字，我們可以用 item 的所有內容減去 letter_span 的內容和徽章
                
                # 簡單方法：先取得選項的所有文字
                full_text = item.text.strip()
                
                # 移除字母部分 (如 A.)
                if letter_span.text:
                    full_text = full_text.replace(letter_span.text.strip(), '', 1) 
                
                # 移除 'Most Voted' 徽章文字 (如果存在)
                value = full_text.replace('Most Voted', '').strip()
                
                # 清理多餘的空白和換行
                value = re.sub(r'\s+', ' ', value)
                
                if key and value:
                    options[key] = value
        
        question_data['options'] = options
        
        # 4. 取得建議答案 (Suggested Answer)
        # 選擇器：'span.correct-answer'
        # 這是最可能因為 JS 動態載入而抓不到的部分
        answer_element = soup.select_one('div.question-answer span.correct-answer')
        
        if answer_element:
            # 答案可能是一個或多個字母 (如 A 或 A, B)
            answer_text = answer_element.text.strip()
            # 假設答案是以逗號分隔的單個字母
            question_data['answer'] = [a.strip() for a in answer_text.split(',')]
            
        else:
             # 如果答案抓不到，先使用空列表作為占位符
             # 這強烈提示你需要改用 Selenium/Playwright
             question_data['answer'] = []
             print(f"  [Warning] Suggested Answer not found for ID {question_data.get('id', 'N/A')}. Content may be loaded by JavaScript.")
        
        # 5. 類型
        # 根據答案的數量和 HTML 結構，我們可以初步判斷類型
        question_data['type'] = "single" if len(question_data['answer']) <= 1 else "multiple"
        
        # 驗證資料
        if question_data['text'] and question_data['options']:
            return question_data
        else:
            print(f"  [Failed] Could not parse text or options for {url}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching question page {url}: {e}")
        return None
    except Exception as e:
        print(f"General error parsing HTML on {url}: {e}")
        return None

# --- Main (主程式) ---

if __name__ == "__main__":
    # 步驟 1: 取得所有相關的 URL
    links = find_discussion_links()
    
    if not links:
        print("No matching discussion links found. Exiting.")
    else:
        print(f"Phase 2: Starting to scrape {len(links)} questions...")
        all_questions = []
        
        for link in links:
            print(f"Scraping question from: {link}")
            data = scrape_question(link)
            if data:
                all_questions.append(data)
                
            # *** 關鍵：速率限制 ***
            time.sleep(2) # 每次抓取後休息 2 秒

        # 步驟 3: 儲存為 JSON
        try:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                # ensure_ascii=False 確保中文或特殊符號正確儲存
                # indent=4 讓 JSON 檔案格式化，易於閱讀
                json.dump(all_questions, f, ensure_ascii=False, indent=4)
            print(f"\nSuccess! Scraped {len(all_questions)} questions and saved to {OUTPUT_FILE}")
            
        except IOError as e:
            print(f"Error writing to file {OUTPUT_FILE}: {e}")