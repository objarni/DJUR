import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="objarni",
    version="0.0.1",
    author="Olof Bjarnason",
    author_email="olof.bjarnason@gmail.com",
    description="DJUR reimplementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/objarni/DJUR",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
