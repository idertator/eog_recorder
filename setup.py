from setuptools import setup

def readme():
    with open('./README.md') as f:
        return f.read()

setup(
    name='saccrec',
    version='0.1',
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
        ('share/icons', ['install/SaccRec.png']),
        ('share/applications', ['install/SaccRec.desktop']),
    ],
    packages=[
        'saccrec',
        'saccrec.core',
        'saccrec.core.models',
        'saccrec.engine',        
        'saccrec.gui',
        'saccrec.gui.dialogs',
        'saccrec.gui.dialogs.settings',
        'saccrec.gui.icons',
        'saccrec.gui.widgets',
        'saccrec.gui.wizards',
    ],
    requires=[
        'PyQt5',
        'numpy',
        'scipy',
    ],
    include_package_data=True,
    zip_safe=False
)
