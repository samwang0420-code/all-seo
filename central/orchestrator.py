#!/usr/bin/env python3
"""
SEO Agent Central Orchestrator v2
总控脚本：驱动三个 agent 批量生成，收集结果，处理错误
"""
import subprocess, sys, json, re, os
from datetime import datetime
from pathlib import Path

OUTPUT = Path("/root/.openclaw/workspace-crm/central/reports")
OUTPUT.mkdir(parents=True, exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")
REPORT = OUTPUT / (TODAY + ".json")
LOG_FILE = OUTPUT / (TODAY + ".log")

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    colors = {"INFO": "\033[96m", "OK": "\033[92m", "WARN": "\033[93m", "ERROR": "\033[91m", "STEP": "\033[95m"}
    c = colors.get(level, "\033[0m")
    print(f"{c}[{ts}][{level}] {msg}\033[0m")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}][{level}] {msg}\n")

def run_cmd(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT", -1
    except Exception as e:
        return False, "", str(e), -1

# ── Agent 1: 错误码站 ──────────────────────────────────────
def run_error_code_agent():
    log("=== Agent 1: 错误码站 ===", "INFO")
    brands = ["hisense", "lg", "samsung", "whirlpool", "ge", "maytag", "kenmore",
              "bosch", "frigidaire", "electrolux", "amana", "kitchenaid"]
    categories = ["washer", "dryer"]
    codes = ["E1", "E2", "E3", "E4", "E5", "OE", "IE", "DE", "LE", "UE",
             "TE", "PE", "HE", "HE1", "HE2", "LE1", "E6", "E7", "E8", "E9", "PF", "CL"]
    total_gen, total_err, err_samples = 0, 0, []

    for brand in brands:
        for category in categories:
            for code in codes:
                slug_url = "https://uscomplianceguard.com/error/" + brand + "/" + category + "/" + code + "/"
                cmd = ("python3 /root/.openclaw/workspace-crm/notebooklm_seo/error_code_generator.py "
                       "--brand " + brand + " --category " + category + " --code " + code + " "
                       "--model \"" + brand + " " + category + "\" "
                       "--url \"" + slug_url + "\" --format md 2>&1")
                ok, out, err, rc = run_cmd(cmd, timeout=20)
                if ok and "Generated:" in out:
                    total_gen += 1
                elif not ok:
                    total_err += 1
                    if len(err_samples) < 3:
                        err_samples.append(brand + "/" + category + "/" + code + ": " + err[:80])

    status = "ERROR" if total_err > total_gen * 0.1 else "OK"
    log("错误码站: " + str(total_gen) + " 页, " + str(total_err) + " 错误", "OK" if status == "OK" else "ERROR")
    return {"agent": "error-code", "site": "uscomplianceguard.com",
            "total_generated": total_gen, "total_errors": total_err,
            "error_samples": err_samples, "status": status}

# ── Agent 2: 供应站 ───────────────────────────────────────
def run_supply_agent():
    log("=== Agent 2: 供应站 ===", "INFO")
    slugs = {
        "product": ["clothing", "shoes", "bags", "electronics", "sports",
                    "beauty-products", "toys", "fitness-equipment"],
        "city": ["shenzhen", "guangzhou", "yiwu", "ningbo", "dongguan", "qingdao"],
        "service": ["sourcing", "inspection", "shipping"],
        "guide": ["moq-guide", "quality-control", "shipping-guide",
                  "incoterms-guide", "sourcing-guide"],
    }
    total_gen, total_err, err_samples = 0, 0, []

    for ptype, slug_list in slugs.items():
        for slug in slug_list:
            base_url = "https://uscompliance-team.com/" + slug + ".html"
            cmd = ("python3 /root/.openclaw/workspace-crm/notebooklm_seo/supply_generator.py "
                   "--type " + ptype + " --slug " + slug + " --url \"" + base_url + "\" 2>&1")
            ok, out, err, rc = run_cmd(cmd, timeout=20)
            if ok and "Generated:" in out:
                total_gen += 1
            else:
                total_err += 1
                if len(err_samples) < 3:
                    err_samples.append(ptype + "/" + slug + ": " + err[:80])

    status = "ERROR" if total_err > 0 else "OK"
    log("供应站: " + str(total_gen) + " 页, " + str(total_err) + " 错误", "OK" if status == "OK" else "ERROR")
    return {"agent": "supply", "site": "uscompliance-team.com",
            "total_generated": total_gen, "total_errors": total_err,
            "error_samples": err_samples, "status": status}

# ── Agent 3: 城市数据站 ───────────────────────────────────
def run_city_agent():
    log("=== Agent 3: 城市数据站 ===", "INFO")
    cities = [
        ("New York", "NY", "8,336,817", "$740,000", "$3,500", "$75,000", "45", "7.0"),
        ("Los Angeles", "CA", "3,979,576", "$790,000", "$2,700", "$68,000", "52", "6.8"),
        ("Chicago", "IL", "2,693,976", "$309,000", "$1,500", "$65,000", "48", "7.2"),
        ("Houston", "TX", "2,304,580", "$245,000", "$1,250", "$58,000", "55", "6.5"),
        ("Phoenix", "AZ", "1,608,139", "$380,000", "$1,350", "$62,000", "50", "7.3"),
        ("Philadelphia", "PA", "1,584,064", "$220,000", "$1,200", "$52,000", "58", "6.8"),
        ("San Antonio", "TX", "1,434,625", "$215,000", "$1,050", "$50,000", "42", "7.5"),
        ("San Diego", "CA", "1,386,932", "$840,000", "$2,800", "$79,000", "38", "7.8"),
        ("Dallas", "TX", "1,288,257", "$295,000", "$1,300", "$55,000", "52", "6.9"),
        ("San Jose", "CA", "1,013,240", "$1,400,000", "$3,200", "$120,000", "30", "8.5"),
        ("Austin", "TX", "950,715", "$485,000", "$1,350", "$75,000", "38", "8.1"),
        ("Jacksonville", "FL", "950,181", "$285,000", "$1,180", "$55,000", "48", "7.0"),
        ("Fort Worth", "TX", "935,116", "$265,000", "$1,150", "$58,000", "46", "7.1"),
        ("Columbus", "OH", "898,553", "$235,000", "$1,000", "$52,000", "40", "7.4"),
        ("Charlotte", "NC", "874,579", "$320,000", "$1,200", "$60,000", "44", "7.3"),
        ("Indianapolis", "IN", "863,002", "$215,000", "$950", "$48,000", "50", "6.9"),
        ("Seattle", "WA", "749,256", "$720,000", "$2,400", "$92,000", "35", "8.0"),
        ("Denver", "CO", "716,492", "$510,000", "$1,650", "$82,000", "38", "8.3"),
        ("Washington", "DC", "689,545", "$620,000", "$2,200", "$90,000", "50", "6.7"),
        ("Boston", "MA", "675,647", "$680,000", "$2,600", "$85,000", "42", "7.6"),
        ("Nashville", "TN", "670,820", "$395,000", "$1,400", "$64,000", "45", "7.5"),
        ("Baltimore", "MD", "585,708", "$235,000", "$1,250", "$52,000", "60", "6.3"),
        ("Oklahoma City", "OK", "687,725", "$185,000", "$875", "$48,000", "44", "7.2"),
        ("Louisville", "KY", "617,638", "$215,000", "$950", "$50,000", "46", "7.0"),
        ("Portland", "OR", "641,162", "$525,000", "$1,600", "$72,000", "40", "7.8"),
        ("Las Vegas", "NV", "641,824", "$365,000", "$1,300", "$58,000", "52", "6.5"),
        ("Milwaukee", "WI", "569,330", "$205,000", "$950", "$47,000", "55", "6.8"),
        ("Albuquerque", "NM", "560,218", "$220,000", "$900", "$48,000", "58", "6.7"),
        ("Tucson", "AZ", "548,073", "$265,000", "$950", "$46,000", "50", "7.0"),
        ("Atlanta", "GA", "498,715", "$385,000", "$1,600", "$65,000", "48", "7.1"),
    ]

    total_gen, total_err, err_samples = 0, 0, []

    # 使用批量生成器处理 sitemap 中的全部城市
    slug_file = "/root/.openclaw/workspace-crm/central/all_city_slugs.txt"
    if os.path.exists(slug_file):
        cmd = ("python3 /root/.openclaw/workspace-crm/central/batch_city_generator.py "
               "--file " + slug_file + " 2>&1")
        ok, out, err, rc = run_cmd(cmd, timeout=7200)  # 2h max for 1000 cities
        if ok:
            # 解析输出
            m = re.search(r"完成: 生成 (\d+)/(\d+) 页, 错误 (\d+) 个", out)
            if m:
                total_gen = int(m.group(1))
                total_err = int(m.group(3))
            else:
                # 统计生成的文件数
                total_gen = len([f for f in Path("/root/.openclaw/workspace-crm/notebooklm_seo/output/city-data").glob("**/*.html")])
        else:
            total_err = 1
            err_samples = [err[:200]]
    else:
        # Fallback: 使用内置城市列表
        for city, st, pop, home, rent, income, crime, liv in cities:
            slug = city.lower().replace(" ", "-") + "-" + st.lower()
            url = "https://getuscompliance.com/city/" + slug
            cmd = (
                "python3 /root/.openclaw/workspace-crm/notebooklm_seo/city_data_generator.py "
                "--city \"" + city + "\" --state " + st + " "
                "--url \"" + url + "\" "
                "--population \"" + pop + "\" "
                "--median-home \"" + home + "\" "
                "--median-rent \"" + rent + "\" "
                "--median-income \"" + income + "\" "
                "--crime-index \"" + crime + "\" "
                "--livability \"" + liv + "\" "
                "--format html 2>&1"
            )
            ok, out, err, rc = run_cmd(cmd, timeout=10)
            if ok and "Generated:" in out:
                total_gen += 1
            else:
                total_err += 1
                if len(err_samples) < 3:
                    err_samples.append(city + "/" + st + ": " + err[:80])

    status = "ERROR" if total_err > 0 else "OK"
    log("城市站: " + str(total_gen) + " 页, " + str(total_err) + " 错误",
        "OK" if status == "OK" else "ERROR")
    return {"agent": "city", "site": "getuscompliance.com",
            "total_generated": total_gen, "total_errors": total_err,
            "error_samples": err_samples, "status": status}

# ── 主程序 ─────────────────────────────────────────────────
def main():
    log("=" * 50, "INFO")
    log("SEO AGENT CENTRAL ORCHESTRATOR 启动 " + TODAY, "INFO")
    log("=" * 50, "INFO")
    open(LOG_FILE, "w").close()

    results = {"date": TODAY, "timestamp": datetime.now().isoformat(), "agents": []}

    for fn, name in [(run_error_code_agent, "错误码站"),
                      (run_supply_agent, "供应站"),
                      (run_city_agent, "城市站")]:
        try:
            r = fn()
            results["agents"].append(r)
        except Exception as e:
            log(name + " 异常: " + str(e), "ERROR")
            results["agents"].append({"agent": name, "status": "CRASH", "error": str(e)})

    total_pages = sum(a.get("total_generated", 0) for a in results["agents"])
    total_errors = sum(a.get("total_errors", 0) for a in results["agents"])
    problem_agents = [a for a in results["agents"] if a.get("status") not in ("OK", None)]

    results["summary"] = {
        "total_pages": total_pages,
        "total_errors": total_errors,
        "problem_agents": [a["agent"] for a in problem_agents],
        "needs_attention": len(problem_agents) > 0 or total_errors > 0
    }

    REPORT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    log("报告: " + str(REPORT), "INFO")

    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 " + TODAY + " 生成摘要")
    print("=" * 50)
    names = {"error-code": "错误码站", "supply": "供应站", "city": "城市站"}
    icons = {"OK": "✅", "ERROR": "❌", "CRASH": "💥"}
    for a in results["agents"]:
        nm = names.get(a["agent"], a["agent"])
        icon = icons.get(a.get("status", "?"), "⚠️")
        gen = a.get("total_generated", 0)
        err = a.get("total_errors", 0)
        print("  " + icon + " " + nm + ": " + str(gen) + " 页, " + str(err) + " 错误")
    print("\n总计: " + str(total_pages) + " 页, " + str(total_errors) + " 错误")
    if problem_agents or total_errors > 0:
        print("⚠️  需要关注")
    else:
        print("✅ 全部顺利")

    return 0 if total_errors == 0 and not problem_agents else 1

if __name__ == "__main__":
    sys.exit(main())
