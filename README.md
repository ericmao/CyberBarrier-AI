# 🔒 CyberBarrier AI™

## AI-Powered MSSP Implementation Barrier Diagnosis

**Tired of 31% MSSP adoption failures in SMEs?** CyberBarrier AI™ is the world's first **Q-RCTM v2.0 engine** that diagnoses implementation barriers before they cause your MSSP deployment to fail.

### 🎯 The Problem

Small and Medium Enterprises (SMEs) face a staggering **31% failure rate** when adopting Managed Security Service Provider (MSSP) solutions. These failures cost businesses millions in:
- Wasted implementation time and resources
- Increased vulnerability to cyber threats
- Lost productivity and revenue
- Damaged vendor relationships

### 💡 The Solution

CyberBarrier AI™ uses the proprietary **Q-RCTM v2.0 (Qualitative Risk-Capability-Technology Maturity)** diagnostic engine to:

✅ **Predict** MSSP adoption success probability before implementation  
✅ **Identify** critical barriers across four key dimensions  
✅ **Recommend** actionable steps to improve readiness  
✅ **Prevent** costly failures through AI-powered diagnostics

---

## 🚀 Features

### Q-RCTM v2.0 Engine

The core diagnostic engine evaluates four critical dimensions:

1. **Risk Awareness (R)** - Understanding of cybersecurity threats
   - Security policies and procedures
   - Training frequency and effectiveness
   - Incident response capabilities
   - Threat monitoring maturity

2. **Capability Assessment (C)** - Internal security capabilities
   - Security staff allocation
   - Budget and resource commitment
   - Current security tooling
   - Compliance and certification status

3. **Technology Readiness (T)** - IT infrastructure maturity
   - Cloud adoption level
   - Network infrastructure quality
   - Endpoint management
   - Data backup and recovery

4. **Management Support (M)** - Leadership commitment
   - Executive security awareness
   - Budget prioritization
   - Board-level involvement
   - Strategic security planning

### Analysis Capabilities

- **Single Company Analysis**: Deep dive into one organization's readiness
- **Batch Processing**: Analyze multiple companies for industry insights
- **Risk Classification**: Automatic HIGH/MEDIUM/LOW risk categorization
- **Success Probability**: Quantitative prediction of MSSP adoption success
- **Actionable Recommendations**: Prioritized steps to reduce barriers

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/ericmao/CyberBarrier-AI.git
cd CyberBarrier-AI

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Quick Start with Sample Data

```bash
# Create a sample profile
cyberbarrier create-sample --output my_company.json

# Run analysis
cyberbarrier analyze --profile my_company.json --detailed
```

---

## 🔧 Usage

### Command-Line Interface

#### Analyze a Single Company

```bash
# Basic analysis
cyberbarrier analyze --profile examples/profiles/high_risk_startup.json

# Detailed report
cyberbarrier analyze --profile examples/profiles/high_risk_startup.json --detailed

# Save results to file
cyberbarrier analyze --profile my_company.json --output report.json
```

#### Batch Analysis

```bash
# Analyze all profiles in a directory
cyberbarrier batch --directory examples/profiles/

# Save statistics
cyberbarrier batch --directory ./profiles/ --output stats.json
```

#### Create Sample Profile

```bash
# Generate template
cyberbarrier create-sample --output template.json
```

### Python API

```python
from cyberbarrier import SMEProfile, BarrierAnalyzer

# Create an SME profile
profile = SMEProfile(
    company_name="My Company",
    industry="Technology",
    total_employees=100,
    annual_revenue=10000000.0,
    has_security_policy=0.5,
    security_training_frequency=0.25,
    # ... other metrics
)

# Initialize analyzer
analyzer = BarrierAnalyzer()

# Run analysis
report = analyzer.analyze_sme(profile)

# Print results
print(report.get_summary())
print(f"Success Probability: {report.success_probability:.1%}")

# Access detailed data
for dimension, score in report.dimension_scores.items():
    print(f"{dimension}: {score:.2f}")
```

---

## 📊 Profile Schema

SME profiles are defined using JSON with the following structure:

```json
{
  "company_name": "Company Name",
  "industry": "Industry Type",
  "total_employees": 150,
  "annual_revenue": 10000000.0,
  
  "has_security_policy": 0.5,
  "security_training_frequency": 0.25,
  "incident_response_plan": 0.5,
  "threat_monitoring": 0.5,
  
  "security_staff_count": 2,
  "security_budget_ratio": 0.08,
  "current_security_tools": 0.66,
  "compliance_level": 0.5,
  
  "cloud_adoption_level": 0.66,
  "network_infrastructure_score": 0.5,
  "endpoint_management_score": 0.5,
  "data_backup_score": 0.5,
  
  "executive_security_awareness": 0.5,
  "security_budget_priority": 0.5,
  "board_involvement": 0.5,
  "strategic_security_planning": 0.5,
  
  "previous_incidents": 2,
  "notes": "Optional notes"
}
```

**All scores are normalized to 0.0 - 1.0 range:**
- `0.0` = None/Absent/Low
- `0.5` = Partial/Moderate/Medium
- `1.0` = Complete/High/Comprehensive

---

## 📈 Example Output

```
CyberBarrier AI™ Analysis Report - TechStartup Inc
============================================================

Risk Level: HIGH
Barrier Score: 0.72 / 1.00
Success Probability: 28.0%

Q-RCTM v2.0 Dimension Scores:
  - Risk Awareness: 0.08
  - Capability: 0.12
  - Technology Readiness: 0.58
  - Management Support: 0.13

Identified Barriers (4):
  [CRITICAL] Risk Awareness: 0.92
  [CRITICAL] Management Support: 0.87
  [CRITICAL] Capability: 0.88
  [HIGH] Technology Readiness: 0.42

Recommendations (3):
  1. Enhance Risk Awareness
  2. Secure Management Support
  3. Build Security Capabilities
```

---

## 🧪 Examples

The `examples/profiles/` directory contains three sample scenarios:

1. **high_risk_startup.json** - Fast-growing startup with minimal security
   - Expected Result: HIGH risk, ~28% success probability
   
2. **medium_risk_retail.json** - Mid-sized retail with moderate security
   - Expected Result: MEDIUM risk, ~50% success probability
   
3. **low_risk_fintech.json** - Financial services with strong security culture
   - Expected Result: LOW risk, ~85% success probability

---

## 📚 Understanding Q-RCTM v2.0

### Barrier Score Calculation

The Q-RCTM v2.0 engine calculates barrier scores using weighted dimensions:

```
Barrier Score = Σ (Weight × (1 - Dimension_Score))

Where weights are:
- Risk Awareness: 25%
- Capability: 30%
- Technology Readiness: 25%
- Management Support: 20%
```

### Risk Classification

| Barrier Score | Risk Level | Typical Success Rate |
|--------------|------------|---------------------|
| 0.65 - 1.00  | HIGH       | < 35%               |
| 0.40 - 0.64  | MEDIUM     | 35% - 60%           |
| 0.00 - 0.39  | LOW        | > 60%               |

### Success Probability

```
Success Probability = 1 - Barrier Score
```

This metric represents the likelihood of successful MSSP adoption based on current readiness levels.

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

---

## 📄 License

Copyright © 2025 CyberBarrier AI Team. All rights reserved.

---

## 🔗 Resources

- **Documentation**: See inline code documentation
- **Examples**: Check the `examples/` directory
- **Issue Tracker**: GitHub Issues

---

## 💼 About

CyberBarrier AI™ was developed to address the critical gap in MSSP adoption readiness assessment. By leveraging AI and the proprietary Q-RCTM v2.0 framework, we help organizations make data-driven decisions about cybersecurity investments and MSSP partnerships.

**Target Users:**
- IT Consultants and Advisors
- MSSP Vendors
- SME Security Leaders
- Cybersecurity Assessors

**Use Cases:**
- Pre-implementation readiness assessment
- Gap analysis and roadmap development
- Vendor selection and scoping
- Security maturity benchmarking

---

**Built with ❤️ for a more secure digital world**