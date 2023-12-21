# Gcode module

#### GCode class:
```python
    gcode = GCodeList()
```

#### Open file:
```python
    gcode = GCodeList(
        codes=[
             GCodeFileLoader('./file.gcode')
        ]
    )
```

#### Save file:
```python
    gcode.saveToFile('./file.gcode')
```

#### Create gcode:
```python
    gcode = GCodeList(
        codes=[
            LinearInterpolation(z='15', speed='1000'),
            LinearInterpolation(x='0', y='0', speed='1000'),
            LinearInterpolation(z='0', speed='1000'),
        ]
    )
```

#### Merge gcode:
```python
    gcode1 = GCodeList([GCodeFileLoader('./file1.gcode')])
    gcode2 = GCodeList([GCodeFileLoader('./file2.gcode')])

    merge = GCodeList(
        codes=[
            gcode1,
            gcode2
        ]
    )
```

#### Bunch gcode:
```python
    gcode = GCodeList([GCodeFileLoader('./file.gcode')])

    bunch = GCodeList(
        codes=[
            GCodeBunch(
                gcode.getBunch(0, 100)
            )
        ]
    )

    bunch.saveToFile('./bunch.gcode')
```
