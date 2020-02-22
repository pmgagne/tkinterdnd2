import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tkinterdnd2-pmgagne", # Replace with your own username
    version="0.3.0",
    author="pmgagne",
    description="TkinterDnD2 is a python wrapper for George Petasis'' tkDnD Tk extension version 2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pmgagne/tkinterdnd2",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        # Include tkdnd extension files.
        "tkinterdnd2": ["tkdnd/linux64/*.*", "tkdnd/osx64/*.*", "tkdnd/win64/*.*"],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)