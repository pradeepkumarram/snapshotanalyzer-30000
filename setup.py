from setuptools import setup


setup(
    name='Snapshot Analyzer 30000',
    version='0.1',
    author='Pradeep Kumar',
    author_email='pradeep.139@gmail.com',
    description='Manage AWS EC2 snapshots',
    license='GPLv3+',
    packages=['shotty'],
    url='https://github.com/pradeepkumarramasamy/snapshotanalyzer-30000',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',

)
