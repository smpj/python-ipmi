#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import eq_, ok_, raises

from pyipmi.errors import DecodingError
from pyipmi.sdr import (SdrCommon, SdrFullSensorRecord, SdrCompactSensorRecord,
                        SdrEventOnlySensorRecord, SdrFruDeviceLocator,
                        SdrManagementControllerDeviceLocator)


def test_convert_complement():
    eq_(SdrFullSensorRecord()._convert_complement(0x8, 4), -8)
    eq_(SdrFullSensorRecord()._convert_complement(0x80, 8), -128)
    eq_(SdrFullSensorRecord()._convert_complement(0x8000, 16), -32768)


def test__decode_capabilities():
    record = SdrFullSensorRecord()

    record._decode_capabilities(0)
    ok_('ignore_sensor' not in record.capabilities)
    ok_('auto_rearm' not in record.capabilities)
    ok_('hysteresis_not_supported' in record.capabilities)
    ok_('threshold_not_supported' in record.capabilities)

    record._decode_capabilities(0x80)
    ok_('ignore_sensor' in record.capabilities)
    ok_('auto_rearm' not in record.capabilities)
    ok_('hysteresis_not_supported' in record.capabilities)
    ok_('threshold_not_supported' in record.capabilities)

    record._decode_capabilities(0x40)
    ok_('ignore_sensor' not in record.capabilities)
    ok_('auto_rearm' in record.capabilities)
    ok_('hysteresis_not_supported' in record.capabilities)
    ok_('threshold_not_supported' in record.capabilities)

    record._decode_capabilities(0x30)
    ok_('ignore_sensor' not in record.capabilities)
    ok_('auto_rearm' not in record.capabilities)
    ok_('hysteresis_fixed' in record.capabilities)
    ok_('threshold_not_supported' in record.capabilities)

    record._decode_capabilities(0x0c)
    ok_('ignore_sensor' not in record.capabilities)
    ok_('auto_rearm' not in record.capabilities)
    ok_('hysteresis_not_supported' in record.capabilities)
    ok_('threshold_fixed' in record.capabilities)


@raises(DecodingError)
def test_sdrcommon_invalid_data_length():
    data = (0x00, 0x01, 0x02, 0x03)
    SdrCommon(data)


def test_sdrcommon_object():
    data = (0x00, 0x01, 0x02, 0x03, 0x04)
    sdr = SdrCommon(data)
    eq_(sdr.id, 0x0100)
    eq_(sdr.version, 0x02)
    eq_(sdr.type, 0x03)
    eq_(sdr.length, 0x04)


@raises(DecodingError)
def test_sdrfullsensorrecord_invalid_length():
    data = (0, 0, 0, 0, 0)
    SdrFullSensorRecord(data)


@raises(DecodingError)
def test_sdrfullsensorrecord_linearization_key_error():
    sdr = SdrFullSensorRecord(None)
    sdr.linearization = 12
    sdr.l(1)


def test_sdrfullsensorrecord_linearization():
    sdr = SdrFullSensorRecord(None)

    # linear
    sdr.linearization = 0
    eq_(sdr.l(1), 1)
    eq_(sdr.l(10), 10)

    # ln
    sdr.linearization = 1
    eq_(sdr.l(1), 0)

    # log
    sdr.linearization = 2
    eq_(sdr.l(10), 1)
    eq_(sdr.l(100), 2)

    # log
    sdr.linearization = 3
    eq_(sdr.l(8), 3)
    eq_(sdr.l(16), 4)

    # e
    sdr.linearization = 4
    eq_(sdr.l(1), 2.718281828459045)

    # exp10
    sdr.linearization = 5
    eq_(sdr.l(1), 10)
    eq_(sdr.l(2), 100)

    # exp2
    sdr.linearization = 6
    eq_(sdr.l(3), 8)
    eq_(sdr.l(4), 16)

    # 1/x
    sdr.linearization = 7
    eq_(sdr.l(2), 0.5)
    eq_(sdr.l(4), 0.25)

    # sqr
    sdr.linearization = 8
    eq_(sdr.l(2), 4)

    # cube
    sdr.linearization = 9
    eq_(sdr.l(2), 8)
    eq_(sdr.l(3), 27)

    # sqrt
    sdr.linearization = 10
    eq_(sdr.l(16), 4)

    # cubert
    sdr.linearization = 11
    eq_(sdr.l(8), 2)
    eq_(sdr.l(27), 3)


@raises(DecodingError)
def test_sdrcompactsensorrecord():
    data = (0, 0, 0, 0, 0)
    SdrCompactSensorRecord(data)


@raises(DecodingError)
def test_sdreventonlysensorrecord():
    data = (0, 0, 0, 0, 0)
    SdrEventOnlySensorRecord(data)


@raises(DecodingError)
def test_sdrfrudevicelocator():
    data = (0, 0, 0, 0, 0)
    SdrFruDeviceLocator(data)


@raises(DecodingError)
def test_sdrmanagementcontollerdevicelocator():
    data = (0, 0, 0, 0, 0)
    SdrManagementControllerDeviceLocator(data)
