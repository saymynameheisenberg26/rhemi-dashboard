"""
Helper script to generate a password hash for authentication
"""
from passlib.hash import pbkdf2_sha256
import sys


def main():
    print("\n🔐 Password Hash Generator")
    print("=" * 40)
    print()
    
    if len(sys.argv) > 1:
        # Password provided as argument
        password = sys.argv[1]
    else:
        # Prompt for password
        password = input("Enter your password: ")
    
    if not password:
        print("❌ Password cannot be empty!")
        return
    
    # Generate hash
    password_hash = pbkdf2_sha256.hash(password)
    
    print()
    print("✅ Password hash generated!")
    print()
    print("Copy this hash to your .env file as PASSWORD_HASH:")
    print()
    print(password_hash)
    print()
    print("Example .env entry:")
    print(f"PASSWORD_HASH={password_hash}")
    print()


if __name__ == "__main__":
    main()
