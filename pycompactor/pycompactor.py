#!/usr/bin/env python3 
import json
import sys
    

def __compact_v_0_1(value):
    types = []
    type_to_idx = {}
    __simpletypes = [str, int, float]
    def __register_type(keys):
        sorted_keys = sorted(keys)
        sorted_keys_str = ':'.join(sorted_keys)
        if sorted_keys_str not in type_to_idx:
            types.append(sorted_keys)
            type_to_idx[sorted_keys_str] = len(types) - 1
        return type_to_idx[sorted_keys_str], sorted_keys

    def __serialize(v):
        if v is None: 
            return None
        elif isinstance(v, dict):
            type_id, keys = __register_type(v.keys())
            return [type_id] + [__serialize(v[k]) for k in keys]
        elif isinstance(v, list):
            return [-1] + [__serialize(v2) for v2 in v]
        elif any([isinstance(v, t) for t in __simpletypes]): # for debug purposes?
            return v
        else:
            raise Exception('Data type %s is not supported' % (type(v),))
      
    return {
        "v": __VERSION_0_1,
        "t": types,
        "d": __serialize(value)
    }


def __uncompact_v_0_1(value):
    types = value['t']
    def __deserialize(v):
        if isinstance(v, list):
            if not isinstance(v[0], int):
                raise Exception('First array element expected to be typeid, but found %s' % (type(v[0]),))
            if v[0] == -1:
                return [__deserialize(vv) for vv in v[1:]]
            elif v[0] < len(types):
                typeinfo = types[v[0]]
                return {typeinfo[idx - 1]: __deserialize(v[idx]) for idx in range(1, len(v))}
            else:
                raise Exception('Type id %d is not found. Total count of types: %d' % (v[0], len(types)))
        else:
          return v
    return __deserialize(value['d'])


__VERSION_0_1 = '0.1'
__PACKERS = {
    __VERSION_0_1: (__compact_v_0_1, __uncompact_v_0_1)
}


def pack(value, version = __VERSION_0_1):
    if version not in __PACKERS:
        raise Exception('Version %s is not available for packing. Supported versions: %s' % (version, ', '.join(__PACKERS.keys())))
    return __PACKERS[version][0](value)


def depack(value):
    if value['v'] not in __PACKERS:
        raise Exception('Unpacker for version %s is not available. Supported versions: %s' % (value['v'], ', '.join(__PACKERS.keys())))
    return __PACKERS[value['v']][1](value)


def __main(path):
    
    with open(path, 'r') as f: 
        data = json.load(f)

    source_size = len(json.dumps(data))
    compacted_data = pack(data)
    types = json.dumps(compacted_data['t'])
    c_data = json.dumps(compacted_data['d'])
    c_all = json.dumps(compacted_data)

    print('Compression. Type system: %d, data: %d. Total: %d, Source: %d. Compaction: %f' % (len(types), len(c_data), len(c_all), source_size, (100.*len(c_all))/source_size))

    print('Uncompressed data size: %d' % (len(json.dumps(depack(json.loads(c_all)))),))


if __name__ == '__main__':
    __main(sys.argv[1])
