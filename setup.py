import setuptools
with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pymf",#python membership function
    version="0.0.1",
    author="Guan-Lin Chen",
    author_email="ken54787845@gmail.com",
    description="It is used to quickly establish membership functions for subsequent fuzzy transformations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)