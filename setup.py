from setuptools import setup

with open('README.md', 'r') as fin:
    long_description = fin.read()

setup(
     name='slurm-cola',
     version='0.0.1',
     author='Cyril Danilevski',
     author_email='cydanil@gmail.com',
     description='A tool to easily cancel slurm jobs belonging together',
     long_description=long_description,
     long_description_content_type="text/markdown",
     url='https://github.com/cydanil/slurm-cola',
     packages=['slurm_cola'],
     install_requires=['PyQt5>=5.12.0'],
     tests_require=['pytest'],
     python_requires='>=3.6',
     entry_points={
          "console_scripts": [
              'slurm-cola = slurm_cola.main:main',
          ],
     },
     classifiers=[
         'Environment :: X11 Applications :: Qt',
         'Intended Audience :: Developers',
         'Intended Audience :: Science/Research',
         'License :: OSI Approved :: BSD License',
         'Operating System :: POSIX :: Linux',
         'Topic :: Scientific/Engineering',
        ],
)
