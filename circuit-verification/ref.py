import re
from oxidd.bdd import BDDManager
manager = BDDManager(100_000_000, 1_000_000, 8)

x = [manager.new_var() for i in range(1000)]
phis = [manager.new_var() for i in range(1000)]

y = [manager.new_var() for i in range(1000)]
psys = [manager.new_var() for i in range(1000)]

def ultimate_function(equations, mom, outputs1, outputs2, phis):
    pattern = r'x(\d+)'

    # Iterate over each equation in the list.
    for eq in equations:
        left_side, right_side = eq.split(' = ')
        i_left = re.findall(pattern, left_side)
        is_right = re.findall(pattern, right_side)

        if right_side.startswith("NAND"):
            supp = x[int(is_right[0])].nand(x[int(is_right[1])])
            if len(is_right) > 2:
                for variable in is_right[2:]:
                    supp = supp.nand(x[int(variable)])

            phis[int(i_left[0])] = supp
            del supp

        elif right_side.startswith("AND"):
            supp = x[int(is_right[0])].__and__(x[int(is_right[1])])
            if len(is_right) > 2:
                for variable in is_right[2:]:
                    supp = supp.__and__(x[int(variable)])

            phis[int(i_left[0])] = supp
            del supp

        elif right_side.startswith("NOT"):
            supp = (x[int(is_right[0])].__invert__())
            phis[int(i_left[0])] = supp


        elif right_side.startswith("OR"):
            supp = x[int(is_right[0])].__or__(x[int(is_right[1])])
            if len(is_right) > 2:
                for variable in is_right[2:]:
                    supp = supp.__or__(x[int(variable)])    

            phis[int(i_left[0])] = supp
            del supp


        else:
            raise ValueError(f"Unsupported operation: {right_side}")






# Iterate over each equation in the list.
    for eq in mom:
        left_side, right_side = eq.split(' = ')
        i_left = re.findall(pattern, left_side)
        is_right = re.findall(pattern, right_side)

        if right_side.startswith("NAND"):
            supp = y[int(is_right[0])].nand(y[int(is_right[1])])
            if len(is_right) > 2:
                for variable in is_right[2:]:
                    supp = supp.nand(y[int(variable)])

            psys[int(i_left[0])] = supp
            del supp

        elif right_side.startswith("AND"):
            supp = y[int(is_right[0])].__and__(y[int(is_right[1])])
            if len(is_right) > 2:
                for variable in is_right[2:]:
                    supp = supp.__and__(y[int(variable)])

            psys[int(i_left[0])] = supp
            del supp

        elif right_side.startswith("NOT"):
            supp = (y[int(is_right[0])].__invert__())
            psys[int(i_left[0])] = supp


        elif right_side.startswith("OR"):
            supp = y[int(is_right[0])].__or__(y[int(is_right[1])])
            if len(is_right) > 2:
                for variable in is_right[2:]:
                    supp = supp.__or__(y[int(variable)])    

            psys[int(i_left[0])] = supp
            del supp

        elif right_side.startswith("NOR"):
            supp = y[int(is_right[0])].nor(y[int(is_right[1])])
            if len(is_right) > 2:
                for variable in is_right[2:]:
                    supp = supp.nor(y[int(variable)])    

            psys[int(i_left[0])] = supp
            del supp

        else:
            raise ValueError(f"Unsupported operation: {right_side}")


    outputs1 = str(outputs1)
    indeces = re.findall(pattern, outputs1)
    supp = phis[int(indeces[0])].equiv(psys[int(indeces[0])])
    for index in indeces[1:]:
        supp = supp.__and__(phis[int(index)].equiv(psys[int(index)]))
    gamma = supp 
    del supp




    '''supp = x[0].__and__(x[1])
    supp = supp.__and__(x[2])
    supp = supp.__and__(x[3])
    supp = supp.__and__(x[15])
    supp = supp.__and__(x[5])
    supp = supp.__and__(x[6])
    supp = supp.__and__(x[7])
    supp = supp.__and__(x[8])
    supp = supp.__and__(x[9])
    supp = supp.__and__(x[10])
    supp = supp.__and__(x[11])
    supp = supp.__and__(x[12])
    supp = supp.__and__(x[13])
    supp = supp.__and__(x[14])
    supp = supp.__and__(x[4])'''

    # FIX THIS SHIT
    # now we do the logical and among these variables
    supp = (phis[0]).__and__(phis[1])
    supp2 = (psys[0]).__and__(psys[1])
    for i in range(2, len(x)):
        supp = supp.__and__(phis[i])
        supp2 = supp2.__and__(psys[i])
    phi_S = supp
    del supp
    phi_T = supp2
    del supp2
    final = (phi_S.__and__(phi_T)).__and__(gamma.__invert__())

    # result = final.__and__(gamma.__invert__())
    # result = final.imp(gamma)

    return result

out1 = ['x7', 'x3', 'x8', 'x9', 'x10', 'x11', 'x12']
out2 = ['y7', 'y3', 'y8', 'y9', 'y10', 'y11', 'y12']
mom = ['x13 = OR(x14, x1)', 'x12 = AND(x15, x5, x6)', 'x10 = NAND(x16, x17, x18, x19)', 'x9 = NAND(x20, x21, x22)', 'x23 = OR(x2, x1)', 'x15 = NOT(x4)', 'x14 = NOT(x2)', 'x26 = NOT(x5)', 'x27 = NOT(x6)', 'x28 = NAND(x27, x5)', 'x30 = NAND(x28, x4)', 'x8 = NAND(x32, x33)', 'x11 = NAND(x34, x35)', 'x36 = NAND(x1, x2)', 'x37 = NOT(x23)', 'x39 = NAND(x37, x27)', 'x42 = NOT(x28)', 'x44 = NOT(x36)', 'x46 = NAND(x28, x36)', 'x49 = NAND(x37, x4)', 'x51 = NAND(x36, x6)', 'x53 = NAND(x51, x49)', 'x56 = NAND(x36, x4)', 'x21 = NAND(x23, x4, x6)', 'x20 = NAND(x42, x56)', 'x22 = NAND(x53, x26)', 'x66 = NOT(x30)', 'x17 = NAND(x15, x26, x71, x72)', 'x16 = NAND(x66, x23)', 'x76 = NAND(x36, x23)', 'x33 = NAND(x46, x15)', 'x32 = NAND(x39, x26, x4)', 'x19 = NAND(x12, x36)', 'x18 = NAND(x44, x42)', 'x72 = NAND(x36, x6)', 'x71 = NAND(x44, x27)', 'x95 = NAND(x1, x14)', 'x97 = NAND(x13, x95)', 'x35 = NAND(x66, x76)', 'x34 = NAND(x97, x30)']

o = ['x1', 'x6', 'x7', 'x8', 'x9']
e = ['x9 = AND(x10, x11, x3)', 'x8 = NAND(x12, x13)', 'x6 = NAND(x14, x15)', 'x16 = NOT(x3)', 'x10 = NOT(x5)', 'x18 = NOT(x2)', 'x11 = NOT(x4)', 'x7 = NAND(x20, x21)', 'x22 = NAND(x23, x24, x10)', 'x26 = OR(x2, x3)', 'x15 = NAND(x26, x5)', 'x14 = NAND(x22, x4)', 'x31 = OR(x2, x4)', 'x32 = NAND(x16, x31)', 'x35 = NAND(x2, x16)', 'x37 = NAND(x35, x5)', 'x13 = OR(x2, x3, x5)', 'x12 = NAND(x37, x11)', 'x24 = NAND(x2, x16)', 'x23 = NAND(x18, x3)', 'x21 = NAND(x32, x5)', 'x20 = NAND(x16, x10, x4)']
m = ['x9 = NOR(x10, x4, x5)', 'x8 = NAND(x11, x12)', 'x6 = NAND(x13, x14)', 'x10 = NOT(x3)', 'x16 = NOT(x5)', 'x7 = NAND(x17, x18)', 'x19 = NOT(x2)', 'x20 = OR(x2, x3, x4)', 'x14 = NAND(x22, x4)', 'x13 = NAND(x20, x5)', 'x25 = OR(x2, x4)', 'x26 = NAND(x10, x25)', 'x12 = NAND(x30, x31, x10)', 'x11 = OR(x4, x5)', 'x34 = NAND(x2, x10)', 'x36 = NAND(x19, x3)', 'x22 = NAND(x36, x34)', 'x18 = NAND(x26, x5)', 'x17 = NAND(x10, x16, x4)', 'x31 = NAND(x19, x5)', 'x30 = NAND(x2, x4)']


orco = ['x22', 'x23', 'x24', 'x25', 'x35', 'x36', 'x37', 'x38', 'x39', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x60', 'x61', 'x62', 'x1', 'x63']
eq = ['x64 = AND(x65, x66)', 'x67 = AND(x65, x34)', 'x63 = NOT(x1)', 'x61 = NAND(x69, x70)', 'x62 = NAND(x69, x72)', 'x46 = NAND(x73, x74)', 'x45 = NAND(x75, x76)', 'x44 = NAND(x77, x78)', 'x43 = NAND(x79, x80, x81)', 'x42 = NAND(x82, x83, x84)', 'x41 = NAND(x85, x86, x87)', 'x40 = NAND(x88, x89, x90)', 'x39 = NAND(x91, x92, x93)', 'x38 = NAND(x94, x95, x96)', 'x37 = NAND(x97, x98, x99)', 'x36 = NAND(x100, x101, x102)', 'x35 = NAND(x103, x104, x105)', 'x66 = NOT(x34)', 'x107 = NOT(x26)', 'x108 = NAND(x109, x26)', 'x110 = NOT(x29)', 'x69 = NAND(x29, x1)', 'x65 = NAND(x113, x114, x115)', 'x116 = NOT(x6)', 'x117 = NOT(x7)', 'x118 = NOT(x8)', 'x119 = NOT(x27)', 'x120 = NOT(x31)', 'x47 = NAND(x121, x122)', 'x48 = NAND(x123, x124)', 'x49 = NAND(x125, x126)', 'x50 = NAND(x127, x128)', 'x51 = NAND(x129, x130)', 'x52 = NAND(x131, x132)', 'x53 = NAND(x133, x134)', 'x54 = NAND(x135, x136)', 'x55 = NAND(x137, x138)', 'x56 = NAND(x139, x140)', 'x57 = NAND(x141, x142)', 'x58 = NAND(x143, x144)', 'x59 = NAND(x145, x146)', 'x60 = NAND(x147, x148)', 'x109 = NOT(x33)', 'x114 = NAND(x151, x34)', 'x152 = NOT(x28)', 'x153 = NOT(x32)', 'x154 = NOT(x69)', 'x151 = OR(x27, x28, x31, x32)', 'x157 = NOT(x114)', 'x159 = NOT(x108)', 'x161 = NAND(x159, x152)', 'x164 = NAND(x165, x166, x161)', 'x115 = NAND(x110, x164, x1)', 'x113 = NAND(x154, x119)', 'x174 = NOT(x65)', 'x176 = OR(x26, x33)', 'x177 = NAND(x110, x176)', 'x104 = NAND(x64, x177)', 'x103 = NAND(x67, x9)', 'x105 = NAND(x174, x6)', 'x101 = NAND(x108, x110, x64)', 'x100 = NAND(x67, x10)', 'x102 = NAND(x174, x7)', 'x98 = NAND(x110, x109, x64)', 'x97 = NAND(x67, x11)', 'x99 = NAND(x174, x8)', 'x95 = NAND(x67, x12)', 'x94 = NAND(x64, x6)', 'x96 = NAND(x174, x9)', 'x92 = NAND(x67, x13)', 'x91 = NAND(x64, x7)', 'x93 = NAND(x174, x10)', 'x89 = NAND(x67, x14)', 'x88 = NAND(x64, x8)', 'x90 = NAND(x174, x11)', 'x86 = NAND(x67, x15)', 'x85 = NAND(x64, x9)', 'x87 = NAND(x174, x12)', 'x83 = NAND(x67, x16)', 'x82 = NAND(x64, x10)', 'x84 = NAND(x174, x13)', 'x80 = NAND(x67, x17)', 'x79 = NAND(x64, x11)', 'x81 = NAND(x174, x14)', 'x78 = NAND(x64, x12)', 'x77 = NAND(x174, x15)', 'x76 = NAND(x64, x13)', 'x75 = NAND(x174, x16)', 'x74 = NAND(x64, x14)', 'x73 = NAND(x174, x17)', 'x72 = NAND(x63, x27)', 'x70 = NAND(x2, x63)', 'x166 = NAND(x120, x33)', 'x165 = NAND(x107, x153, x109, x30)', 'x122 = NAND(x114, x18)', 'x121 = NAND(x118, x117, x157, x6)', 'x124 = NAND(x114, x19)', 'x123 = NAND(x118, x116, x157, x7)', 'x126 = NAND(x114, x20)', 'x125 = NAND(x117, x116, x157, x8)', 'x128 = NAND(x114, x21)', 'x127 = NAND(x157, x6, x7, x8)', 'x130 = NAND(x63, x22)', 'x129 = NAND(x18, x1)', 'x132 = NAND(x63, x23)', 'x131 = NAND(x19, x1)', 'x134 = NAND(x63, x24)', 'x133 = NAND(x20, x1)', 'x136 = NAND(x63, x25)', 'x135 = NAND(x21, x1)', 'x138 = NAND(x4, x63)', 'x137 = NAND(x26, x1)', 'x140 = NAND(x63, x28)', 'x139 = NAND(x26, x1)', 'x142 = NAND(x5, x63)', 'x141 = NAND(x30, x1)', 'x144 = NAND(x63, x31)', 'x143 = NAND(x33, x1)', 'x146 = NAND(x63, x32)', 'x145 = NAND(x30, x1)', 'x148 = NAND(x3, x63)', 'x147 = NAND(x33, x1)']
mm = ['x64 = OR(x65, x28)', 'x66 = OR(x67, x31)', 'x68 = OR(x69, x26, x32, x33)', 'x69 = NOT(x30)', 'x71 = OR(x72, x27)', 'x73 = NOR(x74, x34)', 'x75 = AND(x76, x34)', 'x58 = NAND(x72, x78)', 'x56 = NAND(x72, x80)', 'x36 = NAND(x81, x82, x83)', 'x37 = NAND(x84, x85, x86)', 'x38 = NAND(x87, x88, x89)', 'x39 = NAND(x90, x91, x92)', 'x40 = NAND(x93, x94, x95)', 'x41 = NAND(x96, x97, x98)', 'x42 = NAND(x99, x100, x101)', 'x43 = NAND(x102, x103, x104)', 'x44 = NAND(x105, x106)', 'x45 = NAND(x107, x108)', 'x46 = NAND(x109, x110)', 'x35 = NAND(x111, x112, x113)', 'x63 = NOT(x5)', 'x114 = NOT(x29)', 'x115 = NOT(x8)', 'x116 = NOT(x7)', 'x117 = NOT(x6)', 'x65 = NAND(x67, x26)', 'x72 = NAND(x5, x29)', 'x76 = NAND(x71, x123, x124)', 'x62 = NAND(x125, x126)', 'x61 = NAND(x127, x128)', 'x60 = NAND(x129, x130)', 'x59 = NAND(x131, x132)', 'x57 = NAND(x133, x134)', 'x55 = NAND(x135, x136)', 'x54 = NAND(x137, x138)', 'x53 = NAND(x139, x140)', 'x52 = NAND(x141, x142)', 'x51 = NAND(x143, x144)', 'x50 = NAND(x145, x146)', 'x49 = NAND(x147, x148)', 'x48 = NAND(x149, x150)', 'x47 = NAND(x151, x152)', 'x67 = NOT(x33)', 'x123 = NAND(x155, x34)', 'x78 = NAND(x1, x63)', 'x80 = NAND(x63, x27)', 'x155 = OR(x27, x28, x31, x32)', 'x159 = NOT(x123)', 'x161 = NAND(x68, x66, x64)', 'x124 = NAND(x114, x161, x5)', 'x74 = NOT(x76)', 'x110 = NAND(x74, x17)', 'x109 = NAND(x73, x14)', 'x108 = NAND(x74, x16)', 'x107 = NAND(x73, x13)', 'x106 = NAND(x74, x15)', 'x105 = NAND(x73, x12)', 'x103 = NAND(x75, x17)', 'x102 = NAND(x74, x14)', 'x104 = NAND(x73, x11)', 'x100 = NAND(x75, x16)', 'x99 = NAND(x74, x13)', 'x101 = NAND(x73, x10)', 'x97 = NAND(x75, x15)', 'x96 = NAND(x74, x12)', 'x98 = NAND(x73, x9)', 'x94 = NAND(x75, x14)', 'x93 = NAND(x74, x11)', 'x95 = NAND(x73, x8)', 'x91 = NAND(x75, x13)', 'x90 = NAND(x74, x10)', 'x92 = NAND(x73, x7)', 'x88 = NAND(x75, x12)', 'x87 = NAND(x74, x9)', 'x89 = NAND(x73, x6)', 'x85 = NAND(x67, x114, x73)', 'x84 = NAND(x75, x11)', 'x86 = NAND(x74, x8)', 'x82 = NAND(x65, x114, x73)', 'x81 = NAND(x75, x10)', 'x83 = NAND(x74, x7)', 'x234 = OR(x26, x33)', 'x235 = NAND(x114, x234)', 'x112 = NAND(x73, x235)', 'x111 = NAND(x75, x9)', 'x113 = NAND(x74, x6)', 'x126 = NAND(x2, x63)', 'x125 = NAND(x5, x33)', 'x128 = NAND(x63, x32)', 'x127 = NAND(x5, x30)', 'x130 = NAND(x63, x31)', 'x129 = NAND(x5, x33)', 'x132 = NAND(x4, x63)', 'x131 = NAND(x5, x30)', 'x134 = NAND(x63, x28)', 'x133 = NAND(x5, x26)', 'x136 = NAND(x3, x63)', 'x135 = NAND(x5, x26)', 'x138 = NAND(x63, x25)', 'x137 = NAND(x5, x21)', 'x140 = NAND(x63, x24)', 'x139 = NAND(x5, x20)', 'x142 = NAND(x63, x23)', 'x141 = NAND(x5, x19)', 'x144 = NAND(x63, x22)', 'x143 = NAND(x5, x18)', 'x146 = NAND(x123, x21)', 'x145 = NAND(x159, x6, x7, x8)', 'x148 = NAND(x123, x20)', 'x147 = NAND(x116, x117, x159, x8)', 'x150 = NAND(x123, x19)', 'x149 = NAND(x115, x117, x159, x7)', 'x152 = NAND(x123, x18)', 'x151 = NAND(x115, x116, x159, x6)']


outtoto = ['x7', 'x8', 'x9', 'x10', 'x11', 'x2', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x19']
eccheccazzo = ['x20 = AND(x21, x22)', 'x14 = NAND(x20, x24)', 'x13 = NAND(x25, x26, x27, x28)', 'x12 = NAND(x29, x30)', 'x16 = NAND(x31, x32, x33, x34)', 'x15 = NAND(x35, x36, x37)', 'x18 = NAND(x1, x38, x20)', 'x17 = NAND(x27, x41)', 'x19 = NAND(x42, x43)', 'x44 = AND(x4, x5, x6)', 'x45 = NOT(x5)', 'x46 = NOT(x1)', 'x28 = NAND(x1, x5)', 'x48 = NOT(x4)', 'x49 = NOT(x6)', 'x32 = OR(x4, x6)', 'x36 = NAND(x45, x48, x6)', 'x54 = NOT(x28)', 'x27 = NAND(x49, x45, x46, x4)', 'x60 = NOT(x32)', 'x62 = NOT(x36)', 'x41 = NAND(x54, x4)', 'x38 = NAND(x4, x5)', 'x67 = OR(x5, x6)', 'x24 = NAND(x46, x67)', 'x30 = NAND(x62, x46)', 'x29 = NAND(x24, x4)', 'x26 = NAND(x1, x48, x6)', 'x25 = NAND(x60, x5)', 'x43 = NAND(x46, x60, x5)', 'x42 = OR(x3, x44)', 'x37 = NAND(x54, x49)', 'x35 = NAND(x24, x4)', 'x90 = NAND(x1, x49)', 'x31 = NAND(x4, x6)', 'x22 = NAND(x60, x45)', 'x21 = NAND(x5, x6)', 'x34 = NAND(x1, x45)', 'x33 = NAND(x90, x5)']
mamma = ['x20 = OR(x21, x1)', 'x22 = AND(x23, x24)', 'x14 = NAND(x22, x26)', 'x13 = NAND(x27, x28, x29, x30)', 'x12 = NAND(x31, x20)', 'x16 = NAND(x33, x34, x35, x36)', 'x15 = NAND(x37, x21, x39)', 'x18 = NAND(x1, x40, x22)', 'x17 = NAND(x30, x43)', 'x19 = NAND(x44, x45)', 'x46 = AND(x4, x5, x6)', 'x47 = NOT(x5)', 'x48 = NOT(x1)', 'x29 = NAND(x1, x5)', 'x50 = NOT(x4)', 'x51 = NOT(x6)', 'x34 = OR(x4, x6)', 'x21 = NAND(x47, x50, x6)', 'x30 = NAND(x51, x47, x48, x4)', 'x60 = NOT(x34)', 'x62 = NOT(x29)', 'x43 = NAND(x62, x4)', 'x40 = NAND(x4, x5)', 'x67 = OR(x5, x6)', 'x26 = NAND(x48, x67)', 'x31 = NAND(x26, x4)', 'x28 = NAND(x1, x50, x6)', 'x27 = NAND(x60, x5)', 'x45 = NAND(x48, x60, x5)', 'x44 = OR(x3, x46)', 'x39 = NAND(x62, x51)', 'x37 = NAND(x26, x4)', 'x87 = NAND(x1, x51)', 'x33 = NAND(x4, x6)', 'x24 = NAND(x60, x47)', 'x23 = NAND(x5, x6)', 'x36 = NAND(x1, x47)', 'x35 = NAND(x87, x5)']

# Example usage with your list of equations:
equations = ['x12 = NOT(x13)', 'x13 = NAND(x15, x5, x6)', 'x10 = NAND(x16, x17, x18, x19)', 'x9 = NAND(x20, x21, x22)', 'x23 = OR(x2, x1)', 'x15 = NOT(x4)', 'x25 = NOT(x5)', 'x26 = NOT(x2)', 'x27 = NOT(x1)', 'x28 = NOT(x6)', 'x29 = NAND(x28, x5)', 'x11 = NAND(x31, x32)', 'x8 = NAND(x33, x34)', 'x35 = NAND(x36, x37)', 'x38 = NAND(x1, x2)']
result = ultimate_function(equations, mom, out1, out1, phis)

print('Cmon')