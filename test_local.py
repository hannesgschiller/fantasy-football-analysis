#!/usr/bin/env python3
"""
Test script to verify all components work before uploading to GitHub
"""

import sys
import os
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing imports...")
    
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly',
        'matplotlib'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("✅ All packages imported successfully!")
        return True

def test_analyzer():
    """Test if our analyzer works"""
    print("\n🧪 Testing analyzer...")
    
    try:
        from fantasy_analyzer_simple import FantasyFootballAnalyzer
        print("✅ Analyzer imported successfully")
        
        # Test with sample data
        analyzer = FantasyFootballAnalyzer("/Users/hannesschiller/Documents/NFL Fantasy data")
        analyzer.load_weekly_data()
        analyzer.load_season_data()
        
        print(f"✅ Loaded data for {len(analyzer.weekly_data)} weeks")
        print(f"✅ Loaded season data for {len(analyzer.season_data)} positions")
        
        # Test getting top performers
        qb_top = analyzer.get_top_performers('QB', week=None, top_n=3)
        if qb_top is not None:
            print("✅ Top performers analysis working")
            print(f"   Top QB: {qb_top.iloc[0]['Player']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analyzer test failed: {e}")
        return False

def test_streamlit_app():
    """Test if Streamlit app can be imported"""
    print("\n🧪 Testing Streamlit app...")
    
    try:
        # Test if we can import the app functions
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Test if our app file exists and can be imported
        if os.path.exists('streamlit_app.py'):
            print("✅ streamlit_app.py exists")
            
            # Try to import the main function
            import importlib.util
            spec = importlib.util.spec_from_file_location("streamlit_app", "streamlit_app.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'main'):
                print("✅ main() function found")
            else:
                print("⚠️ main() function not found")
                
        else:
            print("❌ streamlit_app.py not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Streamlit app test failed: {e}")
        return False

def test_data_access():
    """Test if data can be accessed"""
    print("\n🧪 Testing data access...")
    
    data_path = "/Users/hannesschiller/Documents/NFL Fantasy data"
    
    if os.path.exists(data_path):
        print(f"✅ Data path exists: {data_path}")
        
        # Check for week folders
        week_folders = [f for f in os.listdir(data_path) if f.startswith('Week')]
        print(f"✅ Found {len(week_folders)} week folders")
        
        # Check for season data
        season_path = os.path.join(data_path, "Full Season")
        if os.path.exists(season_path):
            print("✅ Full Season data exists")
        else:
            print("⚠️ Full Season data not found")
            
        return True
    else:
        print(f"❌ Data path not found: {data_path}")
        print("   The app will use sample data for demonstration")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        'streamlit_app.py',
        'fantasy_analyzer_simple.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present!")
        return True

def main():
    """Run all tests"""
    print("🏈 Fantasy Football Analysis - Local Test Suite")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Package Imports", test_imports),
        ("Data Access", test_data_access),
        ("Analyzer", test_analyzer),
        ("Streamlit App", test_streamlit_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your dashboard is ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Run: python run_analysis.py (choose option 4 for dashboard)")
        print("2. Or run: streamlit run streamlit_app.py")
        print("3. Deploy to GitHub when ready")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please fix issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    main() 