### Usage

```shell
cd /path/to/MyBlog/  

python3 -m venv venv

pip3 install -r requirements.txt

export FLASK_APP=flaskr

flask init-db

flask run

flask run --host=0.0.0.0 (if you want see the website at phones)

```
Then you can open `localhost:5000` or `127.0.0.1` to see the website
