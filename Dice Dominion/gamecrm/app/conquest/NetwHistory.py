

class NetwHistory:
    def __init__(self):
        self.seq_no = -1
        self.quads = list()
        self.saved_seq = set()

    def update(self, full_history):
        new_chunk = list()
        for h_element in full_history:
            if h_element[0] not in self.saved_seq:
                new_chunk.append(h_element)

        for elt in new_chunk:
            self.add(elt)
        return new_chunk

    def add(self, quad_form):
        self.saved_seq.add(quad_form[0])
        self.quads.append(quad_form)
        self.seq_no += 1

    def get_free_seq_nb(self):
        return self.seq_no + 1
