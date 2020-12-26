from setuptools import setup


def readme():
    with open('./README.md') as f:
        return f.read()


setup(
    name='saccrec',
    version='0.2',
    description='Saccades recording using OpenBCI Hardware',
    long_description=readme(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha'
    ],
    url='https://github.com/rdlfgrcwork/saccrec',
    author='Rodolfo Valentín García Bermúdez',
    author_email='rodgarberm@gmail.com',
    license='GPLv3',
    scripts=[
        'bin/SaccRec.py',
    ],
    data_files=[
        ('share/icons', ['data/SaccRec.png']),
        ('share/applications', ['data/SaccRec.desktop']),
    ],
    packages=[
        'saccrec',
        'saccrec.core',
        'saccrec.engine',
        'saccrec.gui',
        'saccrec.gui.icons',
        'saccrec.gui.widgets',
        'saccrec.gui.wizards',
        'saccrec.gui.wizards.setup',
    ],
    requires=[
        'PySide6',
        'numpy',
    ],
    # include_package_data=True,
    zip_safe=False
)
