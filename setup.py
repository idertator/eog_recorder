from setuptools import setup


def readme():
    with open('./README.md') as f:
        return f.read()


def requirements() -> List[str]:
    with open('requirements/base.txt') as f:
        return [
            line.strip()
            for line in f if line.strip() != ''
        ]


setup(
    name='saccrec',
    version='1.0.0-alpha',
    description='Saccades recording using OpenBCI Hardware',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],
    url='https://github.com/rdlfgrcwork/saccrec',
    author='Roberto Antonio Becerra García',
    author_email='idertator@gmail.com',
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
        'saccrec.gui',
        'saccrec.gui.dialogs',
        'saccrec.gui.icons',
        'saccrec.gui.widgets',
        'saccrec.gui.wizards',
        'saccrec.gui.wizards.setup',
        'saccrec.recording',
    ],
    install_requires=requirements(),
    python_requires='>=3.9',
    include_package_data=True,
    zip_safe=False
)
