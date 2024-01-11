from setuptools import find_packages,setup

setup(
  name='mcqgenerator',
  version='0.1',
  author="Abdul Qadir",
  author_email="abdulkadir9929@gmail.com",
  install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
  packages=find_packages()
)