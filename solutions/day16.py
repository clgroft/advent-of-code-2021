from math import prod


class Packet:
    BIN_FROM_HEX = {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
    }

    def __init__(self, version):
        self.version = version

    def sum_versions(self):
        return self.version

    @classmethod
    def parse(cls, line):
        bin_line = ''.join(Packet.BIN_FROM_HEX[c] for c in line.strip())
        packet, _ = cls._parse(bin_line)
        return packet

    @classmethod
    def _parse(cls, bin_line):
        version_bits, bin_line = bin_line[:3], bin_line[3:]
        version = int(version_bits, 2)
        type_id_bits, bin_line = bin_line[:3], bin_line[3:]
        type_id = int(type_id_bits, 2)

        if type_id == 4:  # literal packet
            keep_reading_bit, literal_bits = '1', ''
            while keep_reading_bit == '1':
                keep_reading_bit, value_bits, bin_line = (
                    bin_line[0], bin_line[1:5], bin_line[5:]
                )
                literal_bits += value_bits
            literal = int(literal_bits, 2)
            packet = LiteralPacket(version, literal)
            return LiteralPacket(version, literal), bin_line

        # operator packet
        length_type_bit, bin_line = bin_line[0], bin_line[1:]
        if length_type_bit == '0':
            length_bits, bin_line = bin_line[:15], bin_line[15:]
            length = int(length_bits, 2)
            subpackets_bits, bin_line = bin_line[:length], bin_line[length:]
            subpackets = []
            while subpackets_bits:
                subpacket, subpackets_bits = cls._parse(subpackets_bits)
                subpackets.append(subpacket)
            return OperatorPacket(version, type_id, subpackets), bin_line
        else:
            num_subpackets_bits, bin_line = bin_line[:11], bin_line[11:]
            num_subpackets = int(num_subpackets_bits, 2)
            subpackets = []
            for _ in range(num_subpackets):
                subpacket, bin_line = cls._parse(bin_line)
                subpackets.append(subpacket)
            return OperatorPacket(version, type_id, subpackets), bin_line


class LiteralPacket(Packet):
    def __init__(self, version, value):
        super().__init__(version)
        self.value = value

    def __str__(self):
        return f'{self.version}: {self.value}'

    def get_value(self):
        return self.value


class OperatorPacket(Packet):
    def __init__(self, version, type_id, subpackets):
        super().__init__(version)
        self.type_id = type_id
        self.subpackets = subpackets

    def __str__(self):
        return (f'{self.version}, {self.type_id}: ' +
                f'[{", ".join(map(str, self.subpackets))}]')

    def sum_versions(self):
        return self.version + sum(v.sum_versions() for v in self.subpackets)

    def get_value(self):
        if self.type_id == 0:
            return sum(p.get_value() for p in self.subpackets)
        if self.type_id == 1:
            return prod(p.get_value() for p in self.subpackets)
        if self.type_id == 2:
            return min(p.get_value() for p in self.subpackets)
        if self.type_id == 3:
            return max(p.get_value() for p in self.subpackets)

        p, q = self.subpackets
        if self.type_id == 5:
            return 1 if p.get_value() > q.get_value() else 0
        if self.type_id == 6:
            return 1 if p.get_value() < q.get_value() else 0
        if self.type_id == 7:
            return 1 if p.get_value() == q.get_value() else 0


def solution(day, lines):
    print()
    for l in lines:
        print(l.strip())
        packet = Packet.parse(l)
        print(packet)
        print(f'Version sum: {packet.sum_versions()}')
        print(f'Value: {packet.get_value()}')
        print()
