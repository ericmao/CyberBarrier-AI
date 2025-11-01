from setuptools import setup, find_packages

setup(
    name="cyberbarrier-ai",
    version="2.0.0",
    description="AI-Powered MSSP Implementation Barrier Diagnosis using Q-RCTM v2.0",
    author="CyberBarrier AI Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.0",
        "pyyaml>=5.4.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "cyberbarrier=cyberbarrier.cli:main",
        ],
    },
)
