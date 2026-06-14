#!/usr/bin/env python3
"""
GRC Compliance Checker
Automated tool for running governance, risk, and compliance checks
"""

import json
import os
import subprocess
import datetime
import logging
from pathlib import Path

class GRCChecker:
    def __init__(self, config_file="config/grc_checks.json"):
        """Initialize the GRC Checker with configuration"""
        self.config_file = config_file
        self.checks = []
        self.results = []
        self.setup_logging()
        self.load_configuration()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/grc_checker.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_configuration(self):
        """Load GRC checks from configuration file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.checks = config.get('security_checks', [])
            self.logger.info(f"Loaded {len(self.checks)} GRC checks")
        except FileNotFoundError:
            self.logger.error(f"Configuration file {self.config_file} not found")
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON in configuration file")
    
    def run_password_policy_check(self):
        """Check password policy compliance"""
        try:
            # Check if password policy file exists
            policy_files = ['/etc/pam.d/common-password', '/etc/login.defs']
            issues = []
            
            for policy_file in policy_files:
                if not os.path.exists(policy_file):
                    issues.append(f"Policy file {policy_file} not found")
            
            # Check password aging settings
            try:
                with open('/etc/login.defs', 'r') as f:
                    content = f.read()
                    if 'PASS_MAX_DAYS' not in content:
                        issues.append("Password maximum age not configured")
                    if 'PASS_MIN_LEN' not in content:
                        issues.append("Minimum password length not configured")
            except FileNotFoundError:
                issues.append("Login definitions file not found")
            
            return {
                'status': 'FAIL' if issues else 'PASS',
                'issues': issues,
                'details': 'Password policy configuration checked'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'issues': [str(e)],
                'details': 'Error checking password policy'
            }
    
    def run_ssh_config_check(self):
        """Check SSH configuration security"""
        try:
            ssh_config = '/etc/ssh/sshd_config'
            issues = []
            
            if not os.path.exists(ssh_config):
                return {
                    'status': 'FAIL',
                    'issues': ['SSH configuration file not found'],
                    'details': 'SSH config file missing'
                }
            
            with open(ssh_config, 'r') as f:
                content = f.read()
                
                # Check for root login
                if 'PermitRootLogin yes' in content:
                    issues.append("Root login is enabled")
                
                # Check for password authentication
                if 'PasswordAuthentication yes' in content:
                    issues.append("Password authentication enabled (consider key-based)")
                
                # Check for protocol version
                if 'Protocol 1' in content:
                    issues.append("SSH Protocol 1 is enabled (insecure)")
            
            return {
                'status': 'FAIL' if issues else 'PASS',
                'issues': issues,
                'details': 'SSH configuration security checked'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'issues': [str(e)],
                'details': 'Error checking SSH configuration'
            }
    
    def run_file_permissions_check(self):
        """Check critical file permissions"""
        try:
            critical_files = [
                ('/etc/passwd', '644'),
                ('/etc/shadow', '640'),
                ('/etc/group', '644'),
                ('/etc/gshadow', '640')
            ]
            
            issues = []
            
            for file_path, expected_perm in critical_files:
                if os.path.exists(file_path):
                    # Get actual permissions
                    actual_perm = oct(os.stat(file_path).st_mode)[-3:]
                    if actual_perm != expected_perm:
                        issues.append(f"{file_path} has permissions {actual_perm}, expected {expected_perm}")
                else:
                    issues.append(f"Critical file {file_path} not found")
            
            return {
                'status': 'FAIL' if issues else 'PASS',
                'issues': issues,
                'details': 'File permissions audit completed'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'issues': [str(e)],
                'details': 'Error checking file permissions'
            }
    
    def run_service_status_check(self):
        """Check critical services status"""
        try:
            critical_services = ['ssh', 'cron', 'rsyslog']
            issues = []
            
            for service in critical_services:
                try:
                    result = subprocess.run(
                        ['systemctl', 'is-active', service],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        issues.append(f"Service {service} is not active")
                except FileNotFoundError:
                    # Fallback for systems without systemctl
                    try:
                        result = subprocess.run(
                            ['service', service, 'status'],
                            capture_output=True,
                            text=True
                        )
                        if result.returncode != 0:
                            issues.append(f"Service {service} status unknown")
                    except FileNotFoundError:
                        issues.append("Unable to check service status (no systemctl or service command)")
            
            return {
                'status': 'FAIL' if issues else 'PASS',
                'issues': issues,
                'details': 'Service status monitoring completed'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'issues': [str(e)],
                'details': 'Error checking service status'
            }
    
    def run_log_integrity_check(self):
        """Check log file integrity"""
        try:
            log_directories = ['/var/log', '/var/log/auth.log']
            issues = []
            
            # Check if log directory exists
            if not os.path.exists('/var/log'):
                issues.append("Log directory /var/log not found")
                return {
                    'status': 'FAIL',
                    'issues': issues,
                    'details': 'Log directory missing'
                }
            
            # Check log file permissions
            important_logs = [
                '/var/log/auth.log',
                '/var/log/syslog',
                '/var/log/kern.log'
            ]
            
            for log_file in important_logs:
                if os.path.exists(log_file):
                    # Check if log file is readable
                    if not os.access(log_file, os.R_OK):
                        issues.append(f"Log file {log_file} is not readable")
                    
                    # Check if log file is too old (no recent entries)
                    stat = os.stat(log_file)
                    age_days = (datetime.datetime.now().timestamp() - stat.st_mtime) / 86400
                    if age_days > 7:
                        issues.append(f"Log file {log_file} hasn't been updated in {age_days:.1f} days")
            
            return {
                'status': 'FAIL' if issues else 'PASS',
                'issues': issues,
                'details': 'Log file integrity check completed'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'issues': [str(e)],
                'details': 'Error checking log integrity'
            }
    
    def run_all_checks(self):
        """Execute all configured GRC checks"""
        self.logger.info("Starting GRC compliance checks...")
        
        check_methods = {
            'SEC001': self.run_password_policy_check,
            'SEC002': self.run_ssh_config_check,
            'SEC003': self.run_file_permissions_check,
            'SEC004': self.run_service_status_check,
            'SEC005': self.run_log_integrity_check
        }
        
        for check in self.checks:
            check_id = check['id']
            self.logger.info(f"Running check {check_id}: {check['name']}")
            
            if check_id in check_methods:
                result = check_methods[check_id]()
                
                check_result = {
                    'check_id': check_id,
                    'name': check['name'],
                    'category': check['category'],
                    'severity': check['severity'],
                    'status': result['status'],
                    'issues': result['issues'],
                    'details': result['details'],
                    'timestamp': datetime.datetime.now().isoformat()
                }
                
                self.results.append(check_result)
                
                if result['status'] == 'FAIL':
                    self.logger.warning(f"Check {check_id} FAILED: {', '.join(result['issues'])}")
                elif result['status'] == 'PASS':
                    self.logger.info(f"Check {check_id} PASSED")
                else:
                    self.logger.error(f"Check {check_id} ERROR: {', '.join(result['issues'])}")
        
        self.logger.info("GRC compliance checks completed")
        return self.results
    
    def get_failed_checks(self):
        """Return only the failed checks"""
        return [result for result in self.results if result['status'] == 'FAIL']
    
    def generate_report(self):
        """Generate a summary report"""
        total_checks = len(self.results)
        passed_checks = len([r for r in self.results if r['status'] == 'PASS'])
        failed_checks = len([r for r in self.results if r['status'] == 'FAIL'])
        error_checks = len([r for r in self.results if r['status'] == 'ERROR'])
        
        report = {
            'summary': {
                'total_checks': total_checks,
                'passed': passed_checks,
                'failed': failed_checks,
                'errors': error_checks,
                'compliance_rate': f"{(passed_checks/total_checks)*100:.1f}%" if total_checks > 0 else "0%"
            },
            'results': self.results,
            'generated_at': datetime.datetime.now().isoformat()
        }
        
        return report

if __name__ == "__main__":
    # Create and run GRC checker
    checker = GRCChecker()
    results = checker.run_all_checks()
    
    # Generate and display report
    report = checker.generate_report()
    print(f"\nGRC Compliance Report")
    print(f"=====================")
    print(f"Total Checks: {report['summary']['total_checks']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"Errors: {report['summary']['errors']}")
    print(f"Compliance Rate: {report['summary']['compliance_rate']}")
