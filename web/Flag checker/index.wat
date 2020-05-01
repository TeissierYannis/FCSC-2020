(module
  (type $t0 (func (param i32) (result i32))) # $t0 2 params : int 32 bits, int 32 bits
  (type $t1 (func)) // $t1 pas de params
  (type $t2 (func (param i32))) // $t2 1 param : int 32 bits
  (type $t3 (func (result i32))) // t3 1 param : int 32 bits
  (import "a" "memory" (memory $a.memory 256 256)) 
  (func $e (export "e") (type $t2) (param $p0 i32)
    (global.set $g0
      (local.get $p0)))
  (func $d (export "d") (type $t0) (param $p0 i32) (result i32)
    (global.set $g0
      (local.tee $p0
        (i32.and
          (i32.sub
            (global.get $g0)
            (local.get $p0))
          (i32.const -16))))
    (local.get $p0))
  (func $c (export "c") (type $t3) (result i32)
    (global.get $g0))
  (func $f3 (type $t0) (param $p0 i32) (result i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    (local.set $l3
      (i32.const 70))
    (local.set $l1
      (i32.const 1024))
    (block $B0
      (br_if $B0
        (i32.eqz
          (local.tee $l2
            (i32.load8_u
              (local.get $p0)))))
      (loop $L1
        (block $B2
          (br_if $B2
            (i32.ne
              (local.get $l2)
              (local.tee $l4
                (i32.load8_u
                  (local.get $l1)))))
          (br_if $B2
            (i32.eqz
              (local.tee $l3
                (i32.add
                  (local.get $l3)
                  (i32.const -1)))))
          (br_if $B2
            (i32.eqz
              (local.get $l4)))
          (local.set $l1
            (i32.add
              (local.get $l1)
              (i32.const 1)))
          (local.set $l2
            (i32.load8_u offset=1
              (local.get $p0)))
          (local.set $p0
            (i32.add
              (local.get $p0)
              (i32.const 1)))
          (br_if $L1
            (local.get $l2))
          (br $B0)))
      (local.set $l5
        (local.get $l2)))
    (i32.sub
      (i32.and
        (local.get $l5)
        (i32.const 255))
      (i32.load8_u
        (local.get $l1))))
  (func $b (export "b") (type $t0) (param $p0 i32) (result i32)
    (local $l1 i32) (local $l2 i32)
    (if $I0
      (local.tee $l2
        (i32.load8_u
          (local.get $p0)))
      (then
        (local.set $l1
          (local.get $p0))
        (loop $L1
          (i32.store8
            (local.get $l1)
            (i32.xor
              (local.get $l2)
              (i32.const 3)))
          (local.set $l2
            (i32.load8_u offset=1
              (local.get $l1)))
          (local.set $l1
            (i32.add
              (local.get $l1)
              (i32.const 1)))
          (br_if $L1
            (local.get $l2)))))
    (i32.eqz
      (call $f3
        (local.get $p0))))
  (func $a (export "a") (type $t1)
    (nop))
  (global $g0 (mut i32) (i32.const 5244480))
  (data $d0 (i32.const 1024) "E@P@x4f1g7f6ab:42`1g:f:7763133;e0e;03`6661`bee0:33fg732;b6fea44be34g0~"))
