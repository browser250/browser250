import os
import sys
# Enforce strict rendering and sandbox flags while preserving media compatibility layers
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-gpu-compositing --disable-gpu-rasterization --use-gl=swiftshader --disable-dev-shm-usage --disable-blink-features=AutomationControlled --lang=en-US --enable-widevine-cdm --widevine-path=/usr/lib/qt6/plugins/ppapi/libwidevinecdm.so"

import re
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTabWidget)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineProfile, QWebEnginePage, QWebEngineSettings, QWebEngineScript

BLOCKED_KEYWORDS = [
    "amazon-adsystem", "doubleclick", "googleadservices", "googlesyndication",
    "adservice", "analytics", "telemetry", "facebook.net/tr", "pixel",
    "popunder", "adserver", "adskeeper", "taboola", "outbrain"
]

CONFIG_DIR = os.path.expanduser("~/.config/clean_browser")
HISTORY_FILE = os.path.join(CONFIG_DIR, "last_url.txt")
PROFILE_DIR = os.path.join(CONFIG_DIR, "browser_profile")
START_PAGE_FILE = os.path.join(CONFIG_DIR, "start_page.html")
MANIFESTO_PAGE_FILE = os.path.join(CONFIG_DIR, "manifesto.html")

os.makedirs(PROFILE_DIR, exist_ok=True)

def generate_local_pages():
    start_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Browser 250 Home</title>
        <style>
            body { background-color: #121214; color: #e2e8f0; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; min-height: 100vh; margin: 0; padding: 0; }
            .usa-banner { width: 100%; background: linear-gradient(180deg, #0a2540 0%, #051424 100%); border-bottom: 5px solid #cc241d; padding: 50px 20px; text-align: center; }
            .banner-title { color: #ffffff; font-size: 48px; font-weight: 900; letter-spacing: 2px; margin: 0; text-transform: uppercase; text-shadow: 3px 3px 0px #cc241d; }
            .banner-subtitle { color: #3a66a1; font-size: 14px; font-weight: 800; letter-spacing: 6px; margin-top: 10px; text-transform: uppercase; }
            .content-body { max-width: 700px; width: 100%; padding: 60px 20px; text-align: center; }
            .search-box { display: flex; background-color: #1a1a1e; border: 2px solid #2d2d34; border-radius: 28px; padding: 6px 15px; margin-bottom: 50px; }
            .search-box input { background: none; border: none; color: #ffffff; font-size: 16px; flex: 1; padding: 8px; outline: none; }
            .search-box button { background-color: #3a66a1; color: #ffffff; border: none; border-radius: 20px; padding: 0 25px; font-weight: 600; cursor: pointer; }
            .historic-link-container { margin-top: 20px; padding: 20px; background-color: #1a1a1e; border: 1px dashed #3a66a1; border-radius: 12px; display: inline-block; }
            .historic-link { color: #ffffff; font-size: 16px; font-weight: 700; text-decoration: none; text-transform: uppercase; display: flex; align-items: center; gap: 10px; }
        </style>
        <script>
            function performSearch(event) {
                event.preventDefault();
                var queryVal = document.getElementById('query').value;
                if(queryVal.trim() !== "") { console.info("B250_SEARCH:" + queryVal); }
            }
            function openManifesto() { console.info("B250_NAVIGATE:manifesto"); }
        </script>
    </head>
    <body>
        <div class="usa-banner">
            <h1 class="banner-title">Browser 250</h1>
            <div class="banner-subtitle">America's Sovereign Window • Freedom For All</div>
        </div>
        <div class="content-body">
            <form class="search-box" onsubmit="performSearch(event)">
                <input type="text" id="query" placeholder="Search cleanly or enter direct web address..." autocomplete="off" autofocus />
                <button type="submit">Go</button>
            </form>
            <div class="historic-link-container">
                <a href="#" class="historic-link" onclick="openManifesto(); return false;">📜 Read the Sovereign Declaration of Digital Independence</a>
            </div>
        </div>
    </body>
    </html>
    """

    manifesto_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Sovereign Declaration</title>
        <style>
            body { background-color: #121214; color: #e2e8f0; font-family: "Times New Roman", Times, serif; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; min-height: 100vh; margin: 0; padding: 0; box-sizing: border-box; }
            .header-panel { width: 100%; background: #051424; border-bottom: 4px solid #cc241d; padding: 30px 20px; text-align: center; box-sizing: border-box; }
            .header-title { color: #ffffff; font-size: 28px; font-weight: 900; text-transform: uppercase; text-shadow: 2px 2px 0px #cc241d; letter-spacing: 1px; }
            .container { max-width: 800px; width: 100%; padding: 40px 20px; box-sizing: border-box; }
            .btn-back { background-color: #1a1a1e; color: #94a3b8; border: 1px solid #2d2d34; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: 600; text-decoration: none; display: inline-block; margin-bottom: 30px; font-family: sans-serif; }
            .manifesto-paper { background-color: #1a1a1e; border: 1px solid #2d2d34; border-radius: 4px; padding: 50px; text-align: left; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            .section-title { font-size: 20px; color: #ffffff; margin-top: 30px; margin-bottom: 15px; border-bottom: 1px solid #cc241d; padding-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }
            .manifesto-paper p { font-size: 16px; line-height: 1.8; color: #cbd5e1; margin: 0 0 20px 0; text-align: justify; }
            .preamble { font-size: 18px; font-style: italic; color: #ffffff; text-align: center; margin-bottom: 40px; line-height: 1.7; font-weight: bold; }
        </style>
        <script>function goHome() { console.info("B250_NAVIGATE:home"); }</script>
    </head>
    <body>
        <div class="header-panel"><div class="header-title">The Sovereign Declaration of Digital Independence</div></div>
        <div class="container">
            <a href="#" class="btn-back" onclick="goHome(); return false;">◀ Back to Home Search</a>
            <div class="manifesto-paper">
                <p class="preamble">
                    WE THE PEOPLE of the Sovereign Digital Commons, in Order to form a more perfect Union between Man and Machine, establish Privacy, insure domestic Data-Tranquility, provide for the common Defense against corporate Surveillance, promote the general Liberty of Bandwidth, and secure the Blessings of Independence to ourselves and our Posterity, do ordain and establish this Constitution for Browser 250.
                </p>
                
                <div class="section-title">ARTICLE I. Of System Power and the Purge of Corporate Encroachment</div>
                <p>All computational Powers herein granted shall be vested strictly in the User of the local Machine, and shall under no circumstance be shared, bartered, or leaked to any foreign Analytics Array or commercial Entity without an explicit, negotiated Treaty.</p>
                <p>The Core Engine shall function as a closed Citadel. No background Tracking Script, pixelated Beacon, or telemetry Engine shall be permitted Quarter within the memory Sectors of this Container; they shall be considered as unlawful Interlopers and summarily Denied execution.</p>
                
                <div class="section-title">ARTICLE II. Of Defensive Standardization and the Standardized Lie</div>
                <p>Whereas the monopolistic Data-Brokers do employ treacherous Tactics—namely HTML5 Canvas Fingerprinting and WebGL Driver Profiling—to track and mark the individual Citizen across the digital World, the Engine shall exercise the Right of Counter-Stratagem.</p>
                <p>The Engine shall not openly refuse the Queries of these Tracking Servers, lest the Citizen be barred behind Captcha Walls or arbitrarily Lock’d out of the public Web. Instead, the Engine shall answer with a Faultless and Pristine Standardized Lie.</p>
                <p>To every analytical Inquisitor, the Engine shall present identical, generic System Parameters. Let the corporate Analytics Models be utterly Poison’d by the uniformity of our Responses; when they seek to profile the Individual, they shall find only the unbreakable Profile of the Whole.</p>
                
                <div class="section-title">ARTICLE III. Of True Hardware Liberation and Freedom of Movement</div>
                <p>The dedicated Acceleration of the Silicon—namely the Power of the local Graphics Processing Unit—shall be reserved exclusively for the rapid Rendering of true Page Content as directed by the User, and shall never be commandeered to calculate unique Identity Hashes for corporate Profit.</p>
                <p>Freedom of Access shall not be abridged. The secure Pipelines of media Playback and standard Encryption shall remain intact, ensuring the Citizen may cross the digital Boundaries of any public Portal or Streaming Service without throwing security Flags or paying the Toll of his private Identity.</p>
            </div>
        </div>
    </body>
    </html>
    """

    with open(START_PAGE_FILE, "w") as f: f.write(start_html.strip())
    with open(MANIFESTO_PAGE_FILE, "w") as f: f.write(manifesto_html.strip())

generate_local_pages()

class CleanRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url_string = info.requestUrl().toString().lower()
        for keyword in BLOCKED_KEYWORDS:
            if keyword in url_string:
                info.block(True)
                return
        if "netflix.com" in url_string or "accounts.google.com" in url_string or "googleusercontent.com" in url_string:
            mobile_agent = b"Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
            info.setHttpHeader(b"User-Agent", mobile_agent)

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent, window_manager):
        super().__init__(profile, parent)
        self.window_manager = window_manager

    def javaScriptConsoleMessage(self, level, message, line, source_id):
        if "B250_SEARCH:" in message:
            raw_query = message.split("B250_SEARCH:")[1].strip()
            if not raw_query: return
            if raw_query.startswith('http://') or raw_query.startswith('https://') or ('.' in raw_query and ' ' not in raw_query):
                target_url = raw_query if raw_query.startswith('http') else 'https://' + raw_query
            else:
                clean_query = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_query)
                clean_query = " ".join(clean_query.split())
                target_url = 'https://html.duckduckgo.com/html/?q=' + QUrl.toPercentEncoding(clean_query).data().decode('utf-8')
            self.window_manager.load_url_in_current_tab(target_url)
        elif "B250_NAVIGATE:" in message:
            target = message.split("B250_NAVIGATE:")[1].strip()
            if target == "manifesto":
                self.window_manager.load_url_in_current_tab(QUrl.fromLocalFile(MANIFESTO_PAGE_FILE).toString())
            elif target == "home":
                self.window_manager.load_url_in_current_tab(QUrl.fromLocalFile(START_PAGE_FILE).toString())

class CleanBrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser 250")
        self.resize(1280, 720)

        self.browser_profile = QWebEngineProfile("CleanProfile", self)
        self.browser_profile.setPersistentStoragePath(PROFILE_DIR)
        
        secure_agent = "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
        self.browser_profile.setHttpUserAgent(secure_agent)
        
        self.interceptor = CleanRequestInterceptor()
        self.browser_profile.setUrlRequestInterceptor(self.interceptor)
        
        self.apply_modern_styling()
        self.setup_defensive_scripts()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        control_layout = QHBoxLayout()
        self.back_button = QPushButton("◀")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setFixedWidth(40)
        
        self.forward_button = QPushButton("▶")
        self.forward_button.clicked.connect(self.go_forward)
        self.forward_button.setFixedWidth(40)
        
        self.refresh_button = QPushButton("⟳")
        self.refresh_button.clicked.connect(self.handle_refresh)
        self.refresh_button.setFixedWidth(40)
        
        self.home_button = QPushButton("⌂")
        self.home_button.clicked.connect(self.handle_home)
        self.home_button.setFixedWidth(40)
        
        self.url_input = QLineEdit()
        self.url_input.returnPressed.connect(self.navigate_to_url)
        
        self.new_tab_button = QPushButton("+ Tab")
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab())
        self.new_tab_button.setFixedWidth(75)
        
        control_layout.addWidget(self.back_button)
        control_layout.addWidget(self.forward_button)
        control_layout.addWidget(self.refresh_button)
        control_layout.addWidget(self.home_button)
        control_layout.addWidget(self.url_input)
        control_layout.addWidget(self.new_tab_button)
        main_layout.addLayout(control_layout)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        main_layout.addWidget(self.tabs)

        self.add_new_tab(QUrl.fromLocalFile(START_PAGE_FILE).toString(), "Home")

    def apply_modern_styling(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #121214; }
            QPushButton { background-color: #1a1a1e; color: #e2e8f0; border: 1px solid #2d2d34; border-radius: 8px; padding: 6px; font-weight: bold; font-size: 13px; }
            QPushButton:hover { background-color: #2d2d34; border-color: #3a66a1; }
            QLineEdit { background-color: #1a1a1e; color: #ffffff; border: 1px solid #2d2d34; border-radius: 8px; padding: 6px 12px; font-size: 14px; }
            QTabWidget::panel { border: 1px solid #2d2d34; background-color: #121214; }
            QTabBar::tab { background-color: #1a1a1e; color: #94a3b8; border: 1px solid #2d2d34; padding: 8px 16px; margin-right: 4px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
            QTabBar::tab:selected { background-color: #121214; color: #ffffff; font-weight: bold; }
        """)

    def setup_defensive_scripts(self):
        js_payload = """
        (function() {
            if (window.RTCPeerConnection) {
                window.RTCPeerConnection = function() { return {}; };
                window.RTCPeerConnection.prototype.createOffer = function() { return Promise.reject(); };
                window.RTCPeerConnection.prototype.createAnswer = function() { return Promise.reject(); };
            }
            if (window.location.hostname.includes('google.com') || window.location.hostname.includes('netflix.com')) return;

            const maskProperties = {
                platform: { get: () => 'Linux armv8l' },
                hardwareConcurrency: { get: () => 8 },
                deviceMemory: { get: () => 8 }
            };
            Object.defineProperties(navigator, maskProperties);

            const spoofWebGL = function(ctx) {
                if (!ctx) return;
                const nativeGetParameter = ctx.getParameter;
                ctx.getParameter = function(pname) {
                    if (pname === 0x9245) return 'Intel Open Source Technology Center';
                    if (pname === 0x9246) return 'Mesa DRI Intel(R) HD Graphics (Skylake GT2)';
                    return nativeGetParameter.apply(this, arguments);
                };
            };

            const nativeGetContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type, attributes) {
                const ctx = nativeGetContext.apply(this, arguments);
                if (type === 'webgl' || type === 'webgl2' || type === 'experimental-webgl') {
                    spoofWebGL(ctx);
                }
                return ctx;
            };

            const nativeProtoGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(pname) {
                if (pname === 0x9245) return 'Intel Open Source Technology Center';
                if (pname === 0x9246) return 'Mesa DRI Intel(R) HD Graphics (Skylake GT2)';
                return nativeProtoGetParameter.apply(this, arguments);
            };
            if (window.WebGL2RenderingContext) {
                const nativeProtoGetParameter2 = WebGL2RenderingContext.prototype.getParameter;
                WebGL2RenderingContext.prototype.getParameter = function(pname) {
                    if (pname === 0x9245) return 'Intel Open Source Technology Center';
                    if (pname === 0x9246) return 'Mesa DRI Intel(R) HD Graphics (Skylake GT2)';
                    return nativeProtoGetParameter2.apply(this, arguments);
                };
            }

            const nativeGetComputedStyle = window.getComputedStyle;
            window.getComputedStyle = function(element, pseudoElt) {
                const style = nativeGetComputedStyle.apply(this, arguments);
                if (element && element.style && element.style.fontFamily) {
                    const fam = element.style.fontFamily.toLowerCase();
                    if (fam.includes('segoe') || fam.includes('arial') || fam.includes('calibri') || fam.includes('tahoma') || fam.includes('times')) {
                        Object.defineProperty(element, 'offsetWidth', { get: () => 140, configurable: true });
                        Object.defineProperty(element, 'offsetHeight', { get: () => 22, configurable: true });
                    }
                }
                return style;
            };

            const nativePerformanceNow = performance.now;
            performance.now = function() { return Math.floor(nativePerformanceNow.apply(this, arguments) / 100) * 100; };
        })();
        """
        defensive_script = QWebEngineScript()
        defensive_script.setSourceCode(js_payload)
        defensive_script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        defensive_script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        defensive_script.setRunsOnSubFrames(True)
        self.browser_profile.scripts().insert(defensive_script)

    def add_new_tab(self, url_str=None, label="New Tab"):
        if url_str is None: url_str = QUrl.fromLocalFile(START_PAGE_FILE).toString()
        browser_view = QWebEngineView()
        web_page = CustomWebEnginePage(self.browser_profile, browser_view, self)
        browser_view.setPage(web_page)
        
        browser_view.loadFinished.connect(lambda chg, bv=browser_view: self.dump_telemetry_to_console(bv))
        
        settings = web_page.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        
        browser_view.urlChanged.connect(lambda qurl, bv=browser_view: self.update_url_bar(qurl, bv))
        browser_view.titleChanged.connect(lambda title, bv=browser_view: self.update_tab_title(title, bv))
        
        index = self.tabs.addTab(browser_view, label)
        browser_view.setUrl(QUrl(url_str))
        self.tabs.setCurrentIndex(index)
        return browser_view

    def dump_telemetry_to_console(self, bv):
        url = bv.url().toString()
        if "creepjs" in url or "browserleaks" in url or "turnstile" in url:
            bv.page().toPlainText(lambda text, target_url=url: print(f"\n[LIVE METRICS DUMP FOR {target_url}]\n{text}\n[END DUMP]\n", flush=True))

    def load_url_in_current_tab(self, target_url):
        current_bv = self.get_current_browser()
        if current_bv:
            if isinstance(target_url, str):
                current_bv.setUrl(QUrl(target_url))
            else:
                current_bv.setUrl(target_url)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            if widget: widget.deleteLater()
            self.tabs.removeTab(index)
        else:
            self.get_current_browser().setUrl(QUrl.fromLocalFile(START_PAGE_FILE))

    def get_current_browser(self): return self.tabs.currentWidget()

    def navigate_to_url(self):
        target_url = self.url_input.text().strip()
        if not any(target_url.startswith(s) for s in ["http://", "https://", "file://"]):
            target_url = "https://" + target_url
        current_bv = self.get_current_browser()
        if current_bv: current_bv.setUrl(QUrl(target_url))

    def update_url_bar(self, qurl, browser_view):
        if browser_view == self.get_current_browser():
            url_str = qurl.toString()
            self.url_input.setText("" if url_str.startswith("file://") else url_str)

    def update_tab_title(self, title, browser_view):
        index = self.tabs.indexOf(browser_view)
        if index != -1:
            if "start_page.html" in title or "manifesto.html" in title or not title: title = "Browser 250"
            self.tabs.setTabText(index, title[:15] + "..." if len(title) > 15 else title)

    def tab_changed(self, index):
        current_bv = self.get_current_browser()
        if current_bv:
            url_str = current_bv.url().toString()
            self.url_input.setText("" if url_str.startswith("file://") else url_str)

    def go_back(self):
        current_bv = self.get_current_browser()
        if current_bv and current_bv.history().canGoBack(): current_bv.back()

    def go_forward(self):
        current_bv = self.get_current_browser()
        if current_bv and current_bv.history().canGoForward(): current_bv.forward()

    def handle_refresh(self):
        current_bv = self.get_current_browser()
        if current_bv: current_bv.reload()

    def handle_stop(self):
        current_bv = self.get_current_browser()
        if current_bv: current_bv.stop()

    def handle_home(self):
        current_bv = self.get_current_browser()
        if current_bv:
            current_bv.setUrl(QUrl.fromLocalFile(START_PAGE_FILE))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser_window = CleanBrowserWindow()
    browser_window.show()
    sys.exit(app.exec())
