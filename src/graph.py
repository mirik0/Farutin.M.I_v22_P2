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
