#!/usr/bin/env python3
"""
ARINC840Forge Pro — Automated Unit & Regression Test Suite
10 Comprehensive Verification Tests for ARINC 840 EFB Package Compiler & Auditor
"""

import unittest
from arinc840_cli import ARINC840Simulator

class TestARINC840ForgePro(unittest.TestCase):
    def setUp(self):
        self.sim = ARINC840Simulator()

    def test_01_xml_manifest_generation(self):
        """Test 01: ARINC 840 XML EFB Distribution Manifest Generation"""
        xml = self.sim.generate_manifest()
        self.assertIn("<EFBSoftwareDistributionPackage", xml)
        self.assertIn("xmlns=\"http://www.arinc.com/standards/arinc840\"", xml)
        self.assertIn("<PackageID>PKG-840-UAL-2611-PERF</PackageID>", xml)

    def test_02_payload_file_manifest(self):
        """Test 02: Multi-File Payload Manifest & SHA-256 Digests"""
        self.assertEqual(len(self.sim.payload_files), 3)
        for f in self.sim.payload_files:
            self.assertEqual(len(f["sha256"]), 64)
            self.assertTrue(f["size"] > 0)

    def test_03_digital_signature_presence(self):
        """Test 03: W3C XML Digital Signature (XML-DSig) Integrity"""
        xml = self.sim.generate_manifest()
        self.assertIn("<ds:Signature", xml)
        self.assertIn("<ds:SignatureValue>", xml)
        self.assertGreaterEqual(len(self.sim.signature_digest), 32)

    def test_04_ground_safety_interlock_airborne(self):
        """Test 04: In-Flight EFB Update Inhibit (Airborne Protection)"""
        self.sim.on_ground = False # Airborne state
        val = self.sim.validate()
        self.assertFalse(val["valid"])
        self.assertIn("INFLIGHT_UPDATE_INHIBITED", val["errors"])

    def test_05_ground_speed_interlock(self):
        """Test 05: Active Taxi Speed Inhibit (>0.0 kt)"""
        self.sim.on_ground = True
        self.sim.ground_speed = 18.0 # Taxiing
        val = self.sim.validate()
        self.assertFalse(val["valid"])
        self.assertIn("INFLIGHT_UPDATE_INHIBITED", val["errors"])

    def test_06_type_b_classification_validation(self):
        """Test 06: FAA AC 120-76E Type B Performance Classification"""
        self.assertTrue(self.sim.classification.startswith("TYPE_B"))
        val = self.sim.validate()
        self.assertTrue(val["valid"])

    def test_07_arinc429_label303_parity(self):
        """Test 07: ARINC 429 Label 303 Bit 32 Odd Parity Verification"""
        words = self.sim.generate_arinc429_words()
        word303_int = int(words["label303"], 16)
        bit_count = bin(word303_int).count('1')
        self.assertEqual(bit_count % 2, 1, f"Label 303 parity must be odd (bits: {bit_count})")

    def test_08_arinc429_label304_parity(self):
        """Test 08: ARINC 429 Label 304 Bit 32 Odd Parity Verification"""
        words = self.sim.generate_arinc429_words()
        word304_int = int(words["label304"], 16)
        bit_count = bin(word304_int).count('1')
        self.assertEqual(bit_count % 2, 1, f"Label 304 parity must be odd (bits: {bit_count})")

    def test_09_payload_size_mb_aggregation(self):
        """Test 09: Total EFB Payload Size Aggregation (MB)"""
        val = self.sim.validate()
        self.assertGreater(val["total_size_mb"], 50)
        self.assertLess(val["total_size_mb"], 70)

    def test_10_interlock_violation_counter(self):
        """Test 10: Interlock Violation Interception Counter Increment"""
        initial = self.sim.interlock_violations
        self.sim.on_ground = False
        self.sim.validate()
        self.assertEqual(self.sim.interlock_violations, initial + 1)

if __name__ == "__main__":
    unittest.main()
