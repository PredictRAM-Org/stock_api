from setuptools import setup, find_packages

setup(
    name="predictrampyfy",
    version="1.0.0",
    description="A Python package to access stock market data via API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
    ],
    python_requires=">=3.7",
)
