"""
Command-line interface for CyberBarrier AI
"""

import argparse
import json
import sys
from pathlib import Path

from cyberbarrier.models.sme_profile import SMEProfile
from cyberbarrier.core.barrier_analyzer import BarrierAnalyzer


def load_profile_from_file(filepath: str) -> SMEProfile:
    """Load SME profile from JSON file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return SMEProfile.from_dict(data)


def analyze_command(args):
    """Execute the analyze command"""
    try:
        # Load profile
        profile = load_profile_from_file(args.profile)
        
        # Initialize analyzer
        analyzer = BarrierAnalyzer()
        
        # Perform analysis
        print(f"\nAnalyzing {profile.company_name}...")
        print("Running Q-RCTM v2.0 diagnostic engine...\n")
        
        report = analyzer.analyze_sme(profile)
        
        # Display results
        if args.detailed:
            print(report.get_detailed_report())
        else:
            print(report.get_summary())
        
        # Save to file if requested
        if args.output:
            output_data = report.to_dict()
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"\n✓ Report saved to: {args.output}")
        
        return 0
        
    except FileNotFoundError:
        print(f"Error: Profile file not found: {args.profile}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        return 1


def batch_command(args):
    """Execute the batch analysis command"""
    try:
        # Load all profiles
        profiles = []
        profile_dir = Path(args.directory)
        
        for profile_file in profile_dir.glob("*.json"):
            profile = load_profile_from_file(str(profile_file))
            profiles.append(profile)
        
        if not profiles:
            print(f"No profile files found in: {args.directory}", file=sys.stderr)
            return 1
        
        print(f"\nBatch analyzing {len(profiles)} companies...")
        print("Running Q-RCTM v2.0 diagnostic engine...\n")
        
        # Initialize analyzer
        analyzer = BarrierAnalyzer()
        
        # Analyze all profiles
        reports = analyzer.batch_analyze(profiles)
        
        # Display results
        for report in reports:
            print("\n" + "=" * 80)
            print(report.get_summary())
        
        # Generate statistics
        stats = analyzer.get_industry_statistics(reports)
        
        print("\n" + "=" * 80)
        print("INDUSTRY STATISTICS")
        print("=" * 80)
        print(f"Total Companies Analyzed: {stats['total_analyzed']}")
        print(f"High Risk: {stats['high_risk_percentage']:.1f}%")
        print(f"Medium Risk: {stats['medium_risk_percentage']:.1f}%")
        print(f"Low Risk: {stats['low_risk_percentage']:.1f}%")
        print(f"Average Barrier Score: {stats['average_barrier_score']:.2f}")
        print(f"Average Success Probability: {stats['average_success_probability']:.1%}")
        
        if stats['common_barriers']:
            print("\nMost Common Barriers:")
            for barrier, count in stats['common_barriers'][:5]:
                barrier_name = barrier.replace('_', ' ').title()
                print(f"  - {barrier_name}: {count} companies")
        
        # Save statistics if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(stats, f, indent=2)
            print(f"\n✓ Statistics saved to: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"Error during batch analysis: {e}", file=sys.stderr)
        return 1


def create_sample_command(args):
    """Create a sample profile file"""
    sample_profile = {
        "company_name": "Sample Tech Corp",
        "industry": "Technology",
        "total_employees": 150,
        "annual_revenue": 10000000.0,
        "has_security_policy": 0.5,
        "security_training_frequency": 0.25,
        "incident_response_plan": 0.0,
        "threat_monitoring": 0.5,
        "security_staff_count": 1,
        "security_budget_ratio": 0.05,
        "current_security_tools": 0.33,
        "compliance_level": 0.0,
        "cloud_adoption_level": 0.66,
        "network_infrastructure_score": 0.5,
        "endpoint_management_score": 0.5,
        "data_backup_score": 0.5,
        "executive_security_awareness": 0.5,
        "security_budget_priority": 0.3,
        "board_involvement": 0.0,
        "strategic_security_planning": 0.0,
        "previous_incidents": 2,
        "notes": "Sample company for demonstration"
    }
    
    output_file = args.output or "sample_profile.json"
    
    with open(output_file, 'w') as f:
        json.dump(sample_profile, f, indent=2)
    
    print(f"✓ Sample profile created: {output_file}")
    print("\nYou can now run: cyberbarrier analyze --profile sample_profile.json")
    
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="CyberBarrier AI™ - AI-Powered MSSP Implementation Barrier Diagnosis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single company
  cyberbarrier analyze --profile company.json
  
  # Get detailed report
  cyberbarrier analyze --profile company.json --detailed
  
  # Batch analyze multiple companies
  cyberbarrier batch --directory ./profiles/
  
  # Create a sample profile
  cyberbarrier create-sample --output my_company.json
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='CyberBarrier AI v2.0.0 (Q-RCTM Engine)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze a single SME profile'
    )
    analyze_parser.add_argument(
        '--profile',
        required=True,
        help='Path to SME profile JSON file'
    )
    analyze_parser.add_argument(
        '--detailed',
        action='store_true',
        help='Generate detailed report'
    )
    analyze_parser.add_argument(
        '--output',
        help='Save report to file (JSON format)'
    )
    analyze_parser.set_defaults(func=analyze_command)
    
    # Batch command
    batch_parser = subparsers.add_parser(
        'batch',
        help='Batch analyze multiple SME profiles'
    )
    batch_parser.add_argument(
        '--directory',
        required=True,
        help='Directory containing profile JSON files'
    )
    batch_parser.add_argument(
        '--output',
        help='Save statistics to file (JSON format)'
    )
    batch_parser.set_defaults(func=batch_command)
    
    # Create sample command
    sample_parser = subparsers.add_parser(
        'create-sample',
        help='Create a sample profile file'
    )
    sample_parser.add_argument(
        '--output',
        help='Output file path (default: sample_profile.json)'
    )
    sample_parser.set_defaults(func=create_sample_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
