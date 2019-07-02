# sframe-compressor
This is an internal tool to compress SFrames into the .TEJAS format.

## Getting Started

Download the repo.

```bash 
git clone https://github.com/vitae-gravitas/sframe-compressor.git
```

To **compress**, run `compress.py` with the required options. Note that the input directory should include SFrames only.
```bash
python compress.py -s [INPUT DIRECTORY PATH] -o [OUTPUT DIRECTORY PATH]
```

To **decompress**, run `dcompress.py` with the required options. Note that the input directory should include .TEJAS files only.
```bash
python compress.py -t [INPUT DIRECTORY PATH] -o [OUTPUT DIRECTORY PATH]
```

## Tips
Don't try to further compress the .TEJAS folder! This will not aid in further downsizing.
