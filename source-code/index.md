## 

ARINC840Forge Pro

v1.0.0 \| EFB Electronic Distribution of Software (ARINC 840 & FAA AC 120-76E) Studio

EFB EDS SYNC VERIFIED

### 

Target EFB Hardware & Cycle

Target EFB Device Platform Apple iPad Pro (Class 1 Portable / iPadOS 18\) Microsoft Surface Pro (Class 2 Mounted / Win11) Boeing 787 / A350 Installed Class 3 Cockpit Display

AIRAC Navigation Database Cycle

Software Class: **TYPE B (PERFORMANCE)**

Regulatory Standard: **FAA AC 120-76E**

Fleet Applicability: **B787-9 (UAL FLEET)**

### 

Airworthiness Interlocks (AC 120-76E)

Aircraft on Ground (Parked)

---

Ground Speed \< 0.1 kt

---

Pilot Swap Confirmation

---

Rapid Decompression Certified

---

Evaluate Operational Suitability

### 

ARINC 840 XML Distribution Manifest

Schema: ARINC 840-1 XML-DSig • RSA-SHA256 Authority: United Airlines Flight Ops

### 

Type B Takeoff Performance & W\&B Engine (B787-9)

V1 Decision  
**148 kt**

VR Rotation  
**154 kt**

V2 Climbout  
**160 kt**

**b787\_takeoff\_perf\_engine.bin**  
12.0 MB • Type B Performance • SHA-256 Valid

**DEPLOYED**

**terminal\_charts\_kden.sqlite**  
46.0 MB • AIRAC Cycle 2611 Charts • SHA-256 Valid

**DEPLOYED**

Deploy AIRAC Update Corrupt Signature Test

### 

ARINC 429 Cockpit Bus Output

Label 303 (EFB Status & AIRAC Cycle):

0x83C308C3 \[ODD PARITY VALID\]

Label 304 (Perf Engine & W\&B Integrity):

0x813C00C4 \[ODD PARITY VALID\]

Bit 32 Parity: **ODD PARITY VERIFIED (PASS)**

### 

10-Point Normative Auditor

✓ ARINC 840 Manifest XML Conformance Verified

✓ FAA AC 120-76E Type A/B Classification Valid

✓ W3C XML-DSig RSA-SHA256 Authenticity Confirmed

✓ Multi-Asset Cryptographic Hash Checksums Match

✓ In-Flight Database Swap Inhibit Armed

Run Full 10-Point Audit