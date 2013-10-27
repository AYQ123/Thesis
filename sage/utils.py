def enumerate_graph(G,enum):
    for source_vert in enum.iterkeys():
        for term_vert in enum[source_vert].iterkeys():
            G.set_edge_label(source_vert,term_vert, enum[source_vert][term_vert])

def random_enumeration(G):
    import random

    enum = dict()

    for v in G.vertex_iterator():
        nhbd = G[v]
        deg = len(nhbd)
        random.shuffle(nhbd)
        enum[v] = dict(zip(range(0,deg), nhbd))

    return enum

def inverse_dict(d):

    return dict( [ [v,k] for k,v in d.iteritems()])


def parity_circuit(enum, init_edge):
    
    inv_enum = dict([[v, inverse_dict(d)] for v,d in enum.iteritems()])
    
    init_vert = init_edge[0]
    next_vert = init_edge[1]
    init_enum = inv_enum[init_vert][next_vert]

    circ = [init_vert, next_vert]
    cur_vert = init_vert


    out_enum = inv_enum[init_edge[0]][init_edge[1]]
    in_enum = inv_enum[next_vert][cur_vert]
    out_enum = (in_enum + 2)%4
    cur_vert = next_vert

    
    while ( (cur_vert, out_enum) != (init_vert, init_enum) ):
        next_vert = enum[cur_vert][out_enum]
        circ.append(next_vert)
        in_enum = inv_enum[next_vert][cur_vert]
        out_enum = (in_enum + 2)%4
        cur_vert = next_vert
        
    return circ[:-1]

def zig_zag(G,H, enum):
    ZZ = DiGraph()
    
    inv_enum = dict([[v, inverse_dict(d)] for v,d in enum.iteritems()])
     
    for e in G.edge_iterator():
        [ ZZ.add_edge((e[0],a) ,(e[1],b) ) for a in H[inv_enum[e[0]][e[1]]] for b in H[inv_enum[e[1]][e[0]] ] ]

    return ZZ

def replacement(G,H,enum):
    RR = DiGraph()
    inv_enum = dict([[v, inverse_dict(d)] for v,d in enum.iteritems()])

    for v in G.vertex_iterator():
        [ RR.add_edge((v,e[0]), (v,e[1])) for e in H.edge_iterator() ]
    for e in G.edge_iterator():
        RR.add_edge( (e[0], inv_enum[e[0]][e[1]] ), (e[1],inv_enum[e[1]][e[0]] )) 

    return RR

def source_mat(G):
    L = list()
    D = DiGraph(G)
    n = D.num_verts()
    verts = D.vertices()
    
    for e in D.edge_iterator():
        row = [ 0 for i in range(n)]
        row[verts.index(e[0])] = 1
        L.append(row)
    return(Matrix(L))

def rot_mat(G,perm=None):
    D = DiGraph(G)
    n = D.num_edges()
    L = list()

    if perm == None:
        edges = D.edges()
    else:
        raise NotImplemented

    for e in edges:
        row = [0 for i in range(n) ]
        row[edges.index((e[1],e[0],None))] = 1
        L.append(row)

    return(Matrix(L))
