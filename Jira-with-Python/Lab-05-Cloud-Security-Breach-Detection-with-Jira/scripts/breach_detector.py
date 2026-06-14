#!/usr/bin/env python3
"""
Cloud Security Breach Detection Engine
Analyzes S3 access logs and detects potential security breaches
"""

import json
import datetime
import re
from typing import Dict, List, Tuple
from collections import defaultdict

class SecurityBreachDetector:
    def __init__(self, config_file: str):
        """Initialize the breach detector with configuration"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Define breach detection rules
        self.breach_rules = {
            'unauthorized_ip': {
                'severity': 'HIGH',
                'description': 'Access from unauthorized IP address'
            },
            'unauthorized_user': {
                'severity': 'HIGH', 
                'description': 'Access attempt by unauthorized user'
            },
            'suspicious_object': {
                'severity': 'MEDIUM',
                'description': 'Access to sensitive/confidential files'
            },
            'failed_auth': {
                'severity': 'MEDIUM',
                'description': 'Multiple failed authentication attempts'
            },
            'unusual_activity': {
                'severity': 'LOW',
                'description': 'Unusual access patterns detected'
            }
        }
        
        # Sensitive file patterns
        self.sensitive_patterns = [
            r'.*confidential.*',
            r'.*secret.*',
            r'.*private.*',
            r'.*api[_-]key.*',
            r'.*password.*',
            r'.*financial.*'
        ]
    
    def load_logs(self, log_file: str) -> List[Dict]:
        """Load access logs from file"""
        logs = []
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line.strip()))
            print(f"📊 Loaded {len(logs)} log entries for analysis")
            return logs
        except FileNotFoundError:
            print(f"❌ Error: Log file {log_file} not found")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing log file: {e}")
            return []
    
    def check_unauthorized_ip(self, log_entry: Dict) -> bool:
        """Check if IP address is unauthorized"""
        source_ip = log_entry.get('source_ip', '')
        authorized_ips = self.config.get('authorized_ips', [])
        return source_ip not in authorized_ips
    
    def check_unauthorized_user(self, log_entry: Dict) -> bool:
        """Check if user is unauthorized"""
        user = log_entry.get('user', '')
        authorized_users = self.config.get('authorized_users', [])
        return user not in authorized_users
    
    def check_sensitive_file_access(self, log_entry: Dict) -> bool:
        """Check if accessing sensitive files"""
        object_key = log_entry.get('object_key', '').lower()
        
        for pattern in self.sensitive_patterns:
            if re.match(pattern, object_key):
                return True
        return False
    
    def check_failed_authentication(self, log_entry: Dict) -> bool:
        """Check for authentication failures"""
        status_code = log_entry.get('status_code', 200)
        return status_code in [401, 403]
    
    def analyze_access_patterns(self, logs: List[Dict]) -> Dict:
        """Analyze logs for unusual access patterns"""
        ip_counts = defaultdict(int)
        user_counts = defaultdict(int)
        
        for log in logs:
            ip_counts[log.get('source_ip', '')] += 1
            user_counts[log.get('user', '')] += 1
        
        # Detect unusual patterns (more than 5 requests from same IP/user)
        suspicious_ips = [ip for ip, count in ip_counts.items() if count > 5]
        suspicious_users = [user for user, count in user_counts.items() if count > 5]
        
        return {
            'suspicious_ips': suspicious_ips,
            'suspicious_users': suspicious_users,
            'total_unique_ips': len(ip_counts),
            'total_unique_users': len(user_counts)
        }
    
    def detect_breaches(self, logs: List[Dict]) -> List[Dict]:
        """Main breach detection function"""
        breaches = []
        
        print("🔍 Starting breach detection analysis...")
        print("-" * 40)
        
        # Analyze access patterns first
        patterns = self.analyze_access_patterns(logs)
        
        for i, log_entry in enumerate(logs):
            detected_issues = []
            
            # Check each breach rule
            if self.check_unauthorized_ip(log_entry):
                detected_issues.append('unauthorized_ip')
            
            if self.check_unauthorized_user(log_entry):
                detected_issues.append('unauthorized_user')
            
            if self.check_sensitive_file_access(log_entry):
                detected_issues.append('suspicious_object')
            
            if self.check_failed_authentication(log_entry):
                detected_issues.append('failed_auth')
            
            # Check for unusual activity patterns
            if (log_entry.get('source_ip') in patterns['suspicious_ips'] or 
                log_entry.get('user') in patterns['suspicious_users']):
                detected_issues.append('unusual_activity')
            
            # If any issues detected, create breach record
            if detected_issues:
                breach = self.create_breach_record(log_entry, detected_issues)
                breaches.append(breach)
                
                print(f"🚨 Breach #{len(breaches)}: {breach['severity']} - {breach['description']}")
                print(f"   Source: {log_entry.get('source_ip')} | User: {log_entry.get('user')}")
                print(f"   Object: {log_entry.get('object_key')}")
        
        print(f"\n📈 Analysis Complete: {len(breaches)} breaches detected out of {len(logs)} log entries")
        return breaches
    
    def create_breach_record(self, log_entry: Dict, issues: List[str]) -> Dict:
        """Create a structured breach record"""
        # Determine highest severity
        severities = [self.breach_rules[issue]['severity'] for issue in issues]
        severity_order = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}
        max_severity = max(severities, key=lambda x: severity_order[x])
        
        # Create description
        descriptions = [self.breach_rules[issue]['description'] for issue in issues]
        
        breach_record = {
            'breach_id': f"BREACH_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(issues)}",
            'timestamp': log_entry.get('timestamp'),
            'severity': max_severity,
            'description': '; '.join(descriptions),
            'source_ip': log_entry.get('source_ip'),
            'user': log_entry.get('user'),
            'bucket': log_entry.get('bucket'),
            'object_key': log_entry.get('object_key'),
            'action': log_entry.get('action'),
            'status_code': log_entry.get('status_code'),
            'detected_issues': issues,
            'impact_assessment': self.assess_impact(max_severity, issues),
            'recommended_actions': self.get_recommended_actions(issues)
        }
        
        return breach_record
    
    def assess_impact(self, severity: str, issues: List[str]) -> str:
        """Assess the potential impact of the breach"""
        if severity == 'HIGH':
            return "Critical: Immediate action required. Potential data compromise."
        elif severity == 'MEDIUM':
            return "Moderate: Investigation needed. Possible security risk."
        else:
            return "Low: Monitor situation. Unusual but not immediately threatening."
    
    def get_recommended_actions(self, issues: List[str]) -> List[str]:
        """Get recommended actions based on detected issues"""
        actions = []
        
        if 'unauthorized_ip' in issues:
            actions.append("Block suspicious IP address")
            actions.append("Review firewall rules")
        
        if 'unauthorized_user' in issues:
            actions.append("Disable compromised user account")
            actions.append("Force password reset")
        
        if 'suspicious_object' in issues:
            actions.append("Audit file access permissions")
            actions.append("Review data classification")
        
        if 'failed_auth' in issues:
            actions.append("Implement account lockout policies")
            actions.append("Enable MFA if not already active")
        
        if 'unusual_activity' in issues:
            actions.append("Monitor user behavior patterns")
            actions.append("Implement rate limiting")
        
        return actions
    
    def save_breach_report(self, breaches: List[Dict], filename: str):
        """Save breach detection report"""
        report = {
            'report_timestamp': datetime.datetime.now().isoformat(),
            'total_breaches': len(breaches),
            'severity_breakdown': self.get_severity_breakdown(breaches),
            'breaches': breaches
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📋 Breach report saved to {filename}")
    
    def get_severity_breakdown(self, breaches: List[Dict]) -> Dict:
        """Get breakdown of breaches by severity"""
        breakdown = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for breach in breaches:
            severity = breach.get('severity', 'LOW')
            breakdown[severity] += 1
        
        return breakdown

def main():
    """Main function to run breach detection"""
    print("🔍 Starting Cloud Security Breach Detection")
    print("=" * 50)
    
    # Initialize detector
    detector = SecurityBreachDetector('../config/aws_config.json')
    
    # Find the most recent log file
    import os
    import glob
    
    log_files = glob.glob('../logs/s3_access_logs_*.json')
    if not log_files:
        print("❌ No log files found. Please run the breach simulation first.")
        return
    
    # Use the most recent log file
    latest_log = max(log_files, key=os.path.getctime)
    print(f"📁 Analyzing log file: {latest_log}")
    
    # Load and analyze logs
    logs = detector.load_logs(latest_log)
    if not logs:
        return
    
    # Detect breaches
    breaches = detector.detect_breaches(logs)
    
    # Save breach report
    report_filename = f"../logs/breach_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    detector.save_breach_report(breaches, report_filename)
    
    # Print summary
    print("\n" + "=" * 50)
    print("🎯 BREACH DETECTION SUMMARY")
    print("=" * 50)
    
    if breaches:
        severity_breakdown = detector.get_severity_breakdown(breaches)
        print(f"Total Breaches Detected: {len(breaches)}")
        print(f"High Severity: {severity_breakdown['HIGH']}")
        print(f"Medium Severity: {severity_breakdown['MEDIUM']}")
        print(f"Low Severity: {severity_breakdown['LOW']}")
        print(f"\n📊 Report saved: {report_filename}")
    else:
        print("✅ No security breaches detected!")

if __name__ == "__main__":
    main()
