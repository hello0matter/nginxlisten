#!/usr/bin/env python3
"""
nginx_trace_hunter.py

面向应急溯源场景的 Nginx 日志智能分析脚本。
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import fnmatch
import json
import logging
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional


ACCESS_LOG_PATTERNS = ("*.access.log", "access.log", "*access*.log")
NGINX_CONF_PATTERNS = ("nginx.conf", "*.conf", "*.vhost", "*.config")
TEXT_SEARCH_EXTS = {
    ".conf",
    ".config",
    ".ini",
    ".env",
    ".json",
    ".yml",
    ".yaml",
    ".xml",
    ".properties",
    ".cs",
    ".java",
    ".kt",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".vue",
    ".py",
    ".php",
    ".go",
    ".rb",
    ".sh",
    ".sql",
    ".aspx",
    ".asmx",
    ".svc",
    ".cshtml",
    ".jsp",
    ".jspx",
}
ARCHIVE_SUFFIXES = (".zip", ".tar", ".tgz", ".tar.gz", ".gz", ".7z", ".rar")
SCAN_PROGRESS_LINES = 10000
SCAN_KEYWORDS = (
    "/admin",
    "/manage",
    "/login",
    "/auth",
    "/approval",
    "/upload",
    "/download",
    "/export",
    "/import",
    "/swagger",
    "/api-docs",
    "/actuator",
    "/debug",
    "/console",
    "/shell",
    "/backup",
    "/.git",
    "/.env",
    "/phpmyadmin",
    "/sql",
)
SENSITIVE_PARAM_RE = re.compile(
    r"(?:^|_)(?:id|uid|userid|applyid|projectid|patientid|orderid|recordid|docid|pid|sid)$",
    re.IGNORECASE,
)
TEXT_ENCODING_CANDIDATES = ("utf-8", "gb18030", "gbk", "latin-1")
ACCESS_LOG_RE = re.compile(
    r'^(?P<remote_addr>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<target>[^"]*?)\s+(?P<protocol>HTTP/[0-9.]+|-)"\s+'
    r'(?P<status>\d{3})\s+(?P<body_bytes>\d+|-)\s+'
    r'"(?P<referer>[^"]*)"\s+"(?P<user_agent>[^"]*)"'
    r'(?P<tail>.*)$'
)
TRAILING_IP_RE = re.compile(r'"((?:\d{1,3}\.){3}\d{1,3}|-)"\s*$')
BARE_IP_RE = re.compile(r'((?:\d{1,3}\.){3}\d{1,3})')
LOCATION_RE = re.compile(r"^\s*location\s+(?:=|~\*|~|\^~)?\s*(?P<path>\S+)\s*\{", re.IGNORECASE)
SERVER_NAME_RE = re.compile(r"^\s*server_name\s+(?P<names>[^;]+);", re.IGNORECASE)
ACCESS_LOG_CONF_RE = re.compile(r"^\s*access_log\s+(?P<path>[^ ;]+)", re.IGNORECASE)
SIMPLE_DIRECTIVE_RE = {
    "proxy_pass": re.compile(r"^\s*proxy_pass\s+(?P<value>[^;]+);", re.IGNORECASE),
    "root": re.compile(r"^\s*root\s+(?P<value>[^;]+);", re.IGNORECASE),
    "alias": re.compile(r"^\s*alias\s+(?P<value>[^;]+);", re.IGNORECASE),
    "try_files": re.compile(r"^\s*try_files\s+(?P<value>[^;]+);", re.IGNORECASE),
    "fastcgi_pass": re.compile(r"^\s*fastcgi_pass\s+(?P<value>[^;]+);", re.IGNORECASE),
    "uwsgi_pass": re.compile(r"^\s*uwsgi_pass\s+(?P<value>[^;]+);", re.IGNORECASE),
}

LOGGER = logging.getLogger("nginx_trace_hunter")


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def setup_logging(output_dir: Path) -> Path:
    ensure_dir(output_dir)
    log_path = output_dir / "hunter.log"
    LOGGER.setLevel(logging.INFO)
    LOGGER.handlers.clear()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)
    LOGGER.propagate = False
    return log_path


def log_info(message: str) -> None:
    LOGGER.info(message)


def log_error(message: str) -> None:
    LOGGER.error(message)


def open_path(path: Path) -> None:
    target = str(path)
    if os.name == "nt":
        os.startfile(target)
        return
    if sys.platform == "darwin":
        subprocess.Popen(["open", target])
        return
    subprocess.Popen(["xdg-open", target])


def safe_read_text(path: Path, size_limit: int = 2 * 1024 * 1024) -> str:
    if not path.is_file():
        return ""
    if path.stat().st_size > size_limit:
        return ""
    data = path.read_bytes()
    for enc in TEXT_ENCODING_CANDIDATES:
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="ignore")


def maybe_to_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except Exception:
        return None


def percentile_from_counter(counter: Counter[int], ratio: float) -> int:
    if not counter:
        return 0
    total = sum(counter.values())
    target = max(1, math.ceil(total * ratio))
    seen = 0
    for size in sorted(counter):
        seen += counter[size]
        if seen >= target:
            return size
    return max(counter)


def summarize_reason_tags(tags: dict[str, float]) -> list[str]:
    ordered = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    return [name for name, score in ordered if score > 0]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def app_data_root() -> Path:
    if os.name == "nt":
        base = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base)
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg)
    return Path.home() / ".config"


def default_app_root() -> Path:
    return ensure_dir(app_data_root() / "nginx_trace_hunter")


def default_cfg_path() -> Path:
    return default_app_root() / "config.json"


def default_output_dir() -> Path:
    return ensure_dir(default_app_root() / "output")


def load_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_json_file(path: Path, data: dict[str, Any]) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def post_json(url: str, payload: dict[str, Any], timeout: int = 20) -> tuple[bool, str]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            text = response.read().decode("utf-8", errors="ignore")
        return True, text[:500]
    except Exception as exc:
        return False, str(exc)


def file_name_service(path: Path) -> str:
    name = path.name
    if name.endswith(".access.log"):
        return name[: -len(".access.log")]
    if name == "access.log":
        return "default"
    return name


def path_prefixes(uri_path: str, max_depth: int = 6) -> list[str]:
    parts = [p for p in uri_path.split("/") if p]
    prefixes = ["/" + "/".join(parts[:i]) for i in range(len(parts), 0, -1)]
    if uri_path == "/":
        prefixes.append("/")
    return prefixes[:max_depth]


def derive_search_tokens(uri_path: str) -> list[str]:
    parts = [p for p in uri_path.split("/") if p]
    tokens: list[str] = []
    if uri_path and uri_path != "/":
        tokens.append(uri_path)
    if parts:
        tokens.append(parts[-1])
        tokens.extend(parts[-3:])
    compact = [p for p in parts if len(p) >= 3 and not p.isdigit()]
    tokens.extend(compact)
    camel_case_tokens: list[str] = []
    for token in list(tokens):
        camel_case_tokens.extend(re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", token))
    tokens.extend(camel_case_tokens)
    seen: set[str] = set()
    result: list[str] = []
    for token in tokens:
        clean = token.strip()
        if not clean or clean in seen or len(clean) < 3:
            continue
        seen.add(clean)
        result.append(clean)
    return result[:20]


@dataclass
class RunningSizeStats:
    count: int = 0
    total: int = 0
    total_sq: float = 0.0
    min_size: int = 0
    max_size: int = 0
    histogram: Counter[int] = field(default_factory=Counter)

    def add(self, size: int) -> None:
        self.count += 1
        self.total += size
        self.total_sq += float(size) * float(size)
        self.min_size = size if self.count == 1 else min(self.min_size, size)
        self.max_size = max(self.max_size, size)
        self.histogram[size] += 1

    @property
    def mean(self) -> float:
        if not self.count:
            return 0.0
        return self.total / self.count

    @property
    def stdev(self) -> float:
        if self.count <= 1:
            return 0.0
        mean = self.mean
        variance = max(0.0, self.total_sq / self.count - mean * mean)
        return math.sqrt(variance)

    @property
    def p95(self) -> int:
        return percentile_from_counter(self.histogram, 0.95)


@dataclass
class SampleEvent:
    timestamp: str
    method: str
    target: str
    status: int
    body_bytes: int
    host: str
    source_file: str
    referer: str
    user_agent: str
    remote_addr: str
    real_ip: str


@dataclass
class IpStats:
    total: int = 0
    bytes_total: int = 0
    unique_paths: set[str] = field(default_factory=set)
    unique_targets: set[str] = field(default_factory=set)
    methods: Counter[str] = field(default_factory=Counter)
    statuses: Counter[int] = field(default_factory=Counter)
    hosts: Counter[str] = field(default_factory=Counter)
    paths: Counter[str] = field(default_factory=Counter)
    hours: Counter[str] = field(default_factory=Counter)
    second_counts: dict[str, int] = field(default_factory=dict)
    max_rps: int = 0
    scan_hits: int = 0
    auth_hits: int = 0
    anomaly_hits: int = 0
    sample_events: list[SampleEvent] = field(default_factory=list)
    user_agents: Counter[str] = field(default_factory=Counter)
    referers: Counter[str] = field(default_factory=Counter)

    def add_sample(self, sample: SampleEvent, limit: int = 5) -> None:
        if len(self.sample_events) < limit:
            self.sample_events.append(sample)


@dataclass
class UriStats:
    total: int = 0
    bytes_stats: RunningSizeStats = field(default_factory=RunningSizeStats)
    statuses: Counter[int] = field(default_factory=Counter)
    ips: Counter[str] = field(default_factory=Counter)
    methods: Counter[str] = field(default_factory=Counter)
    hosts: Counter[str] = field(default_factory=Counter)
    second_counts: dict[str, int] = field(default_factory=dict)
    max_rps: int = 0
    sample_events: list[SampleEvent] = field(default_factory=list)
    distinct_targets: set[str] = field(default_factory=set)
    query_param_names: Counter[str] = field(default_factory=Counter)

    def add_sample(self, sample: SampleEvent, limit: int = 5) -> None:
        if len(self.sample_events) < limit:
            self.sample_events.append(sample)


@dataclass
class IpUriStats:
    total: int = 0
    bytes_stats: RunningSizeStats = field(default_factory=RunningSizeStats)
    statuses: Counter[int] = field(default_factory=Counter)
    distinct_targets: set[str] = field(default_factory=set)
    numeric_ids: set[int] = field(default_factory=set)
    numeric_overflow: int = 0
    param_names: Counter[str] = field(default_factory=Counter)
    second_counts: dict[str, int] = field(default_factory=dict)
    max_rps: int = 0
    sample_events: list[SampleEvent] = field(default_factory=list)

    def add_numeric_id(self, value: int, limit: int = 5000) -> None:
        if len(self.numeric_ids) < limit:
            self.numeric_ids.add(value)
        else:
            self.numeric_overflow += 1

    def add_sample(self, sample: SampleEvent, limit: int = 5) -> None:
        if len(self.sample_events) < limit:
            self.sample_events.append(sample)


@dataclass
class NginxLocation:
    file_path: str
    server_names: list[str]
    location: str
    directives: dict[str, str]
    access_log: Optional[str]


@dataclass
class RouteCandidate:
    uri_path: str
    source: str
    reason: str
    match_value: str
    file_path: str


@dataclass
class AnalyzerConfig:
    inputs: list[Path]
    search_roots: list[Path]
    output_dir: Path
    cfg_file: Path
    top_n: int
    focus_ips: set[str]
    focus_uris: list[str]
    from_date: Optional[dt.date]
    to_date: Optional[dt.date]
    archive_mode: str
    ai_enabled: bool
    ai_base_url: Optional[str]
    ai_model: Optional[str]
    ai_api_key: Optional[str]
    max_search_files: int
    mode: str
    interval_sec: int
    state_file: Path
    bootstrap_bytes: int
    discover_every: int
    gui_mode: bool
    alert_enabled: bool
    alert_min_score: float
    ding_url: Optional[str]
    ding_kw: Optional[str]
    wx_url: Optional[str]
    fs_url: Optional[str]


def config_to_persist_dict(config: AnalyzerConfig) -> dict[str, Any]:
    return {
        "inputs": [str(p) for p in config.inputs],
        "search_roots": [str(p) for p in config.search_roots],
        "output_dir": str(config.output_dir),
        "top_n": config.top_n,
        "focus_ips": sorted(config.focus_ips),
        "focus_uris": config.focus_uris,
        "from_date": config.from_date.isoformat() if config.from_date else None,
        "to_date": config.to_date.isoformat() if config.to_date else None,
        "archive_mode": config.archive_mode,
        "ai_enabled": config.ai_enabled,
        "ai_base_url": config.ai_base_url,
        "ai_model": config.ai_model,
        "ai_api_key": config.ai_api_key,
        "max_search_files": config.max_search_files,
        "mode": config.mode,
        "interval_sec": config.interval_sec,
        "state_file": str(config.state_file),
        "bootstrap_bytes": config.bootstrap_bytes,
        "discover_every": config.discover_every,
        "alert_enabled": config.alert_enabled,
        "alert_min_score": config.alert_min_score,
        "ding_url": config.ding_url,
        "ding_kw": config.ding_kw,
        "wx_url": config.wx_url,
        "fs_url": config.fs_url,
        "platform": platform.system(),
    }


class NginxTraceHunter:
    def __init__(self, config: AnalyzerConfig) -> None:
        self.config = config
        self.ip_stats: dict[str, IpStats] = defaultdict(IpStats)
        self.uri_stats: dict[str, UriStats] = defaultdict(UriStats)
        self.ip_uri_stats: dict[tuple[str, str], IpUriStats] = defaultdict(IpUriStats)
        self.path_size_stats: dict[str, RunningSizeStats] = defaultdict(RunningSizeStats)
        self.log_files: list[Path] = []
        self.archives_used: list[dict[str, str]] = []
        self.extracted_roots: list[Path] = []
        self.nginx_locations: list[NginxLocation] = []
        self.route_candidates: dict[str, list[RouteCandidate]] = defaultdict(list)
        self.total_records = 0
        self.parsed_records = 0
        self.failed_records = 0
        self.date_counter: Counter[str] = Counter()
        self.service_counter: Counter[str] = Counter()
        self.attack_windows: Counter[tuple[str, str]] = Counter()
        self.top_anomalies: list[dict[str, Any]] = []

    def run(self) -> dict[str, Any]:
        ensure_dir(self.config.output_dir)
        log_info(f"开始分析。mode={self.config.mode} inputs={','.join(str(p) for p in self.config.inputs)}")
        self.log_files = self.discover_log_files()
        if not self.log_files:
            log_error("未发现 access log。")
            raise RuntimeError("未发现 access log，请检查输入路径或开启归档处理。")
        log_info(f"发现日志文件 {len(self.log_files)} 个。")

        self.prepare_search_archives()
        self.nginx_locations = self.discover_nginx_locations()
        log_info(f"发现 nginx/location 候选 {len(self.nginx_locations)} 个。")
        self.first_pass()
        self.second_pass_collect_anomalies()
        suspicious_ips = self.rank_suspicious_ips()
        suspicious_uris = self.rank_suspicious_uris()
        self.route_candidates = self.map_routes_for_uris([item["uri_path"] for item in suspicious_uris[: self.config.top_n]])

        report = {
            "generated_at": dt.datetime.now().astimezone().isoformat(),
            "inputs": [str(p) for p in self.config.inputs],
            "search_roots": [str(p) for p in self.config.search_roots],
            "output_dir": str(self.config.output_dir),
            "log_files": [str(p) for p in self.log_files],
            "archives_used": self.archives_used,
            "summary": self.build_summary(suspicious_ips, suspicious_uris),
            "suspicious_ips": suspicious_ips,
            "suspicious_uris": suspicious_uris,
            "top_anomalies": self.top_anomalies[: self.config.top_n],
            "route_candidates": {
                uri: [candidate.__dict__ for candidate in candidates[:20]]
                for uri, candidates in self.route_candidates.items()
            },
            "nginx_locations": [self.location_to_dict(loc) for loc in self.nginx_locations[:500]],
        }
        report["review_ip_groups"] = self.select_review_ip_groups(report["suspicious_ips"])
        if self.config.ai_enabled and self.should_invoke_ai(report):
            log_info("触发 AI 研判。")
            report["ai_judgement"] = self.ask_ai(report)
        self.write_outputs(report)
        log_info(f"分析完成。有效记录={self.parsed_records} top_ip={(report.get('summary', {}) or {}).get('top_ip', {}).get('ip', '-')}")
        return report

    def should_invoke_ai(self, report: dict[str, Any]) -> bool:
        top_ip = report.get("summary", {}).get("top_ip") or {}
        top_uri = report.get("summary", {}).get("top_uri") or {}
        top_score = max(float(top_ip.get("score", 0) or 0), float(top_uri.get("score", 0) or 0))
        if top_score >= 35:
            return True
        return bool(report.get("top_anomalies"))

    def prepare_search_archives(self) -> None:
        archives = [root for root in self.config.search_roots if root.is_file() and self.is_archive(root)]
        if not archives:
            return
        extracted = self.extract_archives(archives)
        for root in extracted:
            if root not in self.extracted_roots:
                self.extracted_roots.append(root)

    def discover_log_files(self) -> list[Path]:
        log_files: list[Path] = []
        archives: list[Path] = []
        log_info("开始发现日志文件。")
        for root in self.config.inputs:
            if root.is_file():
                if self.is_access_log(root):
                    log_files.append(root)
                elif self.is_archive(root):
                    archives.append(root)
                continue
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.is_file():
                    if self.is_access_log(path):
                        log_files.append(path)
                    elif self.is_archive(path):
                        archives.append(path)

        if log_files:
            log_info(f"目录内直接发现 access log {len(log_files)} 个。")
            return sorted(self.filter_by_date(log_files))

        if self.config.archive_mode == "never":
            log_info("未发现日志，且已禁用归档处理。")
            return []

        extracted_roots = self.extract_archives(archives)
        log_info(f"归档解压根目录 {len(extracted_roots)} 个。")
        for root in extracted_roots:
            for path in root.rglob("*"):
                if path.is_file() and self.is_access_log(path):
                    log_files.append(path)
        log_info(f"归档内发现 access log {len(log_files)} 个。")
        return sorted(self.filter_by_date(log_files))

    def discover_nginx_locations(self) -> list[NginxLocation]:
        conf_files: list[Path] = []
        roots = list(dict.fromkeys(self.config.search_roots + self.extracted_roots))
        for root in roots:
            if root.is_file():
                if self.looks_like_nginx_conf(root):
                    conf_files.append(root)
                continue
            if not root.exists():
                continue
            for pattern in NGINX_CONF_PATTERNS:
                conf_files.extend(path for path in root.rglob(pattern) if path.is_file())
        unique_files = []
        seen = set()
        for path in conf_files:
            key = str(path.resolve())
            if key in seen:
                continue
            seen.add(key)
            unique_files.append(path)

        locations: list[NginxLocation] = []
        for conf in unique_files:
            locations.extend(self.parse_nginx_conf(conf))
        return locations

    def first_pass(self) -> None:
        for file_path in self.log_files:
            service = file_name_service(file_path)
            self.service_counter[service] += 1
            log_info(f"第一遍扫描开始: {file_path}")
            line_no = 0
            for raw_line in self.stream_lines(file_path):
                line_no += 1
                if line_no % SCAN_PROGRESS_LINES == 0:
                    log_info(f"第一遍扫描进度: file={file_path} lines={line_no} kept={self.parsed_records} failed={self.failed_records}")
                self.total_records += 1
                parsed = self.parse_access_line(raw_line, file_path)
                if not parsed:
                    self.failed_records += 1
                    continue
                if not self.keep_record(parsed):
                    continue
                self.parsed_records += 1
                self.consume_record(parsed)
            log_info(f"第一遍扫描结束: {file_path} 当前有效记录={self.parsed_records}")

    def second_pass_collect_anomalies(self) -> None:
        anomalies: list[dict[str, Any]] = []
        for file_path in self.log_files:
            log_info(f"第二遍异常检测开始: {file_path}")
            line_no = 0
            for raw_line in self.stream_lines(file_path):
                line_no += 1
                if line_no % SCAN_PROGRESS_LINES == 0:
                    log_info(f"第二遍异常检测进度: file={file_path} lines={line_no} anomalies={len(anomalies)}")
                parsed = self.parse_access_line(raw_line, file_path)
                if not parsed or not self.keep_record(parsed):
                    continue
                path_key = parsed["uri_path"]
                base = self.path_size_stats[path_key]
                size = parsed["body_bytes"]
                if not self.is_large_response_anomaly(size, base):
                    continue
                reason_bits = []
                if base.p95 and size > base.p95:
                    reason_bits.append(f"size>{base.p95}(p95)")
                if base.mean and size > base.mean * 2:
                    reason_bits.append(f"size>{int(base.mean)}x2")
                if base.stdev and size > base.mean + 3 * base.stdev:
                    reason_bits.append("size>mean+3stdev")
                anomalies.append(
                    {
                        "timestamp": parsed["timestamp"].isoformat(),
                        "uri_path": path_key,
                        "target": parsed["target"],
                        "status": parsed["status"],
                        "body_bytes": size,
                        "host": parsed["host"],
                        "remote_addr": parsed["remote_addr"],
                        "real_ip": parsed["real_ip"],
                        "referer": parsed["referer"],
                        "user_agent": parsed["user_agent"][:240],
                        "source_file": str(file_path),
                        "reason": ",".join(reason_bits) or "large-response",
                    }
                )
                self.ip_stats[parsed["real_ip"]].anomaly_hits += 1
            log_info(f"第二遍异常检测结束: {file_path} 当前异常样本={len(anomalies)}")
        anomalies.sort(key=lambda x: (x["body_bytes"], x["timestamp"]), reverse=True)
        self.top_anomalies = anomalies[: max(self.config.top_n * 5, 50)]
        log_info(f"异常检测完成。保留异常样本 {len(self.top_anomalies)} 条。")

    def rank_suspicious_ips(self) -> list[dict[str, Any]]:
        ranked: list[dict[str, Any]] = []
        for ip, stats in self.ip_stats.items():
            score_tags: dict[str, float] = {}
            unique_paths = len(stats.unique_paths)
            unique_targets = len(stats.unique_targets)
            four_xx = sum(v for k, v in stats.statuses.items() if 400 <= k < 500)
            five_xx = sum(v for k, v in stats.statuses.items() if 500 <= k < 600)
            auth_total = sum(count for path, count in stats.paths.items() if self.is_auth_path(path))
            focused_hits = sum(
                count
                for path, count in stats.paths.items()
                if any(focus in path for focus in self.config.focus_uris)
            )
            if stats.total >= 500:
                score_tags["high-volume"] = min(30.0, math.log10(stats.total) * 8)
            if stats.max_rps >= 5:
                score_tags["burst"] = min(18.0, stats.max_rps * 1.5)
            if unique_paths >= 30 and four_xx >= 10:
                score_tags["scan-probe"] = min(20.0, unique_paths * 0.12 + four_xx * 0.25)
            if stats.scan_hits >= 8:
                score_tags["sensitive-path"] = min(12.0, stats.scan_hits * 0.6)
            if auth_total >= 20:
                score_tags["auth-burst"] = min(10.0, auth_total * 0.2)
            if stats.anomaly_hits:
                score_tags["large-response"] = min(16.0, stats.anomaly_hits * 1.2)
            if focused_hits:
                score_tags["focus-uri"] = min(20.0, focused_hits * 0.15)
            if five_xx >= 5:
                score_tags["server-error-touch"] = min(8.0, five_xx * 0.5)

            enum_score = 0.0
            pair_samples: list[dict[str, Any]] = []
            for (pair_ip, uri_path), pair in self.ip_uri_stats.items():
                if pair_ip != ip:
                    continue
                enum_distinct = len(pair.numeric_ids) + pair.numeric_overflow
                if enum_distinct >= 20 and pair.total >= 20:
                    enum_score += min(12.0, enum_distinct * 0.08 + pair.total * 0.01)
                    pair_samples.append(
                        {
                            "uri_path": uri_path,
                            "total": pair.total,
                            "distinct_numeric_ids": enum_distinct,
                            "max_rps": pair.max_rps,
                            "max_body_bytes": pair.bytes_stats.max_size,
                        }
                    )
                elif pair.max_rps >= 10 and pair.total >= 30:
                    enum_score += min(8.0, pair.max_rps * 0.4)
                    pair_samples.append(
                        {
                            "uri_path": uri_path,
                            "total": pair.total,
                            "distinct_numeric_ids": enum_distinct,
                            "max_rps": pair.max_rps,
                            "max_body_bytes": pair.bytes_stats.max_size,
                        }
                    )
            if enum_score:
                score_tags["bulk-enumeration"] = min(20.0, enum_score)

            total_score = round(sum(score_tags.values()), 2)
            if total_score <= 0:
                continue
            top_paths = [{"path": path, "count": count} for path, count in stats.paths.most_common(8)]
            ranked.append(
                {
                    "ip": ip,
                    "score": total_score,
                    "reason_tags": summarize_reason_tags(score_tags),
                    "requests": stats.total,
                    "bytes_total": stats.bytes_total,
                    "max_rps": stats.max_rps,
                    "unique_paths": unique_paths,
                    "unique_targets": unique_targets,
                    "status_top": {str(k): v for k, v in stats.statuses.most_common(6)},
                    "host_top": dict(stats.hosts.most_common(5)),
                    "top_paths": top_paths,
                    "interesting_pairs": pair_samples[:8],
                    "sample_events": [sample.__dict__ for sample in stats.sample_events],
                    "user_agents": dict(stats.user_agents.most_common(5)),
                }
            )
        ranked.sort(key=lambda x: (x["score"], x["requests"], x["max_rps"]), reverse=True)
        return ranked[: max(self.config.top_n * 3, 30)]

    def rank_suspicious_uris(self) -> list[dict[str, Any]]:
        ranked: list[dict[str, Any]] = []
        for uri_path, stats in self.uri_stats.items():
            score_tags: dict[str, float] = {}
            distinct_ips = len(stats.ips)
            static_asset = self.is_static_asset(uri_path)
            if stats.total >= 100:
                score_tags["high-frequency"] = min(25.0, math.log10(stats.total) * 9)
            if stats.max_rps >= 10:
                score_tags["burst"] = min(14.0, stats.max_rps * 0.5)
            if any(keyword in uri_path.lower() for keyword in SCAN_KEYWORDS):
                score_tags["sensitive-uri"] = 8.0
            if distinct_ips >= 5 and stats.total >= 50:
                score_tags["multi-source"] = min(10.0, distinct_ips * 0.8)
            if stats.bytes_stats.count >= 10 and self.is_large_response_anomaly(stats.bytes_stats.max_size, stats.bytes_stats):
                score_tags["large-response-spread"] = 10.0

            enum_ips = 0
            for (ip, pair_uri), pair in self.ip_uri_stats.items():
                if pair_uri != uri_path:
                    continue
                if len(pair.numeric_ids) + pair.numeric_overflow >= 20:
                    enum_ips += 1
            if enum_ips:
                score_tags["id-enumeration"] = min(16.0, enum_ips * 2.5)

            if self.config.focus_uris and any(focus in uri_path for focus in self.config.focus_uris):
                score_tags["focus-uri"] = 20.0

            if static_asset and "large-response-spread" not in score_tags and "sensitive-uri" not in score_tags:
                continue
            if static_asset:
                score_tags["static-asset"] = -20.0

            total_score = round(sum(score_tags.values()), 2)
            if total_score <= 0:
                continue
            ranked.append(
                {
                    "uri_path": uri_path,
                    "score": total_score,
                    "reason_tags": summarize_reason_tags(score_tags),
                    "requests": stats.total,
                    "distinct_ips": distinct_ips,
                    "max_rps": stats.max_rps,
                    "mean_body_bytes": int(stats.bytes_stats.mean),
                    "p95_body_bytes": stats.bytes_stats.p95,
                    "max_body_bytes": stats.bytes_stats.max_size,
                    "status_top": {str(k): v for k, v in stats.statuses.most_common(6)},
                    "ip_top": dict(stats.ips.most_common(8)),
                    "host_top": dict(stats.hosts.most_common(5)),
                    "query_param_names": dict(stats.query_param_names.most_common(8)),
                    "sample_events": [sample.__dict__ for sample in stats.sample_events],
                }
            )
        ranked.sort(key=lambda x: (x["score"], x["requests"], x["max_body_bytes"]), reverse=True)
        return ranked[: max(self.config.top_n * 3, 30)]

    def build_summary(self, suspicious_ips: list[dict[str, Any]], suspicious_uris: list[dict[str, Any]]) -> dict[str, Any]:
        top_ip = suspicious_ips[0] if suspicious_ips else None
        top_uri = suspicious_uris[0] if suspicious_uris else None
        summary = {
            "total_records_seen": self.total_records,
            "parsed_records_kept": self.parsed_records,
            "failed_records": self.failed_records,
            "services_seen": dict(self.service_counter.most_common(20)),
            "dates_seen": dict(self.date_counter.most_common(20)),
            "hot_windows": [
                {"time_bucket": bucket, "uri_path": uri, "count": count}
                for (bucket, uri), count in self.attack_windows.most_common(self.config.top_n)
            ],
            "top_ip": top_ip,
            "top_uri": top_uri,
            "focus_ips": sorted(self.config.focus_ips),
            "focus_uris": self.config.focus_uris,
        }
        return summary

    def select_review_ip_groups(self, suspicious_ips: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        priority: list[dict[str, Any]] = []
        observe: list[dict[str, Any]] = []
        for item in suspicious_ips:
            score = float(item.get("score", 0) or 0)
            requests = int(item.get("requests", 0) or 0)
            max_rps = int(item.get("max_rps", 0) or 0)
            row = {
                "ip": item["ip"],
                "score": score,
                "requests": requests,
                "max_rps": max_rps,
                "reason_tags": item.get("reason_tags", []),
            }
            if score >= 60 or requests >= 1500 or max_rps >= 40:
                priority.append(row)
            elif score >= 30 or requests >= 150 or max_rps >= 15:
                observe.append(row)
        limit = max(self.config.top_n, 20)
        return {
            "priority": priority[:limit],
            "observe": observe[:limit],
            "all": (priority + observe)[: limit * 2],
        }

    def write_outputs(self, report: dict[str, Any]) -> None:
        report_json = self.config.output_dir / "report.json"
        report_md = self.config.output_dir / "report.md"
        ip_csv = self.config.output_dir / "suspicious_ips.csv"
        uri_csv = self.config.output_dir / "suspicious_uris.csv"
        review_csv = self.config.output_dir / "review_ips.csv"
        report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        report_md.write_text(self.render_markdown(report), encoding="utf-8")
        self.write_csv(report["suspicious_ips"], ip_csv, ["ip", "score", "requests", "max_rps", "unique_paths", "reason_tags"])
        self.write_csv(report["suspicious_uris"], uri_csv, ["uri_path", "score", "requests", "distinct_ips", "max_rps", "max_body_bytes", "reason_tags"])
        review_rows = []
        for level in ("priority", "observe"):
            for row in report.get("review_ip_groups", {}).get(level, []):
                review_rows.append({"level": level, **row})
        self.write_csv(review_rows, review_csv, ["level", "ip", "score", "requests", "max_rps", "reason_tags"])
        self.cleanup_legacy_block_outputs()

    def write_csv(self, rows: list[dict[str, Any]], path: Path, fieldnames: list[str]) -> None:
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                data = {}
                for field in fieldnames:
                    value = row.get(field)
                    if isinstance(value, (list, dict)):
                        value = json.dumps(value, ensure_ascii=False)
                    data[field] = value
                writer.writerow(data)

    def cleanup_legacy_block_outputs(self) -> None:
        for name in (
            "block_ips.txt",
            "block_ips.csv",
            "block_ips_comma.txt",
            "block_nginx_deny.conf",
            "block_windows_firewall.ps1",
            "block_linux_iptables.sh",
            "review_ip_list.txt",
        ):
            path = self.config.output_dir / name
            if path.exists():
                path.unlink()

    def render_markdown(self, report: dict[str, Any]) -> str:
        lines: list[str] = []
        lines.append("# Nginx 应急溯源报告")
        lines.append("")
        lines.append(f"- 生成时间: `{report['generated_at']}`")
        lines.append(f"- 输入路径: `{', '.join(report['inputs'])}`")
        lines.append(f"- 日志文件数: `{len(report['log_files'])}`")
        lines.append(f"- 有效日志条数: `{report['summary']['parsed_records_kept']}`")
        lines.append(f"- 解析失败条数: `{report['summary']['failed_records']}`")
        if report.get("archives_used"):
            lines.append(f"- 自动处理归档数: `{len(report['archives_used'])}`")
        lines.append("")

        lines.append("## 结论摘要")
        lines.append("")
        top_ip = report["summary"].get("top_ip")
        top_uri = report["summary"].get("top_uri")
        if top_ip:
            lines.append(
                f"- 最高风险 IP: `{top_ip['ip']}`，评分 `{top_ip['score']}`，请求 `{top_ip['requests']}`，原因 `{', '.join(top_ip['reason_tags'])}`"
            )
        if top_uri:
            lines.append(
                f"- 最高风险 URI: `{top_uri['uri_path']}`，评分 `{top_uri['score']}`，请求 `{top_uri['requests']}`，最大响应 `{top_uri['max_body_bytes']}`"
            )
        for item in report["summary"].get("hot_windows", [])[:8]:
            lines.append(f"- 热点时间窗: `{item['time_bucket']}` `{item['uri_path']}` 次数 `{item['count']}`")
        lines.append("")

        lines.append("## 高风险 IP")
        lines.append("")
        for item in report["suspicious_ips"][: self.config.top_n]:
            lines.append(
                f"- `{item['ip']}` 分数 `{item['score']}` 请求 `{item['requests']}` 峰值RPS `{item['max_rps']}` 路径数 `{item['unique_paths']}` 原因 `{', '.join(item['reason_tags'])}`"
            )
            if item["top_paths"]:
                top_paths = ", ".join(f"{entry['path']}({entry['count']})" for entry in item["top_paths"][:4])
                lines.append(f"  重点路径: {top_paths}")
        lines.append("")

        review_groups = report.get("review_ip_groups") or {}
        priority_ips = review_groups.get("priority") or []
        observe_ips = review_groups.get("observe") or []
        if priority_ips or observe_ips:
            lines.append("## 待人工研判 IP")
            lines.append("")
            lines.append(f"- 分层明细: [{self.config.output_dir / 'review_ips.csv'}]({self.config.output_dir / 'review_ips.csv'})")
            if priority_ips:
                lines.append(f"- 高优先级研判: `{', '.join(item['ip'] for item in priority_ips[:20])}`")
            if observe_ips:
                lines.append(f"- 观察 IP: `{', '.join(item['ip'] for item in observe_ips[:20])}`")
            lines.append("")

        lines.append("## 高风险 URI")
        lines.append("")
        for item in report["suspicious_uris"][: self.config.top_n]:
            lines.append(
                f"- `{item['uri_path']}` 分数 `{item['score']}` 请求 `{item['requests']}` 源IP `{item['distinct_ips']}` 峰值RPS `{item['max_rps']}` 最大响应 `{item['max_body_bytes']}`"
            )
            if item["ip_top"]:
                ip_top = ", ".join(f"{ip}({count})" for ip, count in list(item["ip_top"].items())[:5])
                lines.append(f"  主要来源: {ip_top}")
        lines.append("")

        if report["top_anomalies"]:
            lines.append("## 异常大响应样本")
            lines.append("")
            for item in report["top_anomalies"][: self.config.top_n]:
                lines.append(
                    f"- `{item['timestamp']}` `{item['real_ip']}` `{item['uri_path']}` 状态 `{item['status']}` 响应 `{item['body_bytes']}` 原因 `{item['reason']}`"
                )
            lines.append("")

        if report["route_candidates"]:
            lines.append("## 路由/源码候选")
            lines.append("")
            for uri, candidates in list(report["route_candidates"].items())[: self.config.top_n]:
                lines.append(f"### `{uri}`")
                for candidate in candidates[:8]:
                    lines.append(
                        f"- [{candidate['file_path']}]({candidate['file_path']}) 来源 `{candidate['source']}` 理由 `{candidate['reason']}` 命中 `{candidate['match_value']}`"
                    )
                lines.append("")

        if report.get("ai_judgement"):
            lines.append("## AI 研判")
            lines.append("")
            lines.append(report["ai_judgement"].strip())
            lines.append("")
        return "\n".join(lines)

    def ask_ai(self, report: dict[str, Any]) -> str:
        api_key = self.config.ai_api_key or os.environ.get("OPENAI_API_KEY")
        base_url = self.config.ai_base_url or os.environ.get("OPENAI_BASE_URL")
        model = self.config.ai_model or os.environ.get("OPENAI_MODEL") or "gpt-4o-mini"
        if not api_key or not base_url:
            return "AI 模块未执行：缺少 `OPENAI_API_KEY` 或 `OPENAI_BASE_URL`。"

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一名经验丰富的应急响应分析师。请根据 nginx 日志聚合结果输出精炼研判：攻击方式、攻击是否疑似成功、后续核查建议、需要优先保护的接口。",
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "summary": report["summary"],
                            "suspicious_ips": report["suspicious_ips"][:8],
                            "suspicious_uris": report["suspicious_uris"][:8],
                            "top_anomalies": report["top_anomalies"][:8],
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
            "temperature": 0.2,
        }
        url = base_url.rstrip("/") + "/chat/completions"
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]
        except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError) as exc:
            return f"AI 模块执行失败：{exc}"

    def map_routes_for_uris(self, uris: list[str]) -> dict[str, list[RouteCandidate]]:
        results: dict[str, list[RouteCandidate]] = defaultdict(list)
        if not uris:
            return results

        for uri_path in uris:
            prefixes = path_prefixes(uri_path)
            for location in self.nginx_locations:
                if uri_path.startswith(location.location.rstrip("$")):
                    results[uri_path].append(
                        RouteCandidate(
                            uri_path=uri_path,
                            source="nginx-conf",
                            reason="location 命中",
                            match_value=location.location,
                            file_path=location.file_path,
                        )
                    )
                elif any(
                    uri_path.startswith(prefix.rstrip("$"))
                    for prefix in prefixes
                    if location.location.startswith(prefix)
                ):
                    results[uri_path].append(
                        RouteCandidate(
                            uri_path=uri_path,
                            source="nginx-conf",
                            reason="location 前缀接近",
                            match_value=location.location,
                            file_path=location.file_path,
                        )
                    )

        files_to_scan = self.collect_search_files()
        for uri_path in uris:
            tokens = derive_search_tokens(uri_path)
            if not tokens:
                continue
            for file_path in files_to_scan:
                text = safe_read_text(file_path)
                if not text:
                    continue
                hit_value = ""
                reason = ""
                for token in tokens:
                    if token in text:
                        hit_value = token
                        reason = "文件内容命中 token"
                        break
                if not hit_value:
                    for token in tokens:
                        if token.lower() in file_path.name.lower():
                            hit_value = token
                            reason = "文件名命中 token"
                            break
                if hit_value:
                    results[uri_path].append(
                        RouteCandidate(
                            uri_path=uri_path,
                            source="app-search",
                            reason=reason,
                            match_value=hit_value,
                            file_path=str(file_path),
                        )
                    )
            dedup: list[RouteCandidate] = []
            seen = set()
            for item in results[uri_path]:
                key = (item.source, item.file_path, item.match_value)
                if key in seen:
                    continue
                seen.add(key)
                dedup.append(item)
            results[uri_path] = dedup[:20]
        return results

    def collect_search_files(self) -> list[Path]:
        files: list[Path] = []
        roots = list(dict.fromkeys(self.config.search_roots + self.extracted_roots))
        for root in roots:
            if root.is_file():
                if root.suffix.lower() in TEXT_SEARCH_EXTS:
                    files.append(root)
                continue
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix.lower() in TEXT_SEARCH_EXTS:
                    files.append(path)
                if len(files) >= self.config.max_search_files:
                    return files
        return files

    def parse_nginx_conf(self, path: Path) -> list[NginxLocation]:
        text = safe_read_text(path, size_limit=4 * 1024 * 1024)
        if not text:
            return []
        lines = text.splitlines()
        server_names: list[str] = []
        access_log_path: Optional[str] = None
        locations: list[NginxLocation] = []
        current_location: Optional[str] = None
        current_directives: dict[str, str] = {}
        brace_depth = 0
        location_base_depth: Optional[int] = None

        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                brace_depth += raw_line.count("{") - raw_line.count("}")
                continue

            server_match = SERVER_NAME_RE.match(raw_line)
            if server_match:
                server_names = [item.strip() for item in server_match.group("names").split() if item.strip()]

            access_match = ACCESS_LOG_CONF_RE.match(raw_line)
            if access_match and current_location is None:
                access_log_path = access_match.group("path").strip()

            location_match = LOCATION_RE.match(raw_line)
            if location_match:
                current_location = location_match.group("path").strip()
                current_directives = {}
                location_base_depth = brace_depth + raw_line.count("{") - raw_line.count("}")

            if current_location is not None:
                for key, pattern in SIMPLE_DIRECTIVE_RE.items():
                    directive_match = pattern.match(raw_line)
                    if directive_match:
                        current_directives[key] = directive_match.group("value").strip()

            brace_depth += raw_line.count("{") - raw_line.count("}")

            if current_location is not None and location_base_depth is not None and brace_depth < location_base_depth:
                locations.append(
                    NginxLocation(
                        file_path=str(path),
                        server_names=server_names[:],
                        location=current_location,
                        directives=current_directives.copy(),
                        access_log=access_log_path,
                    )
                )
                current_location = None
                current_directives = {}
                location_base_depth = None
        return locations

    def location_to_dict(self, location: NginxLocation) -> dict[str, Any]:
        return {
            "file_path": location.file_path,
            "server_names": location.server_names,
            "location": location.location,
            "directives": location.directives,
            "access_log": location.access_log,
        }

    def consume_record(self, item: dict[str, Any]) -> None:
        ip = item["real_ip"]
        uri_path = item["uri_path"]
        target = item["target"]
        timestamp: dt.datetime = item["timestamp"]
        second_key = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        hour_key = timestamp.strftime("%Y-%m-%d %H:00")
        date_key = timestamp.strftime("%Y-%m-%d")
        sample = SampleEvent(
            timestamp=timestamp.isoformat(),
            method=item["method"],
            target=item["target"],
            status=item["status"],
            body_bytes=item["body_bytes"],
            host=item["host"],
            source_file=item["source_file"],
            referer=item["referer"],
            user_agent=item["user_agent"][:240],
            remote_addr=item["remote_addr"],
            real_ip=item["real_ip"],
        )

        self.date_counter[date_key] += 1
        self.attack_windows[(hour_key, uri_path)] += 1

        ip_stat = self.ip_stats[ip]
        ip_stat.total += 1
        ip_stat.bytes_total += item["body_bytes"]
        ip_stat.unique_paths.add(uri_path)
        ip_stat.unique_targets.add(target)
        ip_stat.methods[item["method"]] += 1
        ip_stat.statuses[item["status"]] += 1
        ip_stat.hosts[item["host"]] += 1
        ip_stat.paths[uri_path] += 1
        ip_stat.hours[hour_key] += 1
        ip_stat.second_counts[second_key] = ip_stat.second_counts.get(second_key, 0) + 1
        ip_stat.max_rps = max(ip_stat.max_rps, ip_stat.second_counts[second_key])
        ip_stat.user_agents[item["user_agent"][:120]] += 1
        if item["referer"] and item["referer"] != "-":
            ip_stat.referers[item["referer"][:120]] += 1
        if self.path_is_interesting(uri_path):
            ip_stat.scan_hits += 1
        if self.is_auth_path(uri_path):
            ip_stat.auth_hits += 1
        ip_stat.add_sample(sample)

        uri_stat = self.uri_stats[uri_path]
        uri_stat.total += 1
        uri_stat.bytes_stats.add(item["body_bytes"])
        uri_stat.statuses[item["status"]] += 1
        uri_stat.ips[ip] += 1
        uri_stat.methods[item["method"]] += 1
        uri_stat.hosts[item["host"]] += 1
        uri_stat.distinct_targets.add(target)
        uri_stat.second_counts[second_key] = uri_stat.second_counts.get(second_key, 0) + 1
        uri_stat.max_rps = max(uri_stat.max_rps, uri_stat.second_counts[second_key])
        for key in item["query_params"].keys():
            uri_stat.query_param_names[key] += 1
        uri_stat.add_sample(sample)

        pair = self.ip_uri_stats[(ip, uri_path)]
        pair.total += 1
        pair.bytes_stats.add(item["body_bytes"])
        pair.statuses[item["status"]] += 1
        pair.distinct_targets.add(target)
        pair.second_counts[second_key] = pair.second_counts.get(second_key, 0) + 1
        pair.max_rps = max(pair.max_rps, pair.second_counts[second_key])
        pair.add_sample(sample)
        for key, values in item["query_params"].items():
            pair.param_names[key] += 1
            if SENSITIVE_PARAM_RE.search(key):
                for value in values:
                    number = maybe_to_int(value)
                    if number is not None:
                        pair.add_numeric_id(number)
        for number in item["path_numeric_ids"]:
            pair.add_numeric_id(number)

        self.path_size_stats[uri_path].add(item["body_bytes"])

    def keep_record(self, item: dict[str, Any]) -> bool:
        if self.config.focus_ips and item["real_ip"] not in self.config.focus_ips:
            return False
        if self.config.focus_uris and not any(focus in item["uri_path"] or focus in item["target"] for focus in self.config.focus_uris):
            return False
        date_value = item["timestamp"].date()
        if self.config.from_date and date_value < self.config.from_date:
            return False
        if self.config.to_date and date_value > self.config.to_date:
            return False
        return True

    def parse_access_line(self, line: str, file_path: Path) -> Optional[dict[str, Any]]:
        match = ACCESS_LOG_RE.match(line.strip())
        if not match:
            return None

        target = match.group("target").strip()
        parsed_target = urllib.parse.urlsplit(target)
        uri_path = parsed_target.path or "/"
        query_params = urllib.parse.parse_qs(parsed_target.query, keep_blank_values=True)
        timestamp_raw = match.group("time")
        try:
            timestamp = dt.datetime.strptime(timestamp_raw, "%d/%b/%Y:%H:%M:%S %z")
        except ValueError:
            return None

        status = int(match.group("status"))
        body_bytes = 0 if match.group("body_bytes") == "-" else int(match.group("body_bytes"))
        tail = match.group("tail") or ""
        real_ip = match.group("remote_addr")
        quoted_tail_ip = TRAILING_IP_RE.search(tail)
        if quoted_tail_ip and quoted_tail_ip.group(1) != "-":
            real_ip = quoted_tail_ip.group(1)
        else:
            bare = BARE_IP_RE.findall(tail)
            if bare:
                real_ip = bare[-1]

        path_numeric_ids = [int(token) for token in re.findall(r"(?<!\d)(\d{1,12})(?!\d)", uri_path)]
        host = file_name_service(file_path)
        return {
            "remote_addr": match.group("remote_addr"),
            "real_ip": real_ip,
            "timestamp": timestamp,
            "method": match.group("method"),
            "target": target,
            "uri_path": uri_path,
            "query": parsed_target.query,
            "query_params": query_params,
            "path_numeric_ids": path_numeric_ids,
            "status": status,
            "body_bytes": body_bytes,
            "referer": match.group("referer"),
            "user_agent": match.group("user_agent"),
            "host": host,
            "source_file": str(file_path),
        }

    def stream_lines(self, file_path: Path) -> Iterator[str]:
        for encoding in TEXT_ENCODING_CANDIDATES:
            try:
                with file_path.open("r", encoding=encoding, errors="strict") as f:
                    for line in f:
                        yield line
                return
            except UnicodeDecodeError:
                continue
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                yield line

    def extract_archives(self, archives: list[Path]) -> list[Path]:
        if not archives:
            return []
        extraction_root = ensure_dir(self.config.output_dir / "_extracted_archives")
        extracted_roots: list[Path] = []
        for archive in archives:
            target_dir = extraction_root / archive.stem.replace(".", "_")
            log_info(f"处理归档: {archive}")
            if target_dir.exists():
                extracted_roots.append(target_dir)
                self.archives_used.append({"archive": str(archive), "extract_to": str(target_dir), "reused": "true"})
                log_info(f"复用已解压目录: {target_dir}")
                continue
            ensure_dir(target_dir)
            try:
                if archive.suffix.lower() == ".zip":
                    with zipfile.ZipFile(archive) as zf:
                        zf.extractall(target_dir)
                elif archive.suffix.lower() in {".tar", ".tgz"} or archive.name.endswith(".tar.gz"):
                    with tarfile.open(archive) as tf:
                        tf.extractall(target_dir)
                elif archive.suffix.lower() in {".7z", ".rar"}:
                    self.extract_via_7z(archive, target_dir)
                else:
                    continue
                extracted_roots.append(target_dir)
                self.archives_used.append({"archive": str(archive), "extract_to": str(target_dir), "reused": "false"})
                log_info(f"归档解压完成: {target_dir}")
            except Exception as exc:
                self.archives_used.append({"archive": str(archive), "extract_to": str(target_dir), "error": str(exc)})
                log_error(f"归档解压失败: {archive} error={exc}")
        self.extracted_roots = extracted_roots
        return extracted_roots

    def extract_via_7z(self, archive: Path, target_dir: Path) -> None:
        seven_zip = shutil.which("7z") or shutil.which("7za")
        if not seven_zip:
            raise RuntimeError(f"找不到 7z，无法解压 {archive}")
        result = subprocess.run(
            [seven_zip, "x", str(archive), f"-o{target_dir}", "-y"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr or result.stdout or "7z 解压失败")

    def is_large_response_anomaly(self, size: int, stats: RunningSizeStats) -> bool:
        if stats.count < 5:
            return size >= 50000
        if size < max(4096, stats.p95):
            return False
        if stats.max_size <= 0:
            return False
        if size >= max(50000, int(stats.mean * 2), int(stats.mean + 3 * max(stats.stdev, 1.0))):
            return True
        return False

    def filter_by_date(self, files: Iterable[Path]) -> list[Path]:
        if not self.config.from_date and not self.config.to_date:
            return list(files)
        result: list[Path] = []
        for file_path in files:
            date_hint = self.extract_date_from_path(file_path)
            if not date_hint:
                result.append(file_path)
                continue
            if self.config.from_date and date_hint < self.config.from_date:
                continue
            if self.config.to_date and date_hint > self.config.to_date:
                continue
            result.append(file_path)
        return result

    def extract_date_from_path(self, file_path: Path) -> Optional[dt.date]:
        for match in re.findall(r"(20\d{2})-(\d{2})-(\d{2})", str(file_path)):
            try:
                return dt.date(int(match[0]), int(match[1]), int(match[2]))
            except ValueError:
                continue
        return None

    def path_is_interesting(self, uri_path: str) -> bool:
        lowered = uri_path.lower()
        if any(keyword in lowered for keyword in SCAN_KEYWORDS):
            return True
        if any(lowered.endswith(ext) for ext in (".zip", ".tar", ".rar", ".7z", ".bak", ".sql", ".gz", ".old")):
            return True
        return False

    def is_static_asset(self, uri_path: str) -> bool:
        lowered = uri_path.lower()
        return any(
            lowered.endswith(ext)
            for ext in (
                ".css",
                ".js",
                ".png",
                ".jpg",
                ".jpeg",
                ".gif",
                ".svg",
                ".ico",
                ".woff",
                ".woff2",
                ".ttf",
                ".eot",
                ".map",
                ".webp",
                ".bmp",
            )
        )

    def is_auth_path(self, uri_path: str) -> bool:
        lowered = uri_path.lower()
        return any(token in lowered for token in ("/login", "/auth", "/signin", "/token", "/oauth"))

    def is_access_log(self, path: Path) -> bool:
        name = path.name.lower()
        if not name.endswith(".log"):
            return False
        if name.endswith(".error.log") or name == "error.log":
            return False
        return any(fnmatch.fnmatch(name, pattern.lower()) for pattern in ACCESS_LOG_PATTERNS)

    def looks_like_nginx_conf(self, path: Path) -> bool:
        if path.suffix.lower() not in {".conf", ".config", ""} and path.name.lower() != "nginx.conf":
            return False
        text = safe_read_text(path)
        if not text:
            return False
        return "server {" in text or "location " in text or "proxy_pass" in text

    def is_archive(self, path: Path) -> bool:
        lowered = path.name.lower()
        return any(lowered.endswith(suffix) for suffix in ARCHIVE_SUFFIXES)


class ResidentAgent:
    def __init__(self, config: AnalyzerConfig) -> None:
        self.config = config
        ensure_dir(self.config.output_dir)
        ensure_dir(self.config.state_file.parent)
        self.batch_root = ensure_dir(self.config.output_dir / "_agent_batch")

    def load_state(self) -> dict[str, Any]:
        if self.config.state_file.exists():
            try:
                log_info(f"加载状态文件: {self.config.state_file}")
                return json.loads(self.config.state_file.read_text(encoding="utf-8"))
            except Exception:
                log_error(f"状态文件损坏，重新初始化: {self.config.state_file}")
                pass
        return {
            "version": 1,
            "mode": "resident",
            "roots": [str(p) for p in self.config.inputs],
            "search_roots": [str(p) for p in self.config.search_roots],
            "known_logs": {},
            "last_cycle": None,
            "interval_sec": self.config.interval_sec,
            "last_alert_key": None,
        }

    def save_state(self, state: dict[str, Any]) -> None:
        state["last_cycle"] = dt.datetime.now().astimezone().isoformat()
        state["interval_sec"] = self.config.interval_sec
        state["roots"] = [str(p) for p in self.config.inputs]
        state["search_roots"] = [str(p) for p in self.config.search_roots]
        self.config.state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        log_info(f"状态已保存: {self.config.state_file}")

    def discover_logs(self, full_discovery: bool, state: dict[str, Any]) -> list[Path]:
        if not full_discovery:
            log_info("本轮使用已登记日志列表。")
            remembered = []
            for raw_path in state.get("known_logs", {}):
                path = Path(raw_path)
                if path.exists() and path.is_file():
                    remembered.append(path)
            if remembered:
                log_info(f"已登记日志 {len(remembered)} 个。")
                return sorted(remembered)
        log_info("执行完整日志发现。")
        hunter = NginxTraceHunter(self.config)
        return hunter.discover_log_files()

    def build_incremental_batch(self, log_files: list[Path], state: dict[str, Any]) -> list[Path]:
        batch_dir = ensure_dir(self.batch_root / dt.datetime.now().strftime("%Y%m%d_%H%M%S"))
        batch_files: list[Path] = []
        known_logs = state.setdefault("known_logs", {})
        current_seen: set[str] = set()

        for log_path in log_files:
            log_info(f"检查增量日志: {log_path}")
            key = str(log_path.resolve())
            current_seen.add(key)
            meta = known_logs.get(key, {})
            size = log_path.stat().st_size
            offset = int(meta.get("offset", 0) or 0)
            is_new = not meta
            if size < offset:
                offset = 0
            if is_new and size > self.config.bootstrap_bytes:
                offset = max(0, size - self.config.bootstrap_bytes)
                log_info(f"新日志首次接管，仅从尾部开始。file={log_path} offset={offset} size={size}")

            if size <= offset:
                known_logs[key] = {
                    "offset": size,
                    "size": size,
                    "service": file_name_service(log_path),
                    "last_seen": dt.datetime.now().astimezone().isoformat(),
                    "bootstrap_from_tail": bool(is_new and size > self.config.bootstrap_bytes),
                }
                continue

            file_dir = ensure_dir(batch_dir / f"{len(batch_files):04d}")
            out_path = file_dir / log_path.name
            with log_path.open("rb") as src, out_path.open("wb") as dst:
                src.seek(offset)
                while True:
                    chunk = src.read(1024 * 1024)
                    if not chunk:
                        break
                    dst.write(chunk)
            if out_path.stat().st_size > 0:
                batch_files.append(out_path)
                log_info(f"生成增量批文件: {out_path} bytes={out_path.stat().st_size}")

            known_logs[key] = {
                "offset": size,
                "size": size,
                "service": file_name_service(log_path),
                "last_seen": dt.datetime.now().astimezone().isoformat(),
                "bootstrap_from_tail": bool(is_new and size > self.config.bootstrap_bytes),
            }

        for key, meta in known_logs.items():
            if key not in current_seen:
                meta["missing"] = True
        return batch_files

    def run_cycle(self, cycle_index: int = 1) -> Optional[dict[str, Any]]:
        log_info(f"驻场第 {cycle_index} 轮开始。")
        state = self.load_state()
        full_discovery = cycle_index == 1 or cycle_index % max(1, self.config.discover_every) == 0
        log_files = self.discover_logs(full_discovery=full_discovery, state=state)
        batch_files = self.build_incremental_batch(log_files, state)
        self.save_state(state)
        if not batch_files:
            log_info(f"驻场第 {cycle_index} 轮无新增日志。")
            return None

        batch_config = AnalyzerConfig(
            inputs=batch_files,
            search_roots=self.config.search_roots,
            output_dir=self.config.output_dir,
            cfg_file=self.config.cfg_file,
            top_n=self.config.top_n,
            focus_ips=self.config.focus_ips,
            focus_uris=self.config.focus_uris,
            from_date=self.config.from_date,
            to_date=self.config.to_date,
            archive_mode="never",
            ai_enabled=self.config.ai_enabled,
            ai_base_url=self.config.ai_base_url,
            ai_model=self.config.ai_model,
            ai_api_key=self.config.ai_api_key,
            max_search_files=self.config.max_search_files,
            mode="once",
            interval_sec=self.config.interval_sec,
            state_file=self.config.state_file,
            bootstrap_bytes=self.config.bootstrap_bytes,
            discover_every=self.config.discover_every,
            gui_mode=False,
            alert_enabled=False,
            alert_min_score=self.config.alert_min_score,
            ding_url=self.config.ding_url,
            ding_kw=self.config.ding_kw,
            wx_url=self.config.wx_url,
            fs_url=self.config.fs_url,
        )
        hunter = NginxTraceHunter(batch_config)
        report = hunter.run()
        report["resident_agent"] = {
            "cycle_index": cycle_index,
            "batch_files": [str(p) for p in batch_files],
            "state_file": str(self.config.state_file),
            "full_discovery": full_discovery,
            "known_logs": len(state.get("known_logs", {})),
        }
        (self.config.output_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        self.send_alert_if_needed(report, state)
        self.save_state(state)
        log_info(f"驻场第 {cycle_index} 轮结束。")
        return report

    def send_alert_if_needed(self, report: dict[str, Any], state: dict[str, Any]) -> None:
        if not self.config.alert_enabled:
            log_info("告警未启用，跳过推送。")
            return
        top_ip = (report.get("summary", {}) or {}).get("top_ip") or {}
        top_uri = (report.get("summary", {}) or {}).get("top_uri") or {}
        score = max(float(top_ip.get("score", 0) or 0), float(top_uri.get("score", 0) or 0))
        if score < self.config.alert_min_score:
            log_info(f"未达到告警阈值。score={score} threshold={self.config.alert_min_score}")
            return
        alert_key = f"{top_ip.get('ip','-')}|{top_uri.get('uri_path','-')}|{score}"
        if state.get("last_alert_key") == alert_key:
            log_info("告警去重命中，跳过重复推送。")
            return
        text = self.build_alert_text(report, score)
        results = []
        for name, url in (("ding", self.config.ding_url), ("wx", self.config.wx_url), ("fs", self.config.fs_url)):
            if not url:
                continue
            ok, detail = self.send_webhook(name, url, text)
            results.append({"channel": name, "ok": ok, "detail": detail})
            log_info(f"告警推送 channel={name} ok={ok} detail={detail}")
        state["last_alert_key"] = alert_key
        state["last_alert_results"] = results

    def build_alert_text(self, report: dict[str, Any], score: float) -> str:
        top_ip = (report.get("summary", {}) or {}).get("top_ip") or {}
        top_uri = (report.get("summary", {}) or {}).get("top_uri") or {}
        hot = ((report.get("summary", {}) or {}).get("hot_windows") or [])[:3]
        review_groups = report.get("review_ip_groups") or {}
        priority_ips = [item.get("ip", "") for item in review_groups.get("priority", [])[:10] if item.get("ip")]
        observe_ips = [item.get("ip", "") for item in review_groups.get("observe", [])[:10] if item.get("ip")]
        lines = [
            "Nginx Hunter 告警",
            f"评分: {score}",
            f"高风险IP: {top_ip.get('ip', '-')}",
            f"高风险URI: {top_uri.get('uri_path', '-')}",
            f"请求量: {top_uri.get('requests', 0)}",
            f"峰值RPS: {top_uri.get('max_rps', 0)}",
            f"输出目录: {self.config.output_dir}",
        ]
        if priority_ips:
            lines.append(f"高优先级研判IP: {','.join(priority_ips)}")
        if observe_ips:
            lines.append(f"观察IP: {','.join(observe_ips)}")
        for item in hot:
            lines.append(f"热点: {item.get('time_bucket')} {item.get('uri_path')} {item.get('count')}")
        return "\n".join(lines)

    def send_webhook(self, channel: str, url: str, text: str) -> tuple[bool, str]:
        if channel == "ding":
            final_text = text
            if self.config.ding_kw:
                final_text = f"{self.config.ding_kw}\n{final_text}"
            return post_json(url, {"msgtype": "text", "text": {"content": final_text}})
        if channel == "wx":
            return post_json(url, {"msgtype": "text", "text": {"content": text}})
        if channel == "fs":
            return post_json(url, {"msg_type": "text", "content": {"text": text}})
        return False, "unsupported channel"

    def loop(self) -> int:
        cycle = 1
        while True:
            report = self.run_cycle(cycle_index=cycle)
            now = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
            if report is None:
                print(f"[{now}] 无新增日志，{self.config.interval_sec} 秒后继续。")
            else:
                top_ip = (report.get("summary", {}) or {}).get("top_ip") or {}
                top_uri = (report.get("summary", {}) or {}).get("top_uri") or {}
                print(
                    f"[{now}] 已完成第 {cycle} 轮增量扫描。"
                    f" top_ip={top_ip.get('ip', '-')}"
                    f" top_ip_score={top_ip.get('score', 0)}"
                    f" top_uri={top_uri.get('uri_path', '-')}"
                )
            cycle += 1
            time.sleep(self.config.interval_sec)


def parse_args(argv: list[str]) -> AnalyzerConfig:
    parser = argparse.ArgumentParser(
        description="Nginx 应急溯源脚本。默认驻场增量巡检，自动登记日志、记住扫描位置，只分析新增内容。"
    )
    parser.add_argument("inputs", nargs="*", help="软件根目录、日志目录、单个日志文件或归档文件路径。默认当前目录。")
    parser.add_argument("--once", action="store_true", help="只执行一轮，不驻场。")
    parser.add_argument("--interval", type=int, default=600, help="驻场轮询间隔秒数，默认 600。")
    parser.add_argument("--ai", action="store_true", help="开启 AI 二次研判。默认关闭，且只在有明显风险时触发。")
    parser.add_argument("--gui", action="store_true", help="打开图形界面。")
    parser.add_argument("--cfg", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--search-root", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--output-dir", default=None, help="输出目录。默认在当前目录下自动创建 `hunter_output`。")
    parser.add_argument("--top", type=int, default=20, help=argparse.SUPPRESS)
    parser.add_argument("--focus-ip", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--focus-uri", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--from-date", help=argparse.SUPPRESS)
    parser.add_argument("--to-date", help=argparse.SUPPRESS)
    parser.add_argument(
        "--archive-mode",
        choices=("auto", "never"),
        default="auto",
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--ai-base-url", help=argparse.SUPPRESS)
    parser.add_argument("--ai-model", help=argparse.SUPPRESS)
    parser.add_argument("--ai-api-key", help=argparse.SUPPRESS)
    parser.add_argument("--max-search-files", type=int, default=5000, help=argparse.SUPPRESS)
    parser.add_argument("--state-file", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--bootstrap-bytes", type=int, default=64 * 1024 * 1024, help=argparse.SUPPRESS)
    parser.add_argument("--discover-every", type=int, default=12, help=argparse.SUPPRESS)
    parser.add_argument("--alert", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--alert-min", type=float, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--ding", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--dkw", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--wx", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--fs", default=None, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    def parse_date(value: Optional[str]) -> Optional[dt.date]:
        if not value:
            return None
        return dt.datetime.strptime(value, "%Y-%m-%d").date()

    cfg_file = Path(args.cfg).expanduser().resolve() if args.cfg else default_cfg_path().resolve()
    stored = load_json_file(cfg_file)

    raw_inputs = args.inputs or stored.get("inputs") or ["."]
    inputs = [Path(item).expanduser().resolve() for item in raw_inputs]
    stored_search_roots = stored.get("search_roots") or []
    search_roots = [Path(item).expanduser().resolve() for item in (args.search_root or stored_search_roots)]
    for item in inputs:
        if item.is_dir():
            search_roots.append(item)
    search_roots = list(dict.fromkeys(search_roots))
    stored_output = stored.get("output_dir")
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else Path(stored_output).expanduser().resolve() if stored_output else default_output_dir().resolve()
    stored_state = stored.get("state_file")
    state_file = Path(args.state_file).expanduser().resolve() if args.state_file else Path(stored_state).expanduser().resolve() if stored_state else output_dir / "hunter_agent.json"
    ai_enabled = bool(args.ai or stored.get("ai_enabled"))
    ai_base_url = args.ai_base_url if args.ai_base_url is not None else stored.get("ai_base_url")
    ai_model = args.ai_model if args.ai_model is not None else stored.get("ai_model")
    ai_api_key = args.ai_api_key if args.ai_api_key is not None else stored.get("ai_api_key")
    alert_enabled = bool(args.alert or stored.get("alert_enabled"))
    alert_min_score = float(args.alert_min if args.alert_min is not None else stored.get("alert_min_score", 50.0))
    interval_sec = max(10, int(args.interval if args.interval is not None else stored.get("interval_sec", 600)))
    bootstrap_bytes = max(1024 * 1024, int(args.bootstrap_bytes if args.bootstrap_bytes is not None else stored.get("bootstrap_bytes", 64 * 1024 * 1024)))
    discover_every = max(1, int(args.discover_every if args.discover_every is not None else stored.get("discover_every", 12)))
    mode = "once" if args.once else stored.get("mode", "resident")
    return AnalyzerConfig(
        inputs=inputs,
        search_roots=search_roots,
        output_dir=output_dir,
        cfg_file=cfg_file,
        top_n=args.top,
        focus_ips=set(args.focus_ip),
        focus_uris=args.focus_uri,
        from_date=parse_date(args.from_date),
        to_date=parse_date(args.to_date),
        archive_mode=args.archive_mode,
        ai_enabled=ai_enabled,
        ai_base_url=ai_base_url,
        ai_model=ai_model,
        ai_api_key=ai_api_key,
        max_search_files=args.max_search_files,
        mode=mode,
        interval_sec=interval_sec,
        state_file=state_file,
        bootstrap_bytes=bootstrap_bytes,
        discover_every=discover_every,
        gui_mode=args.gui,
        alert_enabled=alert_enabled,
        alert_min_score=alert_min_score,
        ding_url=args.ding if args.ding is not None else stored.get("ding_url"),
        ding_kw=args.dkw if args.dkw is not None else stored.get("ding_kw"),
        wx_url=args.wx if args.wx is not None else stored.get("wx_url"),
        fs_url=args.fs if args.fs is not None else stored.get("fs_url"),
    )


def launch_gui(cfg_path: Optional[Path] = None) -> int:
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except Exception as exc:
        eprint(f"GUI 不可用: {exc}")
        return 1

    cfg_path = cfg_path or default_cfg_path()
    stored = load_json_file(cfg_path)
    setup_logging(default_output_dir())
    log_info(f"启动 GUI。cfg={cfg_path}")
    root = tk.Tk()
    root.title("Nginx Trace Hunter")
    root.geometry("860x760")

    vars_map: dict[str, Any] = {
        "inputs": tk.StringVar(value=";".join(stored.get("inputs") or [str(Path.cwd())])),
        "out": tk.StringVar(value=stored.get("output_dir") or str(default_output_dir())),
        "interval": tk.StringVar(value=str(stored.get("interval_sec", 600))),
        "bootstrap_mb": tk.StringVar(value=str(int(stored.get("bootstrap_bytes", 64 * 1024 * 1024) / (1024 * 1024)))),
        "discover_every": tk.StringVar(value=str(stored.get("discover_every", 12))),
        "state": tk.StringVar(value=stored.get("state_file") or str((default_output_dir() / "hunter_agent.json").resolve())),
        "ai": tk.BooleanVar(value=bool(stored.get("ai_enabled"))),
        "ai_base": tk.StringVar(value=stored.get("ai_base_url") or ""),
        "ai_model": tk.StringVar(value=stored.get("ai_model") or ""),
        "ai_key": tk.StringVar(value=stored.get("ai_api_key") or ""),
        "alert": tk.BooleanVar(value=bool(stored.get("alert_enabled"))),
        "alert_min": tk.StringVar(value=str(stored.get("alert_min_score", 50.0))),
        "ding": tk.StringVar(value=stored.get("ding_url") or ""),
        "ding_kw": tk.StringVar(value=stored.get("ding_kw") or ""),
        "wx": tk.StringVar(value=stored.get("wx_url") or ""),
        "fs": tk.StringVar(value=stored.get("fs_url") or ""),
    }

    def add_row(parent: tk.Widget, row: int, label: str, var: Any, width: int = 90, secret: bool = False) -> None:
        tk.Label(parent, text=label, anchor="w").grid(row=row, column=0, sticky="w", padx=8, pady=6)
        tk.Entry(parent, textvariable=var, width=width, show="*" if secret else "").grid(row=row, column=1, sticky="we", padx=8, pady=6)

    frm = tk.Frame(root)
    frm.pack(fill="both", expand=True, padx=10, pady=10)
    frm.grid_columnconfigure(1, weight=1)

    add_row(frm, 0, "扫描根目录", vars_map["inputs"])
    add_row(frm, 1, "输出目录", vars_map["out"])
    add_row(frm, 2, "状态文件", vars_map["state"])
    add_row(frm, 3, "轮询秒数", vars_map["interval"], width=20)
    add_row(frm, 4, "首次接管尾部MB", vars_map["bootstrap_mb"], width=20)
    add_row(frm, 5, "重新发现日志轮数", vars_map["discover_every"], width=20)

    tk.Checkbutton(frm, text="启用 AI 研判", variable=vars_map["ai"]).grid(row=6, column=0, sticky="w", padx=8, pady=6)
    add_row(frm, 7, "AI Base URL", vars_map["ai_base"])
    add_row(frm, 8, "AI Model", vars_map["ai_model"])
    add_row(frm, 9, "AI Key", vars_map["ai_key"], secret=True)

    tk.Checkbutton(frm, text="启用告警", variable=vars_map["alert"]).grid(row=10, column=0, sticky="w", padx=8, pady=6)
    add_row(frm, 11, "告警阈值", vars_map["alert_min"], width=20)
    add_row(frm, 12, "钉钉 Webhook", vars_map["ding"])
    add_row(frm, 13, "钉钉关键词", vars_map["ding_kw"])
    add_row(frm, 14, "企微 Webhook", vars_map["wx"])
    add_row(frm, 15, "飞书 Webhook", vars_map["fs"])

    status_var = tk.StringVar(value=f"配置文件: {cfg_path}")
    tk.Label(root, textvariable=status_var, anchor="w").pack(fill="x", padx=10, pady=4)

    def current_output_dir() -> Path:
        return Path(vars_map["out"].get().strip() or str(default_output_dir())).expanduser().resolve()

    def current_log_path() -> Path:
        return current_output_dir() / "hunter.log"

    def build_cli_config() -> AnalyzerConfig:
        inputs = [Path(x.strip()).expanduser().resolve() for x in vars_map["inputs"].get().split(";") if x.strip()]
        if not inputs:
            inputs = [Path.cwd().resolve()]
        out_dir = Path(vars_map["out"].get().strip() or str(default_output_dir())).expanduser().resolve()
        state_file = Path(vars_map["state"].get().strip() or str(out_dir / "hunter_agent.json")).expanduser().resolve()
        search_roots = []
        for item in inputs:
            if item.is_dir():
                search_roots.append(item)
        return AnalyzerConfig(
            inputs=inputs,
            search_roots=search_roots,
            output_dir=out_dir,
            cfg_file=cfg_path.resolve(),
            top_n=20,
            focus_ips=set(),
            focus_uris=[],
            from_date=None,
            to_date=None,
            archive_mode="auto",
            ai_enabled=bool(vars_map["ai"].get()),
            ai_base_url=vars_map["ai_base"].get().strip() or None,
            ai_model=vars_map["ai_model"].get().strip() or None,
            ai_api_key=vars_map["ai_key"].get().strip() or None,
            max_search_files=5000,
            mode="resident",
            interval_sec=max(10, int(vars_map["interval"].get().strip() or "600")),
            state_file=state_file,
            bootstrap_bytes=max(1024 * 1024, int(vars_map["bootstrap_mb"].get().strip() or "64") * 1024 * 1024),
            discover_every=max(1, int(vars_map["discover_every"].get().strip() or "12")),
            gui_mode=True,
            alert_enabled=bool(vars_map["alert"].get()),
            alert_min_score=float(vars_map["alert_min"].get().strip() or "50"),
            ding_url=vars_map["ding"].get().strip() or None,
            ding_kw=vars_map["ding_kw"].get().strip() or None,
            wx_url=vars_map["wx"].get().strip() or None,
            fs_url=vars_map["fs"].get().strip() or None,
        )

    def save_cfg() -> AnalyzerConfig:
        config = build_cli_config()
        save_json_file(config.cfg_file, config_to_persist_dict(config))
        log_info(f"GUI 保存配置: {config.cfg_file}")
        status_var.set(f"已保存: {config.cfg_file}")
        return config

    def choose_root() -> None:
        path = filedialog.askdirectory()
        if path:
            current = [x for x in vars_map["inputs"].get().split(";") if x.strip()]
            current.append(path)
            vars_map["inputs"].set(";".join(current))

    def choose_out() -> None:
        path = filedialog.askdirectory()
        if path:
            vars_map["out"].set(path)

    def choose_state() -> None:
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("All", "*.*")])
        if path:
            vars_map["state"].set(path)

    def launch_subprocess(once: bool) -> None:
        config = save_cfg()
        cmd = [sys.executable, str(Path(__file__).resolve()), "--cfg", str(config.cfg_file)]
        if once:
            cmd.append("--once")
        subprocess.Popen(cmd, cwd=str(Path.cwd()))
        log_info(f"GUI 启动子进程: {' '.join(cmd)}")
        mode_name = "单轮模式" if once else "驻场模式"
        messagebox.showinfo("已启动", f"{mode_name} 已启动。\n配置文件: {config.cfg_file}")

    def open_log_file() -> None:
        path = current_log_path()
        if not path.exists():
            messagebox.showwarning("未找到日志", f"日志文件不存在：\n{path}\n请先运行一次。")
            return
        try:
            open_path(path)
            log_info(f"GUI 打开日志文件: {path}")
        except Exception as exc:
            messagebox.showerror("打开失败", str(exc))

    def open_output_dir() -> None:
        path = current_output_dir()
        ensure_dir(path)
        try:
            open_path(path)
            log_info(f"GUI 打开输出目录: {path}")
        except Exception as exc:
            messagebox.showerror("打开失败", str(exc))

    btn = tk.Frame(root)
    btn.pack(fill="x", padx=10, pady=10)
    tk.Button(btn, text="添加根目录", command=choose_root, width=12).pack(side="left", padx=4)
    tk.Button(btn, text="输出目录", command=choose_out, width=12).pack(side="left", padx=4)
    tk.Button(btn, text="状态文件", command=choose_state, width=12).pack(side="left", padx=4)
    tk.Button(btn, text="保存配置", command=save_cfg, width=12).pack(side="left", padx=4)
    tk.Button(btn, text="打开日志", command=open_log_file, width=12).pack(side="left", padx=4)
    tk.Button(btn, text="打开输出", command=open_output_dir, width=12).pack(side="left", padx=4)
    tk.Button(btn, text="运行一次", command=lambda: launch_subprocess(True), width=12).pack(side="left", padx=4)
    tk.Button(btn, text="启动驻场", command=lambda: launch_subprocess(False), width=12).pack(side="left", padx=4)

    root.mainloop()
    return 0


def main(argv: list[str]) -> int:
    try:
        config = parse_args(argv)
        log_path = setup_logging(config.output_dir if not config.gui_mode else default_output_dir())
        log_info(f"程序启动。platform={platform.system()} python={sys.version.split()[0]} argv={' '.join(argv)}")
        log_info(f"日志文件: {log_path}")
        if config.gui_mode:
            return launch_gui(config.cfg_file)
        save_json_file(config.cfg_file, config_to_persist_dict(config))
        log_info(f"配置已持久化: {config.cfg_file}")
        if config.mode == "resident":
            print(f"驻场模式启动。根目录: {', '.join(str(p) for p in config.inputs)}")
            print(f"状态文件: {config.state_file}")
            print(f"配置文件: {config.cfg_file}")
            print(f"输出目录: {config.output_dir}")
            print(f"运行日志: {config.output_dir / 'hunter.log'}")
            agent = ResidentAgent(config)
            return agent.loop()
        hunter = NginxTraceHunter(config)
        report = hunter.run()
        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        print(f"报告已输出到: {config.output_dir}")
        print(f"运行日志: {config.output_dir / 'hunter.log'}")
        return 0
    except KeyboardInterrupt:
        eprint("已中断。")
        try:
            log_info("用户中断。")
        except Exception:
            pass
        return 130
    except Exception as exc:
        eprint(f"执行失败: {exc}")
        try:
            log_error(f"执行失败: {exc}\n{traceback.format_exc()}")
        except Exception:
            pass
        return 1
    finally:
        try:
            logging.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
