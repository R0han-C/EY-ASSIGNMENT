"""
Assignment #2
A demo showcasing Directed Acyclic Graph (DAG) based Dependency Graph.
Make sure to cover all edge cases and be prepared to talk about them (How are you making sure that the dependency graph passed is a DAG?)
Prepare examples for both happy and unhappy test cases.
"""


class DependencyGraph:
    def __init__(self):
        self.graph = {}

    def add_dependency(self, node, dependencies):
        if not self.confirm_dag(node, dependencies):
            raise ValueError("Adding the dependency would create a cycle")
        self.graph[node] = dependencies

    def get_dependencies(self, node):
        return self.graph.get(node, [])

    def confirm_dag(self, node, dependencies):
        visited = set()
        stack = set()

        def dfs(current):
            if current in stack:
                return False
            if current in visited:
                return True

            visited.add(current)
            stack.add(current)

            for neighbor in self.graph.get(current, []):
                if not dfs(neighbor):
                    return False

            stack.remove(current)
            return True

        for dependency in dependencies:
            if not dfs(dependency):
                return False

        return True

if __name__ == "__main__":
    filename = "assignment_2"
    
    graph = DependencyGraph()

    try:

        graph.add_dependency("A", ["B", "C"])
        graph.add_dependency("B", ["D"])
        graph.add_dependency("C", ["D"])
        graph.add_dependency("D", [])

        print("Happy test case: Dependencies added successfully.")

    except ValueError as e:

        print("Happy test case failed:", e)

    try:
        graph.add_dependency("D", ["A"])
        print("Unhappy test case failed: Cycle not detected.")
    except ValueError as e:
        print("Unhappy test case: Cycle detected as expected.")


    print("Dependencies of A:", graph.get_dependencies("A"))
    print("Dependencies of B:", graph.get_dependencies("B"))
    print("Dependencies of C:", graph.get_dependencies("C"))
    print("Dependencies of D:", graph.get_dependencies("D"))

