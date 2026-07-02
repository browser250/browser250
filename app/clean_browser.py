import sys
import os
import re
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTabWidget)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineProfile, QWebEnginePage, QWebEngineSettings

# Core Ad and Tracking Blocker Rule Set
BLOCKED_KEYWORDS = [
    "amazon-adsystem", "doubleclick", "googleadservices", "googlesyndication",
    "adservice", "analytics", "telemetry", "facebook.net/tr", "pixel",
    "popunder", "adserver", "adskeeper", "taboola", "outbrain"
]

CONFIG_DIR = os.path.expanduser("~/.config/clean_browser")
HISTORY_FILE = os.path.join(CONFIG_DIR, "last_url.txt")
PROFILE_DIR = os.path.join(CONFIG_DIR, "browser_profile")
START_PAGE_FILE = os.path.join(CONFIG_DIR, "start_page.html")

os.makedirs(PROFILE_DIR, exist_ok=True)

def generate_start_page():
    """Generates a native local home page featuring Browser 250 as the center of a USA-themed page banner."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Browser 250 Home</title>
        <style>
            body {
                background-color: #121214;
                color: #e2e8f0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                min-height: 100vh;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            .usa-banner {
                width: 100%;
                background: linear-gradient(180deg, #0a2540 0%, #051424 100%);
                border-bottom: 5px solid #cc241d;
                padding: 40px 20px;
                text-align: center;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                position: relative;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .banner-content {
                position: relative;
                display: inline-block;
                padding: 0 60px;
            }
            .banner-title {
                color: #ffffff;
                font-size: 46px;
                font-weight: 900;
                letter-spacing: 2px;
                margin: 0;
                text-transform: uppercase;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.3), 3px 3px 0px #cc241d;
            }
            .banner-subtitle {
                color: #3a66a1;
                font-size: 13px;
                font-weight: 800;
                letter-spacing: 6px;
                margin-top: 8px;
                text-transform: uppercase;
                text-shadow: 0 0 5px rgba(58, 102, 161, 0.5);
            }
            .star-decoration {
                color: #ffffff;
                font-size: 20px;
                opacity: 0.8;
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                text-shadow: 0 0 8px rgba(255,255,255,0.6);
            }
            .star-left { left: 10px; }
            .star-right { right: 10px; }

            .content-body {
                max-width: 650px;
                width: 100%;
                padding: 40px 20px;
                text-align: center;
                box-sizing: border-box;
            }
            .search-box {
                display: flex;
                background-color: #1a1a1e;
                border: 2px solid #2d2d34;
                border-radius: 28px;
                padding: 6px 15px;
                margin-bottom: 40px;
                transition: border-color 0.2s, box-shadow 0.2s;
            }
            .search-box:focus-within {
                border-color: #3a66a1;
                box-shadow: 0 0 10px rgba(58, 102, 161, 0.3);
            }
            .search-box input {
                background: none;
                border: none;
                color: #ffffff;
                font-size: 16px;
                flex: 1;
                padding: 8px;
                outline: none;
            }
            .search-box button {
                background-color: #3a66a1;
                color: #ffffff;
                border: none;
                border-radius: 20px;
                padding: 0 20px;
                font-weight: 600;
                cursor: pointer;
                transition: background-color 0.15s;
            }
            .search-box button:hover {
                background-color: #4a77b2;
            }
            .manifesto-card {
                background-color: #1a1a1e;
                border: 1px solid #2d2d34;
                border-radius: 12px;
                padding: 25px;
                text-align: left;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }
            .manifesto-card h2 {
                font-size: 18px;
                color: #ffffff;
                margin-top: 0;
                margin-bottom: 15px;
                border-bottom: 1px solid #2d2d34;
                padding-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .manifesto-card p {
                font-size: 14px;
                line-height: 1.6;
                color: #94a3b8;
                margin: 0 0 15px 0;
            }
            .badge-list {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 15px;
            }
            .badge {
                font-size: 11px;
                font-weight: 700;
                padding: 4px 10px;
                border-radius: 4px;
                text-transform: uppercase;
                background-color: #221c1c;
                color: #ef4444;
                border: 1px solid #451a1a;
            }
            .badge.free {
                background-color: #1c221c;
                color: #22c55e;
                border: 1px solid #1a3a1a;
            }
        </style>
        <script>
            function performSearch(event) {
                event.preventDefault();
                console.log("B250_SEARCH:" + document.getElementById('query').value);
            }
        </script>
    </head>
    <body>
        <div class="usa-banner">
            <div class="banner-content">
                <span class="star-decoration star-left">★ ★ ★</span>
                <h1 class="banner-title">Browser 250</h1>
                <span class="star-decoration star-right">★ ★ ★</span>
            </div>
            <div class="banner-subtitle">America's Sovereign Window • Freedom For All</div>
        </div>
        
        <div class="content-body">
            <form class="search-box" onsubmit="performSearch(event)">
                <input type="text" id="query" placeholder="Search cleanly or enter direct web address..." autocomplete="off" autofocus />
                <button type="submit">Go</button>
            </form>
            
            <div class="manifesto-card">
                <h2>🛡️ Project Manifesto</h2>
                <p>
                    <strong>Browser 250</strong> is built natively to act as a raw, glass window straight to the open web. It operates with zero telemetry, zero logging data, and zero corporate alignment. It answers to no advertising networks or surveillance layers.
                </p>
                <p>
                    This utility functions independently of corporate monetization strategies and is distributed as an unconditional, free sovereign tool for all users to navigate the web with pure isolation.
                </p>
                <div class="badge-list">
                    <div class="badge">Blocks Analytics</div>
                    <div class="badge">Blocks Facebook Trackers</div>
                    <div class="badge">Blocks Ad Servers</div>
                    <div class="badge.free free">100% Free For All</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    with open(START_PAGE_FILE, "w") as f:
        f.write(html_content.strip())

# Initialize start page content
generate_start_page()

class CleanRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url_string = info.requestUrl().toString().lower()
        
        for keyword in BLOCKED_KEYWORDS:
            if keyword in url_string:
                info.block(True)
                return
                
        if "accounts.google.com" in url_string or "googleusercontent.com" in url_string:
            firefox_agent = b"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
            info.setHttpHeader(b"User-Agent", firefox_agent)

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent, window_manager):
        super().__init__(profile, parent)
        self.window_manager = window_manager

    def javaScriptConsoleMessage(self, level, message, line, source_id):
        if message.startswith("B250_SEARCH:"):
            raw_query = message.replace("B250_SEARCH:", "").strip()
            if not raw_query:
                return
                
            if raw_query.startswith('http://') or raw_query.startswith('https://') or ('.' in raw_query and ' ' not in raw_query):
                target_url = raw_query if raw_query.startswith('http') else 'https://' + raw_query
            else:
                # STRIP ALL PUNCTUATION: Force replace all symbols with white spaces to keep DuckDuckGo from blocking the URL
                clean_query = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_query)
                # Collapse continuous internal spaces down to clean individual spaces
                clean_query = " ".join(clean_query.split())
                target_url = 'https://html.duckduckgo.com/html/?q=' + QUrl.toPercentEncoding(clean_query).data().decode('utf-8')
            
            self.window_manager.load_url_in_current_tab(target_url)

class CleanBrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser 250")
        self.resize(1280, 720)

        # Global Browser Profile Setup
        self.browser_profile = QWebEngineProfile("CleanProfile", self)
        self.browser_profile.setPersistentStoragePath(PROFILE_DIR)
        self.browser_profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        
        secure_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        self.browser_profile.setHttpUserAgent(secure_agent)
        
        self.interceptor = CleanRequestInterceptor()
        self.browser_profile.setUrlRequestInterceptor(self.interceptor)

        # Main Layout Container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)

        # Top Navigation Bar
        control_layout = QHBoxLayout()
        
        self.back_button = QPushButton("◀ Back")
        self.back_button.clicked.connect(self.go_back)
        
        self.forward_button = QPushButton("Forward ▶")
        self.forward_button.clicked.connect(self.go_forward)

        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.clicked.connect(self.handle_refresh)

        self.stop_button = QPushButton("❌ Stop")
        self.stop_button.clicked.connect(self.handle_stop)

        self.home_button = QPushButton("🏠 Home")
        self.home_button.clicked.connect(self.handle_home)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL and press Enter...")
        self.url_input.returnPressed.connect(self.navigate_to_url)
        
        self.new_tab_button = QPushButton("[+] New Tab")
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab())

        self.session_button = QPushButton("Keep Me Logged In: ON")
        self.session_button.setCheckable(True)
        self.session_button.setChecked(True)
        self.session_button.clicked.connect(self.toggle_session_mode)
        
        control_layout.addWidget(self.back_button)
        control_layout.addWidget(self.forward_button)
        control_layout.addWidget(self.refresh_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.home_button)
        control_layout.addWidget(self.url_input)
        control_layout.addWidget(self.new_tab_button)
        control_layout.addWidget(self.session_button)
        main_layout.addLayout(control_layout)

        # Multi-Tab Window Widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        main_layout.addWidget(self.tabs)

        # Force Home Page on Initial App Startup
        local_start_url = QUrl.fromLocalFile(START_PAGE_FILE).toString()
        self.add_new_tab(local_start_url, "Home")

    def add_new_tab(self, url_str=None, label="New Tab"):
        if url_str is None:
            url_str = QUrl.fromLocalFile(START_PAGE_FILE).toString()
            
        browser_view = QWebEngineView()
        web_page = CustomWebEnginePage(self.browser_profile, browser_view, self)
        browser_view.setPage(web_page)
        
        settings = web_page.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        
        browser_view.urlChanged.connect(lambda qurl, bv=browser_view: self.update_url_bar(qurl, bv))
        browser_view.titleChanged.connect(lambda title, bv=browser_view: self.update_tab_title(title, bv))
        
        index = self.tabs.addTab(browser_view, label)
        browser_view.setUrl(QUrl(url_str))
        self.tabs.setCurrentIndex(index)
        return browser_view

    def load_url_in_current_tab(self, target_url):
        current_bv = self.get_current_browser()
        if current_bv:
            current_bv.setUrl(QUrl(target_url))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            if widget:
                widget.deleteLater()
            self.tabs.removeTab(index)
        else:
            local_start = QUrl.fromLocalFile(START_PAGE_FILE).toString()
            self.get_current_browser().setUrl(QUrl(local_start))

    def get_current_browser(self):
        return self.tabs.currentWidget()

    def navigate_to_url(self):
        target_url = self.url_input.text().strip()
        if not target_url.startswith("http://") and not target_url.startswith("https://") and not target_url.startswith("file://"):
            target_url = "https://" + target_url
        current_bv = self.get_current_browser()
        if current_bv:
            current_bv.setUrl(QUrl(target_url))

    def update_url_bar(self, qurl, browser_view):
        if browser_view == self.get_current_browser():
            url_str = qurl.toString()
            if url_str.startswith("file://"):
                self.url_input.setText("")
            else:
                self.url_input.setText(url_str)
                with open(HISTORY_FILE, "w") as f:
                    f.write(url_str)

    def update_tab_title(self, title, browser_view):
        index = self.tabs.indexOf(browser_view)
        if index != -1:
            if "start_page.html" in title or not title:
                title = "Browser 250"
            short_title = title[:15] + "..." if len(title) > 15 else title
            self.tabs.setTabText(index, short_title)

    def tab_changed(self, index):
        current_bv = self.get_current_browser()
        if current_bv:
            url_str = current_bv.url().toString()
            if url_str.startswith("file://"):
                self.url_input.setText("")
            else:
                self.url_input.setText(url_str)

    def go_back(self):
        current_bv = self.get_current_browser()
        if current_bv and current_bv.history().canGoBack():
            current_bv.back()

    def go_forward(self):
        current_bv = self.get_current_browser()
        if current_bv and current_bv.history().canGoForward():
            current_bv.forward()

    def handle_refresh(self):
        current_bv = self.get_current_browser()
        if current_bv:
            current_bv.reload()

    def handle_stop(self):
        current_bv = self.get_current_browser()
        if current_bv:
            current_bv.stop()

    def handle_home(self):
        current_bv = self.get_current_browser()
        if current_bv:
            local_start = QUrl.fromLocalFile(START_PAGE_FILE).toString()
            current_bv.setUrl(QUrl(local_start))

    def toggle_session_mode(self):
        if self.session_button.isChecked():
            self.session_button.setText("Keep Me Logged In: ON")
            self.browser_profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        else:
            self.session_button.setText("Keep Me Logged In: OFF")
            self.browser_profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
            self.browser_profile.clearHttpCache()
            
    def closeEvent(self, event):
        if not self.session_button.isChecked():
            import shutil
            self.browser_profile.clearHttpCache()
            cookie_store = self.browser_profile.cookieStore()
            cookie_store.deleteAllCookies()
            try:
                shutil.rmtree(PROFILE_DIR, ignore_errors=True)
                os.makedirs(PROFILE_DIR, exist_ok=True)
            except Exception:
                pass
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser_window = CleanBrowserWindow()
    browser_window.show()
    sys.exit(app.exec())
