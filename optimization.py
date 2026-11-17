import heapq

class TransportGraph:
    def __init__(self):
        self.vertices = []
        self.edges = {}
        self.all_edges = []

    def add_station(self, name):
        if name not in self.vertices:
            self.vertices.append(name)
            self.edges[name] = []

    def add_route(self, u, v, weight):
        self.edges[u].append((v, weight))
        self.edges[v].append((u, weight))
        self.all_edges.append((u, v, weight))

    def shortest_path_Dijkstra(self, start):
        distances = {station: float('infinity') for station in self.vertices}
        distances[start] = 0
        pq = [(0, start)]
        
        while pq:
            current_dist, current_station = heapq.heappop(pq)
            if current_dist > distances[current_station]:
                continue
                
            for neighbor, weight in self.edges[current_station]:
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
                    
        return distances

    def shortest_path_BellmanFord(self, start):
        distances = {station: float('infinity') for station in self.vertices}
        distances[start] = 0
        for _ in range(len(self.vertices) - 1):
            for u, v, w in self.all_edges:
                if distances[u] != float('infinity') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                if distances[v] != float('infinity') and distances[v] + w < distances[u]:
                    distances[u] = distances[v] + w
                    
        # Проверка наличия отрицательных циклов
        for u, v, w in self.all_edges:
            if distances[u] != float('infinity') and distances[u] + w < distances[v]:
                raise ValueError("Граф содержит отрицательный цикл")
                
        return distances

    def all_pairs_shortest_paths_FloydWarshall(self):
        dist = {u: {v: float('infinity') for v in self.vertices} for u in self.vertices}
        
        for v in self.vertices:
            dist[v][v] = 0
            
        for u, v, w in self.all_edges:
            dist[u][v] = w
            dist[v][u] = w
            
        for k in self.vertices:
            for i in self.vertices:
                for j in self.vertices:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        
        return dist


class NetworkOptimizer:
    def __init__(self, graph):
        self.graph = graph

    def minimum_spanning_tree_Kruskal(self):
        parent = {v: v for v in self.graph.vertices}
        
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
            
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                
        mst = []
        total_weight = 0
        sorted_edges = sorted(self.graph.all_edges, key=lambda item: item[2])
        
        for u, v, weight in sorted_edges:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, weight))
                total_weight += weight
                
        return mst, total_weight

    def minimum_spanning_tree_Prim(self):
        if not self.graph.vertices:
            return [], 0
            
        start = self.graph.vertices[0]
        visited = set([start])
        edges = [(weight, start, to) for to, weight in self.graph.edges[start]]
        heapq.heapify(edges)
        
        mst = []
        total_weight = 0
        
        while edges and len(visited) < len(self.graph.vertices):
            weight, u, v = heapq.heappop(edges)
            if v not in visited:
                visited.add(v)
                mst.append((u, v, weight))
                total_weight += weight
                for next_v, next_weight in self.graph.edges[v]:
                    if next_v not in visited:
                        heapq.heappush(edges, (next_weight, v, next_v))
                        
        return mst, total_weight


if __name__ == "__main__":
    g = TransportGraph()
    stations = [
        "Центр. вокзал", "Пл. Ленина", "Автостанция-1", "Университет",
        "Вокзал-Северный", "Автостанция-2", "Парковая", "Портовая"
    ]
    
    for st in stations:
        g.add_station(st)

    # Добавление маршрутов
    routes = [
        ("Центр. вокзал", "Пл. Ленина", 1.2),
        ("Центр. вокзал", "Автостанция-1", 3.5),
        ("Центр. вокзал", "Вокзал-Северный", 4.0),
        ("Пл. Ленина", "Автостанция-1", 2.1),
        ("Пл. Ленина", "Университет", 0.8),
        ("Пл. Ленина", "Автостанция-2", 3.0),
        ("Пл. Ленина", "Парковая", 1.5),
        ("Автостанция-1", "Автостанция-2", 5.4),
        ("Автостанция-1", "Портовая", 4.2),
        ("Университет", "Вокзал-Северный", 2.7),
        ("Университет", "Автостанция-2", 1.9),
        ("Вокзал-Северный", "Парковая", 3.3),
        ("Вокзал-Северный", "Портовая", 6.0),
        ("Автостанция-2", "Парковая", 2.5)
    ]
    
    for u, v, w in routes:
        g.add_route(u, v, w)

    # Поиск кратчайших путей от "Центр. вокзал" с использованием алгоритма Дейкстры
    print("--- Алгоритм Дейкстры (От Центр. вокзала) ---")
    dijkstra_res = g.shortest_path_Dijkstra("Центр. вокзал")
    for st, dist in dijkstra_res.items():
        print(f"{st}: {dist} км")

    # Проверка наличия отрицательных циклов и поиск кратчайших путей с использованием алгоритма Беллмана-Форда
    print("\n--- Алгоритм Беллмана-Форда (От Центр. вокзала) ---")
    bellman_res = g.shortest_path_BellmanFord("Центр. вокзал")
    for st, dist in bellman_res.items():
        print(f"{st}: {dist} км")

    # Поиск минимальной сети путей с использованием алгоритма Прима и Крускала
    optimizer = NetworkOptimizer(g)
    
    print("\n--- Минимальное остовное дерево (Крускал) ---")
    kruskal_mst, kruskal_weight = optimizer.minimum_spanning_tree_Kruskal()
    print(f"Ребра: {kruskal_mst}")
    print(f"Суммарный вес: {kruskal_weight:.1f} км")

    print("\n--- Минимальное остовное дерево (Прим) ---")
    prim_mst, prim_weight = optimizer.minimum_spanning_tree_Prim()
    print(f"Ребра: {prim_mst}")
    print(f"Суммарный вес: {prim_weight:.1f} км")


    # Таблица
    # Вывод матрицы кратчайших путей (Флойд-Уоршалл) в виде таблицы
    print("\n--- Матрица кратчайших путей (Флойд-Уоршалл) ---")
    floyd_matrix = g.all_pairs_shortest_paths_FloydWarshall()
    
    # Определяем ширину первого столбца и остальных столбцов
    col_width = 16
    val_width = 10
    
    # Печатаем заголовок (сокращаем длинные названия для компактности)
    header = f"{'Узлы':<{col_width}}" + "".join([f"{st[:10]:<{val_width}}" for st in stations])
    print(header)
    print("-" * len(header))
    
    # Печатаем строки таблицы
    for row_st in stations:
        row_str = f"{row_st:<{col_width}}"
        for col_st in stations:
            val = floyd_matrix[row_st][col_st]
            if val == float('infinity'):
                val_str = "-"
            elif val == 0:
                val_str = "0"
            else:
                val_str = f"{val:.1f}"
            row_str += f"{val_str:<{val_width}}"
        print(row_str)