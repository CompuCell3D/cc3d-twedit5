import os
from setuptools import setup, find_packages

rootdir = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(rootdir, 'VERSION.txt')
twedit_version = open(version_path).readline().strip()

setup(name='cc3d-twedit5',
      author='T.J. Sego, Maciek Swat',
      classifiers=[
          'Intended Audience :: Science/Research'
      ],
      description='Twedit: an IDE for developing models, simulations and extensions for CompuCell3D',
      url='https://compucell3d.org',
      version=twedit_version,
      packages=find_packages(
            include=['cc3d.twedit5', 'cc3d.twedit5.*']
      ),
      include_package_data=True,
      package_data={
            '': [
                  '*.information', '*.qrc', '*.*.template', '*.xml'
            ],
            'cc3d.twedit5': [
                  'APIs/*',
                  'icons/*',
                  'libs/*',
                  'Plugins/CC3DCPPHelper/*',
                  'Plugins/CC3DMLHelper/*',
                  'Plugins/CC3DProject/*',
                  'Plugins/CC3DProject/icons/*',
                  'Plugins/CC3DPythonHelper/*',
                  'Plugins/CompuCell3D/*',
                  'Plugins/CompuCell3D/icons/*',
                  'themes/*'
            ]
      },
      entry_points={
          'gui_scripts': ['cc3d-twedit5 = cc3d.twedit5.__main__:main']
      }
      )
