from flask import Flask

app = Flask(__name__)

app.config.from_object("config")


@app.route("/hello")
def hello():
    # return 返回包装了header和状态码
    headers = {
        "content-type":"application/json",
        "location":"http://www.baidu.com"
    }
    return "haha"
    # return "<html></html>", 301,headers
# app.add_url_rule("/hello",view_func=hello)


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])