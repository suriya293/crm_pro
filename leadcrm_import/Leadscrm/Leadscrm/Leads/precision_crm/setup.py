from setuptools import setup, find_packages

setup(
    name="precision_crm",
    version="0.0.1",
    description="Enterprise-grade CRM built on Frappe Framework",
    author="Administrator",
    author_email="admin@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "frappe",
        "requests"
    ]
)
