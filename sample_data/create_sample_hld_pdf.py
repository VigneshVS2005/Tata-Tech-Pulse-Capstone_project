import fitz

def generate_sample_pdf_v1(output_path: str):
    doc = fitz.open()
    
    # Page 1: Architecture & Overview
    page1 = doc.new_page()
    text1 = """AUTOSAR High-Level Design Specification: Engine Control Unit (ECU)
Document Version: v1.0
Classification: Tata Tech Confidential

1. Executive Overview
This document specifies the software architecture for the Engine Control Unit (ECU). The ECU manages fuel injection, ignition timing, and throttle position for 4-cylinder engines.

2. Software Components
The architecture consists of the following primary software components:
- Component: EngineManagementSwc
- Component: FuelInjectionSwc
- Component: IgnitionControlSwc
- Component: ThrottlePositionSwc

3. Interfaces and Ports
- Interface: If_EngineSpeed (Provides engine RPM calculation signals to FuelInjectionSwc and IgnitionControlSwc).
- Interface: If_ThrottleCmd (Port: PPort_ThrottlePosition to RPort_ThrottleActuator).
- Interface: If_FuelInjectionTiming (Port: PPort_FuelPulseWidth).

4. Signal Specifications
- Signal: Sig_EngineRPM (Data type: uint16, Range: 0 - 8000 RPM)
- Signal: Sig_ThrottleAngle (Data type: float32, Range: 0.0 - 100.0 %)
- Signal: Sig_InjectionDuration (Data type: uint32, Unit: microseconds)
"""
    page1.insert_text((50, 50), text1, fontsize=11)
    
    # Page 2: Safety & Diagnostics
    page2 = doc.new_page()
    text2 = """5. Safety & Fault Handling
- Functional Safety Target: ISO 26262 ASIL-C requirement for overspeed prevention.
- Fault Reaction: If Sig_EngineRPM exceeds 7500 RPM for more than 50ms, FuelInjectionSwc must enter limp-home mode.

6. Dependencies & Data Flow
- Component FuelInjectionSwc depends on If_EngineSpeed and Sig_ThrottleAngle to compute Sig_InjectionDuration.
- Component IgnitionControlSwc relies on If_EngineSpeed to calculate ignition spark angle.
"""
    page2.insert_text((50, 50), text2, fontsize=11)
    
    doc.save(output_path)
    doc.close()
    print(f"Generated {output_path}")

def generate_sample_pdf_v2(output_path: str):
    doc = fitz.open()
    
    # Page 1: Architecture & Overview v2.0
    page1 = doc.new_page()
    text1 = """AUTOSAR High-Level Design Specification: Engine Control Unit (ECU)
Document Version: v2.0
Classification: Tata Tech Confidential

1. Executive Overview
This document specifies the updated software architecture for the Engine Control Unit (ECU) supporting hybrid powertrain integration.

2. Software Components
The architecture consists of the following primary software components:
- Component: EngineManagementSwc
- Component: FuelInjectionSwc
- Component: IgnitionControlSwc
- Component: BatteryManagerSwc (NEW in v2.0)
- Component: HybridTorqueSwc (NEW in v2.0)

3. Interfaces and Ports
- Interface: If_EngineSpeed (Provides engine RPM calculation signals).
- Interface: If_ThrottleCmd (Port: PPort_ThrottlePosition to RPort_ThrottleActuator).
- Interface: If_FuelInjectionTiming (Port: PPort_FuelPulseWidth).
- Interface: If_HybridTorqueReq (NEW Interface for hybrid power distribution).

4. Signal Specifications
- Signal: Sig_EngineRPM (Data type: uint16, Range: 0 - 8000 RPM)
- Signal: Sig_ThrottleAngle (Data type: float32, Range: 0.0 - 100.0 %)
- Signal: Sig_BatterySoC (NEW Signal: State of Charge, Range: 0 - 100 %)
"""
    page1.insert_text((50, 50), text1, fontsize=11)
    doc.save(output_path)
    doc.close()
    print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_sample_pdf_v1("sample_data/AUTOSAR_HLD_EngineControl_v1.pdf")
    generate_sample_pdf_v2("sample_data/AUTOSAR_HLD_EngineControl_v2.pdf")
