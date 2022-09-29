PYTHON_VERSION="$(python --version)"
echo "Python version: $PYTHON_VERSION"

echo "Installing packages from 'requirements.txt'"
pip install -r ../requirements.txt

echo "Executing tests for the 'challenges' app."
python manage.py test challenges
