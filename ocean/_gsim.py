from dataclasses import dataclass, field
from heapq import heappop, heappush, heappushpop
from typing import Dict, List, Optional, Tuple

import numpy as np
from sklearn.mixture import GaussianMixture

from core.models.cap import CapType


@dataclass(slots=True)
class Node:
    data: np.ndarray
    level: int
    meta: Dict[str, str] = field(default_factory=dict)
    neighbors: Dict[int, List[Tuple[float, "Node"]]] = field(
        default_factory=dict, compare=False
    )

    def __post_init__(self):
        object.__setattr__(self, "data", np.array(self.data))

    def add_neighbor(self, neighbor: "Node", level: int, max_neighbors: int = 300):
        if level not in self.neighbors:
            self.neighbors[level] = []

        dist = np.linalg.norm(self.data - neighbor.data)

        if len(self.neighbors[level]) < max_neighbors:
            heappush(self.neighbors[level], (-dist, neighbor))
        else:
            heappushpop(self.neighbors[level], (-dist, neighbor))

    def get_neighbors(self, level: int) -> List[Tuple[float, "Node"]]:
        return [(-d, n) for d, n in self.neighbors.get(level, [])]

    def __hash__(self):
        return hash((self.data.tobytes(), self.level))

    def __eq__(self, other: "Node"):
        return np.array_equal(self.data, other.data) and self.level == other.level

    def __lt__(self, other: "Node"):
        return np.linalg.norm(self.data) < np.linalg.norm(other.data)


class SIM:
    def __init__(
        self,
        max_level: int,
        max_neighbors: int = 16,
        ef_construction: int = 200,
        ef_search: int = 10,
    ):
        self.max_level = max_level
        self.max_neighbors = max_neighbors
        self.ef_construction = ef_construction
        self.ef_search = ef_search
        self.entry_point = None
        self.assign_probas = self._set_probas(max_neighbors, 1 / np.log(max_neighbors))
        self.emb = {}
        self.clusters = None
        self.centroids = None
        self.symbol_cluster_map = {}

    def _set_probas(self, max_neighbors: int, m_l: float) -> List[float]:
        nn = 0
        level = 0
        assign_probas = []

        while True:
            proba = np.exp(-level / m_l) * (1 - np.exp(-1 / m_l))
            if proba < 1e-9:
                break
            assign_probas.append(proba)
            nn += max_neighbors * 2 if level == 0 else max_neighbors
            level += 1

        return assign_probas

    def _random_level(self) -> int:
        level = 0

        while level < self.max_level and np.random.rand() < self.assign_probas[level]:
            level += 1

        return level

    def _distance(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        return np.linalg.norm(vec1 - vec2)

    def insert(self, data: np.ndarray, symbol: str) -> None:
        self.emb[symbol] = data

        level = self._random_level()
        new_node = Node(data, level, meta={"symbol": symbol})

        if self.entry_point is None:
            self.entry_point = new_node
            return

        current_node = self.entry_point

        for l in range(self.max_level, -1, -1):
            if l <= level:
                neighbors = self._beam_search(
                    current_node, new_node.data, l, self.ef_construction
                )
                new_node.neighbors[l] = self._select_best_neighbors(neighbors)

                for _, neighbor in new_node.neighbors[l]:
                    neighbor.add_neighbor(new_node, l, self.max_neighbors)

            current_node = self._greedy_search(new_node.data, current_node, l)

    def _beam_search(
        self, entry_node: Node, query: np.ndarray, level: int, ef: int
    ) -> List[Tuple[float, Node]]:
        candidates = [(self._distance(entry_node.data, query), entry_node)]
        visited = {entry_node}
        beam = []

        while candidates:
            dist, node = heappop(candidates)

            if len(beam) < ef:
                beam.append((dist, node))
            else:
                if dist < beam[-1][0]:
                    beam[-1] = (dist, node)

            for _, neighbor in node.get_neighbors(level):
                if neighbor not in visited:
                    visited.add(neighbor)

                    heappush(
                        candidates, (self._distance(neighbor.data, query), neighbor)
                    )

        return beam

    def _greedy_search(self, query: np.ndarray, entry_node: Node, level: int) -> Node:
        current_node = entry_node
        current_dist = self._distance(query, current_node.data)

        while True:
            found_closer = False
            for _, neighbor in current_node.get_neighbors(level):
                dist = self._distance(query, neighbor.data)
                if dist < current_dist:
                    current_node = neighbor
                    current_dist = dist
                    found_closer = True

            if not found_closer:
                break

        return current_node

    def _select_best_neighbors(
        self, neighbors: List[Tuple[float, Node]]
    ) -> List[Tuple[float, Node]]:
        return sorted(neighbors, key=lambda x: x[0])

    def _perform_clustering(self, n_clusters: int = 3) -> None:
        if not self.emb:
            return

        symbols = list(self.emb.keys())
        embeddings = np.array(list(self.emb.values()))

        gmm = GaussianMixture(n_components=n_clusters, random_state=1337)

        self.clusters = gmm.fit_predict(embeddings)
        self.symbol_cluster_map = dict(zip(symbols, self.clusters))
        self.centroids = self._calculate_cluster_centroids()

    def _calculate_cluster_centroids(self) -> Dict[int, np.ndarray]:
        symbols = list(self.emb.keys())
        embeddings = np.array(list(self.emb.values()))
        clusters = np.array([self.symbol_cluster_map[symbol] for symbol in symbols])

        cluster_ids, cluster_counts = np.unique(clusters, return_counts=True)
        centroid_sums = np.zeros((len(cluster_ids), embeddings.shape[1]))

        for i, cluster_id in enumerate(cluster_ids):
            centroid_sums[i] = embeddings[clusters == cluster_id].sum(axis=0)

        centroids = {
            cluster: centroid_sums[i] / cluster_counts[i]
            for i, cluster in enumerate(cluster_ids)
        }
        return centroids

    def search(
        self, query: np.ndarray, top_k: int = 10
    ) -> Optional[List[Tuple[float, Node]]]:
        if self.entry_point is None:
            return None

        current_node = self.entry_point
        ef = max(self.ef_search, top_k)
        candidates = []

        for l in range(self.max_level, -1, -1):
            candidates += self._beam_search(current_node, query, l, ef)
            current_node = self._greedy_search(query, current_node, l)

        re_ranked_results = sorted(set(candidates), key=lambda x: x[0])

        return re_ranked_results[:top_k]

    def find_similar_symbols(self, symbol: str, top_k: int = 10):
        if self.entry_point is None:
            return []

        emb = self.emb.get(symbol)

        if emb is None:
            return []

        similar = self.search(emb, top_k + 1)

        return [
            node.meta.get("symbol")
            for _, node in similar
            if node.meta.get("symbol") != symbol
        ]

    def find_similar_by_cap(self, cap: CapType, top_k: int = 10):
        if self.entry_point is None:
            return []

        if self.clusters is None:
            self._perform_clustering()

        sorted_clusters_by_magnitude = sorted(
            self.centroids.items(), key=lambda x: np.linalg.norm(x[1])
        )
        n_sorted_clusters_by_magnitude = len(sorted_clusters_by_magnitude)

        cap_to_cluster = {
            CapType.A: (
                sorted_clusters_by_magnitude[0][0]
                if n_sorted_clusters_by_magnitude > 0
                else None
            ),
            CapType.B: (
                sorted_clusters_by_magnitude[1][0]
                if n_sorted_clusters_by_magnitude > 1
                else None
            ),
            CapType.C: (
                sorted_clusters_by_magnitude[2][0]
                if n_sorted_clusters_by_magnitude > 2
                else None
            ),
        }

        cluster_index = cap_to_cluster.get(cap)

        if cluster_index is None:
            return []

        q = self.centroids[cluster_index]

        similar = self.search(q, top_k=top_k)

        return [node.meta.get("symbol") for _, node in similar]
