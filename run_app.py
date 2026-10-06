import subprocess
import time
import sys
import os

def main():
    print("==========================================================")
    print("🚘 Automotive Engineering AI Platform Launcher")
    print("   Tata Tech Pulse - Digital Track Case Study 1")
    print("==========================================================")
    
    # Generate sample PDFs if not exist
    if not os.path.exists("sample_data/AUTOSAR_HLD_EngineControl_v1.pdf"):
        print("Generating sample AUTOSAR HLD PDF files...")
        subprocess.run([sys.executable, "sample_data/create_sample_hld_pdf.py"])
        
    print("\n[1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...")
    backend_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"
    ])
    
    time.sleep(3)
    
    print("[2/2] Starting Streamlit Frontend Interface...")
    frontend_proc = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "frontend/app.py"
    ])
    
    print("\n✨ Platform is active!")
    print("• Backend API Docs: http://127.0.0.1:8000/docs")
    print("• Streamlit Frontend: http://localhost:8501")
    print("Press Ctrl+C to stop both services.\n")
    
    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping platform services...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    main()
