// Box.asm  -  K = 48
// Box: starts at row 48, 20 rows tall, 16 px (1 word) wide, left edge.
// Start address = SCREEN + 32*48 = 16384 + 1536 = 17920
// Key pressed -> black box; key released -> box erased.

(MAIN)
    @KBD
    D=M
    @BLACK
    D;JNE           // key pressed -> use -1
    @val
    M=0             // no key -> use 0 (white)
    @DRAW
    0;JMP
(BLACK)
    @val
    M=-1            // all 16 bits black
(DRAW)
    @17920
    D=A
    @addr
    M=D             // addr = first word of row 48
    @20
    D=A
    @count
    M=D             // count = 20 rows
(ROW)
    @val
    D=M
    @addr
    A=M
    M=D             // RAM[addr] = val
    @32
    D=A
    @addr
    M=D+M           // next row (+32 words)
    @count
    MD=M-1
    @ROW
    D;JGT           // repeat until 20 rows done
    @MAIN
    0;JMP