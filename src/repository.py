import io
import json
import re
import tarfile
from pathlib import Path
from urllib.request import urlopen

NETWORK_TIMEOUT = 30


def dependency_name(value):
    return re.split(r"[<>=~]", value, maxsplit=1)[0]


def parse_index(text):
    packages = []
    for block in text.strip().split("\n\n"):
        fields = {}
        for line in block.splitlines():
            key, _, value = line.partition(":")
            fields[key] = value
        packages.append({
            "name": fields["P"], "version": fields["V"],
            "depends": fields.get("D", "").split(),
            "provides": fields.get("p", "").split(),
        })
    return packages


class Repository:

    def __init__(self, packages):
        self.packages = {}
        self.providers = {}
        for package in packages:
            key = (package["name"], package["version"])
            self.packages[key] = package
            for value in package["provides"]:
                name = dependency_name(value)
                self.providers.setdefault(name, package["name"])

    def get(self, name, version=""):
        for (package_name, package_version), package in self.packages.items():
            if package_name == name and (
                not version or package_version == version
            ):
                return package
        raise ValueError(f"пакет не найден: {name}={version}")

    def resolve(self, dependency):
        name = dependency_name(dependency)
        if any(key == name for key, _ in self.packages):
            return name
        return self.providers[name]

    def dependencies(self, package):
        names = []
        for value in package["depends"]:
            if value.startswith("!"):
                continue
            name = self.resolve(value)
            if name not in names:
                names.append(name)
        return names


def load_apk(url):
    url = url.rstrip("/") + "/APKINDEX.tar.gz"
    with urlopen(url, timeout=NETWORK_TIMEOUT) as response:
        data = response.read()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        text = archive.extractfile("APKINDEX").read().decode("utf-8")
    return Repository(parse_index(text))


def load_test(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    packages = []
    for name, versions in data.items():
        for version, depends in versions.items():
            packages.append({"name": name, "version": version,
                             "depends": depends, "provides": []})
    return Repository(packages)
