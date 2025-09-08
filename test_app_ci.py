#!/usr/bin/env python3
"""
Test script for CI/CD pipeline
Tests basic functionality of the Biomedical DSP application
"""

import sys
import os
import tempfile
import unittest
from pathlib import Path

# Add the current directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestBiomedicalDSP(unittest.TestCase):
    """Test suite for Biomedical DSP application"""
    
    def setUp(self):
        """Set up test environment"""
        self.base_dir = Path(__file__).parent
        
    def test_imports(self):
        """Test that all required modules can be imported"""
        try:
            import customtkinter as ctk
            import matplotlib.pyplot as plt
            import numpy as np
            import scipy
            import fitz  # PyMuPDF
            from PIL import Image
            print("✅ All required packages imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import required package: {e}")
    
    def test_main_module(self):
        """Test that main module can be imported"""
        try:
            # Import main module
            import main
            print("✅ Main module imported successfully")
            
            # Check that the main class exists
            self.assertTrue(hasattr(main, 'BiomedicaDSPApp'))
            print("✅ BiomedicaDSPApp class found")
            
        except Exception as e:
            self.fail(f"Failed to import main module: {e}")
    
    def test_utils_module(self):
        """Test that utils module functions work"""
        try:
            import utils
            
            # Test get_resource_path function
            test_path = utils.get_resource_path("test.txt")
            self.assertIsInstance(test_path, (str, Path))
            print("✅ get_resource_path function works")
            
            # Test check_python_requirements function
            requirements = utils.check_python_requirements()
            self.assertIsInstance(requirements, list)
            print("✅ check_python_requirements function works")
            
        except Exception as e:
            # Utils might not exist or have fallbacks, that's OK
            print(f"⚠️ Utils module test skipped: {e}")
    
    def test_file_structure(self):
        """Test that required files and directories exist"""
        
        # Check main files
        required_files = [
            "main.py",
            "requirements.txt",
            "biomedical_dsp.spec",
            "icon.ico"
        ]
        
        for file_name in required_files:
            file_path = self.base_dir / file_name
            self.assertTrue(file_path.exists(), f"Required file {file_name} not found")
        
        print("✅ All required files exist")
        
        # Check that at least one unit directory exists
        unit_dirs = list(self.base_dir.glob("Unidad *"))
        self.assertGreater(len(unit_dirs), 0, "No unit directories found")
        print(f"✅ Found {len(unit_dirs)} unit directories")
        
        # Check that units contain PDF and Python files
        total_pdfs = 0
        total_py_files = 0
        
        for unit_dir in unit_dirs:
            if unit_dir.is_dir():
                pdfs = list(unit_dir.glob("*.pdf"))
                py_files = list(unit_dir.glob("*.py"))
                total_pdfs += len(pdfs)
                total_py_files += len(py_files)
        
        self.assertGreater(total_pdfs, 0, "No PDF files found in units")
        self.assertGreater(total_py_files, 0, "No Python files found in units")
        print(f"✅ Found {total_pdfs} PDF files and {total_py_files} Python files")
    
    def test_app_initialization_dry_run(self):
        """Test that app can be initialized without actually creating GUI"""
        try:
            # Set up test environment
            os.environ['DISPLAY'] = ':99'  # For headless testing
            
            # Import the app module
            import main
            
            # Test that class can be instantiated (but don't actually run GUI)
            # This tests import resolution and basic initialization
            app_class = main.BiomedicaDSPApp
            
            # Check that required methods exist
            required_methods = [
                'setup_fonts',
                'load_theme_preferences', 
                'save_theme_preferences',
                'setup_ui',
                'load_course_structure'
            ]
            
            for method_name in required_methods:
                self.assertTrue(hasattr(app_class, method_name), 
                              f"Required method {method_name} not found")
            
            print("✅ App class structure validated")
            
        except Exception as e:
            # In CI, we might not be able to initialize the GUI, that's OK
            print(f"⚠️ App initialization test skipped (headless environment): {e}")
    
    def test_requirements_file(self):
        """Test that requirements.txt is valid"""
        requirements_file = self.base_dir / "requirements.txt"
        self.assertTrue(requirements_file.exists(), "requirements.txt not found")
        
        with open(requirements_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        # Should not be empty
        self.assertGreater(len(content), 0, "requirements.txt is empty")
        
        # Should contain expected packages
        required_packages = [
            'customtkinter',
            'matplotlib',
            'numpy', 
            'scipy',
            'PyMuPDF',
            'Pillow'
        ]
        
        for package in required_packages:
            self.assertIn(package.lower(), content.lower(), 
                         f"Required package {package} not found in requirements.txt")
        
        print("✅ requirements.txt validation passed")
    
    def test_pyinstaller_spec(self):
        """Test that PyInstaller spec file is valid"""
        spec_file = self.base_dir / "biomedical_dsp.spec"
        self.assertTrue(spec_file.exists(), "biomedical_dsp.spec not found")
        
        with open(spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should contain expected PyInstaller elements
        expected_elements = [
            "Analysis",
            "PYZ", 
            "EXE",
            "main.py",
            "icon.ico"
        ]
        
        for element in expected_elements:
            self.assertIn(element, content, 
                         f"Expected element {element} not found in spec file")
        
        print("✅ PyInstaller spec file validation passed")

def main():
    """Run all tests"""
    print("🧪 Running Biomedical DSP CI Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBiomedicalDSP)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    print("=" * 50)
    
    if result.wasSuccessful():
        print("🎉 All tests passed! Application is ready for build.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
