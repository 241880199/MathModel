"""扫描 corpus/历届优秀论文/ 全部 PDF 的水印形态。

判定三件事：
  1. 水印对象在哪（PieceInfo/Watermark 的 Form XObject，或 /OC 图层）
  2. 水印文字是什么（解 CID 串）
  3. 是否存在"烤进图像"的水印（大图 + 水印色像素占比）

用法：python tools/scan_watermarks.py [--json out.json] [--limit N]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "corpus" / "历届优秀论文"

HEX_TJ = re.compile(rb"\[<([0-9a-fA-F]+)>\]\s*TJ")
TEXT_SHOW = re.compile(rb"\(([^)]*)\)\s*Tj")


def decode_cid(hexstr: str) -> str:
    """把 Adobe CMap 的 2 字节 CID 串按常见中文编码解出。"""
    raw = bytes.fromhex(hexstr)
    if len(raw) % 2:
        return ""
    out = []
    for enc in ("gb18030", "gbk", "big5", "utf-16-be"):
        try:
            s = raw.decode(enc)
            if s.isprintable():
                out.append((enc, s))
        except Exception:
            pass
    return out


def wm_objects(doc):
    """返回所有带 PieceInfo/Watermark 标记的 xref，及其解出的文字。"""
    found = []
    for x in range(1, doc.xref_length()):
        try:
            o = doc.xref_object(x, compressed=True)
        except Exception:
            continue
        if "/PieceInfo" not in o or "/Watermark" not in o:
            continue
        entry = {"xref": x, "has_oc": "/OC" in o}
        try:
            st = doc.xref_stream(x) or b""
        except Exception:
            st = b""
        entry["stream_len"] = len(st)
        txts = []
        for m in HEX_TJ.finditer(st):
            for enc, s in decode_cid(m.group(1).decode()):
                txts.append({"enc": enc, "text": s})
        for m in TEXT_SHOW.finditer(st):
            txts.append({"enc": "literal", "text": m.group(1).decode("latin-1")})
        entry["texts"] = txts
        # 颜色
        entry["red"] = bool(re.search(rb"1 0 0 rg", st))
        tf = re.findall(rb"/(\S+)\s+([\d.]+)\s+Tf", st)
        entry["font"] = [m[0].decode("latin-1") for m in tf]
        entry["fontsize"] = [float(m[1]) for m in tf]
        found.append(entry)
    return found


def image_watermark_check(doc, max_pages=6):
    """抽样页面：看是否有大图，以及红色像素占比（烤进图的红色水印）。"""
    res = []
    for i in range(min(max_pages, len(doc))):
        p = doc[i]
        try:
            imgs = p.get_images(full=True)
        except Exception:
            imgs = []
        big = 0
        for im in imgs:
            w, h = im[2], im[3]
            if w * h > 200_000:
                big += 1
        res.append({"page": i + 1, "n_img": len(imgs), "n_big": big})
    return res


def scan_one(path: Path):
    rec = {"file": str(path.relative_to(ROOT)), "ok": True}
    try:
        doc = fitz.open(path)
    except Exception as e:
        return {**rec, "ok": False, "error": f"open: {e}"}
    try:
        rec["pages"] = len(doc)
        rec["needs_pass"] = doc.needs_pass
        if doc.needs_pass:
            return rec
        wms = wm_objects(doc)
        rec["n_wm"] = len(wms)
        wmtexts = set()
        for w in wms:
            for t in w["texts"]:
                if t["enc"] in ("gb18030", "gbk"):
                    wmtexts.add(t["text"])
        rec["wm_texts"] = sorted(wmtexts)
        rec["wm_red"] = any(w["red"] for w in wms)
        rec["pages_img"] = image_watermark_check(doc)
        # 全文文本里是否出现水印字串
        sample = "".join(doc[i].get_text() for i in range(min(3, len(doc))))
        rec["text_has_wm"] = any(t in sample for t in wmtexts)
        rec["text_len_p1"] = len(doc[0].get_text() or "")
        rec["is_scanned"] = rec["text_len_p1"] < 120
    except Exception as e:
        rec["ok"] = False
        rec["error"] = f"scan: {e}"
    finally:
        doc.close()
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(ROOT / "build" / "watermark-scan.json"))
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    files = sorted(PAPERS.rglob("*.pdf"))
    if args.limit:
        files = files[: args.limit]
    print(f"扫描 {len(files)} 份 PDF ...", file=sys.stderr)

    out = []
    for i, f in enumerate(files, 1):
        rec = scan_one(f)
        out.append(rec)
        flag = "" if rec.get("n_wm") else "  <-- 无标准水印"
        print(f"[{i:3}/{len(files)}] {rec['file'][-52:]} wm={rec.get('n_wm')} "
              f"text={rec.get('wm_texts')} scan={rec.get('is_scanned')}{flag}",
              file=sys.stderr)

    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    # 字节级写入，不经过文本模式。
    #
    # 默认输出是 build/（git 忽略），但 **文档化的复现命令会把它写进
    # tests/papers/recon/**，该目录已标 `-text`**（逐字节保真）：
    # `python tools/scan_watermarks.py --json tests/papers/recon/watermark-scan.json`
    # 此时若用 write_text，Windows 默认写 CRLF，而入库的是 LF——`-text` 之后
    # git 不再代为归一化，重跑一次就会把 CRLF 提交进去，静默抵消归一化。
    # 故无论落点在哪，一律字节级写入。
    #
    # 不加尾随换行——已入库的 watermark-scan.json 末字节是 `]`，
    # 改了就会让"重跑 == 入库"这条不再成立，证据的逐字节保真随之失效。
    Path(args.json).write_bytes(
        json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
    )
    print(f"\n结果写入 {args.json}", file=sys.stderr)

    # 汇总
    from collections import Counter
    print("\n=== 汇总 ===")
    print("总数:", len(out))
    print("无 PieceInfo/Watermark 水印:", sum(1 for r in out if not r.get("n_wm")))
    print("疑似扫描件(首页文字<120):", sum(1 for r in out if r.get("is_scanned")))
    print("文本层直接含水印字:", sum(1 for r in out if r.get("text_has_wm")))
    print("\n水印文字分布:")
    for t, c in Counter(tuple(r.get("wm_texts") or ["(无)"]) for r in out).most_common(20):
        print(f"  {c:4}  {t}")
    print("\n各合集:")
    for t, c in Counter(
        str(Path(r["file"]).parts[2]) if len(Path(r["file"]).parts) > 2 else "?"
        for r in out if r.get("file")
    ).most_common():
        print(f"  {c:4}  {t}")
    print("\n失败:", [r["file"] for r in out if not r.get("ok")][:10])


if __name__ == "__main__":
    main()
