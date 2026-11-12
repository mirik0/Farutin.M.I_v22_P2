def to_plantuml(graph):
    lines = ["@startuml", "left to right direction"]
    aliases = {}
    for number, name in enumerate(graph):
        alias = f"N{number}"
        aliases[name] = alias
        lines.append(f'component "{name}" as {alias}')
    for name, depends in graph.items():
        for dependency in depends:
            lines.append(f"{aliases[name]} --> {aliases[dependency]}")
    lines.append("@enduml")
    return "\n".join(lines)
