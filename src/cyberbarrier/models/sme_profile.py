"""
SME Profile Model - Represents an SME's current state for assessment
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SMEProfile:
    """
    Profile of a Small/Medium Enterprise for MSSP barrier assessment
    
    All scores are normalized to 0.0-1.0 range where applicable
    """
    
    # Company identification
    company_name: str
    industry: str
    total_employees: int
    annual_revenue: float  # in USD
    
    # Risk Awareness metrics (0.0 to 1.0)
    has_security_policy: float = 0.0  # 0=no, 1=yes
    security_training_frequency: float = 0.0  # 0=never, 0.25=annual, 0.5=quarterly, 1.0=monthly
    incident_response_plan: float = 0.0  # 0=no, 0.5=partial, 1.0=comprehensive
    threat_monitoring: float = 0.0  # 0=none, 0.5=basic, 1.0=advanced
    
    # Capability metrics
    security_staff_count: int = 0
    security_budget_ratio: float = 0.0  # % of IT budget for security (normalized to 0-1)
    current_security_tools: float = 0.0  # 0=none, 0.33=basic, 0.66=moderate, 1.0=comprehensive
    compliance_level: float = 0.0  # 0=none, 0.5=partial, 1.0=certified
    
    # Technology Readiness metrics (0.0 to 1.0)
    cloud_adoption_level: float = 0.0  # 0=none, 0.33=basic, 0.66=hybrid, 1.0=cloud-first
    network_infrastructure_score: float = 0.0  # 0=outdated, 0.5=adequate, 1.0=modern
    endpoint_management_score: float = 0.0  # 0=none, 0.5=partial, 1.0=comprehensive
    data_backup_score: float = 0.0  # 0=none, 0.5=basic, 1.0=robust
    
    # Management Support metrics (0.0 to 1.0)
    executive_security_awareness: float = 0.0  # 0=low, 0.5=moderate, 1.0=high
    security_budget_priority: float = 0.0  # 0=low, 0.5=medium, 1.0=high
    board_involvement: float = 0.0  # 0=none, 0.5=occasional, 1.0=regular
    strategic_security_planning: float = 0.0  # 0=none, 0.5=ad-hoc, 1.0=formal
    
    # Additional context
    previous_incidents: int = 0  # Number of security incidents in past year
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Validate profile data"""
        # Ensure all normalized values are in 0-1 range
        normalized_fields = [
            'has_security_policy', 'security_training_frequency',
            'incident_response_plan', 'threat_monitoring',
            'security_budget_ratio', 'current_security_tools', 'compliance_level',
            'cloud_adoption_level', 'network_infrastructure_score',
            'endpoint_management_score', 'data_backup_score',
            'executive_security_awareness', 'security_budget_priority',
            'board_involvement', 'strategic_security_planning'
        ]
        
        for field_name in normalized_fields:
            value = getattr(self, field_name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{field_name} must be between 0.0 and 1.0, got {value}"
                )
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SMEProfile':
        """Create SMEProfile from dictionary"""
        return cls(**data)
    
    def to_dict(self) -> dict:
        """Convert SMEProfile to dictionary"""
        from dataclasses import asdict
        return asdict(self)
