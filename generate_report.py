import markdown, pathlib

CSS = """
body{font-family:sans-serif;max-width:860px;margin:32px auto;padding:0 24px;line-height:1.6}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:0.82em;table-layout:fixed;word-wrap:break-word}
th,td{border:1px solid #ddd;padding:5px 7px;text-align:left;overflow:hidden}
th{background:#f2f2f2;font-weight:bold}
code{background:#f4f4f4;padding:2px 5px;border-radius:3px;font-size:0.82em;word-break:break-all}
pre{background:#f4f4f4;padding:12px;border-radius:6px;overflow-x:auto;font-size:0.8em;white-space:pre-wrap;word-wrap:break-word}
pre code{background:none;padding:0}
img{max-width:100%;height:auto;display:block;margin:12px 0}
h1{color:#111;border-bottom:2px solid #ddd;padding-bottom:8px}
h2{color:#222;border-bottom:1px solid #eee;padding-bottom:4px;margin-top:32px}
h3{color:#333}
blockquote{border-left:4px solid #ddd;margin:0;padding:8px 16px;color:#555}
hr{border:none;border-top:1px solid #eee;margin:24px 0}
@media print{body{max-width:100%;padding:0 16px}table{font-size:0.75em}img{page-break-inside:avoid;page-break-before:auto;page-break-after:auto}pre{page-break-inside:avoid}blockquote{page-break-inside:avoid}}
"""

def generate(src, dest):
    md = pathlib.Path(src).read_text(encoding='utf-8')
    html = markdown.markdown(md, extensions=['tables', 'fenced_code'])
    full = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html}</body></html>"
    pathlib.Path(dest).write_text(full, encoding='utf-8')
    print(f'Done: {dest}')

generate('C:/Users/stang/polyp-detect/README.md',     'C:/Users/stang/polyp-detect/report_en.html')
generate('C:/Users/stang/polyp-detect/report_th.md',  'C:/Users/stang/polyp-detect/report_th.html')
