import argparse
import re
from pathlib import Path
from urllib.parse import urlparse


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


def conf_dump(args):
    for key, value in vars(args).items():
        print(f"{key}={value}")


def main(argv=None):
    conf_dump(read_args(argv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
