class BitStream:
    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = open(filename, f"{mode}b")
        self.write_buffer = [] if mode == 'w' else None
        self.read_buffer = [] if mode == 'r' else None
        self.bit_ptr = 0  # Вказівник для читання

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.mode == 'w' and self.write_buffer:
            padding = (8 - len(self.write_buffer) % 8) % 8
            self.write_buffer.extend([0] * padding)
            self._flush_write_buffer()
        self.file.close()

    def _flush_write_buffer(self):
        while len(self.write_buffer) >= 8:
            byte = 0
            for i in range(8):
                byte |= self.write_buffer.pop(0) << (7 - i)
            self.file.write(bytes([byte]))

    def write_bit_sequence(self, data, num_bits):
        bits = []
        for byte in data:
            for shift in range(7, -1, -1):
                bits.append((byte >> shift) & 1)
        bits = bits[:num_bits]
        self.write_buffer.extend(bits)
        self._flush_write_buffer()

    def read_bit_sequence(self, num_bits):
        result_bits = []
        while num_bits > 0:
            if self.bit_ptr >= len(self.read_buffer):
                byte = self.file.read(1)
                if not byte:
                    break
                self.read_buffer = [(byte[0] >> i) & 1 for i in range(7, -1, -1)]
                self.bit_ptr = 0

            result_bits.append(self.read_buffer[self.bit_ptr])
            self.bit_ptr += 1
            num_bits -= 1

        byte_arr = bytearray()
        current_byte = 0
        bit_count = 0
        for bit in result_bits:
            current_byte = (current_byte << 1) | bit
            bit_count += 1
            if bit_count == 8:
                byte_arr.append(current_byte)
                current_byte = 0
                bit_count = 0

        if bit_count > 0:
            current_byte <<= (8 - bit_count)
            byte_arr.append(current_byte)

        return bytes(byte_arr), len(result_bits)
