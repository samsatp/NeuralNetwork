import math
import numpy as np

class Value:
    def __init__(self, data: float, label: str = "", previous = []) -> None:
        self.data =  data
        self.label = label
        self.grad = 0.0
        self._backward = lambda : None
        self._previous = previous

    def __repr__(self) -> str:
        if self.label != "":
            return f"Value(label = {self.label}, data = {self.data})"
        return f"Value(data = {self.data})"

    def __add__(self, other):
        # Forward pass
        other = Value(data=other) if not isinstance(other, Value) else other
        output = Value(data = self.data + other.data, previous=[self, other])

        # Backward pass function
        def _backward():
            self.grad += output.grad * 1.0
            other.grad += output.grad * 1.0
        output._backward = _backward
        
        return output

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        # Forward pass
        other = Value(data=other) if not isinstance(other, Value) else other
        output = Value(data = self.data * other.data, previous=[self, other])

        # Backward pass function
        def _backward():
            self.grad += output.grad * other.data
            other.grad += output.grad * self.data
        output._backward = _backward

        return output

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * other**(-1)

    def __pow__(self, n):
        assert isinstance(n, (int, float))
        # Forward pass
        output = Value(data=self.data ** n, previous=[self])

        # Backward pass function
        def _backward():
            self.grad += output.grad * ((n) * self.data ** (n-1))
        output._backward = _backward

        return output

    def __neg__(self):
        return -1 * self


    def tanh(self):
        # Forward pass
        x = self.data
        t = (math.exp(2*x) - 1)/(math.exp(2*x) + 1)
        output = Value(data = t, previous=[self])
        
        # Backward pass function
        def _backward():
            self.grad += (1 - t**2) * output.grad
        output._backward = _backward

        return output

    def backward(self):
        self.grad = 1.0

        def bfs(root): #function for BFS
            visited = []
            queue = []
            visited.append(root)
            queue.append(root)

            out = []
            while queue:          # Creating loop to visit each node
                m = queue.pop(0) 
                out.append(m)

                for neighbour in m._previous:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)

            return out
        output_order = bfs(self)
        for node in output_order:
            node._backward()