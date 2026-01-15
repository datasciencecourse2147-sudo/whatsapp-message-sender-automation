import os
import time
import csv
import pyperclip
from flask import Flask, render_template_string, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Message Sender</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 700px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            border-bottom: 2px solid #e0e0e0;
        }
        .tab {
            padding: 12px 24px;
            background: none;
            border: none;
            color: #666;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
        }
        .tab:hover {
            color: #667eea;
        }
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }
        .hint {
            font-size: 12px;
            color: #888;
            font-weight: normal;
            margin-left: 5px;
        }
        input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 2px dashed #667eea;
            border-radius: 8px;
            background: #f8f9ff;
            cursor: pointer;
            transition: all 0.3s;
        }
        input[type="file"]:hover {
            border-color: #764ba2;
            background: #f0f1ff;
        }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .numbers-textarea {
            min-height: 120px;
        }
        .message-textarea {
            min-height: 250px;
        }
        .btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        .btn:active {
            transform: translateY(0);
        }
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .file-info {
            margin-top: 10px;
            padding: 10px;
            background: #e8f4f8;
            border-radius: 5px;
            font-size: 13px;
            color: #0c5460;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 WhatsApp Message Sender</h1>
        <p class="subtitle">Send bulk messages to WhatsApp contacts</p>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('csv')">📄 Upload CSV File</button>
            <button class="tab" onclick="switchTab('manual')">✍️ Enter Numbers Manually</button>
        </div>
        
        <form id="messageForm" enctype="multipart/form-data">
            <!-- CSV Upload Tab -->
            <div id="csvTab" class="tab-content active">
                <div class="form-group">
                    <label for="csvFile">📄 Upload CSV File <span class="hint">(Phone numbers in first column)</span></label>
                    <input type="file" id="csvFile" name="csvFile" accept=".csv">
                    <div class="file-info" id="fileInfo"></div>
                </div>
            </div>
            
            <!-- Manual Entry Tab -->
            <div id="manualTab" class="tab-content">
                <div class="form-group">
                    <label for="phoneNumbers">📞 Enter Phone Numbers <span class="hint">(One per line)</span></label>
                    <textarea id="phoneNumbers" name="phoneNumbers" class="numbers-textarea" placeholder="9820137264
917021429836
9820137234
918201572643

Enter one phone number per line..."></textarea>
                </div>
            </div>
            
            <!-- Message (Common for both) -->
            <div class="form-group">
                <label for="message">✉️ Message to Send</label>
                <textarea id="message" name="message" required class="message-textarea" placeholder="Enter your message here...">बदलाचा नवा संकल्प…
राष्ट्रवादी काँग्रेस पक्षाच्या अधिकृत उमेदवार
सौ. राजेश्री सुधीर फुलपगार
अ प्रवर्ग – प्रभाग क्रमांक १४
आपल्या प्रभागाच्या विकासासाठी, सक्षम आणि विश्वासार्ह नेतृत्वासाठी
⏰ घड्याळ या चिन्हासमोर बटन क्रमांक ५ दाबून
सौ. राजेश्री सुधीर फुलपगार यांना
प्रचंड बहुमताने विजयी करा.
दिनांक : १५ जानेवारी
🕖 वेळ : सकाळी ७:०० ते सायंकाळी ५:३०
आपले मत – आपला अधिकार.
प्रभागाच्या उज्ज्वल भविष्यासाठी नक्की मतदान करा.</textarea>
            </div>
            
            <button type="submit" class="btn" id="sendBtn">
                🚀 Send Messages to WhatsApp
            </button>
        </form>
        
        <div class="status" id="status"></div>
    </div>

    <script>
        const form = document.getElementById('messageForm');
        const statusDiv = document.getElementById('status');
        const sendBtn = document.getElementById('sendBtn');
        const fileInput = document.getElementById('csvFile');
        const fileInfo = document.getElementById('fileInfo');
        const phoneNumbers = document.getElementById('phoneNumbers');
        
        let activeTab = 'csv';

        function switchTab(tab) {
            activeTab = tab;
            
            // Update tab buttons
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            
            // Update tab content
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            if (tab === 'csv') {
                document.getElementById('csvTab').classList.add('active');
            } else {
                document.getElementById('manualTab').classList.add('active');
            }
        }

        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                const file = e.target.files[0];
                fileInfo.style.display = 'block';
                fileInfo.textContent = `Selected: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
            }
        });

        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Validation
            if (activeTab === 'csv' && !fileInput.files.length) {
                statusDiv.className = 'status error';
                statusDiv.style.display = 'block';
                statusDiv.textContent = 'Please upload a CSV file or switch to manual entry.';
                return;
            }
            
            if (activeTab === 'manual' && !phoneNumbers.value.trim()) {
                statusDiv.className = 'status error';
                statusDiv.style.display = 'block';
                statusDiv.textContent = 'Please enter at least one phone number.';
                return;
            }
            
            const formData = new FormData(form);
            formData.append('inputMode', activeTab);
            
            sendBtn.disabled = true;
            sendBtn.textContent = '⏳ Processing...';
            
            statusDiv.className = 'status info';
            statusDiv.style.display = 'block';
            statusDiv.textContent = 'Starting WhatsApp automation... Please scan QR code if prompted.';
            
            try {
                const response = await fetch('/send', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    statusDiv.className = 'status success';
                    statusDiv.textContent = result.message;
                } else {
                    statusDiv.className = 'status error';
                    statusDiv.textContent = 'Error: ' + result.message;
                }
            } catch (error) {
                statusDiv.className = 'status error';
                statusDiv.textContent = 'Error: ' + error.message;
            } finally {
                sendBtn.disabled = false;
                sendBtn.textContent = '🚀 Send Messages to WhatsApp';
            }
        });
    </script>
</body>
</html>
"""

def normalize_phone_number(phone):
    """Normalize phone number to include country code"""
    phone = str(phone).strip().replace('+', '').replace('-', '').replace(' ', '')
    
    # If 10 digits, add 91 (India country code)
    if len(phone) == 10:
        phone = '91' + phone
    
    return phone

def read_csv_numbers(file_path):
    """Read phone numbers from CSV file"""
    numbers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row and row[0].strip():
                normalized = normalize_phone_number(row[0])
                numbers.append(normalized)
    return numbers

def parse_manual_numbers(numbers_text):
    """Parse phone numbers from manual text input"""
    numbers = []
    lines = numbers_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:
            normalized = normalize_phone_number(line)
            numbers.append(normalized)
    return numbers

def send_whatsapp_messages(phone_numbers, message):
    """Send WhatsApp messages using Selenium"""
    try:
        print(f"Found {len(phone_numbers)} phone numbers")
        
        # Setup Chromium options (for Docker deployment)
        chrome_options = Options()

        # Use Chromium binary (set in Dockerfile)
        if os.getenv('CHROME_BIN'):
            chrome_options.binary_location = os.getenv('CHROME_BIN')

        # Headless mode for server environments (Render)
        if os.getenv('RENDER') or os.getenv('HEADLESS', 'false').lower() == 'true':
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_argument('--disable-notifications')

        # Fix for server environments (Linux/Render)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # User data directory for session persistence
        user_data_dir = os.path.abspath('./whatsapp_session')
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        chrome_options.add_argument('--profile-directory=Default')

        # Initialize driver with Chromium
        if os.getenv('CHROMEDRIVER_PATH'):
            # Use system-installed ChromeDriver
            service = Service(os.getenv('CHROMEDRIVER_PATH'))
        else:
            # Fallback to ChromeDriverManager
            service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Open WhatsApp Web
        driver.get('https://web.whatsapp.com')
        print("Please scan QR code if prompted...")
        
        # Wait for WhatsApp to load
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        print("WhatsApp Web loaded successfully!")
        
        success_count = 0
        failed_numbers = []
        
        for idx, phone in enumerate(phone_numbers, 1):
            try:
                print(f"Sending message {idx}/{len(phone_numbers)} to {phone}")
                
                # Open chat with phone number
                url = f'https://web.whatsapp.com/send?phone={phone}'
                driver.get(url)
                
                # Wait for chat to load
                time.sleep(3)
                
                # Find message input box
                message_box = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
                
                # Click to focus
                message_box.click()
                time.sleep(0.5)
                
                # Copy message to clipboard
                pyperclip.copy(message)
                
                # Paste using Ctrl+V (works with emojis)
                message_box.send_keys(Keys.CONTROL, 'v')
                
                time.sleep(1)
                
                # Press Enter to send
                message_box.send_keys(Keys.ENTER)
                
                success_count += 1
                print(f"✓ Message sent successfully to {phone}")
                
                # Wait between messages to avoid being blocked
                time.sleep(5)
                
            except Exception as e:
                print(f"✗ Failed to send message to {phone}: {str(e)}")
                failed_numbers.append(phone)
                continue
        
        print(f"\n{'='*50}")
        print(f"Process completed!")
        print(f"Total numbers: {len(phone_numbers)}")
        print(f"Successful: {success_count}")
        print(f"Failed: {len(failed_numbers)}")
        
        if failed_numbers:
            print(f"\nFailed numbers: {', '.join(failed_numbers)}")
        
        # Keep browser open for 5 seconds
        time.sleep(5)
        driver.quit()
        
        return {
            'total': len(phone_numbers),
            'success': success_count,
            'failed': len(failed_numbers),
            'failed_numbers': failed_numbers
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        raise e

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send', methods=['POST'])
def send_messages():
    try:
        message = request.form.get('message', '')
        input_mode = request.form.get('inputMode', 'csv')
        
        if not message.strip():
            return jsonify({'success': False, 'message': 'Message cannot be empty'})
        
        phone_numbers = []
        
        # Handle CSV upload
        if input_mode == 'csv':
            if 'csvFile' not in request.files:
                return jsonify({'success': False, 'message': 'No file uploaded'})
            
            file = request.files['csvFile']
            
            if file.filename == '':
                return jsonify({'success': False, 'message': 'No file selected'})
            
            # Save uploaded file
            upload_folder = 'uploads'
            os.makedirs(upload_folder, exist_ok=True)
            csv_path = os.path.join(upload_folder, 'temp_numbers.csv')
            file.save(csv_path)
            
            # Read numbers from CSV
            phone_numbers = read_csv_numbers(csv_path)
            
            # Clean up
            os.remove(csv_path)
        
        # Handle manual entry
        else:
            manual_numbers = request.form.get('phoneNumbers', '')
            if not manual_numbers.strip():
                return jsonify({'success': False, 'message': 'Please enter at least one phone number'})
            
            phone_numbers = parse_manual_numbers(manual_numbers)
        
        if not phone_numbers:
            return jsonify({'success': False, 'message': 'No valid phone numbers found'})
        
        # Send messages
        result = send_whatsapp_messages(phone_numbers, message)
        
        return jsonify({
            'success': True,
            'message': f"✓ Completed! Sent {result['success']}/{result['total']} messages successfully."
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))

    print("="*50)
    print("WhatsApp Message Sender")
    print("="*50)
    print(f"\nStarting web server on port {port}...")
    print("Production mode (Render)")
    print("\nPress Ctrl+C to stop the server")
    print("="*50)
    app.run(host='0.0.0.0', port=port)