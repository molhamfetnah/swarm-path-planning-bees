# Contributing to Swarm Path Planning - Modernized Bees Algorithm

Thank you for your interest in contributing!

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or request features
- Include clear reproduction steps
- Specify environment details (Python version, OS, etc.)

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit with clear messages
7. Push to your fork
8. Submit a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/swarm-path-planning-bees.git
cd swarm-path-planning-bees

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Run tests
pytest
```

### Code Style
- Follow PEP 8
- Use type hints where possible
- Write docstrings for all public functions
- Keep functions focused and small

### Testing
- Write unit tests for core algorithms
- Add integration tests for pipelines
- Include stress tests for edge cases
- Run full test suite before submitting

## Project Structure
```
swarm-path-planning-bees/
├── src/algorithms/     # Core algorithm implementations
├── src/wrappers/       # Integration wrappers
├── tests/              # Test suite
├── simulations/        # Simulation scenarios
├── docs/               # Documentation
└── benchmarks/         # Benchmark results
```

## Contact
For questions, open an issue or contact the maintainer.