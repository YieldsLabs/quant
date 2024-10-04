import hashlib
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
        if not isinstance(self.data, np.ndarray):
            object.__setattr__(self, "data", np.array(self.data))

    def add_neighbor(self, neighbor: "Node", level: int, max_neighbors: int = 300):
        if level not in self.neighbors:
            self.neighbors[level] = []

        dist = self._distance(self.data, neighbor.data)

        if len(self.neighbors[level]) < max_neighbors:
            heappush(self.neighbors[level], (-dist, neighbor))
        else:
            heappushpop(self.neighbors[level], (-dist, neighbor))

    def get_neighbors(self, level: int) -> List["Node"]:
        return [n for _, n in self.neighbors.get(level, [])]

    @staticmethod
    def _distance(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        return np.linalg.norm(vec_a - vec_b)

    def __eq__(self, other: "Node"):
        return (
            np.allclose(self.data, other.data, rtol=1e-5, atol=1e-8)
            and self.level == other.level
        )

    def __hash__(self):
        hasher = hashlib.md5()

        hasher.update(self.data.round(decimals=5).tobytes())
        hasher.update(self.level.to_bytes(4, "little"))

        return int(hasher.hexdigest(), 16)

    def __lt__(self, other: "Node"):
        return np.isclose(
            np.linalg.norm(self.data), np.linalg.norm(other.data), rtol=1e-5, atol=1e-8
        ) or np.linalg.norm(self.data) < np.linalg.norm(other.data)


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
        self.cum_probas = np.cumsum(self._set_probas(1 / np.log(max_neighbors)))
        self.emb = {}
        self.clusters = None
        self.centroids = None
        self.symbol_cluster_map = {}

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

                for neighbor in new_node.get_neighbors(l):
                    neighbor.add_neighbor(new_node, l, self.max_neighbors)

            current_node = self._greedy_search(new_node.data, current_node, l)

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

        if self.clusters is None or self.centroids is None:
            self.perform_clustering()

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

    def perform_clustering(self, n_clusters: int = 3) -> None:
        if not self.emb:
            return

        symbols = list(self.emb.keys())
        embeddings = np.array(list(self.emb.values()))

        gmm = GaussianMixture(
            n_components=n_clusters, init_params="k-means++", random_state=1337
        )

        self.clusters = gmm.fit_predict(embeddings)
        self.symbol_cluster_map = dict(zip(symbols, self.clusters))
        self.centroids = self._calculate_cluster_centroids()

    def _random_level(self) -> int:
        rand_val = np.random.rand()
        return int(np.searchsorted(self.cum_probas, rand_val))

    def _beam_search(
        self, entry_node: Node, query: np.ndarray, level: int, ef: int
    ) -> List[Tuple[float, Node]]:
        candidates = [(self._distance(entry_node.data, query), entry_node)]
        visited = {entry_node}
        beam = []

        while candidates:
            dist, node = heappop(candidates)

            if len(beam) < ef:
                heappush(beam, (dist, node))
            else:
                if dist < beam[0][0]:
                    heappushpop(beam, (dist, node))

            for neighbor in node.get_neighbors(level):
                if neighbor not in visited:
                    visited.add(neighbor)
                    neighbor_dist = self._distance(neighbor.data, query)

                    heappush(candidates, (neighbor_dist, neighbor))

        return beam

    def _greedy_search(self, query: np.ndarray, entry_node: Node, level: int) -> Node:
        current_node = entry_node
        current_dist = self._distance(query, current_node.data)

        while True:
            found_closer = False

            for neighbor in current_node.get_neighbors(level):
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
        return sorted(neighbors, key=lambda x: (x[0], id(x[1])))

    def _calculate_cluster_centroids(self) -> Dict[int, np.ndarray]:
        clusters = np.array(
            [self.symbol_cluster_map[symbol] for symbol in self.emb.keys()]
        )
        cluster_ids = np.unique(clusters)
        centroid_sums = np.vstack(
            [
                np.mean(np.array(list(self.emb.values()))[clusters == cluster], axis=0)
                for cluster in cluster_ids
            ]
        )

        return dict(zip(cluster_ids, centroid_sums))

    @staticmethod
    def _set_probas(m_l: float) -> List[float]:
        levels = np.arange(0, 100)

        probas = np.exp(-levels / m_l) * (1 - np.exp(-1 / m_l))
        probas = probas[probas >= 1e-9]

        return probas

    @staticmethod
    def _distance(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        return np.linalg.norm(vec_a - vec_b)
