from setuptools import setup, find_packages

requires = [
    'pandas',
    'xlsxwriter',
]

setup(
    name='ambrmreport',
    version='0.1.0',
    description='Get report for Ambari metrics in XLS format with graphs',
    author='McWladkoE',
    author_email='svevladislav@gmail.com',
    url='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requires,
    entry_points="""\
        [console_scripts]
        ambrmreport_report = ambrmreport.report:main
    """,
)
