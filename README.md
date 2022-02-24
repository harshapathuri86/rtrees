# RTrees

> Harsha Pathuri 2019101086

### Code Execution

- Usage: `python3 code.py <input_file>`

## Implementation Details

### Classes:

- `Point`: Implements `(x,y)` points which are inserted into the RTree.
- `Rectangle`: Implements the mbb of nodes in the RTree.
- `Node`: Implements the nodes in the RTree.
- `RTree`: Implements the RTree.

### `Node`:

**Functions**

- `update_rectangle` updates the mbb of the node.
- `leaf_insert`
  - Tries to insert point at the current leaf node.
  - If the leaf node overflows, it splits and returns a new node to insert into the tree to its parent node.
- `intermediate_insert`
  - Tries to insert a newly created node at the current inner node of the tree.
  - If the node overflows, it splits and returns a new node to insert into the tree to its parent node.
- `find`
  - Returns `True` if given point is found in the subtree of the current node. Else `False`
- `range`
  - Returns count of points in the subtree of the current node which fall inside the given `rectangle`

**Variables**

- `max_children` : 2, maximum number of children of an inner node.
- `max_points` : 12, maximum number of points that can be inserted into a leaf node. 
- `rectange` : `mbb` of the node
- `children` : List of child nodes.
- `is_leaf` :  True if the node is a leaf node. False for the inner node.

### `Rtree`

**Functions**

- `recursive_insert`
  - Inserts the given `point` into the tree recursively. If a split happens, returns the newly created node to the parent node.
  - If point does not fall into any `mbb`, it is inserted into the closest rectangle with change in area as the distance metric. 
- `insert`
  - Inserts the given point into the tree using the `recursive_insert` function and creates a new `root` if required.
- `find`
  - Calls `find` for the root node to find given `point` in the tree.
- `range`
  - Calls `range` for the root node to return the points in the given `rectangle`

**Variables**

- `root` : Root node of the Rtree.