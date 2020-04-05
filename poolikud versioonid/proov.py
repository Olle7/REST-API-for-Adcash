l=[{"id":0},{"id":1},{"id":2},{"id":4},{"id":10}]

def leia_vähim_vaba_id(l):
    new_id = 0
    new_id_free = False
    while not new_id_free:
        new_id_free = True
        for d in l:
            if new_id == d["id"]:
                new_id_free = False
                new_id += 1
                break
    return new_id

print(leia_vähim_vaba_id(l))