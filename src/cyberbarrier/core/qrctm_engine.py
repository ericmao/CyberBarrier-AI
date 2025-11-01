"""
Q-RCTM v2.0 (Qualitative Risk-Capability-Technology Maturity) Engine
Core diagnostic engine for analyzing MSSP implementation barriers
"""

import numpy as np
from typing import Dict, List, Tuple
from ..models.sme_profile import SMEProfile


class QRCTMEngine:
    """
    Q-RCTM v2.0 Engine - Qualitative Risk-Capability-Technology Maturity
    
    This engine evaluates four key dimensions:
    - Risk Awareness (R): Understanding of cybersecurity threats
    - Capability Assessment (C): Internal security capabilities
    - Technology Readiness (T): IT infrastructure maturity
    - Management Support (M): Leadership commitment
    """
    
    # Weighting factors for Q-RCTM dimensions (sum to 1.0)
    DIMENSION_WEIGHTS = {
        'risk_awareness': 0.25,
        'capability': 0.30,
        'technology_readiness': 0.25,
        'management_support': 0.20
    }
    
    # Threshold for barrier risk classification
    # Based on industry data showing 31% MSSP adoption failure rate in SMEs
    # HIGH_RISK_THRESHOLD (0.65): Companies with barrier scores >= 0.65 have
    # a success probability of 35% or less, aligning with the failure rate
    HIGH_RISK_THRESHOLD = 0.65
    MEDIUM_RISK_THRESHOLD = 0.40
    
    # Capability calculation constant: expected security staff per 50 employees
    SECURITY_STAFF_RATIO_BASE = 50
    
    def __init__(self):
        """Initialize the Q-RCTM v2.0 engine"""
        self.barrier_history = []
        
    def calculate_dimension_scores(self, profile: SMEProfile) -> Dict[str, float]:
        """
        Calculate normalized scores for each Q-RCTM dimension
        
        Args:
            profile: SME profile containing assessment data
            
        Returns:
            Dictionary of dimension scores (0.0 to 1.0)
        """
        scores = {}
        
        # Risk Awareness Score (based on threat understanding)
        scores['risk_awareness'] = self._calculate_risk_awareness(profile)
        
        # Capability Score (based on current security posture)
        scores['capability'] = self._calculate_capability(profile)
        
        # Technology Readiness Score (based on infrastructure)
        scores['technology_readiness'] = self._calculate_technology_readiness(profile)
        
        # Management Support Score (based on leadership commitment)
        scores['management_support'] = self._calculate_management_support(profile)
        
        return scores
    
    def _calculate_risk_awareness(self, profile: SMEProfile) -> float:
        """Calculate risk awareness score (0.0 = low awareness, 1.0 = high awareness)"""
        factors = [
            profile.has_security_policy * 0.3,
            profile.security_training_frequency * 0.25,
            profile.incident_response_plan * 0.25,
            profile.threat_monitoring * 0.2
        ]
        return sum(factors)
    
    def _calculate_capability(self, profile: SMEProfile) -> float:
        """Calculate capability score (0.0 = low capability, 1.0 = high capability)"""
        factors = [
            profile.security_staff_count / max(profile.total_employees / self.SECURITY_STAFF_RATIO_BASE, 1) * 0.35,
            profile.security_budget_ratio * 0.30,
            profile.current_security_tools * 0.20,
            profile.compliance_level * 0.15
        ]
        # Normalize to 0-1 range
        return min(sum(factors), 1.0)
    
    def _calculate_technology_readiness(self, profile: SMEProfile) -> float:
        """Calculate technology readiness score (0.0 = low readiness, 1.0 = high readiness)"""
        factors = [
            profile.cloud_adoption_level * 0.30,
            profile.network_infrastructure_score * 0.30,
            profile.endpoint_management_score * 0.25,
            profile.data_backup_score * 0.15
        ]
        return sum(factors)
    
    def _calculate_management_support(self, profile: SMEProfile) -> float:
        """Calculate management support score (0.0 = low support, 1.0 = high support)"""
        factors = [
            profile.executive_security_awareness * 0.35,
            profile.security_budget_priority * 0.30,
            profile.board_involvement * 0.20,
            profile.strategic_security_planning * 0.15
        ]
        return sum(factors)
    
    def calculate_barrier_score(self, dimension_scores: Dict[str, float]) -> float:
        """
        Calculate overall barrier score using weighted dimensions
        
        Higher score = Higher barrier to MSSP adoption
        
        Args:
            dimension_scores: Dictionary of dimension scores
            
        Returns:
            Barrier score (0.0 = no barriers, 1.0 = maximum barriers)
        """
        # Invert scores (high capability = low barrier)
        barrier_contributions = {}
        for dimension, score in dimension_scores.items():
            weight = self.DIMENSION_WEIGHTS[dimension]
            # Invert: low score in dimension = high barrier
            barrier_contributions[dimension] = (1.0 - score) * weight
        
        total_barrier_score = sum(barrier_contributions.values())
        return total_barrier_score
    
    def classify_risk_level(self, barrier_score: float) -> str:
        """
        Classify the risk level based on barrier score
        
        Args:
            barrier_score: Overall barrier score (0.0 to 1.0)
            
        Returns:
            Risk level classification
        """
        if barrier_score >= self.HIGH_RISK_THRESHOLD:
            return "HIGH"
        elif barrier_score >= self.MEDIUM_RISK_THRESHOLD:
            return "MEDIUM"
        else:
            return "LOW"
    
    def identify_critical_barriers(
        self, 
        dimension_scores: Dict[str, float]
    ) -> List[Tuple[str, float, str]]:
        """
        Identify the most critical barriers to MSSP adoption
        
        Args:
            dimension_scores: Dictionary of dimension scores
            
        Returns:
            List of tuples (dimension, barrier_score, severity)
        """
        barriers = []
        
        for dimension, score in dimension_scores.items():
            barrier_score = 1.0 - score  # Invert to get barrier
            
            if barrier_score >= 0.7:
                severity = "CRITICAL"
            elif barrier_score >= 0.5:
                severity = "HIGH"
            elif barrier_score >= 0.3:
                severity = "MEDIUM"
            else:
                severity = "LOW"
            
            barriers.append((dimension, barrier_score, severity))
        
        # Sort by barrier score (highest first)
        barriers.sort(key=lambda x: x[1], reverse=True)
        
        return barriers
    
    def generate_recommendations(
        self,
        barriers: List[Tuple[str, float, str]]
    ) -> List[Dict[str, str]]:
        """
        Generate actionable recommendations based on identified barriers
        
        Args:
            barriers: List of barrier tuples from identify_critical_barriers
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        recommendation_map = {
            'risk_awareness': {
                'title': 'Enhance Risk Awareness',
                'actions': [
                    'Implement regular cybersecurity awareness training',
                    'Develop and document security policies',
                    'Establish incident response procedures',
                    'Deploy threat monitoring capabilities'
                ]
            },
            'capability': {
                'title': 'Build Security Capabilities',
                'actions': [
                    'Hire or train dedicated security personnel',
                    'Increase security budget allocation',
                    'Deploy essential security tools (firewall, antivirus, SIEM)',
                    'Pursue relevant compliance certifications'
                ]
            },
            'technology_readiness': {
                'title': 'Improve Technology Infrastructure',
                'actions': [
                    'Modernize network infrastructure',
                    'Implement endpoint management solutions',
                    'Establish robust data backup systems',
                    'Consider cloud migration for scalability'
                ]
            },
            'management_support': {
                'title': 'Secure Management Support',
                'actions': [
                    'Educate executives on cybersecurity importance',
                    'Integrate security into strategic planning',
                    'Ensure board-level security oversight',
                    'Prioritize security in budget decisions'
                ]
            }
        }
        
        for dimension, barrier_score, severity in barriers:
            if severity in ['CRITICAL', 'HIGH']:
                rec_template = recommendation_map.get(dimension, {})
                recommendations.append({
                    'dimension': dimension,
                    'severity': severity,
                    'barrier_score': f"{barrier_score:.2f}",
                    'title': rec_template.get('title', 'Address Barrier'),
                    'actions': rec_template.get('actions', [])
                })
        
        return recommendations
    
    def diagnose(self, profile: SMEProfile) -> Dict:
        """
        Complete Q-RCTM v2.0 diagnosis of MSSP implementation barriers
        
        Args:
            profile: SME profile to analyze
            
        Returns:
            Complete diagnosis report
        """
        # Calculate dimension scores
        dimension_scores = self.calculate_dimension_scores(profile)
        
        # Calculate overall barrier score
        barrier_score = self.calculate_barrier_score(dimension_scores)
        
        # Classify risk level
        risk_level = self.classify_risk_level(barrier_score)
        
        # Identify critical barriers
        barriers = self.identify_critical_barriers(dimension_scores)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(barriers)
        
        # Store in history
        diagnosis = {
            'company_name': profile.company_name,
            'dimension_scores': dimension_scores,
            'barrier_score': barrier_score,
            'risk_level': risk_level,
            'barriers': barriers,
            'recommendations': recommendations,
            'success_probability': 1.0 - barrier_score
        }
        
        self.barrier_history.append(diagnosis)
        
        return diagnosis
