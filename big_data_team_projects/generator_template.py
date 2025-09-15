
#!/usr/bin/env python3
import argparse, json, uuid, random, math, gzip, os, sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

def parse_args():
    p = argparse.ArgumentParser(description="Configurable Synthetic Data Generator (no external deps)")
    p.add_argument("--config", required=True, help="Path to JSON config")
    p.add_argument("--out", required=True, help="Output file path")
    p.add_argument("--n", type=int, default=None, help="Override: number of records; else use config.entity_count")
    p.add_argument("--format", choices=["csv","jsonl"], default=None, help="Override: output format")
    p.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    p.add_argument("--gzip", action="store_true", help="Gzip-compress the output")
    return p.parse_args()

def weighted_choice(choices):
    vals, wts = zip(*choices)
    total = sum(wts) if wts else 0.0
    if total <= 0:
        return random.choice(vals)
    r = random.uniform(0, total)
    upto = 0.0
    for v, w in choices:
        upto += w
        if upto >= r:
            return v
    return vals[-1]

def pick_category(field_cfg, context):
    if "choices" in field_cfg:
        parsed = []
        for c in field_cfg["choices"]:
            if isinstance(c, dict):
                parsed.append((c["value"], float(c.get("weight", 1.0))))
            else:
                parsed.append((c, 1.0))
        return weighted_choice(parsed)
    cond = field_cfg.get("conditional_on")
    if cond:
        ref = context.get(cond)
        table = field_cfg.get("conditional_table", {})
        bucket = table.get(str(ref)) or table.get(ref) or table.get("_default")
        if not bucket:
            return "NA"
        parsed = []
        for c in bucket:
            if isinstance(c, dict):
                parsed.append((c["value"], float(c.get("weight", 1.0))))
            else:
                parsed.append((c, 1.0))
        return weighted_choice(parsed)
    return "NA"

def gen_string(field_cfg):
    pattern = field_cfg.get("pattern", "STR-{0000-9999}")
    out = []
    i = 0
    while i < len(pattern):
        ch = pattern[i]
        if ch == "{" and "}" in pattern[i:]:
            j = pattern.index("}", i+1)
            token = pattern[i+1:j]
            if token == "A-Z":
                out.append(chr(random.randint(65, 90)))
            elif token == "a-z":
                out.append(chr(random.randint(97, 122)))
            elif "-" in token and token.replace("-","").isdigit():
                lo, hi = token.split("-")
                n = random.randint(int(lo), int(hi))
                width = max(len(lo), len(hi))
                out.append(str(n).zfill(width))
            else:
                out.append(token)
            i = j + 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)

def gen_int(field_cfg):
    lo = int(field_cfg.get("min", 0))
    hi = int(field_cfg.get("max", 100))
    skew = float(field_cfg.get("skew", 1.0))
    if skew == 1.0:
        return random.randint(lo, hi)
    u = random.random()
    x = int(lo + (hi - lo) * (u ** skew))
    return max(lo, min(hi, x))

def gen_float(field_cfg):
    dist = field_cfg.get("distribution", "uniform")
    if dist == "uniform":
        lo = float(field_cfg.get("min", 0.0))
        hi = float(field_cfg.get("max", 1.0))
        return random.uniform(lo, hi)
    elif dist == "normal":
        mu = float(field_cfg.get("mean", 0.0))
        sigma = float(field_cfg.get("stddev", 1.0))
        return random.gauss(mu, sigma)
    elif dist == "lognormal":
        mu = float(field_cfg.get("mean", 0.0))
        sigma = float(field_cfg.get("stddev", 1.0))
        return random.lognormvariate(mu, sigma)
    elif dist == "exponential":
        lam = float(field_cfg.get("lambda", 1.0))
        return random.expovariate(lam)
    else:
        lo = float(field_cfg.get("min", 0.0))
        hi = float(field_cfg.get("max", 1.0))
        return random.uniform(lo, hi)

def gen_bool(field_cfg):
    p_true = float(field_cfg.get("p_true", 0.5))
    return random.random() < p_true

def gen_geo(field_cfg):
    bbox = field_cfg.get("bbox", [12.9, 77.5, 13.0, 77.7])
    lat = random.uniform(bbox[0], bbox[2])
    lon = random.uniform(bbox[1], bbox[3])
    prec = int(field_cfg.get("precision", 6))
    return round(lat, prec), round(lon, prec)

def seasonality_weight(ts, cfg):
    w = 1.0
    hod = ts.hour
    dow = ts.weekday()
    hod_cfg = cfg.get("hour_of_day", {})
    if hod_cfg:
        if str(hod) in hod_cfg:
            w *= float(hod_cfg[str(hod)])
        elif "_default" in hod_cfg:
            w *= float(hod_cfg["_default"])
    dow_cfg = cfg.get("day_of_week", {})
    if dow_cfg:
        if str(dow) in dow_cfg:
            w *= float(dow_cfg[str(dow)])
        elif "_default" in dow_cfg:
            w *= float(dow_cfg["_default"])
    return w

def gen_datetime(cfg, i, n, global_time):
    start = datetime.fromisoformat(global_time["start"])
    end   = datetime.fromisoformat(global_time["end"])
    mode = cfg.get("mode", "uniform")
    if mode == "ramp":
        t = i / max(1, n-1)
        if cfg.get("direction", "up") == "down":
            t = 1.0 - t
        delta = (end - start) * t
        return start + delta
    elif mode == "seasonality":
        seas = cfg.get("profile", {})
        for _ in range(1000):
            u = random.random()
            candidate = start + (end - start) * u
            w = seasonality_weight(candidate, seas)
            if random.random() < min(1.0, w):
                return candidate
        u = random.random()
        return start + (end - start) * u
    else:
        u = random.random()
        return start + (end - start) * u

def gen_field(field_cfg, context, i, n, global_time):
    if random.random() < float(field_cfg.get("null_prob", 0.0)):
        return None
    ftype = field_cfg["type"]
    if ftype == "uuid":
        return str(uuid.uuid4())
    if ftype == "id_sequence":
        start = int(field_cfg.get("start", 1))
        step = int(field_cfg.get("step", 1))
        return start + i * step
    if ftype == "int":
        return gen_int(field_cfg)
    if ftype == "float":
        return gen_float(field_cfg)
    if ftype == "bool":
        return gen_bool(field_cfg)
    if ftype == "category":
        return pick_category(field_cfg, context)
    if ftype == "string":
        return gen_string(field_cfg)
    if ftype == "datetime":
        dt = gen_datetime(field_cfg, i, n, global_time)
        fmt = field_cfg.get("format", "iso")
        if fmt == "epoch_ms":
            return int(dt.timestamp() * 1000)
        elif fmt == "epoch_s":
            return int(dt.timestamp())
        elif fmt == "iso":
            return dt.isoformat()
        else:
            return dt.strftime(fmt)
    if ftype == "geo":
        lat, lon = gen_geo(field_cfg)
        if field_cfg.get("as_object", True):
            return {"lat": lat, "lon": lon}
        else:
            return f"{lat},{lon}"
    if ftype == "derived_concat":
        parts = field_cfg.get("parts", [])
        sep = field_cfg.get("sep", "-")
        vals = [str(context.get(p, "")) for p in parts]
        return sep.join(vals)
    if ftype == "derived_map":
        src = field_cfg.get("from_field")
        mapping = field_cfg.get("map", {})
        default = field_cfg.get("default", None)
        key = context.get(src)
        return mapping.get(str(key), mapping.get(key, default))
    return None

def open_out(path, gz):
    if gz or path.endswith(".gz"):
        return gzip.open(path, "wt", encoding="utf-8")
    return open(path, "w", encoding="utf-8")

def write_csv_header(f, fields):
    headers = [fld["name"] for fld in fields]
    f.write(",".join(headers) + "\n")

def csv_escape(val):
    if val is None:
        return ""
    s = str(val)
    if any(c in s for c in [",", "\"", "\n"]):
        s = "\"" + s.replace("\"", "\"\"") + "\""
    return s

def write_csv_row(f, row_vals):
    out = []
    for v in row_vals:
        if isinstance(v, dict):
            import json as _json
            out.append(csv_escape(_json.dumps(v, ensure_ascii=False)))
        else:
            out.append(csv_escape(v))
    f.write(",".join(out) + "\n")

def write_jsonl_row(f, obj):
    import json as _json
    f.write(_json.dumps(obj, ensure_ascii=False) + "\n")

def main():
    args = parse_args()
    with open(args.config, "r", encoding="utf-8") as cf:
        cfg = json.load(cf)

    if args.seed is not None:
        random.seed(args.seed)
    elif "seed" in cfg:
        random.seed(int(cfg["seed"]))

    n = args.n if args.n is not None else int(cfg.get("entity_count", 1000))
    out_fmt = args.format if args.format is not None else cfg.get("output", {}).get("format", "csv")
    fields = cfg["schema"]["fields"]
    global_time = cfg.get("time_window", {
        "start": "2025-01-01T00:00:00",
        "end":   "2025-01-07T23:59:59"
    })

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open_out(args.out, args.gzip) as f:
        if out_fmt == "csv":
            write_csv_header(f, fields)
        for i in range(n):
            context = {}
            for fld in fields:
                val = gen_field(fld, context, i, n, global_time)
                context[fld["name"]] = val
            if out_fmt == "csv":
                write_csv_row(f, [context[name["name"]] for name in fields])
            else:
                write_jsonl_row(f, context)
    print(f"✅ Wrote {n} records to {args.out} (format={out_fmt}{', gzip' if args.gzip else ''})")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
