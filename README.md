# 📱 WhatsApp Chat Analyzer

A comprehensive **WhatsApp Chat Analyzer** built with Python and Streamlit that provides detailed insights into your WhatsApp conversations. Analyze message patterns, user behavior, emoji usage, and much more with beautiful interactive visualizations.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### 📊 **Chat Analysis**
- **Basic Statistics**: Total messages, users, conversation duration
- **User Metrics**: Messages per user, average message length
- **Response Time Analysis**: Calculate average response times between users

### 👥 **Individual User Analysis**
- **Personal Statistics**: Detailed breakdown for each participant
- **User Comparison**: Side-by-side comparison of different metrics
- **Fast User Switching**: Optimized performance for instant user selection

### ⏰ **Time Patterns**
- **Hourly Activity**: Message distribution throughout the day
- **Daily Activity**: Conversation patterns across weekdays
- **Peak Hours**: Identify most active communication periods

### 📝 **Content Analysis**
- **Word Frequency**: Most commonly used words (supports Hebrew & English)
- **Emoji Analysis**: Top emojis and emoji usage per user
- **Laugh Detection**: Analyze humor patterns with "חחח", "lol", "lmao" detection
- **Message Bursts**: Detect when users send multiple messages quickly
- **Conversation Starters**: Identify who initiates conversations after inactivity

### 🎨 **Visualizations**
- Interactive charts powered by Plotly
- Hebrew text support with proper RTL rendering
- Responsive design for all screen sizes
- Export-ready visualizations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
   cd whatsapp-chat-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run src/streamlit_app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to access the application.

## 📁 How to Export WhatsApp Chat

### For Android:
1. Open WhatsApp and go to the chat you want to analyze
2. Tap the three dots menu (⋮) → More → Export chat
3. Choose "Without Media" (recommended for faster processing)
4. Save the `.txt` file to your device

### For iPhone:
1. Open WhatsApp and go to the chat you want to analyze
2. Tap the contact/group name at the top
3. Scroll down and tap "Export Chat"
4. Choose "Without Media"
5. Save the `.txt` file to your device

## 🎯 Usage

1. **Upload Your Chat**: Use the file uploader to select your exported WhatsApp chat file
2. **Automatic Processing**: The app automatically detects and parses the chat format
3. **Explore Insights**: Navigate through different tabs to explore various analytics:
   - **Chat Analysis**: Overall conversation statistics
   - **User Analysis**: Individual user breakdowns with fast switching
   - **Time Patterns**: Temporal analysis of conversations
   - **Words & Emojis**: Content and expression analysis

## 🏗️ Project Structure

```
whatsapp-chat-analyzer/
├── src/
│   ├── streamlit_app.py      # Main Streamlit application
│   ├── analyzer.py           # Core analysis functions
│   ├── parser.py             # WhatsApp chat parsing logic
│   ├── visualizer.py         # Chart generation functions
│   ├── ui_components.py      # UI components and layouts
│   ├── file_utils.py         # File handling utilities
│   ├── hebrew_utils.py       # Hebrew text processing
│   └── main.py              # Alternative entry point
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔧 Technical Details

### Performance Optimizations
- **Session State Caching**: Efficient caching system for fast user switching
- **Pre-calculated Analytics**: User data computed once and cached for instant access
- **Optimized DataFrame Operations**: Efficient pandas operations for large chat files

### Language Support
- **Hebrew & English**: Full support for both languages
- **RTL Text Rendering**: Proper right-to-left text display for Hebrew
- **Unicode Emoji Processing**: Advanced emoji extraction and analysis

### Data Privacy
- **Local Processing**: All analysis happens locally on your device
- **No Data Upload**: Your chat data never leaves your computer
- **Memory Management**: Efficient processing of large chat files

## 📊 Supported Chat Formats

The analyzer supports WhatsApp export formats from:
- ✅ Android devices
- ✅ iPhone devices
- ✅ WhatsApp Web
- ✅ Multiple languages (Hebrew, English, and more)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/whatsapp-chat-analyzer/issues) page
2. Create a new issue with detailed description
3. Include your Python version and operating system

## 🚀 Future Enhancements

- [ ] Support for group chat role analysis
- [ ] Sentiment analysis integration
- [ ] Export functionality for analysis results
- [ ] Advanced filtering options
- [ ] Additional visualization types
- [ ] Multi-language stopword support

## ⭐ Star History

If you found this project helpful, please consider giving it a star! It helps others discover the project.

---

**Made with ❤️ and Python**
