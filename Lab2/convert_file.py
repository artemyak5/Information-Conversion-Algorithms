from bitstream import BitStream

def convert_file(input_filename, output_filename):
    # Читаємо файл порціями по 1024 біта
    chunk_size = 1024
    with BitStream(input_filename, "r") as bs_in, BitStream(output_filename, "w") as bs_out:
        while True:
            data, bits_read = bs_in.read_bit_sequence(chunk_size)
            if bits_read == 0:
                break
            # Записуємо прочитані біти у вихідний файл
            bs_out.write_bit_sequence(data, bits_read)
    print(f"Конвертація завершена. Вихідний файл: {output_filename}")

def main():
    # Використовуємо прямі слеші для коректного формування шляху
    input_filename = "Information-Conversion-Algorithms/Lab2/file.bin"         
    output_filename = "Information-Conversion-Algorithms/Lab2/output_file.bin"  
    convert_file(input_filename, output_filename)

if __name__ == "__main__":
    main()
