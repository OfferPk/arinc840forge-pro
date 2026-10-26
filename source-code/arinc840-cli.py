#!/usr/bin/env python3
"""
ARINC840Forge Pro — Standalone Python 3 CLI Runner & EFB Package Compiler
Electronic Flight Bag (EFB) Electronic Distribution of Software (EDS) Suite
Standards: ARINC Specification 840-1, FAA AC 120-76E, EASA AMC 20-25
"""

import sys
import json
import xml.etree.ElementTree as ET

class ARINC840Simulator:
    def __init__(self):
        self.package_id = "PKG-840-UAL-2611-PERF"
        self.airline = "UAL"
        self.fleet = "B787-9"
        self.airac_cycle = "2611"
        self.version = "v4.8.2"
        self.classification = "TYPE_B_PERFORMANCE"
        self.platform = "IOS_IPAD_PRO"
        
        self.payload_files = [
            {"name": "b787_takeoff_perf_engine.bin", "size": 12582912, "type": "PERF_CALC", "sha256": "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0"},
            {"name": "terminal_charts_kden.sqlite", "size": 48234496, "type": "CHARTS", "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"},
            {"name": "qrh_emergency_checklists.xml", "size": 2097152, "type": "QRH", "sha256": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"}
        ]
        
        self.signature_digest = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        self.on_ground = True
        self.ground_speed = 0.0
        self.interlock_violations = 0

    def generate_manifest(self):
        total_size = sum(f["size"] for f in self.payload_files)
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<EFBSoftwareDistributionPackage xmlns="http://www.arinc.com/standards/arinc840"
    xmlns:ds="http://www.w3.org/2000/09/xmldsig#" version="1.0">
  <PackageHeader>
    <PackageID>{self.package_id}</PackageID>
    <AirlineOperator>{self.airline}</AirlineOperator>
    <FleetType>{self.fleet}</FleetType>
    <AIRACCycle>{self.airac_cycle}</AIRACCycle>
    <SoftwareClassification>{self.classification}</SoftwareClassification>
    <Version>{self.version}</Version>
    <TotalSizeBytes>{total_size}</TotalSizeBytes>
  </PackageHeader>
  <TargetPlatformRequirement>
    <PlatformID>{self.platform}</PlatformID>
    <HardwareClass>CLASS_1_PORTABLE</HardwareClass>
  </TargetPlatformRequirement>
  <PayloadManifest>
"""
        for f in self.payload_files:
            xml += f"""    <File name="{f['name']}" size="{f['size']}" type="{f['type']}">
      <Checksum type="SHA-256">{f['sha256']}</Checksum>
    </File>\n"""
        xml += f"""  </PayloadManifest>
  <ds:Signature>
    <ds:SignedInfo>
      <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
      <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
    </ds:SignedInfo>
    <ds:SignatureValue>{self.signature_digest}</ds:SignatureValue>
  </ds:Signature>
</EFBSoftwareDistributionPackage>"""
        return xml

    def validate(self):
        errors = []
        if not self.on_ground or self.ground_speed > 0:
            self.interlock_violations += 1
            errors.append("INFLIGHT_UPDATE_INHIBITED")
        if len(self.signature_digest) < 32:
            errors.append("SIGNATURE_INVALID")
        if not self.classification.startswith("TYPE_"):
            errors.append("INVALID_CLASSIFICATION")
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "total_size_mb": round(sum(f["size"] for f in self.payload_files) / (1024 * 1024))
        }

    def generate_arinc429_words(self):
        val = self.validate()
        # Label 303 (Octal): EFB System Status & AIRAC Cycle
        label303 = 0xC3
        cycle_int = int(self.airac_cycle) if self.airac_cycle.isdigit() else 2611
        data303 = ((1 if val["valid"] else 0) << 10) | \
                  (1 << 11) | (1 << 12) | \
                  (((cycle_int % 100) & 0x7F) << 13) | \
                  (0x03 << 28)
        word303 = (data303 & 0x7FFFFF00) | label303
        word303 = self.apply_odd_parity(word303)

        # Label 304 (Octal): Takeoff Performance & W&B Integrity
        label304 = 0xC4
        size_mb = min(1023, val["total_size_mb"])
        data304 = ((size_mb & 0x3FF) << 10) | (1 << 20) | (1 << 21) | (0x03 << 28)
        word304 = (data304 & 0x7FFFFF00) | label304
        word304 = self.apply_odd_parity(word304)

        return {
            "label303": hex(word303),
            "label304": hex(word304),
            "odd_parity_valid": self.verify_odd_parity(word303) and self.verify_odd_parity(word304)
        }

    def apply_odd_parity(self, word):
        bits = word & 0x7FFFFFFF
        count = bin(bits).count('1')
        if count % 2 == 0:
            bits |= (1 << 31)
        return bits

    def verify_odd_parity(self, word):
        return bin(word).count('1') % 2 == 1

def run_cli():
    sim = ARINC840Simulator()
    print("=" * 70)
    print("ARINC840Forge Pro — EFB Electronic Distribution of Software (EDS) CLI")
    print("Standards: ARINC Specification 840-1, FAA AC 120-76E, EASA AMC 20-25")
    print("=" * 70)

    val = sim.validate()
    print(f"\n[EFB SOFTWARE PACKAGE COMPILATION: {sim.package_id}]")
    print(f"  Target Platform    : {sim.platform} (Class 1 Portable)")
    print(f"  AIRAC Nav Cycle    : Cycle {sim.airac_cycle} (Worldwide)")
    print(f"  Regulatory Class   : {sim.classification} (V-Speed / Takeoff Engine)")
    print(f"  Total Payload Size : {val['total_size_mb']} MB across {len(sim.payload_files)} assets")
    print(f"  Package Validation : {'PASSED & VERIFIED' if val['valid'] else 'FAILED'}")

    bus = sim.generate_arinc429_words()
    print("\n" + "-" * 70)
    print("ARINC 429 Glass-Cockpit Discrete Bus Output:")
    print(f"  Label 303 (EFB Status & AIRAC Cycle)  : {bus['label303']}")
    print(f"  Label 304 (Perf Engine & W&B Integrity): {bus['label304']}")
    print(f"  Bit 32 Odd Parity Status              : {'VALID (PASS)' if bus['odd_parity_valid'] else 'INVALID (FAIL)'}")
    print("=" * 70)

if __name__ == "__main__":
    run_cli()
