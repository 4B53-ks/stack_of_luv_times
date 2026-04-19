from setuptools import setup

setup(
    name="stack_of_luv_times",
    version="0.1.0",
    install_requires=[
        "fastapi",
        "uvicorn",
    ],
    packages=["."],
)