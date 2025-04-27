# main.py
# Реалізація Task 1 (trie) та Task 2 (Aho–Korasick) з двома вхідними файлами.

import os

class Queue:
    def __init__(self):
        self._data = []
        self._head = 0
    def enqueue(self, x):
        self._data.append(x)
    def dequeue(self):
        if self._head < len(self._data):
            val = self._data[self._head]
            self._head += 1
            return val
        raise IndexError("dequeue з порожньої черги")
    def is_empty(self):
        return self._head >= len(self._data)

class AhoCorasick:
    def __init__(self):
        # children[node] = {символ: індекс вузла}
        self.children = []
        self.fail = []
        self.output = []
        self._create_node()
    def _create_node(self):
        self.children.append({})
        self.fail.append(0)
        self.output.append([])
        return len(self.children) - 1
    def add_pattern(self, pattern, pid):
        node = 0
        for ch in pattern:
            if ch not in self.children[node]:
                nxt = self._create_node()
                self.children[node][ch] = nxt
            node = self.children[node][ch]
        self.output[node].append(pid)
    def build_automaton(self):
        q = Queue()
        for ch, nxt in self.children[0].items():
            self.fail[nxt] = 0
            q.enqueue(nxt)
        while not q.is_empty():
            cur = q.dequeue()
            for pid in self.output[self.fail[cur]]:
                self.output[cur].append(pid)
            for ch, nxt in self.children[cur].items():
                q.enqueue(nxt)
                f = self.fail[cur]
                while f != 0 and ch not in self.children[f]:
                    f = self.fail[f]
                self.fail[nxt] = self.children[f].get(ch, 0)
    def find_all(self, text, patterns):
        result = set()
        node = 0
        for i, ch in enumerate(text):
            while node != 0 and ch not in self.children[node]:
                node = self.fail[node]
            node = self.children[node].get(ch, 0)
            for pid in self.output[node]:
                start = i - len(patterns[pid]) + 1
                result.add(start)
        return sorted(result)


def task1_trie(patterns):
    root = {}
    node_id = {id(root): 0}
    next_id = 1
    edges = []
    for pat in patterns:
        node = root
        for ch in pat:
            if ch not in node:
                new_node = {}
                node[ch] = new_node
                parent = node_id[id(node)]
                node_id[id(new_node)] = next_id
                edges.append(f"{parent}->{next_id}:{ch}")
                next_id += 1
            node = node[ch]
    return edges


def task2_aho(text, patterns):
    ac = AhoCorasick()
    for idx, p in enumerate(patterns):
        ac.add_pattern(p, idx)
    ac.build_automaton()
    return ac.find_all(text, patterns)


def main():
    base = os.path.dirname(__file__)
    # Шляхи до двох вхідних файлів
    trie_in = os.path.join(base, 'input_trie.dat')
    aho_in  = os.path.join(base, 'input_aho.dat')
    # Шляхи до файлів-виходів
    trie_out = os.path.join(base, 'output_trie.dat')
    aho_out  = os.path.join(base, 'output_aho.dat')

    # Task 1: Trie
    if os.path.exists(trie_in):
        with open(trie_in, 'r', encoding='utf-8') as fin:
            lines = [l.strip() for l in fin if l.strip()]
        if lines and lines[0].isdigit():
            n = int(lines[0])
            patterns = lines[1:1+n]
            edges = task1_trie(patterns)
            with open(trie_out, 'w', encoding='utf-8') as fout:
                for e in edges:
                    fout.write(e + '\n')

    # Task 2: Aho–Korasick
    if os.path.exists(aho_in):
        with open(aho_in, 'r', encoding='utf-8') as fin:
            lines = [l.strip() for l in fin if l.strip()]
        if lines:
            text = lines[0]
            n = int(lines[1]) if len(lines) > 1 else 0
            patterns = lines[2:2+n]
            matches = task2_aho(text, patterns)
            with open(aho_out, 'w', encoding='utf-8') as fout:
                if matches:
                    fout.write(' '.join(map(str, matches)))

if __name__ == '__main__':
    main()
