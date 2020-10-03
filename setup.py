import setuptools

setuptools.setup(
    name='dash-google-oauth',
    version='1.1',
    author='Hossein Jazayeri',
    author_email='hossein.jaza@gmail.com',
    description='Authenticate to Dash app using Google OAuth',
    long_description=open('README.md', 'rt').read().strip(),
    long_description_content_type='text/markdown',
    url='https://github.com/hossein-jazayeri/dash-google-oauth',
    packages=['dash_google_oauth'],
    install_requires=[
        'dash>=1.2.0',
        'Flask>=1.1.1',
        'authlib==0.11',
        'ua_parser',
        'chart_studio>=1.0.0',
    ],
    classifiers=[
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    license='MIT',
)
