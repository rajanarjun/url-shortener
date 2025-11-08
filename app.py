from flask import Flask, render_template
import utils
import database
import base62


app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/su")
def short_url(long_url: str):
    try:
        valid_url = utils.validate_url(long_url)
        if not valid_url:
            raise utils.InvalidURL("Invalid URL")

        db_id = database.insert_db(long_url)
        encoded_string = base62.encode(db_id)
        short_url_path = f"{settings.BASE_URL}/su/{encoded_string}"

        return render_template("result.html", original=long_url, short=short_url_path)

    except Exception as e:
        return render_template("error.html", error=e)


if __name__ == "__main__":
    app.run(debug=True)
