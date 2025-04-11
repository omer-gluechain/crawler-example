# Contributing to crawler-example

Thank you for your interest in contributing to the crawler-example project! This document outlines the contribution process and guidelines to help you get started.

## Code of Conduct

We expect all contributors to act professionally and respectfully. Be kind to others, be open to constructive feedback, and focus on making the project better for everyone. Harassment or disrespectful behavior will not be tolerated.

## How to Contribute

### Prerequisites

Before you begin, make sure you have:

1. Git installed on your machine
2. Python 3.6 or higher
3. A GitHub account

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/crawler-example.git
   cd crawler-example
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/bugfix-<feature-name>
   ```
   
2. Make your changes, following the code style guidelines below

3. Test your changes thoroughly

4. Commit your changes with a clear message:
   ```bash
   git commit -m "Description of your changes"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/bugfix-<feature-name>
   ```

6. Create a pull request from your branch to the main repository

## Code Style Guidelines

Follow these style guidelines to maintain code consistency:

### Documentation
- Use Google-style docstrings for functions and classes
- Include docstrings for all public methods with Args/Returns sections
- Write clear module-level docstrings
- Add inline comments for complex code sections

### Python Conventions
- Use PascalCase for class names (e.g., `WebCrawler`)
- Use snake_case for functions and variables (e.g., `get_html`, `visited_urls`)
- Use UPPER_SNAKE_CASE for constants
- Choose descriptive names for functions and variables

### Code Organization
- Maintain logical separation of concerns
- Follow clear class structures with well-defined method responsibilities

### Error Handling
- Use try-except blocks appropriately
- Check HTTP status codes with `raise_for_status()`
- Provide helpful error messages

## Pull Request Guidelines

When submitting a pull request:

1. Keep the scope focused on a specific feature or fix
2. Ensure your code adheres to the style guidelines
3. Include tests for your changes when applicable
4. Update documentation if necessary
5. Describe what your changes do and why they should be included

## Reporting Issues

When reporting issues, include:

1. A clear description of the problem
2. Steps to reproduce the issue
3. Expected behavior vs. actual behavior
4. Your environment details (Python version, OS)
5. Any relevant logs or error messages

## Suggesting Enhancements

We welcome suggestions for enhancements! When suggesting features:

1. Clearly describe the feature and its benefits
2. Explain how the feature would work
3. Consider how the feature fits with the project's scope

Thank you for contributing to crawler-example!