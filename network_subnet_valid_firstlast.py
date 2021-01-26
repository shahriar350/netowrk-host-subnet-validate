# network = input("enter network id: ")
# subnet = list(map(int,input("enter subnet id: ").split('.')))
from prettytable import PrettyTable


def dec_to_bin(x):
    return int(bin(x)[2:])


def bin_to_dec(n):
    return bin(n).replace("0b", "")


x = PrettyTable()
is_cidr = input('is you network include CIDR? Y/n: ')

if is_cidr == 'Y':
    print("Example of network: 172.168.12.0/24 ")
    net = input("Enter your network id: ").split('/')
    network = net[0].split(".")
    a = ''
    subnet = []
    for i in range(0, 32):
        if i < int(net[1]):
            a += '1'
        else:
            a += '0'
    for aloop in range(0, 32, 8):
        temp = ''
        for j in range(0, 8):
            temp += a[aloop]
            aloop += 1
        subnet.append((int(temp, 2)))
else:
    network = input("Enter your network id: ").split(".")
    subnet = list(map(int,input("Enter your subnet id: ").split(".")))

for i in subnet:
    if i > 255:
        raise ValueError("Please enter a valid subnet mask")

if 1 <= int(network[0]) <= 127:
    print("Network is A group member")
elif 128 < int(network[0]) <= 191:
    print("Network is B group member")
elif 192 < int(network[0]) <= 223:
    print("Network is C group member")

block_size = 0
sub_bin_only_cidr = []
for i in subnet:
    if i < 255:
        if block_size == 0:
            block_size = 256 - i
        sub_bin_only_cidr.append(dec_to_bin(i))
zero = 0
one = 0
for i in sub_bin_only_cidr:
    for j in str(i):
        if j == '1':
            one += 1
        elif j == '0':
            zero += 1

total_subnet = 2 ** one
total_host = 2 ** zero
total_valid_host = total_host - 2

print(f'total block size: {block_size}')
print(f'total number of subnet/network is: {total_subnet}')
print(f'total host is: {total_host}')
print(f'total valid host is: {total_valid_host}')
current_subnet = 0
fast_valid_host = current_subnet + 1
calculate = [{"subnet_id": current_subnet, "first_valid_host": fast_valid_host}]

for i in range(0, total_subnet - 1):
    current_subnet += block_size
    fast_valid_host = current_subnet + 1
    calculate.append({"subnet_id": current_subnet, "first_valid_host": fast_valid_host})

for i in range(0, total_subnet):
    if i == total_subnet - 1:
        # print(len(str(total_subnet)))
        broadcast = 255
    else:
        broadcast = calculate[i + 1].get("subnet_id") - 1
    last_valid_host = broadcast - 1
    calculate[i]["last_valid_id"] = last_valid_host
    calculate[i]["broadcast_address"] = broadcast

x.field_names = ["Subnet id", "First valid host", "Last valid id", "Broadcast address"]

for i in calculate:
    x.add_row(i.values())
print(x)
