import asyncio
import json
import subprocess
import time
from datetime import datetime
from typing import List


async def run_oha(url: str, duration: int, concurrency: int) -> dict:
    """Run oha and return parsed results"""
    cmd = [
        "oha", 
        "-z", str(duration) + 's',      # number of requests
        "-c", str(concurrency),   # concurrency
        "-j",                     # json output
        url
    ]
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        print(f"Error running oha: {stderr.decode()}")
        return {}
    
    return json.loads(stdout.decode())

async def test_endpoints():
    urls = [
        "http://localhost:8001/test",
        "http://localhost:8002/test",
        "http://localhost:8003/test"
    ]
    
    print(f"\nStarting test at {datetime.now()}")
    
    tasks = [run_oha(url, duration=30, concurrency=50) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for url, result in zip(urls, results):
        if not result:
            continue
            
        print(f"\nResults for {url}:")
        
        # Show status code distribution
        print("\nStatus codes:")
        for status, count in result['statusCodeDistribution'].items():
            print(f"  {status}: {count}")

async def main():
    while True:
        await test_endpoints()
        print("\nWaiting 15 seconds before next test...")
        await asyncio.sleep(15)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest stopped by user")