from setuptools import setup


setup(
    name='cldfbench_norare',
    py_modules=['cldfbench_norare'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'norare=cldfbench_norare:Dataset',
        ],
        'cldfbench.commands': [
            'norare=norarecommands',
        ]

    },
    install_requires=[
        'clldutils>=3.13.0',
        'wordcloud',
        'csvw>=3.1.3',
        'pycldf>=1.29.0',
        'cldfbench>=1.13.0',
    ],
    extras_require={
        'test': [
            'pytest-cldf>=0.3',
        ],
        'correlation': [
            'pandas',
            'seaborn',
        ],
    },
)
