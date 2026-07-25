.PHONY: pdf test lint validate package clean

pdf:
	cd docs && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
	cp docs/main.pdf docs/Geometric_Path_Memory.pdf

test:
	pytest

lint:
	ruff check src tests scripts

validate:
	python scripts/validate_html.py tools/open_quantum_order_lab.html tools/mmals_path_memory_lab.html
	pytest

package: pdf validate
	cd .. && zip -r mmals-geometric-path-memory.zip mmals-geometric-path-memory \
		-x '*/.venv/*' '*/__pycache__/*' '*/.pytest_cache/*' '*/docs/*.aux' \
		'*/docs/*.log' '*/docs/*.out' '*/docs/*.toc' '*/docs/*.fls' '*/docs/*.fdb_latexmk'

clean:
	cd docs && latexmk -C || true
	rm -f docs/Geometric_Path_Memory.pdf
