"""
Main entry point for WhatsApp Chat Analyzer
Launches Streamlit web interface
"""

import subprocess
import sys
import os

def main():
    """Main entry point - Launch Streamlit app"""
    print("📱 WhatsApp Chat Analyzer")
    print("=" * 40)
    print("🌐 Launching Streamlit Web App...")
    
    # Check if streamlit_app.py exists
    if not os.path.exists("streamlit_app.py"):
        print("❌ streamlit_app.py not found!")
        print("💡 Make sure streamlit_app.py is in the same directory")
        return
    
    try:
        print("🚀 Starting web interface...")
        print("💡 Your browser will open automatically")
        print("📍 URL: http://localhost:8501")
        print("\n" + "="*40)
        
        # Launch Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
        
    except FileNotFoundError:
        print("❌ Streamlit not installed!")
        print("💡 Install with: pip install streamlit plotly")
        print("💡 Then run: python main.py")
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")
        print("💡 Try running directly: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()