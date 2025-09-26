import os

# Create necessary folders for the backend
def create_backend_structure():
    """Create the required folder structure for the backend"""
    
    # Create charts directory if it doesn't exist
    charts_dir = 'charts'
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
        print(f"✅ Created {charts_dir}/ directory")
    else:
        print(f"✅ {charts_dir}/ directory already exists")
    
    # Create __pycache__ will be created automatically by Python
    print("✅ Backend folder structure ready!")
    print("\nNext steps:")
    print("1. Create virtual environment: python -m venv venv")
    print("2. Activate virtual environment:")
    print("   - Windows: venv\\Scripts\\activate")
    print("   - Mac/Linux: source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Run the server: python app.py")

if __name__ == "__main__":
    create_backend_structure()