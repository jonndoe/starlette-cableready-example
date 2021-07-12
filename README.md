# An example Starlette with CableReady application



Install and run:

```shell
git clone https://github.com/encode/starlette-example.git
conda env create -f environment.yml
conda activate env38_starlette
cd starlette-example
pip install -f requirements.txt
python app.py
```

Open `http://127.0.0.1:8000/` in your browser:

Navigate to path that is not routed, eg `http://127.0.0.1:8000/nope`:

Raise a server error by navigating to `http://127.0.0.1:8000/error`:

Switch the `app = Starlette(debug=True)` line to `app = Starlette()` to see a regular 500 page instead.

base templates: https://github.com/encode/starlette-example
