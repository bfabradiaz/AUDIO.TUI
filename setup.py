from setuptools import setup, find_packages

setup(
    name="audio-tui",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "textual>=0.1.18",
        "rich>=13.0.0",
        "pydub>=0.25.1",
        "sounddevice>=0.4.6",
        "numpy>=1.24.0",
        "librosa>=0.10.0",
        "soundfile>=0.12.1",
        "python-vlc>=3.0.18121",
    ],
    entry_points={
        'console_scripts': [
            'audio-tui=audio.tui.app:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.css', '*.txt'],
    },
)
