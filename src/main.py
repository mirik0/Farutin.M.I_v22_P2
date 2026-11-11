import argparse
import re
import sys
import tarfile
from pathlib import Path
from urllib.parse import urlparse

from .graph import reverse_graph
from .repository import load_apk, load_test


def read_args(argv=None):
    parser = argparse.ArgumentParser(description="Зависимости APK, вариант 22")
    parser.add_argument("--package", required=True, help="имя пакета")
    parser.add_argument("--version", required=True, help="точная версия пакета")
    parser.add_argument("--repo", required=True,
                        help="URL репозитория или путь к тестовому JSON")
    parser.add_argument("--test-repo", action="store_true",
                        help="использовать тестовый репозиторий")
    args = parser.parse_args(argv)
    pattern = r"[A-Z]+" if args.test_repo else r"[a-z0-9][a-z0-9+_.-]*"
    if not re.fullmatch(pattern, args.package):
        parser.error("--package: неверное имя пакета")
    if not args.version.strip():
        parser.error("--version: укажите версию пакета")
    if args.test_repo:
        if not Path(args.repo).is_file():
            parser.error("--repo: тестовый файл не найден")
    else:
        try:
            url = urlparse(args.repo)
        except ValueError:
            parser.error("--repo: неверный URL")
        if url.scheme not in ("http", "https") or not url.netloc:
            parser.error("--repo: нужен URL с http:// или https://")
    return args


def main(argv=None):
    args = read_args(argv)
    try:
        repo = load_test(args.repo) if args.test_repo else load_apk(args.repo)
        graph = reverse_graph(repo, args.package, args.version)
        for name in graph:
            if name != args.package:
                print(name)
    except (OSError, ValueError, KeyError, tarfile.TarError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
