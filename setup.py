import textwrap

import setuptools

setuptools.setup(
    name='ceilometerclient',
    version='0.1',
    description='Client for ceilometer metering API',
    author='Doug Hellmann',
    author_email='doug.hellmann@dreamhost.com',
    url='https://github.com/dreamhost/ceilometerclient',
    packages=setuptools.find_packages(exclude=['bin']),
    include_package_data=True,
    test_suite='nose.collector',
    scripts=[],
    py_modules=[],
    entry_points=textwrap.dedent("""
    """),
    )
