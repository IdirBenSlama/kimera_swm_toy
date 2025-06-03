#!/usr/bin/env python3
"""
Setup Translation Services for Kimera
====================================

Interactive script to help configure translation services.
"""

import os
import sys
import json
import yaml
from pathlib import Path
from getpass import getpass


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")


def print_section(text):
    """Print a section header."""
    print("\n" + "-"*40)
    print(text)
    print("-"*40)


def check_google_setup():
    """Check and help set up Google Translate."""
    print_section("Google Translate Setup")
    
    # Check for existing credentials
    creds_env = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    project_env = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    if creds_env and os.path.exists(creds_env):
        print("✅ Google credentials found at:", creds_env)
        print("✅ Project ID:", project_env or "Not set")
        return True
    
    print("❌ Google Translate not configured")
    print("\nTo set up Google Translate:")
    print("1. Go to https://console.cloud.google.com")
    print("2. Create a new project or select existing")
    print("3. Enable the Cloud Translation API")
    print("4. Create a service account key (JSON)")
    print("5. Download the key file")
    
    setup = input("\nDo you have a service account key file? (y/n): ").lower()
    
    if setup == 'y':
        key_path = input("Enter path to your service account key JSON: ").strip()
        if os.path.exists(key_path):
            project_id = input("Enter your Google Cloud project ID: ").strip()
            
            # Create .env file
            env_content = f"""# Google Cloud Translation
GOOGLE_APPLICATION_CREDENTIALS={os.path.abspath(key_path)}
GOOGLE_CLOUD_PROJECT={project_id}
"""
            
            with open('.env', 'a') as f:
                f.write(env_content)
            
            print("\n✅ Google Translate configuration saved to .env")
            print("   Restart your terminal or run: source .env")
            return True
    
    return False


def check_deepl_setup():
    """Check and help set up DeepL."""
    print_section("DeepL Translation Setup")
    
    # Check for existing API key
    api_key = os.getenv('DEEPL_API_KEY')
    
    if api_key:
        print("✅ DeepL API key found")
        return True
    
    print("❌ DeepL not configured")
    print("\nTo set up DeepL:")
    print("1. Go to https://www.deepl.com/pro-api")
    print("2. Sign up for free or paid account")
    print("3. Get your API key from the account page")
    
    setup = input("\nDo you have a DeepL API key? (y/n): ").lower()
    
    if setup == 'y':
        api_key = getpass("Enter your DeepL API key: ").strip()
        
        # Test if it's a free or pro key
        endpoint = "https://api-free.deepl.com/v2" if api_key.endswith(":fx") else "https://api.deepl.com/v2"
        
        # Add to .env
        env_content = f"""
# DeepL Translation
DEEPL_API_KEY={api_key}
DEEPL_API_ENDPOINT={endpoint}
"""
        
        with open('.env', 'a') as f:
            f.write(env_content)
        
        print("\n✅ DeepL configuration saved to .env")
        return True
    
    return False


def check_huggingface_setup():
    """Check and help set up Hugging Face."""
    print_section("Hugging Face Local Translation Setup")
    
    try:
        import transformers
        import torch
        print("✅ Transformers library installed")
        print(f"✅ PyTorch installed (device: {'cuda' if torch.cuda.is_available() else 'cpu'})")
        return True
    except ImportError:
        print("❌ Transformers not installed")
        print("\nTo set up Hugging Face translations:")
        print("1. Install transformers: pip install transformers torch")
        print("2. First run will download models (~500MB each)")
        print("3. Models are cached locally for offline use")
        
        install = input("\nInstall transformers now? (y/n): ").lower()
        
        if install == 'y':
            print("\nInstalling transformers and torch...")
            os.system(f"{sys.executable} -m pip install transformers torch")
            return True
    
    return False


def create_config_file():
    """Create or update translation configuration file."""
    print_section("Creating Configuration File")
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    config_path = config_dir / "translation_config.yaml"
    
    # Determine default service based on what's available
    services_available = []
    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        services_available.append('google')
    if os.getenv('DEEPL_API_KEY'):
        services_available.append('deepl')
    
    try:
        import transformers
        services_available.append('huggingface')
    except ImportError:
        pass
    
    if not services_available:
        services_available.append('mock')
    
    default_service = services_available[0]
    
    # Create configuration
    config = {
        'default_service': default_service,
        'services': {
            'google': {
                'credentials_path': '${GOOGLE_APPLICATION_CREDENTIALS}',
                'project_id': '${GOOGLE_CLOUD_PROJECT}',
                'rate_limit': 10,
                'batch_size': 100
            },
            'deepl': {
                'api_key': '${DEEPL_API_KEY}',
                'api_endpoint': '${DEEPL_API_ENDPOINT}',
                'rate_limit': 5
            },
            'huggingface': {
                'model_name': 'Helsinki-NLP/opus-mt-en-es',
                'device': 'cuda' if check_cuda() else 'cpu',
                'cache_dir': '~/.cache/huggingface'
            }
        },
        'cache': {
            'enabled': True,
            'backend': 'sqlite',
            'ttl': 86400,
            'sqlite_path': 'cache/translation_cache.db'
        },
        'languages': {
            'supported': ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh', 'ar', 'hi'],
            'default_source': None,
            'default_target': 'en'
        }
    }
    
    # Write configuration
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Configuration saved to {config_path}")
    print(f"   Default service: {default_service}")
    print(f"   Available services: {', '.join(services_available)}")


def check_cuda():
    """Check if CUDA is available."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


def test_configuration():
    """Test the configuration."""
    print_section("Testing Configuration")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from kimera.linguistics.translation_config import get_config
        from kimera.linguistics.translation_service import create_translation_service
        
        # Load configuration
        config = get_config()
        validation = config.validate()
        
        print("Configuration validation:")
        print(f"  Valid: {'✅' if validation['valid'] else '❌'}")
        print(f"  Available services: {', '.join(validation['available_services'])}")
        
        if validation['errors']:
            print("\nErrors:")
            for error in validation['errors']:
                print(f"  ❌ {error}")
        
        if validation['warnings']:
            print("\nWarnings:")
            for warning in validation['warnings']:
                print(f"  ⚠️  {warning}")
        
        # Try to create service
        if validation['available_services']:
            print(f"\nTesting {validation['available_services'][0]} service...")
            service = create_translation_service(
                service_type=validation['available_services'][0],
                enable_cache=True
            )
            print("✅ Service created successfully")
            
            # Try a simple translation
            import asyncio
            async def test():
                result = await service.translate("Hello world", "es")
                print(f"\nTest translation:")
                print(f"  Input: Hello world")
                print(f"  Output: {result.translated_text}")
                print(f"  Service: {result.metadata.get('service', 'unknown')}")
            
            asyncio.run(test())
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")


def main():
    """Main setup flow."""
    print_header("Kimera Translation Services Setup")
    
    print("This script will help you configure translation services")
    print("for multi-language analysis in Kimera.\n")
    
    print("Available translation services:")
    print("1. Google Translate (cloud-based, requires API key)")
    print("2. DeepL (cloud-based, free tier available)")
    print("3. Hugging Face (local, free, requires ~2GB disk space)")
    print("4. Mock (built-in, for testing only)")
    
    # Check each service
    google_ok = check_google_setup()
    deepl_ok = check_deepl_setup()
    hf_ok = check_huggingface_setup()
    
    # Create configuration file
    create_config_file()
    
    # Test configuration
    test_configuration()
    
    # Summary
    print_header("Setup Complete")
    
    print("Services configured:")
    print(f"  Google Translate: {'✅' if google_ok else '❌'}")
    print(f"  DeepL: {'✅' if deepl_ok else '❌'}")
    print(f"  Hugging Face: {'✅' if hf_ok else '❌'}")
    print(f"  Mock: ✅ (always available)")
    
    print("\nNext steps:")
    print("1. If you added API keys, restart your terminal or run:")
    print("   export $(cat .env | xargs)")
    print("2. Run the translation test:")
    print("   python examples/test_translation_services.py")
    print("3. Try multi-language analysis:")
    print("   python examples/multilingual_analysis_demo.py")
    
    if not (google_ok or deepl_ok or hf_ok):
        print("\n⚠️  No real translation service configured.")
        print("   Kimera will use mock translations for testing.")
        print("   Configure at least one service for real multi-language analysis.")


if __name__ == "__main__":
    main()