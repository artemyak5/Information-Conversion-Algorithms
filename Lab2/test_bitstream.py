from bitstream import BitStream

if __name__ == "__main__":
    test_data = [
        (bytes.fromhex("A5F0"), 12),  # 101001011111 -> запис 12 бітів
        (bytes.fromhex("3C7D"), 15),  # 001111000111110 -> запис 15 бітів
        (bytes.fromhex("FFAA"), 10),  # 1111111110 -> запис 10 бітів
        (bytes.fromhex("1234"), 16),  # 0001001000110100 -> запис 16 бітів
    ]
    
    with BitStream("test_extended.bin", "w") as bs:
        for data, bits in test_data:
            bs.write_bit_sequence(data, bits)
    
    with BitStream("test_extended.bin", "r") as bs:
        for i, (_, bits) in enumerate(test_data):
            read_data, bits_read = bs.read_bit_sequence(bits)
            print(f"Chunk {i + 1}: {read_data.hex().upper()} (бітів прочитано: {bits_read})")
