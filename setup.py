from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.1',
    description='Sorting files by categories',
    url='https://github.com/Yurii-Potapchuk/Hw07',
    author='Yurii Potapchuk',
    author_email='ypotapchuk01@gmail.com',
    license='UA',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)