import proto_map

proto = proto_map.Proto_map(3, 4)

for t in proto.all_territories:
    print(str(t))

print("Proto map complete")

