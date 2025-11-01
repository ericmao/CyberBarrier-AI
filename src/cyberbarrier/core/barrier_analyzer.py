"""
Barrier Analyzer - High-level analysis and reporting interface
"""

from typing import Dict, List
from .qrctm_engine import QRCTMEngine
from ..models.sme_profile import SMEProfile
from ..models.barrier_report import BarrierReport


class BarrierAnalyzer:
    """
    High-level interface for analyzing MSSP implementation barriers
    """
    
    def __init__(self):
        """Initialize the barrier analyzer with Q-RCTM engine"""
        self.engine = QRCTMEngine()
        
    def analyze_sme(self, profile: SMEProfile) -> BarrierReport:
        """
        Analyze an SME's barriers to MSSP adoption
        
        Args:
            profile: SME profile containing assessment data
            
        Returns:
            BarrierReport with complete analysis
        """
        # Run Q-RCTM diagnosis
        diagnosis = self.engine.diagnose(profile)
        
        # Create barrier report
        report = BarrierReport(
            company_name=diagnosis['company_name'],
            barrier_score=diagnosis['barrier_score'],
            risk_level=diagnosis['risk_level'],
            success_probability=diagnosis['success_probability'],
            dimension_scores=diagnosis['dimension_scores'],
            barriers=diagnosis['barriers'],
            recommendations=diagnosis['recommendations']
        )
        
        return report
    
    def batch_analyze(self, profiles: List[SMEProfile]) -> List[BarrierReport]:
        """
        Analyze multiple SME profiles
        
        Args:
            profiles: List of SME profiles
            
        Returns:
            List of barrier reports
        """
        reports = []
        for profile in profiles:
            report = self.analyze_sme(profile)
            reports.append(report)
        return reports
    
    def get_industry_statistics(self, reports: List[BarrierReport]) -> Dict:
        """
        Calculate aggregate statistics across multiple reports
        
        Args:
            reports: List of barrier reports
            
        Returns:
            Dictionary with industry statistics
        """
        if not reports:
            return {}
        
        total_reports = len(reports)
        high_risk_count = sum(1 for r in reports if r.risk_level == "HIGH")
        medium_risk_count = sum(1 for r in reports if r.risk_level == "MEDIUM")
        low_risk_count = sum(1 for r in reports if r.risk_level == "LOW")
        
        avg_barrier_score = sum(r.barrier_score for r in reports) / total_reports
        avg_success_prob = sum(r.success_probability for r in reports) / total_reports
        
        # Calculate most common barriers
        barrier_counts = {}
        for report in reports:
            for barrier, score, severity in report.barriers:
                if severity in ['CRITICAL', 'HIGH']:
                    barrier_counts[barrier] = barrier_counts.get(barrier, 0) + 1
        
        return {
            'total_analyzed': total_reports,
            'high_risk_percentage': (high_risk_count / total_reports) * 100,
            'medium_risk_percentage': (medium_risk_count / total_reports) * 100,
            'low_risk_percentage': (low_risk_count / total_reports) * 100,
            'average_barrier_score': avg_barrier_score,
            'average_success_probability': avg_success_prob,
            'common_barriers': sorted(
                barrier_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )
        }
