# WhatsApp Message Sender

A Flask web application for sending bulk WhatsApp messages using Selenium automation.

## Features

- 📄 Upload CSV file with phone numbers
- ✍️ Manual entry of phone numbers
- 📱 Automated WhatsApp message sending
- 🎨 Modern, user-friendly web interface
- 🌐 Deployable to Render and other cloud platforms

## Local Setup

### Prerequisites

- Python 3.11+
- Google Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd message-sender
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python send_msg.py
   ```

4. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`

## Deployment to Render

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed step-by-step instructions.

### Quick Start for Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Select **Environment: Docker** (recommended)
4. Render will automatically use the Dockerfile
5. Add environment variable: `HEADLESS=true`
6. Deploy!

## Project Structure

```
message-sender/
├── send_msg.py              # Main Flask application
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration (for Render)
├── render.yaml             # Render configuration (Docker)
├── render-python.yaml      # Render configuration (Python)
├── Procfile                # Process file for Heroku/Render
├── runtime.txt             # Python version specification
├── DEPLOYMENT_GUIDE.md     # Detailed deployment guide
└── README.md               # This file
```

## Usage

1. **Upload CSV File:**
   - Click "Upload CSV File" tab
   - Upload a CSV file with phone numbers in the first column
   - Format: One phone number per row (10 or 12 digits)

2. **Or Enter Numbers Manually:**
   - Click "Enter Numbers Manually" tab
   - Type phone numbers (one per line)

3. **Enter Message:**
   - Type your message in the message box
   - Supports emojis and special characters

4. **Send:**
   - Click "Send Messages to WhatsApp"
   - Scan QR code if prompted (first time only)
   - Wait for messages to be sent

## Phone Number Format

- 10 digits: Automatically adds country code 91 (India)
- 12 digits: Assumes country code is included
- Examples: `9820137264` or `919820137264`

## Important Notes

⚠️ **WhatsApp Web Limitations:**
- Requires QR code scanning for authentication
- Headless mode may have limitations
- WhatsApp may detect automation and block accounts
- Use responsibly and comply with WhatsApp's terms of service

⚠️ **Render Free Tier:**
- Services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Consider upgrading for always-on service

## Troubleshooting

**Chrome/ChromeDriver Issues:**
- Ensure Chrome is installed and up to date
- webdriver-manager handles ChromeDriver automatically
- For headless mode, set `HEADLESS=true` environment variable

**WhatsApp Connection Issues:**
- Ensure you have internet connection
- Check if WhatsApp Web is accessible
- Try scanning QR code again

**Deployment Issues:**
- Check Render build logs for errors
- Verify all files are committed to Git
- Ensure environment variables are set correctly

## License

This project is for educational purposes. Use responsibly and in compliance with WhatsApp's terms of service.

## Support

For deployment help, refer to [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
