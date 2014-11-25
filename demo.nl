package math {

alias real float

const real pi = 3.141592653589793
const real e = 2.718281828459045

func int (int x, int y) pow {
    return x ^ y
}

func real (real deg) radians {
    return deg * pi / 180
}

func real (real rad) degrees {
    return rad * 180 / pi
}

}
