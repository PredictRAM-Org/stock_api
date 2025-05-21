from setuptools import setup, find_packages

setup(
    name="predictrampyfy",
    version="1.0.0",
    description="A Python package to access comprehensive stock market data from Excel",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
    ],
    include_package_data=True,
    package_data={
        "app": ["data/*.xlsx"],
    },
    entry_points={
        "console_scripts": [
            "predictrampyfy=app.main:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)