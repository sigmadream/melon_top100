import setuptools

setuptools.setup(
    name="MelonTop100",
    version="0.1",
    license="MIT",
    author="Sangkon Han",
    author_email="sigmadream@gmail.com",
    description="This is a simple package that brings up the Top 100 list of Melon, a music site in Korea.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/sigmadream/melon_top100",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)