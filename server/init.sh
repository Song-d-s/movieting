echo "��� python 가상환경 설정"
python -m venv venv
echo "��� python 가상환경 실행"
source venv/Scripts/activate
echo "��� pip requirment 설치"
pip install -r requirements.txt
echo "��� make migrations..."
python manage.py makemigrations
echo "��� migrate..."
python manage.py migrate
echo "��� load data..."
python manage.py loaddata actors.json directors.json genres.json keywords.json movies.json
