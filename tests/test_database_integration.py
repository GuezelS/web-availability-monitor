"""
Integration test for database functionality.
Tests all database operations together.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.monitor import check_website
from src.database import (
    init_database,
    save_check,
    get_all_checks,
    get_recent_checks,
    get_checks_by_url,
    get_check_count,
    cleanup_old_checks
)


def test_database_integration():
    """
    Test complete database workflow.
    """
    print("🧪 Starting Database Integration Test\n")
    
    # Step 1: Initialize database
    print("1️⃣  Initializing database...")
    init_database()
    print()
    
    # Step 2: Check multiple websites and save results
    print("2️⃣  Checking websites and saving results...")
    urls = [
        'https://google.com',
        'https://github.com',
        'https://python.org'
    ]
    
    for url in urls:
        result = check_website(url, timeout=5)
        row_id = save_check(result)
        print(f"   Saved check for {url} (ID: {row_id})")
    print()
    
    # Step 3: Query and display statistics
    print("3️⃣  Querying database...")
    
    # Total count
    total = get_check_count()
    print(f"   Total checks in database: {total}")
    
    # All checks
    all_checks = get_all_checks()
    print(f"   Retrieved all checks: {len(all_checks)} rows")
    
    # Recent checks
    recent = get_recent_checks(5)
    print(f"   Recent checks (last 5): {len(recent)} rows")
    
    # Checks by URL
    google_checks = get_checks_by_url('https://google.com')
    print(f"   Checks for google.com: {len(google_checks)} rows")
    print()
    
    # Step 4: Display sample data
    print("4️⃣  Sample check results:")
    for i, check in enumerate(recent[:3], 1):
        status = "✅ UP" if check['success'] else "❌ DOWN"
        print(f"   {i}. {check['url']}")
        print(f"      Status: {status} | Code: {check['status_code']} | Time: {check['response_time']:.3f}s")
        print(f"      Timestamp: {check['timestamp']}")
    print()
    
    # Step 5: Calculate success rate
    print("5️⃣  Statistics:")
    if all_checks:
        successful = sum(1 for c in all_checks if c['success'] == 1)
        success_rate = (successful / len(all_checks)) * 100
        print(f"   Success rate: {success_rate:.1f}% ({successful}/{len(all_checks)})")
        
        avg_response_time = sum(c['response_time'] or 0 for c in all_checks) / len(all_checks)
        print(f"   Average response time: {avg_response_time:.3f}s")
    print()
    
    # Step 6: Test cleanup (won't delete anything recent)
    print("6️⃣  Testing cleanup function...")
    deleted = cleanup_old_checks(days=30)
    print()
    
    # Final verification
    print("7️⃣  Final verification:")
    final_count = get_check_count()
    print(f"   Final check count: {final_count}")
    print()
    
    print("✅ Integration test completed successfully!\n")


if __name__ == '__main__':
    test_database_integration()