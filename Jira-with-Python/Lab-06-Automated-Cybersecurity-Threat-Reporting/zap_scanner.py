from zapv2 import ZAPv2
from dotenv import load_dotenv
import os
import time
import json

load_dotenv()

class ZAPScanner:
    def __init__(self):
        proxy = os.getenv("ZAP_PROXY", "http://127.0.0.1:8080")
        self.zap = ZAPv2(proxies={"http": proxy, "https": proxy})

    def scan(self, target):
        print("Starting spider scan...")
        spider = self.zap.spider.scan(target)

        while int(self.zap.spider.status(spider)) < 100:
            print("Spider:", self.zap.spider.status(spider), "%")
            time.sleep(2)

        print("Spider completed")

        print("Starting active scan...")
        scan = self.zap.ascan.scan(target)

        while int(self.zap.ascan.status(scan)) < 100:
            print("Active Scan:", self.zap.ascan.status(scan), "%")
            time.sleep(5)

        print("Active scan completed")

    def report(self):
        alerts = self.zap.core.alerts()

        report = {
            "total_alerts": len(alerts),
            "alerts": alerts
        }

        with open("security_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print("Report saved to security_report.json")

if __name__ == "__main__":
    target = os.getenv("TARGET_URL", "http://localhost:5000")

    scanner = ZAPScanner()
    scanner.scan(target)
    scanner.report()
