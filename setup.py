import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding='utf-8')

requirements = [
    'requests>=2.31.0',
    'requests-toolbelt>=1.0.0',
    'PySocks>=1.7.1',
    'pydantic>=1.10.13'
]

setup(
    name='radiojavanpython',
    version='0.5.1',
    author='ERFUN-RAD',
    author_email='erfun.rad@gmail.com',
    license='MIT',
    url='https://github.com/ERFUN-RAD/RADIOJAVANPYTHON',
    install_requires=requirements,
    keywords=[
        'radiojavan private api', 'radiojavan-private-api', 'radiojavan api',
        'radiojavan-api', 'rj api', 'rj-api', 'radiojavan', 'radio javan',
        'radio-javan', 'radiojavanpython'
    ],
    description='THIS BUG-FREE VERSION OF THE RADIO JAVAN API WRAPPER IS FAST AND RELIABLE',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['*tests*']),
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ]
)

