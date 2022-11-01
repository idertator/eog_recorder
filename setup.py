from setuptools import setup


def readme():
    with open("./README.md") as f:
        return f.read()


def requirements() -> list[str]:
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() != ""]


setup(
    name="saccrec",
    version="1.0.1",
    description="Saccade Recorder",
    long_description=readme(),
    classifiers=[
        "Environment :: X11 Applications",
        "Intended Audience :: Education",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://git.topgroupexpress.com/eog/saccrec",
    author="Roberto Antonio Becerra García",
    author_email="idertator@gmail.com",
    license="GPLv3",
    entry_points={
        "gui_scripts": ["SaccRec = saccrec:main"],
        "console_scripts": [
            "TestOpenEOGRecordings = saccrec.recording.test_recording:main"
        ],
    },
    data_files=[
        ("share/icons", ["data/SaccRec.png"]),
        ("share/applications", ["data/SaccRec.desktop"]),
    ],
    packages=[
        "saccrec",
        "saccrec.core",
        "saccrec.gui",
        "saccrec.gui.dialogs",
        "saccrec.gui.icons",
        "saccrec.gui.widgets",
        "saccrec.gui.wizards",
        "saccrec.gui.wizards.setup",
        "saccrec.recording",
    ],
    install_requires=requirements(),
    python_requires=">=3.11",
    include_package_data=True,
    zip_safe=False,
)
