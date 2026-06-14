#!/usr/bin/env python3
"""
Cloud Security Breach Simulation Script
Simulates unauthorized access attempts to AWS S3 bucket
"""

import json
import random
import datetime
import time
from typing import Dict, List

class S3BreachSimulator:
    def __init__(self, config_file: str):
        """Initialize the breach simulator with configuration"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Suspicious IP addresses for simulation
        self.suspicious_ips = [
            "203.0.113.45",  # Suspicious foreign IP
            "198.51.100.23", # Known malicious IP
            "192.0.2.100",   # Unauthorized internal IP
            "172.16.254.1"   # Suspicious network range
        ]
        
        # Unauthorized users
        self.unauthorized_users = [
            "hacker@malicious.com",
            "unknown@suspicious.org",
            "attacker@evil.net"
        ]
    
    def generate_access_log(self, is_breach: bool = False) -> Dict:
        """Generate a simulated S3 access log entry"""
        timestamp = datetime.datetime.now().isoformat()
        
        if is_breach:
            # Generate suspicious access
            source_ip = random.choice(self.suspicious_ips)
            user = random.choice(self.unauthorized_users)
            action = random.choice(["GET", "PUT", "DELETE"])
            status_code = random.choice([200, 403, 401])
            object_key = random.choice([
                "confidential/financial_data.xlsx",
                "secrets/api_keys.txt",
                "private/customer_database.sql"
            ])
        else:
            # Generate normal access
            source_ip = random.choice(self.config["authorized_ips"])
            user = random.choice(self.config["authorized_users"])
            action = "GET"
            status_code = 200
            object_key = "public/readme.txt"
        
        return {
            "timestamp": timestamp,
            "bucket": self.config["bucket_name"],
            "source_ip": source_ip,
            "user": user,
            "action": action,
            "object_key": object_key,
            "status_code": status_code,
            "user_agent": "aws-cli/2.0.0 Python/3.8.0",
            "request_id": f"REQ{random.randint(100000, 999999)}"
        }
    
    def simulate_breach_scenario(self, num_logs: int = 10) -> List[Dict]:
        """Simulate a series of access logs with some breaches"""
        logs = []
        
        print(f"Simulating {num_logs} access attempts...")
        
        for i in range(num_logs):
            # 30% chance of generating a breach attempt
            is_breach = random.random() < 0.3
            
            log_entry = self.generate_access_log(is_breach)
            logs.append(log_entry)
            
            if is_breach:
                print(f"⚠️  Breach attempt #{i+1}: {log_entry['source_ip']} -> {log_entry['object_key']}")
            else:
                print(f"✅ Normal access #{i+1}: {log_entry['source_ip']}")
            
            # Small delay to simulate real-time logs
            time.sleep(0.5)
        
        return logs
    
    def save_logs(self, logs: List[Dict], filename: str):
        """Save generated logs to file"""
        with open(filename, 'w') as f:
            for log in logs:
                f.write(json.dumps(log) + '\n')
        print(f"📁 Logs saved to {filename}")

def main():
    """Main function to run the breach simulation"""
    print("🔒 Starting Cloud Security Breach Simulation")
    print("=" * 50)
    
    # Initialize simulator
    simulator = S3BreachSimulator('../config/aws_config.json')
    
    # Generate breach scenario
    logs = simulator.simulate_breach_scenario(15)
    
    # Save logs for analysis
    log_filename = f"../logs/s3_access_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    simulator.save_logs(logs, log_filename)
    
    print("\n🎯 Breach simulation completed!")
    print(f"Generated {len(logs)} log entries")
    print("Ready for breach detection analysis...")

if __name__ == "__main__":
    main()
