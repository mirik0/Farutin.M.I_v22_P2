def dfs(root, get_neighbors):
    graph = {}

    def visit(name):
        if name in graph:
            return
        graph[name] = get_neighbors(name)
        for dependency in graph[name]:
            visit(dependency)

    visit(root)
    return graph


def dependency_graph(repo, name, version):
    root = repo.get(name, version)

    def get_neighbors(current):
        package = root if current == name else repo.get(current)
        return repo.dependencies(package)

    return dfs(name, get_neighbors)


def reverse_graph(repo, name, version):
    repo.get(name, version)
    reversed_edges = {key: [] for key, _ in repo.packages}
    for package in repo.packages.values():
        for dependency in repo.dependencies(package):
            parents = reversed_edges[dependency]
            if package["name"] not in parents:
                parents.append(package["name"])

    def get_neighbors(current):
        return reversed_edges[current]

    return dfs(name, get_neighbors)
