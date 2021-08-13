# araviscam
FLIR Blackfly S GigE camera reader for SDSS-V LVM telescope

## Purpose
A python class subclassed from [sdss/basecam](https://github.com/sdss/basecam) to read monochrome images of [FLIR](https://www.flir.com) Blackfly S GigE cameras.
It uses the [Aravis](https://github.com/AravisProject/aravis) C-library which is an interface to [GenICam](https://www.emva.org/standards-technology/genicam/) cameras. As such it might also be used to read a more general class of GenICam cameras.

Developped for the guider of the Local Volume Mapper (LVM) of the 5th generation of the telescopes of the [Sloan Digital Sky survey](https://en.wikipedia.org/wiki/Sloan_Digital_Sky_Survey) (SDSS-V).

## See Also

* [this project](https://github.com/sdss/araviscam)
* [baslerCam](https://github.com/sdss/baslercam)
* [mantacam](https://github.com/sdss/mantacam)
* [flicamera](https://github.com/sdss/flicamera)
