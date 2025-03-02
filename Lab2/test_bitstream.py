from bitstream import BitStream

def main():
    # Тестові дані: кортеж (байти, кількість бітів для запису)
    test_data = [
        (bytes.fromhex("A5F0"), 12),  # 101001011111 -> запис 12 бітів
        (bytes.fromhex("3C7D"), 15),  # 001111000111110 -> запис 15 бітів
        (bytes.fromhex("FFAA"), 10),  # 1111111110 -> запис 10 бітів
        (bytes.fromhex("1234"), 16),  # 0001001000110100 -> запис 16 бітів
    ]
    
    # Запис тестових даних у файл
    with BitStream("test_extended.bin", "w") as bs:
        for data, bits in test_data:
            bs.write_bit_sequence(data, bits)
    
    # Зчитування та вивід прочитаних даних
    with BitStream("test_extended.bin", "r") as bs:
        for i, (_, bits) in enumerate(test_data, start=1):
            read_data, bits_read = bs.read_bit_sequence(bits)
            print(f"Chunk {i}: {read_data.hex().upper()} (бітів прочитано: {bits_read})")
    
    # Перевірка записаних даних
    BitStream("test_extended.bin", "r").verify_written_data(test_data)
    print("Перевірка пройдена успішно!")
    
    # Додатковий тест: спроба зчитати більше бітів, ніж є у файлі
    with BitStream("test_extended.bin", "r") as bs:
        extra_data, extra_bits = bs.read_bit_sequence(100)
        print(f"Спроба читання 100 бітів: {extra_data.hex().upper()} (бітів прочитано: {extra_bits})")
    
    # Тест з порожнім файлом
    with BitStream("empty.bin", "w") as bs:
        pass
    with BitStream("empty.bin", "r") as bs:
        empty_data, empty_bits = bs.read_bit_sequence(10)
        print(f"Читання з порожнього файлу: {empty_data.hex().upper()} (бітів прочитано: {empty_bits})")

if __name__ == "__main__":
    main()
