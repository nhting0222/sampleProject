# Mock data for XDR Management System

security_events = [
    {
        "id": "EVT-001",
        "timestamp": "2026-02-05T10:30:15Z",
        "severity": "critical",
        "type": "Malware Detected",
        "source": "Endpoint-WKS-042",
        "description": "Ransomware activity detected on Windows workstation",
        "status": "investigating",
        "affectedAssets": ["WKS-042", "FILE-SERVER-01"],
        "iocs": ["hash:a3f5d...", "ip:185.220.101.45"],
        "mitre": ["T1486 - Data Encrypted for Impact"]
    },
    {
        "id": "EVT-002",
        "timestamp": "2026-02-05T10:15:42Z",
        "severity": "high",
        "type": "Suspicious Login",
        "source": "DC-SERVER-01",
        "description": "Multiple failed login attempts from unusual location",
        "status": "resolved",
        "affectedAssets": ["DC-SERVER-01"],
        "iocs": ["ip:203.0.113.42", "user:admin"],
        "mitre": ["T1110 - Brute Force"]
    },
    {
        "id": "EVT-003",
        "timestamp": "2026-02-05T09:45:20Z",
        "severity": "medium",
        "type": "Unusual Network Traffic",
        "source": "FW-EDGE-01",
        "description": "Large data exfiltration attempt detected",
        "status": "monitoring",
        "affectedAssets": ["FW-EDGE-01", "WKS-089"],
        "iocs": ["ip:192.0.2.123", "domain:suspicious-site.com"],
        "mitre": ["T1048 - Exfiltration Over Alternative Protocol"]
    },
    {
        "id": "EVT-004",
        "timestamp": "2026-02-05T09:20:10Z",
        "severity": "low",
        "type": "Policy Violation",
        "source": "WKS-101",
        "description": "Unauthorized software installation attempt",
        "status": "resolved",
        "affectedAssets": ["WKS-101"],
        "iocs": [],
        "mitre": []
    },
    {
        "id": "EVT-005",
        "timestamp": "2026-02-05T08:55:33Z",
        "severity": "critical",
        "type": "Command & Control",
        "source": "WKS-067",
        "description": "C2 beacon communication detected",
        "status": "investigating",
        "affectedAssets": ["WKS-067"],
        "iocs": ["ip:198.51.100.77", "domain:c2-server.malicious"],
        "mitre": ["T1071 - Application Layer Protocol"]
    }
]

incidents = [
    {
        "id": "INC-2026-001",
        "title": "Ransomware Outbreak - Finance Department",
        "severity": "critical",
        "status": "in_progress",
        "createdAt": "2026-02-05T10:30:00Z",
        "updatedAt": "2026-02-05T11:45:00Z",
        "assignee": "John Smith",
        "description": "Multiple endpoints in finance department affected by ransomware",
        "affectedSystems": 12,
        "relatedEvents": ["EVT-001", "EVT-005"],
        "timeline": [
            {"time": "10:30", "action": "Incident created", "user": "System"},
            {"time": "10:35", "action": "Assigned to John Smith", "user": "Manager"},
            {"time": "10:40", "action": "Isolated affected systems", "user": "John Smith"},
            {"time": "11:15", "action": "Initiated forensic analysis", "user": "John Smith"}
        ]
    },
    {
        "id": "INC-2026-002",
        "title": "Brute Force Attack - Domain Controller",
        "severity": "high",
        "status": "resolved",
        "createdAt": "2026-02-05T10:15:00Z",
        "updatedAt": "2026-02-05T10:50:00Z",
        "assignee": "Sarah Johnson",
        "description": "Multiple failed login attempts detected on domain controller",
        "affectedSystems": 1,
        "relatedEvents": ["EVT-002"],
        "timeline": [
            {"time": "10:15", "action": "Incident created", "user": "System"},
            {"time": "10:17", "action": "Blocked source IP", "user": "Sarah Johnson"},
            {"time": "10:30", "action": "Verified no compromise", "user": "Sarah Johnson"},
            {"time": "10:50", "action": "Incident closed", "user": "Sarah Johnson"}
        ]
    }
]

assets = [
    {
        "id": "WKS-042",
        "name": "Finance-WKS-042",
        "type": "Workstation",
        "os": "Windows 11 Pro",
        "ip": "10.0.10.42",
        "status": "compromised",
        "lastSeen": "2026-02-05T10:30:00Z",
        "owner": "Jane Doe",
        "department": "Finance",
        "riskScore": 95
    },
    {
        "id": "DC-SERVER-01",
        "name": "Primary Domain Controller",
        "type": "Server",
        "os": "Windows Server 2022",
        "ip": "10.0.1.10",
        "status": "healthy",
        "lastSeen": "2026-02-05T11:00:00Z",
        "owner": "IT Department",
        "department": "IT",
        "riskScore": 15
    }
]

alert_rules = [
    {
        "id": "RULE-001",
        "name": "Ransomware Detection",
        "severity": "critical",
        "enabled": True,
        "conditions": "File encryption activity + Ransom note creation",
        "actions": ["isolate_endpoint", "notify_soc", "create_incident"]
    },
    {
        "id": "RULE-002",
        "name": "Brute Force Detection",
        "severity": "high",
        "enabled": True,
        "conditions": ">5 failed logins within 5 minutes",
        "actions": ["block_ip", "notify_admin"]
    }
]

dashboard_stats = {
    "totalEvents": 1247,
    "criticalEvents": 23,
    "activeIncidents": 5,
    "resolvedToday": 18,
    "assetsMonitored": 342,
    "compromisedAssets": 3,
    "averageResponseTime": "12 mins",
    "threatLevel": "high"
}
