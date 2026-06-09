# Classic Computer Vision Environment

This workspace is set up for learning classic computer vision with Python 3.
It intentionally avoids deep-learning packages such as Ultralytics, PyTorch, and TensorFlow.

## Activate

```bash
source .venv/bin/activate
```

## Install or Refresh Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Use With Jupyter

```bash
python -m ipykernel install --user --name cpv301-classic-cv --display-name "CPV301 Classic CV"
jupyter lab
```

## Verify

```bash
python scripts/check_env.py
```
