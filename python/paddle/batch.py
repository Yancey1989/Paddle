# Copyright (c) 2016 PaddlePaddle Authors. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__all__ = ['batch']


def batch(reader, batch_size, drop_last=False, num_devices=1):
    """
    Create a batched reader.

    :param reader: the data reader to read from.
    :type reader: callable
    :param batch_size: size of each mini-batch
    :type batch_size: int
    :param drop_last: drop the last batch, if the size of last batch is not equal to batch_size.
    :type drop_last: bool
    :param num_devices: Align the size of each mini-batch on each devices.
    :type num_devices: int
    :return: the batched reader.
    :rtype: callable
    """

    def batch_reader():
        r = reader()
        b = []
        for instance in r:
            b.append(instance)
            if len(b) == batch_size:
                yield b
                b = []
        if drop_last == False and len(b) != 0:
            yield b

    # Batch size check
    batch_size = int(batch_size)
    if batch_size <= 0:
        raise ValueError("batch_size should be a positive integeral value, "
                         "but got batch_size={}".format(batch_size))

    def multi_devices_batch_reader():
        r = batch_reader()
        multi_devices_batch = []
        for batch in r:
            multi_devices_batch.append(batch)
            if len(multi_devices_batch) == num_devices:
                for b in multi_devices_batch:
                    yield b
                multi_devices_batch = []

    return multi_devices_batch_reader if num_devices > 1 else batch_reader
