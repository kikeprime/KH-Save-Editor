from dash import Dash, page_container


app = Dash("KH1 Save Editor", suppress_callback_exceptions=True, use_pages=True)

app.title = "KH1 Save Editor"

app.layout= [
    page_container,
]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
