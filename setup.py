# setup.py for swarm-path-planning-bees

from setuptools import setup, find_packages

setup(
    name="swarm-path-planning-bees",
    version="0.1.0",
    description="Modernized Bees Algorithm for dynamic path planning",
    author="Research Portfolio",
    author_email="contact@example.com",
    url="https://github.com/molhamfetnah/swarm-path-planning-bees",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
        "ros": [
            "rospkg>=1.3.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="path-planning bees-algorithm swarm-intelligence robotics",
)