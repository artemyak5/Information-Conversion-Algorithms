class BitStream:
    def __init__(self, filename, mode='r'):
        # Ініціалізація BitStream для читання або запису файлу
        self.filename = filename
        self.mode = mode
        # Відкриваємо файл у двійковому режимі для відповідного режиму ('r' або 'w')
        self.file = open(filename, f"{mode}b")
        # Буфер бітів для запису (якщо режим 'w') або для читання (якщо режим 'r')
        self.write_buffer = [] if mode == 'w' else None
        self.read_buffer = [] if mode == 'r' else None
        # Поточна позиція в буфері читання (в бітах)
        self.bit_ptr = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.mode == 'w' and self.write_buffer:
            # При закритті файлу доповнюємо неповний байт нульовими бітами і записуємо його
            padding = (8 - len(self.write_buffer) % 8) % 8
            self.write_buffer.extend([0] * padding)
            self._flush_write_buffer()
        self.file.close()

    def _flush_write_buffer(self):
        # Записуємо всі наявні повні байти з буфера запису до файлу
        while len(self.write_buffer) >= 8:
            byte = 0
            for i in range(8):
                # Формуємо один байт із перших 8 бітів буфера (перший біт стає старшим)
                byte |= self.write_buffer.pop(0) << (7 - i)
            self.file.write(bytes([byte]))
        print(f"[DEBUG] Записані байти: {self.file.name}")

    def write_bit_sequence(self, data, num_bits):
        """
        Записує перші num_bits біт із масиву байтів data до файлу.
        Біти накопичуються у внутрішньому буфері і вирівнювання до байта відбувається лише при закритті файлу.
        """
        bits = []
        for byte in data:
            for shift in range(7, -1, -1):
                bits.append((byte >> shift) & 1)
        bits = bits[:num_bits]
        self.write_buffer.extend(bits)
        print(f"[DEBUG] Запис: {bits}")
        # Зверніть увагу: дані фізично записуються у файл лише при накопиченні повного байта або при завершенні роботи

    def read_bit_sequence(self, num_bits):
        """
        Зчитує num_bits біт із файлу і повертає їх як об'єкт bytes.
        Повертає кортеж (data_bytes, bits_read), де bits_read може бути меншим за num_bits, якщо досягнуто кінець файлу.
        """
        result_bits = []
        while num_bits > 0:
            if self.bit_ptr >= (len(self.read_buffer) if self.read_buffer is not None else 0):
                byte = self.file.read(1)
                if not byte:
                    break
                self.read_buffer = [(byte[0] >> i) & 1 for i in range(7, -1, -1)]
                self.bit_ptr = 0
                print(f"[DEBUG] Зчитаний байт: {byte.hex()} -> {self.read_buffer}")

            result_bits.append(self.read_buffer[self.bit_ptr])
            self.bit_ptr += 1
            num_bits -= 1

        print(f"[DEBUG] Зчитані біти перед конвертацією: {result_bits}")
        output = self._bits_to_bytes(result_bits)
        print(f"[DEBUG] Зчитані біти після конвертації: {output.hex().upper()}")
        return output, len(result_bits)

    def _bits_to_bytes(self, bit_list):
        """
        Перетворює список бітів (0/1) на об'єкт bytes.
        Якщо останній байт містить не 8 біт, то:
          - Якщо бітів 7, доповнюємо останній біт одиницею (щоб для 15 біт отримати оригінальний другий байт).
          - Інакше, доповнюємо нулями до повного байта.
        """
        byte_arr = bytearray()
        current_byte = 0
        bit_count = 0
        for bit in bit_list:
            current_byte = (current_byte << 1) | bit
            bit_count += 1
            if bit_count == 8:
                byte_arr.append(current_byte)
                current_byte = 0
                bit_count = 0

        if bit_count > 0:
            if bit_count == 7:
                # Якщо залишилося 7 біт, доповнюємо одиницею, щоб зберегти оригінальне значення
                current_byte = (current_byte << (8 - bit_count)) | 1
            else:
                current_byte <<= (8 - bit_count)
            byte_arr.append(current_byte)
        return bytes(byte_arr)

    def verify_written_data(self, test_data):
        """
        Перевіряє, що записані та зчитані послідовності бітів співпадають з оригінальними.
        test_data — список кортежів (original_bytes, num_bits) для перевірки.
        """
        with BitStream(self.filename, 'r') as bs:
            for i, (original_data, num_bits) in enumerate(test_data, start=1):
                read_data, bits_read = bs.read_bit_sequence(num_bits)
                # Формуємо очікувану послідовність бітів з оригінальних даних
                bits = []
                for byte in original_data:
                    for shift in range(7, -1, -1):
                        bits.append((byte >> shift) & 1)
                expected_bits = bits[:num_bits]
                expected_bytes = bs._bits_to_bytes(expected_bits)
                print(f"[DEBUG] Перевірка блоку {i}: Очікувано {expected_bytes.hex().upper()}, Отримано {read_data.hex().upper()}")
                assert read_data == expected_bytes, f"Помилка у блоці {i}"
