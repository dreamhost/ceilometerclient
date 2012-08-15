import textwrap

import setuptools

setuptools.setup(
    name='ceilometerclient',
    version='0.1',

    description='Client for ceilometer metering API',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 #'Programming Language :: Python :: 3',
                 #'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Web Environment',
                 ],

    author='Doug Hellmann',
    author_email='doug.hellmann@dreamhost.com',

    url='https://github.com/dreamhost/ceilometerclient',

    packages=setuptools.find_packages(exclude=['bin']),
    include_package_data=True,

    test_suite='nose.collector',

    scripts=[],

    install_requires=['requests'],

    zip_safe=False,
    )
