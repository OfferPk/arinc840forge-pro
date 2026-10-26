# ARINC Specification 840-1 Electronic Flight Bag (EFB) Electronic Distribution of Software Specification

**Document ID**: ARINC840-SPEC-2026-v1.0  
**Normative Standards**: ARINC Specification 840-1, FAA AC 120-76E, EASA AMC 20-25, RTCA DO-178C, ICAO Annex 6  
**Classification**: Commercial Aircraft Electronic Flight Bag & Operational Data Distribution Standard

---

## 1\. Executive Summary & Operational Scope

The **ARINC Specification 840-1 (Electronic Flight Bag Electronic Distribution of Software \- EFB EDS)** standardizes the XML packaging schemas, cryptographic authentication, ground-to-cockpit synchronization, and operational validation protocols for Electronic Flight Bags (EFBs).

With global commercial airlines transitioning all flight deck documentation, terminal approach charts, and takeoff performance tools to mobile and mounted EFBs, ARINC 840 standardizes:

1. Automated XML Software Distribution Manifest (`efb-manifest.xml`) authoring.  
2. W3C XML Digital Signatures (XML-DSig) for tamper-evident airworthiness verification.  
3. Rigorous regulatory classification under FAA AC 120-76E and EASA AMC 20-25 (Type A Document Viewers vs Type B Interactive Aeronautical Calculations).  
4. Multi-platform hardware target binding (Class 1 Portable iPads, Class 2 Mounted Windows devices, Class 3 Installed Displays).  
5. Airworthiness safety interlocks inhibiting in-flight database swaps or unapproved software updates.

---

## 2\. FAA AC 120-76E & EASA AMC 20-25 Software Classification

ARINC 840 strictly enforces regulatory boundaries across EFB software applications:

- **Type A Software**: Document viewing applications (Aircraft Flight Manuals, QRH checklists, company flight operations policy documents, airport directory manuals). Failure of Type A software does not directly impact flight safety.  
- **Type B Software**: Interactive aeronautical calculations (takeoff & landing performance engines, V-speed calculation \$V\_1, V\_R, V\_2\$, weight and balance CG calculators, interactive airport moving maps). Requires operational suitability verification, airline pilot training, and Principal Operations Inspector (POI) approval.  
- **Type C Software**: Certified airborne avionics software running on installed avionics systems, governed strictly by RTCA DO-178C.

---

## 3\. Cryptographic Packaging & Manifest Architecture

The distribution package includes an XML manifest (`efb-manifest.xml`) defining:

- `<PackageHeader>`: Unique package identifier, airline ICAO code, aircraft fleet type (e.g., Boeing 787-9), active worldwide AIRAC cycle (e.g., Cycle 2611), and application version.  
- `<TargetPlatformRequirement>`: Restricts execution to authorized hardware targets (e.g., `IOS_IPAD_PRO`, `WIN_SURFACE_PRO`, `AVIONICS_CLASS3_EFB`).  
- `<PayloadManifest>`: Itemizes all binary calculation engines, navigation database tables, SQLite chart archives, and XML checklists with mandatory 256-bit SHA-256 cryptographic hashes.  
- `<ds:Signature>`: Complies with W3C XML-DSig utilizing RSA-SHA256, verifying that performance database curves originate exclusively from the authorized Airline Flight Operations Engineering department.

---

## 4\. In-Flight Safety Interlocks & Lossless Rollback

To prevent pilot distraction or critical computation errors during active flight:

- **Ground Inhibit**: Software updates, chart cycle roll-overs, and takeoff performance engine swaps are strictly prohibited when the aircraft is airborne (ground speed \> 0 kt).  
- **Atomic Rollback**: If cryptographic signature validation fails or an unexpected termination occurs during update ingestion, the EFB runtime immediately reverts to the previous certified AIRAC navigation baseline.

---

## 5\. ARINC 429 Glass-Cockpit Discrete Bus Output

The installed EFB interface LRU broadcasts operational health onto the low-speed aircraft ARINC 429 bus:

- **Label 303 (Octal)**: EFB System Status & AIRAC Cycle  
  - Bit 11: EFB Distribution Package Validated (1: Verified)  
  - Bit 12: Ground Sync Link Active (1: Synchronized)  
  - Bit 13: Type B Operational Authorization Active (1: Cleared)  
  - Bits 14-20: Active AIRAC Cycle Code (e.g. 11 for 2611\)  
  - Bits 29-30: SSM (Normal Operation: 11b)  
  - Bit 32: Odd Parity  
- **Label 304 (Octal)**: EFB Takeoff Performance & Weight/Balance Integrity  
  - Bits 11-20: Package Payload Size in Megabytes (0 \- 1023 MB)  
  - Bit 21: V-Speed Takeoff Engine Integrity (1: Validated)  
  - Bit 22: Weight & Balance Center of Gravity Check (1: Safe MAC Envelope)  
  - Bits 29-30: SSM  
  - Bit 32: Odd Parity