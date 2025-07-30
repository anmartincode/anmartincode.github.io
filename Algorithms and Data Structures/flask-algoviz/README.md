# Flask-AlgoViz

Flask-AlgoViz is an interactive visualization tool for data structures and algorithms, built with Flask (Python) and a modern HTML/CSS/JS frontend.

## Features
- Choose and visualize AVL Tree, Min/Max Heap, and Graph (adjacency-list)
- Step through operations (insertion, deletion, search, etc.)
- Live, animated SVG visualizations
- Operation log and replay
- Benchmarking and export (CSV)
- Responsive, dark-mode UI

## Setup
1. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   export FLASK_APP=app
   flask run
   ```

## Contributing
- Expand algorithms in `app/algorithms/`
- Improve UI in `app/templates/` and `app/static/`
- PRs welcome!
