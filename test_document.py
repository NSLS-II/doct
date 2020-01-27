import time as ttime
import datetime
import uuid
import pytest

from doct import Document, pretty_print_time, DocumentIsReadOnly, ref_doc_to_uid


# some useful globals
run_start_uid = None
document_insertion_time = None
descriptor_uid = None
run_stop_uid = None


def _syn_data_helper():
    src_str = 'ABCDEFGHI'
    dd = {k: ord(k) for k in src_str}
    doc_test = Document('testing', dd)
    return src_str, dd, doc_test


def test_doc_plain():
    src_str, dd, doc_test = _syn_data_helper()
    "testing" == doc_test._name

    assert len(src_str) == len(doc_test)

    assert set(doc_test.keys()) == set(dd.keys())
    for k in doc_test:
        assert doc_test[k] == ord(k)
        assert dd[k] == doc_test[k]
        assert getattr(doc_test, k) == doc_test[k]
        assert k in doc_test

    for k, v in doc_test.items():
        assert v == ord(k)

    assert set(dd.values()) == set(doc_test.values())


def test_doc_descructive_pop():
    src_str, dd, doc_test = _syn_data_helper()
    k = next(doc_test.keys())
    with pytest.raises(DocumentIsReadOnly):
        doc_test.pop(k)


def test_doc_descructive_del():
    src_str, dd, doc_test = _syn_data_helper()
    k = next(doc_test.keys())
    with pytest.raises(DocumentIsReadOnly):
        del doc_test[k]


def test_doc_descructive_delattr():
    src_str, dd, doc_test = _syn_data_helper()
    k = next(doc_test.keys())
    with pytest.raises(DocumentIsReadOnly):
        delattr(doc_test, k)


def test_doc_descructive_setitem():
    src_str, dd, doc_test = _syn_data_helper()
    k = next(doc_test.keys())
    with pytest.raises(DocumentIsReadOnly):
        doc_test[k] = "aardvark"


def test_doc_descructive_setattr():
    src_str, dd, doc_test = _syn_data_helper()
    k = next(doc_test.keys())
    with pytest.raises(DocumentIsReadOnly):
        setattr(doc_test, k, "aardvark")


def test_doc_descructive_update():
    src_str, dd, doc_test = _syn_data_helper()
    with pytest.raises(DocumentIsReadOnly):
        doc_test.update(dd)


def test_getattr_fail():
    src_str, dd, doc_test = _syn_data_helper()
    with pytest.raises(AttributeError):
        getattr(doc_test, "aardavark")


def test_html_smoke():
    pytest.importorskip('jinja2')
    src_str, dd, doc_test = _syn_data_helper()

    doc_test._repr_html_()


def test_str_smoke():
    d = {'data_keys': {k: {'source': k,
                           'dtype': 'number',
                           'shape': None} for k in 'ABCEDEFHIJKL'},
         'uid': str(uuid.uuid4()), }
    d = Document('desc', d)
    a = Document('animal', {'uid': str(uuid.uuid4()),
                            'animal': 'arrdvark',
                            'food': {'ants': 'great',
                                     'beef': 'bad'}})
    b = Document('zoo', {'name': 'BNL Zoo',
                         'prime_attraction': a,
                         'descriptors': [d, d]})

    str(b)


def test_round_trip():
    src_str, dd, doc_test = _syn_data_helper()
    name, doc_dict = doc_test.to_name_dict_pair()
    assert name == doc_test["_name"]
    assert name == doc_test._name
    assert dd == doc_dict
    new_doc = Document(name, doc_dict)
    assert doc_test == new_doc


def test_ref_to_uid():
    a = Document("animal", {"uid": str(uuid.uuid4()), "animal": "arrdvark"})
    b = Document("zoo", {"name": "BNL Zoo", "prime_attraction": a})
    b2 = ref_doc_to_uid(b, "prime_attraction")
    assert b2["prime_attraction"] == a["uid"]
    assert b["prime_attraction"] == a


def test_pprint_time():
    offset_seconds = 50
    target = "{off} seconds ago ({dt})"
    test = ttime.time() - offset_seconds
    res = pretty_print_time(test)

    dt = datetime.datetime.fromtimestamp(test).isoformat()
    expt = target.format(off=offset_seconds, dt=dt)
    assert res == expt


def test_forgiving_pprint_time():
    ts = "20200124-185311"
    # this should not raise
    assert ts == pretty_print_time(ts)


def test_forgiving_pprint_time2():
    ts = {"time": "20200124-185311"}
    # this should not raise
    assert ts == pretty_print_time(ts)
