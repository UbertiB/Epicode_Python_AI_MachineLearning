## Quick project summary

This is a single-script data-analysis project for a retail electronics chain. The main script is `ProgettoFinale.py` and it expects a CSV named `vendite.csv` in the same directory.

Key libraries: pandas, numpy, matplotlib.

## How to run (dev)

1. Install dependencies (Windows PowerShell):

```powershell
pip install pandas numpy matplotlib
```

2. Run the main script from project root:

```powershell
python ProgettoFinale.py
```

Note: the script will prompt "Vuoi visualizzare i grafici (parte 5) S/N?" — in non-interactive runs set up a small wrapper to bypass the prompt or edit the script.

## Data contract (required CSV columns)

The code expects `vendite.csv` with these columns (exact spelling):

- `Data` (YYYY-MM-DD)
- `Negozio` (string)
- `Prodotto` (string)
- `Quantita` (integer)  <-- IMPORTANT: no accent, code uses `Quantita`
- `Prezzo_unitario` (float)

Example CSV row:

```
2023-09-01,Milano,Smartphone,5,499.99
```

## Important code patterns & conventions

- The project is a single-module script divided into numbered "Parte 1..5" sections inside `ProgettoFinale.py`.
- Numeric heavy-lifting uses NumPy arrays derived from Pandas columns (e.g. `df_vendite["Quantita"].to_numpy()`), and results are cross-checked with DataFrame columns (e.g. `np.allclose(...)`).
- Grouping/aggregation uses Pandas `groupby` to produce per-store and per-product summaries: see `df_vendite.groupby(["Negozio"])` and `df_vendite.groupby(["Negozio","Prodotto"])`.
- The script adds an `Incasso` column computed as `Quantita * Prezzo_unitario` and prints aggregates like `.sum()` and `.mean()`.

## Integration & I/O

- Input: only `vendite.csv` in project root. There are commented helper snippets inside `ProgettoFinale.py` showing how to generate a sample dataset programmatically.
- Output: console text and optional Matplotlib figures.

## Debugging tips specific to this repo

- If the script seems to hang, it's likely waiting at the interactive prompt for S/N. To avoid interaction for automated runs, either edit the script to set `risp="N"` by default or run a small wrapper that provides input.
- Watch for column-name mismatches (accented vs non-accented): code uses `Quantita` not `Quantità`.

## Small, concrete examples for edits

- To add new analyses, follow the file's structure and place code inside the appropriate "Parte" block. Use `df_vendite` as the canonical DataFrame. For example, to compute monthly revenue, you can add:

```python
df_vendite['Data']=pd.to_datetime(df_vendite['Data'])
monthly = df_vendite.resample('M', on='Data')['Incasso'].sum()
print(monthly)
```

## Files to inspect when changing behavior

- `ProgettoFinale.py` — single source of truth for logic and flows.
- `vendite.csv` — sample/real data; maintain columns as listed above.

## When to ask the repo owner

- Confirm expected locale for decimal separators (the code assumes `.` decimal points in CSV floats).
- If you add non-interactive CI runs, ask whether plots should be saved to files or skipped.

If anything here is unclear or you'd like more examples (unit tests, a non-interactive runner, or a requirements.txt), tell me which and I'll add it.
