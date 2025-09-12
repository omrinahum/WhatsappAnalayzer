# 📱 WhatsApp Chat Analyzer

A comprehensive **WhatsApp Chat Analyzer** built with Python and Streamlit that provides detailed insights into your WhatsApp conversations. Analyze message patterns, user behavior, emoji usage, and much more with interactive visualizations.

##  Features

###  **Chat Analysis**
- **Basic Statistics**: Total messages, users, conversation duration
- **User Metrics**: Messages per user, average message length
- **Response Time Analysis**: Calculate average response times between users

###  **Individual User Analysis**
- **Personal Statistics**: Detailed breakdown for each participant
- **User Comparison**: Side-by-side comparison of different metrics
- **Fast User Switching**: Optimized performance for instant user selection

###  **Time Patterns**
- **Hourly Activity**: Message distribution throughout the day
- **Daily Activity**: Conversation patterns across weekdays
- **Peak Hours**: Identify most active communication periods

###  **Content Analysis**
- **Word Frequency**: Most commonly used words (supports Hebrew & English)
- **Emoji Analysis**: Top emojis and emoji usage per user
- **Laugh Detection**: Analyze humor patterns with "חחח", "lol", "lmao" detection
- **Message Bursts**: Detect when users send multiple messages quickly
- **Conversation Starters**: Identify who initiates conversations after inactivity

###  **Visualizations**
- Interactive charts powered by Plotly
- Hebrew text support with proper RTL rendering
- Responsive design for all screen sizes
- Export-ready visualizations

##  Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/omrinahum/WhatsappAnalayzer.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   cd src
   python main.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to access the application.

##  How to Export WhatsApp Chat

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
WhatsappAnalyzer/
├── src/
│   ├── streamlit_app.py      # Main Streamlit application
│   ├── analyzer.py           # Core analysis functions
│   ├── parser.py             # WhatsApp chat parsing logic
│   ├── visualizer.py         # Chart generation functions
│   ├── ui_components.py      # UI components and layouts
│   ├── file_utils.py         # File handling utilities
│   ├── hebrew_utils.py       # Hebrew text processing
│   └── main.py               # Alternative entry point
├── tests/
│   ├── test.parser.py        # Parser functionallity tests
│   ├── test.analyzer.py      # Analyzer functionallity tests
├── requirements.txt          # Python dependencies
└── README.md                 # This file
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

## ⚡ Optimizations Highlights

- **Optimized Processing Pipeline**: Streamlined parsing and visualization for high performance on large datasets.
- **Intelligent Caching**: Stores pre-computed analytics in session state for instant tab and user switching.
- **High Throughput**: Processes up to 5M characters in under 2 seconds without compromising accuracy.

## 🧪 Testing

The project includes unit tests to ensure reliability.

### Running Tests
```bash
python -m pytest
```

### Test Coverage
- **Parser Testing**: Validates Hebrew and English date format parsing
- **Analysis Functions**: Tests all analysis components (emojis, laughs, response times, etc.)
- **Format Compatibility**: Ensures support for different WhatsApp export formats
- **Edge Cases**: Handles empty files, invalid formats, and error conditions
- **System Message Filtering**: Verifies proper filtering of WhatsApp system messages
