---
name: notebook-clean-generation
description: Refresh the suanPan manual notebook examples and their generated markdown. Use when re-executing notebooks against a rebuilt suanPan binary, converting notebooks to markdown, or cleansing notebook outputs for a documentation sync.
---

# Notebook clean generation

Re-execute every Jupyter notebook in `docs/` against the current suanPan
binary, regenerate its markdown page and image assets, and leave the notebooks
output-free and minimal.

## 1. Build suanPan

The source lives in `../suanPan`. `SUANPAN_MT` is enabled by
`SP_BUILD_PARALLEL`, and the examples that read `.h5` record files need
`SP_ENABLE_HDF5=ON`; without it `hdf5recorder` silently writes `.txt`.

```bash
cmake -S ../suanPan -B /tmp/opencode/suanpan-build \
  -DCMAKE_BUILD_TYPE=Release \
  -DSP_BUILD_PARALLEL=ON \
  -DSP_ENABLE_HDF5=ON \
  -DCMAKE_INSTALL_PREFIX=/tmp/opencode/suanpan-install
cmake --build /tmp/opencode/suanpan-build --target install --parallel
```

Check `suanPan -v` and confirm the TBB line. Put a `suanpan` symlink to the
installed binary on `PATH`. Run every notebook with `OMP_WAIT_POLICY=passive`
to avoid spin-wait overhead.

## 2. Prepare Python

This environment is externally managed, so install into a target directory
and expose it via `PYTHONPATH`:

```bash
pip install --target /tmp/opencode/pylibs -r requirements.txt \
  jupyter nbconvert nbformat ipykernel matplotlib scipy
```

Create a kernelspec in `JUPYTER_PATH` whose `env` sets `PYTHONPATH`,
`PATH` (with the `suanpan` symlink), `LD_LIBRARY_PATH` (installed TBB libs)
and `OMP_WAIT_POLICY=passive`. Include the nbconvert template directory in
`JUPYTER_PATH` or `--to markdown` will fail after setting a custom
`JUPYTER_PATH`.

The AISC v15 download URL returns 403. The notebooks must use the bundled
`docs/Library/Section/Code/aisc-shapes-database-v16.0.xlsx` instead; from
`docs/Example/Structural/Dynamics/` the path is
`../../../Library/Section/Code/aisc-shapes-database-v16.0.xlsx`.

## 3. Notebook authoring rules

- Run suanPan inside a temporary directory. Never leave `.sp`, `.h5`, `.txt`,
  `DIST.tex`, or recorder JSON files in the documentation tree. Use
  `TemporaryDirectory` for models and result files.
- `thin-walled-section.zip` bundles the validation H5 records; extract them
  into a temporary directory before reading them.
- Suppress unwanted `execute_result` text with `_ = <call>` (for example
  `_ = to_fibre_section(...)`, `_ = plt.legend(...)`, `_ = main_file.write(...)`).
  A bare `pass` used to do this but triggers ruff warnings; a trailing semicolon
  triggers E703. `ruff check` on all notebooks must pass.
- Use `$$...$$` for all math, including inline expressions. Convert single
  dollar math in both notebook markdown cells and generated markdown.
- Keep one sentence per line, state facts only, and proofread prose before
  regenerating. Typical defects are "the assist of" (use "the aid of"),
  "musted/recommanded" (use "recommended"), "not any" (use "not every"),
  and "a AF" (use "an AF-type").
- Transient completion/highlight JSON files written by the section validation
  notebooks are unused by the site; delete them after execution.

## 4. Process each notebook

For every `docs/**/*.ipynb`:

1. `nbconvert --clear-output --inplace` to drop existing outputs.
2. `nbconvert --to notebook --execute --inplace` with the prepared kernel and
   environment, cwd set to the notebook directory.
3. Verify no `error` outputs exist and that each plotting cell produced the
   expected image count.
4. `nbconvert --to markdown`. This writes `<name>.md` and `<name>_files/`.
5. Remove every file in `<name>_files/` that the generated `.md` does not
   reference. Keep only image references prefixed with the notebook stem;
   markdown links such as `three-storey-frame.svg` are not generated assets.
6. Assert the number of files in `<name>_files/` equals the number tracked in
   `HEAD`. A changed count means a plot was skipped or an output was added.
7. Delete transient suanPan record files created during execution.
8. `nbconvert --clear-output --inplace` again.
9. Strip `metadata.execution` from every cell so the notebook stays minimal.
10. Strip trailing whitespace and the trailing blank line from the generated
    markdown; `git diff --check` must pass.

## 5. Wire up new pages

When a notebook is converted for the first time:

- Add its `.ipynb` to the `mkdocs-jupyter` `ignore` list in `mkdocs.yml` so
  MkDocs does not render both the notebook and the markdown page.
- Add the new `.md` to the relevant `docs/SUMMARY.md` TOC.

## 6. Verify and commit

```bash
git diff --check
python -m zensical build          # must report "No issues found"
git status --short --untracked-files=all
```

Confirm no broken markdown image references, no unused files in any `_files`
directory, all notebooks have zero outputs, and asset counts match `HEAD`.
Stage everything (including new markdown, images, updated PDFs and archives),
then commit on a feature branch and push.
