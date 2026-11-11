import io
import tarfile
from urllib.request import urlopen

NETWORK_TIMEOUT = 30


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
        for package in packages:
            key = (package["name"], package["version"])
            self.packages[key] = package

    def get(self, name, version=""):
        for (package_name, package_version), package in self.packages.items():
            if package_name == name and (
                not version or package_version == version
            ):
                return package
        raise ValueError(f"пакет не найден: {name}={version}")


def load_apk(url):
    url = url.rstrip("/") + "/APKINDEX.tar.gz"
    with urlopen(url, timeout=NETWORK_TIMEOUT) as response:
        data = response.read()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        text = archive.extractfile("APKINDEX").read().decode("utf-8")
    return Repository(parse_index(text))
