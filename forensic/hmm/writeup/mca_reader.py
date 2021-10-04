"""Code to read .mca region files

I modified the javascript library mca-js to create this file.
mca-js: https://github.com/thejonwithnoh/mca-js

This is largely just a python interpretation of that script.
-----------
MIT License

Copyright (c) 2019 Nicholas Westerhausen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import gzip
import zlib


class Mca:
    """Class used to read Minecraft region files and the chunk information contained within.

    Use by creating a new object with the filepath for the region file. Then you can get_timestamp and get_data
    for individual chunks in the region by specifying the chunkX or chunkY if they were to always go from 0 to 32
    for each region.

    region = Mca('/opt/mc/region/r.1.1.mca')
    nbt = region.get_data(0,0)  # gets the raw nbt data for chunk 0,0
    # here you can do stuff with that nbt data. It is the same format as if you open('level.dat','r+b)
    """
    SECTOR_OFFSET_SIZE = 3  # Chunk offset is a 3-byte value
    SECTOR_COUNT_SIZE = 1  # Chunk size is a 1-byte value
    TIMESTAMP_SIZE = 4  # Timestamp is a 4-byte value
    DATA_SIZE_SIZE = 4  # First 4 bytes of the chunk data are its size
    COMPRESSION_TYPE_SIZE = 1  # Compression type is a single byte
    DIMENSION_SIZE_POWER = 5  # Used for bit shifting (2**5 = 32), 32 x or z values
    DIMENSION_COUNT = 2  # There is only the X and Z dimension for the chunks.
    SECTOR_SIZE_POWER = 12  # Used for bit shifting (2**12 = 4096), 4096 per sector of the file
    SECTOR_DETAILS_SIZE = SECTOR_OFFSET_SIZE + SECTOR_COUNT_SIZE  # Full size of the chunk details (4 bytes)
    DATA_HEADER_SIZE = DATA_SIZE_SIZE + COMPRESSION_TYPE_SIZE  # Full size of the chunk header (5 bytes)
    DIMENSION_SIZE = 1 << DIMENSION_SIZE_POWER  # Used for bitwise operations on the provided chunk x and z values
    DIMENSION_SIZE_MASK = DIMENSION_SIZE - 1  # DIM_SIZE = 0b100000, MASK = -0b11111 and used for bitwise operations
    INDEX_COUNT = DIMENSION_SIZE * DIMENSION_COUNT  # How many indexes (32 * 2 = 64)
    HEADER_SIZE = SECTOR_DETAILS_SIZE + INDEX_COUNT  # 64 indexes + 4 byte details = 68
    SECTOR_SIZE = 1 << SECTOR_SIZE_POWER  # 4096 bytes
    # Compression types
    COMPRESSION_GZIP = 1
    COMPRESSION_ZLIB = 2

    def __init__(self, filepath):
        """Given a filename, returns an object to reference region file data.

        We open the file as a binary file. Once you instantiate an object using this class,
        you are likely to call get_data(chunkX, chunkZ) or get_timestamp(chunkX, chunkZ).
        We frequently pass chunkX, chunkZ as *args in this Class.

        filepath: full path to the region file (e.g. /opt/mc/region/r.1.1.mca)"""
        self.data = open(filepath, 'r+b')

    def get_index(self, *args):
        """Get the index for the chunk

        This computes the index to locate both the chunk timestamp and size in the
        size and timestamp tables at the beginning of the region file.

        See https://minecraft.gamepedia.com/Region_file_format#Structure"""
        index = 0
        for dimension in range(self.DIMENSION_COUNT):
            index |= (args[dimension] & self.DIMENSION_SIZE_MASK) << dimension * self.DIMENSION_SIZE_POWER
        return index

    def get_sector_offset_offset(self, *args):
        """Get the offset for the offset of the sector.

        Returns the offset for the three-byte offset in 4KiB sectors from the start of the file
        where the chunk data is stored.

        See https://minecraft.gamepedia.com/Region_file_format#Chunk_location"""
        return self.get_index(*args) * self.SECTOR_DETAILS_SIZE

    def get_sector_count_offset(self, *args):
        """Return the offset for the size of the chunk.

         Returns the offset for the byte which gives the length of the chunk (in 4KiB sectors, rounded up).

        See https://minecraft.gamepedia.com/Region_file_format#Chunk_location"""
        return self.get_sector_offset_offset(*args) + self.SECTOR_OFFSET_SIZE

    def get_timestamp_offset(self, *args):
        """Return the offset for the last modification of the chunk.

         Returns the offset for the 4 bytes which gives the timestamp of last modification for the chunk.

        See https://minecraft.gamepedia.com/Region_file_format#Chunk_timestamps"""
        return self.get_index(*args) * self.TIMESTAMP_SIZE + self.HEADER_SIZE

    def get_sector_offset(self, *args):
        """Return the sector offset value.

        Uses the earlier-defined function to seek appropriately in the file, and then it will return an int representing
        how many 4096 byte offsets from the start of the file the chunk is at."""
        offset = self.get_sector_offset_offset(*args)
        self.data.seek(offset, 0)
        return int.from_bytes(self.data.read(self.SECTOR_OFFSET_SIZE), 'big')

    def get_data_offset(self, *args):
        """Return the byte offset for the chunk.

        Basically multiplies the sector offset value by 4096. But we do it with bitshifting. This value is the location
        of where the chunk data begins."""
        return self.get_sector_offset(*args) << self.SECTOR_SIZE_POWER

    def get_sector_count(self, *args):
        """Return the sector size value.

        Uses the earlier-defined function to seek appropriately in the file, and then it will return an int representing
        how many 4096 bytes the chunk data occupies."""
        offset = self.get_sector_count_offset(*args)
        self.data.seek(offset)
        return int.from_bytes(self.data.read(self.SECTOR_COUNT_SIZE), 'big')

    def get_timestamp(self, *args):
        """Return the last modified timestamp.

        Seeks using the timestamp_offset and returns the timestamp as an int"""
        offset = self.get_timestamp_offset(*args)
        self.data.seek(offset, 0)
        return int.from_bytes(self.data.read(self.TIMESTAMP_SIZE), 'big')

    def get_data_size(self, *args):
        """Return the byte size for the chunk.

        The first 4 bytes of the chunk data is the byte-length of the chunk data. We return that as an int.

        See https://minecraft.gamepedia.com/Region_file_format#Chunk_data"""
        offset = self.get_data_offset(*args)
        self.data.seek(offset, 0)
        return int.from_bytes(self.data.read(self.DATA_SIZE_SIZE), 'big')

    def get_compression_type(self, *args):
        """Return the compression type for the chunk.

        This value is either 1 or 2 for GZip or Zlib respectively"""
        offset = self.get_data_offset(*args) + self.DATA_SIZE_SIZE
        self.data.seek(offset, 0)
        return int.from_bytes(self.data.read(self.COMPRESSION_TYPE_SIZE), 'big')

    def get_data(self, *args):
        """Returns NBT data for the chunk specified by x and z in *args.

        We get the start location of the chunk data. If that is valid, we skip the 4-byte header and read the size
        learned from get_data_size. Based on the compression type, we either gzip or zlib decompress the data."""
        datastart = self.get_data_offset(*args)
        if datastart != 0:
            payloadstart = datastart + self.DATA_HEADER_SIZE
            payloadsize = self.get_data_size(*args)
            self.data.seek(payloadstart, 0)
            payload = self.data.read(payloadsize)
            compressiontype = self.get_compression_type(*args)
            if compressiontype == self.COMPRESSION_GZIP:
                return gzip.decompress(payload)
            elif compressiontype == self.COMPRESSION_ZLIB:
                return zlib.decompress(payload)
