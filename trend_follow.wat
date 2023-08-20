(module
  (type (;0;) (func (param i32 i32 i32) (result i32)))
  (type (;1;) (func (param i32 i32) (result i32)))
  (type (;2;) (func (param i32)))
  (type (;3;) (func (param i32 i32)))
  (type (;4;) (func (param i32 i32) (result i32 f32)))
  (type (;5;) (func (param i32) (result i32)))
  (type (;6;) (func (param i32) (result i64)))
  (type (;7;) (func (param i32) (result i32 i32)))
  (type (;8;) (func (param i32 i32 i32 i32) (result i32)))
  (type (;9;) (func (param i32 i32 i32 i32)))
  (type (;10;) (func (param i32 f32)))
  (type (;11;) (func (param i32 i32 i32 i32 i32)))
  (type (;12;) (func (param i32 i32 i32)))
  (type (;13;) (func (param i32 i32 i32) (result i32 i32)))
  (type (;14;) (func))
  (type (;15;) (func (param i32 i32 i32) (result i64)))
  (type (;16;) (func (param i32 i32 i64) (result i32)))
  (type (;17;) (func (param i64 i64 i32) (result i64)))
  (type (;18;) (func (param i64 i32 i32) (result i32)))
  (type (;19;) (func (param i32 i32 i32 i32 i32 i32)))
  (type (;20;) (func (param i32 i64 i32) (result i32)))
  (type (;21;) (func (param i32 i32) (result i32 i32)))
  (type (;22;) (func (result i32)))
  (type (;23;) (func (param i32 i32 f32 f32 f32 f32 f32)))
  (type (;24;) (func (param i32 i32 i32 i32 i32 i32) (result i32)))
  (type (;25;) (func (param i32 i32 i32 i32 i32) (result i32)))
  (type (;26;) (func (param i32 i32 i32 i32 i32 i32 i32) (result i32)))
  (import "wasi_snapshot_preview1" "random_get" (func $_ZN4wasi13lib_generated22wasi_snapshot_preview110random_get17h9e4fa943327627f2E (type 1)))
  (import "wasi_snapshot_preview1" "fd_write" (func $_ZN4wasi13lib_generated22wasi_snapshot_preview18fd_write17h82bd99e8a5fb7244E (type 8)))
  (import "wasi_snapshot_preview1" "environ_get" (func $__imported_wasi_snapshot_preview1_environ_get (type 1)))
  (import "wasi_snapshot_preview1" "environ_sizes_get" (func $__imported_wasi_snapshot_preview1_environ_sizes_get (type 1)))
  (import "wasi_snapshot_preview1" "proc_exit" (func $__imported_wasi_snapshot_preview1_proc_exit (type 2)))
  (func $_ZN106_$LT$core..iter..adapters..flatten..Flatten$LT$I$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$4last17h2bcb6d668b68b047E (type 5) (param i32) (result i32)
    (local i32 i32 i32 i32 i32)
    local.get 0
    i32.load8_u offset=17
    local.set 1
    local.get 0
    i32.load
    local.set 2
    i32.const 2
    local.set 3
    block  ;; label = @1
      local.get 0
      i32.load8_u offset=16
      local.tee 4
      i32.const 3
      i32.eq
      br_if 0 (;@1;)
      i32.const 2
      local.get 4
      call $_ZN4core3ops8function5FnMut8call_mut17he4f6f1c1b498c0cdE
      i32.const 255
      i32.and
      local.set 3
    end
    block  ;; label = @1
      local.get 2
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      i32.load offset=12
      local.set 5
      local.get 0
      i32.load offset=8
      local.set 4
      local.get 0
      i32.load offset=4
      local.set 0
      block  ;; label = @2
        loop  ;; label = @3
          local.get 4
          local.get 5
          i32.eq
          br_if 1 (;@2;)
          local.get 3
          local.get 4
          i32.load8_u
          call $_ZN4core3ops8function5FnMut8call_mut17he4f6f1c1b498c0cdE
          i32.const 255
          i32.and
          local.set 3
          local.get 4
          i32.const 1
          i32.add
          local.set 4
          br 0 (;@3;)
        end
      end
      local.get 2
      local.get 0
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h3ad717a5de7f5611E
    end
    block  ;; label = @1
      local.get 1
      i32.const 255
      i32.and
      i32.const 3
      i32.eq
      br_if 0 (;@1;)
      local.get 3
      local.get 1
      call $_ZN4core3ops8function5FnMut8call_mut17he4f6f1c1b498c0cdE
      i32.const 255
      i32.and
      local.set 3
    end
    local.get 3)
  (func $_ZN4core3ops8function5FnMut8call_mut17he4f6f1c1b498c0cdE (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32)
    i32.const 2
    local.set 2
    loop  ;; label = @1
      local.get 2
      local.set 3
      local.get 1
      i32.const 1
      i32.and
      local.set 2
      local.get 1
      i32.const 255
      i32.and
      local.set 4
      i32.const 2
      local.set 1
      local.get 4
      i32.const 2
      i32.ne
      br_if 0 (;@1;)
    end
    local.get 0
    local.get 3
    local.get 3
    i32.const 255
    i32.and
    i32.const 2
    i32.eq
    select)
  (func $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h3ad717a5de7f5611E (type 3) (param i32 i32)
    block  ;; label = @1
      local.get 1
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      call $_ZN63_$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$10deallocate17h61bf6a4893a1c41aE
    end)
  (func $_ZN4core3ptr47drop_in_place$LT$alloc..vec..Vec$LT$f32$GT$$GT$17h5ba05a9c2fc58ac5E (type 3) (param i32 i32)
    block  ;; label = @1
      local.get 1
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      i32.const 2
      i32.shl
      call $_ZN63_$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$10deallocate17h61bf6a4893a1c41aE
    end)
  (func $_ZN63_$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$10deallocate17h61bf6a4893a1c41aE (type 3) (param i32 i32)
    block  ;; label = @1
      local.get 1
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      call $free
    end)
  (func $_ZN60_$LT$alloc..string..String$u20$as$u20$core..fmt..Display$GT$3fmt17h44520808cb144237E (type 1) (param i32 i32) (result i32)
    local.get 1
    local.get 0
    i32.load
    local.get 0
    i32.load offset=8
    call $_ZN4core3fmt9Formatter3pad17h2cd94e1fc1b5b777E)
  (func $_ZN4core3fmt9Formatter3pad17h2cd94e1fc1b5b777E (type 0) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.load
        local.tee 3
        local.get 0
        i32.load offset=8
        local.tee 4
        i32.or
        i32.eqz
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 4
          i32.eqz
          br_if 0 (;@3;)
          local.get 1
          local.get 2
          i32.add
          local.set 5
          local.get 0
          i32.const 12
          i32.add
          i32.load
          i32.const 1
          i32.add
          local.set 6
          i32.const 0
          local.set 7
          local.get 1
          local.set 8
          block  ;; label = @4
            loop  ;; label = @5
              local.get 8
              local.set 4
              local.get 6
              i32.const -1
              i32.add
              local.tee 6
              i32.eqz
              br_if 1 (;@4;)
              local.get 4
              local.get 5
              i32.eq
              br_if 2 (;@3;)
              block  ;; label = @6
                block  ;; label = @7
                  local.get 4
                  i32.load8_s
                  local.tee 9
                  i32.const -1
                  i32.le_s
                  br_if 0 (;@7;)
                  local.get 4
                  i32.const 1
                  i32.add
                  local.set 8
                  local.get 9
                  i32.const 255
                  i32.and
                  local.set 9
                  br 1 (;@6;)
                end
                local.get 4
                i32.load8_u offset=1
                i32.const 63
                i32.and
                local.set 10
                local.get 9
                i32.const 31
                i32.and
                local.set 8
                block  ;; label = @7
                  local.get 9
                  i32.const -33
                  i32.gt_u
                  br_if 0 (;@7;)
                  local.get 8
                  i32.const 6
                  i32.shl
                  local.get 10
                  i32.or
                  local.set 9
                  local.get 4
                  i32.const 2
                  i32.add
                  local.set 8
                  br 1 (;@6;)
                end
                local.get 10
                i32.const 6
                i32.shl
                local.get 4
                i32.load8_u offset=2
                i32.const 63
                i32.and
                i32.or
                local.set 10
                block  ;; label = @7
                  local.get 9
                  i32.const -16
                  i32.ge_u
                  br_if 0 (;@7;)
                  local.get 10
                  local.get 8
                  i32.const 12
                  i32.shl
                  i32.or
                  local.set 9
                  local.get 4
                  i32.const 3
                  i32.add
                  local.set 8
                  br 1 (;@6;)
                end
                local.get 10
                i32.const 6
                i32.shl
                local.get 4
                i32.load8_u offset=3
                i32.const 63
                i32.and
                i32.or
                local.get 8
                i32.const 18
                i32.shl
                i32.const 1835008
                i32.and
                i32.or
                local.tee 9
                i32.const 1114112
                i32.eq
                br_if 3 (;@3;)
                local.get 4
                i32.const 4
                i32.add
                local.set 8
              end
              local.get 7
              local.get 4
              i32.sub
              local.get 8
              i32.add
              local.set 7
              local.get 9
              i32.const 1114112
              i32.ne
              br_if 0 (;@5;)
              br 2 (;@3;)
            end
          end
          local.get 4
          local.get 5
          i32.eq
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 4
            i32.load8_s
            local.tee 8
            i32.const -1
            i32.gt_s
            br_if 0 (;@4;)
            local.get 8
            i32.const -32
            i32.lt_u
            br_if 0 (;@4;)
            local.get 8
            i32.const -16
            i32.lt_u
            br_if 0 (;@4;)
            local.get 4
            i32.load8_u offset=2
            i32.const 63
            i32.and
            i32.const 6
            i32.shl
            local.get 4
            i32.load8_u offset=1
            i32.const 63
            i32.and
            i32.const 12
            i32.shl
            i32.or
            local.get 4
            i32.load8_u offset=3
            i32.const 63
            i32.and
            i32.or
            local.get 8
            i32.const 255
            i32.and
            i32.const 18
            i32.shl
            i32.const 1835008
            i32.and
            i32.or
            i32.const 1114112
            i32.eq
            br_if 1 (;@3;)
          end
          block  ;; label = @4
            block  ;; label = @5
              local.get 7
              i32.eqz
              br_if 0 (;@5;)
              block  ;; label = @6
                local.get 7
                local.get 2
                i32.lt_u
                br_if 0 (;@6;)
                i32.const 0
                local.set 4
                local.get 7
                local.get 2
                i32.eq
                br_if 1 (;@5;)
                br 2 (;@4;)
              end
              i32.const 0
              local.set 4
              local.get 1
              local.get 7
              i32.add
              i32.load8_s
              i32.const -64
              i32.lt_s
              br_if 1 (;@4;)
            end
            local.get 1
            local.set 4
          end
          local.get 7
          local.get 2
          local.get 4
          select
          local.set 2
          local.get 4
          local.get 1
          local.get 4
          select
          local.set 1
        end
        block  ;; label = @3
          local.get 3
          br_if 0 (;@3;)
          local.get 0
          i32.load offset=20
          local.get 1
          local.get 2
          local.get 0
          i32.const 24
          i32.add
          i32.load
          i32.load offset=12
          call_indirect (type 0)
          return
        end
        local.get 0
        i32.load offset=4
        local.set 11
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              local.get 2
              i32.const 16
              i32.lt_u
              br_if 0 (;@5;)
              local.get 2
              local.get 1
              i32.const 3
              i32.add
              i32.const -4
              i32.and
              local.tee 9
              local.get 1
              i32.sub
              local.tee 8
              i32.sub
              local.tee 3
              i32.const 3
              i32.and
              local.set 5
              i32.const 0
              local.set 10
              i32.const 0
              local.set 4
              block  ;; label = @6
                local.get 9
                local.get 1
                i32.eq
                br_if 0 (;@6;)
                local.get 8
                i32.const 3
                i32.and
                local.set 7
                i32.const 0
                local.set 4
                block  ;; label = @7
                  local.get 9
                  local.get 1
                  i32.const -1
                  i32.xor
                  i32.add
                  i32.const 3
                  i32.lt_u
                  br_if 0 (;@7;)
                  i32.const 0
                  local.set 6
                  loop  ;; label = @8
                    local.get 4
                    local.get 1
                    local.get 6
                    i32.add
                    local.tee 8
                    i32.load8_s
                    i32.const -65
                    i32.gt_s
                    i32.add
                    local.get 8
                    i32.const 1
                    i32.add
                    i32.load8_s
                    i32.const -65
                    i32.gt_s
                    i32.add
                    local.get 8
                    i32.const 2
                    i32.add
                    i32.load8_s
                    i32.const -65
                    i32.gt_s
                    i32.add
                    local.get 8
                    i32.const 3
                    i32.add
                    i32.load8_s
                    i32.const -65
                    i32.gt_s
                    i32.add
                    local.set 4
                    local.get 6
                    i32.const 4
                    i32.add
                    local.tee 6
                    br_if 0 (;@8;)
                  end
                end
                local.get 7
                i32.eqz
                br_if 0 (;@6;)
                local.get 1
                local.set 8
                loop  ;; label = @7
                  local.get 4
                  local.get 8
                  i32.load8_s
                  i32.const -65
                  i32.gt_s
                  i32.add
                  local.set 4
                  local.get 8
                  i32.const 1
                  i32.add
                  local.set 8
                  local.get 7
                  i32.const -1
                  i32.add
                  local.tee 7
                  br_if 0 (;@7;)
                end
              end
              block  ;; label = @6
                local.get 5
                i32.eqz
                br_if 0 (;@6;)
                local.get 9
                local.get 3
                i32.const -4
                i32.and
                i32.add
                local.tee 8
                i32.load8_s
                i32.const -65
                i32.gt_s
                local.set 10
                local.get 5
                i32.const 1
                i32.eq
                br_if 0 (;@6;)
                local.get 10
                local.get 8
                i32.load8_s offset=1
                i32.const -65
                i32.gt_s
                i32.add
                local.set 10
                local.get 5
                i32.const 2
                i32.eq
                br_if 0 (;@6;)
                local.get 10
                local.get 8
                i32.load8_s offset=2
                i32.const -65
                i32.gt_s
                i32.add
                local.set 10
              end
              local.get 3
              i32.const 2
              i32.shr_u
              local.set 5
              local.get 10
              local.get 4
              i32.add
              local.set 7
              loop  ;; label = @6
                local.get 9
                local.set 3
                local.get 5
                i32.eqz
                br_if 3 (;@3;)
                local.get 5
                i32.const 192
                local.get 5
                i32.const 192
                i32.lt_u
                select
                local.tee 10
                i32.const 3
                i32.and
                local.set 12
                local.get 10
                i32.const 2
                i32.shl
                local.set 13
                block  ;; label = @7
                  block  ;; label = @8
                    local.get 10
                    i32.const 252
                    i32.and
                    local.tee 14
                    br_if 0 (;@8;)
                    i32.const 0
                    local.set 8
                    br 1 (;@7;)
                  end
                  local.get 3
                  local.get 14
                  i32.const 2
                  i32.shl
                  i32.add
                  local.set 6
                  i32.const 0
                  local.set 8
                  local.get 3
                  local.set 4
                  loop  ;; label = @8
                    local.get 4
                    i32.eqz
                    br_if 1 (;@7;)
                    local.get 4
                    i32.const 12
                    i32.add
                    i32.load
                    local.tee 9
                    i32.const -1
                    i32.xor
                    i32.const 7
                    i32.shr_u
                    local.get 9
                    i32.const 6
                    i32.shr_u
                    i32.or
                    i32.const 16843009
                    i32.and
                    local.get 4
                    i32.const 8
                    i32.add
                    i32.load
                    local.tee 9
                    i32.const -1
                    i32.xor
                    i32.const 7
                    i32.shr_u
                    local.get 9
                    i32.const 6
                    i32.shr_u
                    i32.or
                    i32.const 16843009
                    i32.and
                    local.get 4
                    i32.const 4
                    i32.add
                    i32.load
                    local.tee 9
                    i32.const -1
                    i32.xor
                    i32.const 7
                    i32.shr_u
                    local.get 9
                    i32.const 6
                    i32.shr_u
                    i32.or
                    i32.const 16843009
                    i32.and
                    local.get 4
                    i32.load
                    local.tee 9
                    i32.const -1
                    i32.xor
                    i32.const 7
                    i32.shr_u
                    local.get 9
                    i32.const 6
                    i32.shr_u
                    i32.or
                    i32.const 16843009
                    i32.and
                    local.get 8
                    i32.add
                    i32.add
                    i32.add
                    i32.add
                    local.set 8
                    local.get 4
                    i32.const 16
                    i32.add
                    local.tee 4
                    local.get 6
                    i32.ne
                    br_if 0 (;@8;)
                  end
                end
                local.get 5
                local.get 10
                i32.sub
                local.set 5
                local.get 3
                local.get 13
                i32.add
                local.set 9
                local.get 8
                i32.const 8
                i32.shr_u
                i32.const 16711935
                i32.and
                local.get 8
                i32.const 16711935
                i32.and
                i32.add
                i32.const 65537
                i32.mul
                i32.const 16
                i32.shr_u
                local.get 7
                i32.add
                local.set 7
                local.get 12
                i32.eqz
                br_if 0 (;@6;)
              end
              block  ;; label = @6
                local.get 3
                br_if 0 (;@6;)
                i32.const 0
                local.set 4
                br 2 (;@4;)
              end
              local.get 3
              local.get 14
              i32.const 2
              i32.shl
              i32.add
              local.tee 8
              i32.load
              local.tee 4
              i32.const -1
              i32.xor
              i32.const 7
              i32.shr_u
              local.get 4
              i32.const 6
              i32.shr_u
              i32.or
              i32.const 16843009
              i32.and
              local.set 4
              local.get 12
              i32.const 1
              i32.eq
              br_if 1 (;@4;)
              local.get 8
              i32.load offset=4
              local.tee 9
              i32.const -1
              i32.xor
              i32.const 7
              i32.shr_u
              local.get 9
              i32.const 6
              i32.shr_u
              i32.or
              i32.const 16843009
              i32.and
              local.get 4
              i32.add
              local.set 4
              local.get 12
              i32.const 2
              i32.eq
              br_if 1 (;@4;)
              local.get 8
              i32.load offset=8
              local.tee 8
              i32.const -1
              i32.xor
              i32.const 7
              i32.shr_u
              local.get 8
              i32.const 6
              i32.shr_u
              i32.or
              i32.const 16843009
              i32.and
              local.get 4
              i32.add
              local.set 4
              br 1 (;@4;)
            end
            block  ;; label = @5
              local.get 2
              br_if 0 (;@5;)
              i32.const 0
              local.set 7
              br 2 (;@3;)
            end
            local.get 2
            i32.const 3
            i32.and
            local.set 8
            block  ;; label = @5
              block  ;; label = @6
                local.get 2
                i32.const 4
                i32.ge_u
                br_if 0 (;@6;)
                i32.const 0
                local.set 7
                local.get 1
                local.set 4
                br 1 (;@5;)
              end
              local.get 2
              i32.const -4
              i32.and
              local.set 9
              i32.const 0
              local.set 7
              local.get 1
              local.set 4
              loop  ;; label = @6
                local.get 7
                local.get 4
                i32.load8_s
                i32.const -65
                i32.gt_s
                i32.add
                local.get 4
                i32.load8_s offset=1
                i32.const -65
                i32.gt_s
                i32.add
                local.get 4
                i32.load8_s offset=2
                i32.const -65
                i32.gt_s
                i32.add
                local.get 4
                i32.load8_s offset=3
                i32.const -65
                i32.gt_s
                i32.add
                local.set 7
                local.get 4
                i32.const 4
                i32.add
                local.set 4
                local.get 9
                i32.const -4
                i32.add
                local.tee 9
                br_if 0 (;@6;)
              end
            end
            local.get 8
            i32.eqz
            br_if 1 (;@3;)
            loop  ;; label = @5
              local.get 7
              local.get 4
              i32.load8_s
              i32.const -65
              i32.gt_s
              i32.add
              local.set 7
              local.get 4
              i32.const 1
              i32.add
              local.set 4
              local.get 8
              i32.const -1
              i32.add
              local.tee 8
              br_if 0 (;@5;)
              br 2 (;@3;)
            end
          end
          local.get 4
          i32.const 8
          i32.shr_u
          i32.const 459007
          i32.and
          local.get 4
          i32.const 16711935
          i32.and
          i32.add
          i32.const 65537
          i32.mul
          i32.const 16
          i32.shr_u
          local.get 7
          i32.add
          local.set 7
        end
        block  ;; label = @3
          local.get 11
          local.get 7
          i32.le_u
          br_if 0 (;@3;)
          i32.const 0
          local.set 4
          local.get 11
          local.get 7
          i32.sub
          local.tee 8
          local.set 7
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                local.get 0
                i32.load8_u offset=32
                br_table 2 (;@4;) 0 (;@6;) 1 (;@5;) 2 (;@4;) 2 (;@4;)
              end
              i32.const 0
              local.set 7
              local.get 8
              local.set 4
              br 1 (;@4;)
            end
            local.get 8
            i32.const 1
            i32.shr_u
            local.set 4
            local.get 8
            i32.const 1
            i32.add
            i32.const 1
            i32.shr_u
            local.set 7
          end
          local.get 4
          i32.const 1
          i32.add
          local.set 4
          local.get 0
          i32.const 24
          i32.add
          i32.load
          local.set 9
          local.get 0
          i32.const 20
          i32.add
          i32.load
          local.set 6
          local.get 0
          i32.load offset=16
          local.set 8
          block  ;; label = @4
            loop  ;; label = @5
              local.get 4
              i32.const -1
              i32.add
              local.tee 4
              i32.eqz
              br_if 1 (;@4;)
              local.get 6
              local.get 8
              local.get 9
              i32.load offset=16
              call_indirect (type 1)
              i32.eqz
              br_if 0 (;@5;)
            end
            i32.const 1
            return
          end
          i32.const 1
          local.set 4
          local.get 8
          i32.const 1114112
          i32.eq
          br_if 2 (;@1;)
          local.get 6
          local.get 1
          local.get 2
          local.get 9
          i32.load offset=12
          call_indirect (type 0)
          br_if 2 (;@1;)
          i32.const 0
          local.set 4
          loop  ;; label = @4
            block  ;; label = @5
              local.get 7
              local.get 4
              i32.ne
              br_if 0 (;@5;)
              local.get 7
              local.get 7
              i32.lt_u
              return
            end
            local.get 4
            i32.const 1
            i32.add
            local.set 4
            local.get 6
            local.get 8
            local.get 9
            i32.load offset=16
            call_indirect (type 1)
            i32.eqz
            br_if 0 (;@4;)
          end
          local.get 4
          i32.const -1
          i32.add
          local.get 7
          i32.lt_u
          return
        end
        local.get 0
        i32.load offset=20
        local.get 1
        local.get 2
        local.get 0
        i32.const 24
        i32.add
        i32.load
        i32.load offset=12
        call_indirect (type 0)
        return
      end
      local.get 0
      i32.load offset=20
      local.get 1
      local.get 2
      local.get 0
      i32.const 24
      i32.add
      i32.load
      i32.load offset=12
      call_indirect (type 0)
      local.set 4
    end
    local.get 4)
  (func $_ZN89_$LT$base..strategy..BaseStrategy$LT$S$GT$$u20$as$u20$base..strategy..TradingStrategy$GT$11strategy_id17he477e15cd4143f5fE (type 3) (param i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 96
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    i32.const 56
    i32.add
    i32.const 12
    i32.add
    i64.const 2
    i64.store align=4
    local.get 2
    i32.const 80
    i32.add
    i32.const 12
    i32.add
    i32.const 1
    i32.store
    local.get 2
    i32.const 2
    i32.store offset=60
    local.get 2
    i32.const 1055624
    i32.store offset=56
    local.get 2
    local.get 1
    i32.const 20
    i32.add
    i32.store offset=88
    local.get 2
    i32.const 1
    i32.store offset=84
    local.get 2
    local.get 1
    i32.const 16
    i32.add
    i32.store offset=80
    local.get 2
    local.get 2
    i32.const 80
    i32.add
    i32.store offset=64
    local.get 2
    i32.const 40
    i32.add
    local.get 2
    i32.const 56
    i32.add
    call $_ZN5alloc3fmt6format12format_inner17he6923879c36cef02E
    local.get 2
    i32.const 8
    i32.add
    i32.const 12
    i32.add
    i64.const 1
    i64.store align=4
    local.get 2
    i32.const 2
    i32.store offset=36
    local.get 2
    i32.const 1
    i32.store offset=12
    local.get 2
    i32.const 1048584
    i32.store offset=8
    local.get 2
    local.get 2
    i32.const 40
    i32.add
    i32.store offset=32
    local.get 2
    local.get 2
    i32.const 32
    i32.add
    i32.store offset=16
    local.get 0
    local.get 2
    i32.const 8
    i32.add
    call $_ZN5alloc3fmt6format12format_inner17he6923879c36cef02E
    local.get 2
    i32.load offset=40
    local.get 2
    i32.load offset=44
    call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17hce6ec3cb0496d13dE
    local.get 2
    i32.const 96
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core3fmt3num3imp52_$LT$impl$u20$core..fmt..Display$u20$for$u20$u32$GT$3fmt17h4be59bab036c1886E (type 1) (param i32 i32) (result i32)
    local.get 0
    i64.load32_u
    i32.const 1
    local.get 1
    call $_ZN4core3fmt3num3imp7fmt_u6417ha30186d55e58ac6fE)
  (func $_ZN5alloc3fmt6format12format_inner17he6923879c36cef02E (type 3) (param i32 i32)
    (local i32 i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                local.get 1
                i32.load offset=4
                local.tee 3
                i32.eqz
                br_if 0 (;@6;)
                local.get 1
                i32.load
                local.set 4
                local.get 3
                i32.const -1
                i32.add
                i32.const 536870911
                i32.and
                local.tee 3
                i32.const 1
                i32.add
                local.tee 5
                i32.const 7
                i32.and
                local.set 6
                block  ;; label = @7
                  block  ;; label = @8
                    local.get 3
                    i32.const 7
                    i32.ge_u
                    br_if 0 (;@8;)
                    i32.const 0
                    local.set 5
                    local.get 4
                    local.set 3
                    br 1 (;@7;)
                  end
                  local.get 4
                  i32.const 60
                  i32.add
                  local.set 3
                  local.get 5
                  i32.const 1073741816
                  i32.and
                  local.set 7
                  i32.const 0
                  local.set 5
                  loop  ;; label = @8
                    local.get 3
                    i32.load
                    local.get 3
                    i32.const -8
                    i32.add
                    i32.load
                    local.get 3
                    i32.const -16
                    i32.add
                    i32.load
                    local.get 3
                    i32.const -24
                    i32.add
                    i32.load
                    local.get 3
                    i32.const -32
                    i32.add
                    i32.load
                    local.get 3
                    i32.const -40
                    i32.add
                    i32.load
                    local.get 3
                    i32.const -48
                    i32.add
                    i32.load
                    local.get 3
                    i32.const -56
                    i32.add
                    i32.load
                    local.get 5
                    i32.add
                    i32.add
                    i32.add
                    i32.add
                    i32.add
                    i32.add
                    i32.add
                    i32.add
                    local.set 5
                    local.get 3
                    i32.const 64
                    i32.add
                    local.set 3
                    local.get 7
                    i32.const -8
                    i32.add
                    local.tee 7
                    br_if 0 (;@8;)
                  end
                  local.get 3
                  i32.const -60
                  i32.add
                  local.set 3
                end
                block  ;; label = @7
                  local.get 6
                  i32.eqz
                  br_if 0 (;@7;)
                  local.get 3
                  i32.const 4
                  i32.add
                  local.set 3
                  loop  ;; label = @8
                    local.get 3
                    i32.load
                    local.get 5
                    i32.add
                    local.set 5
                    local.get 3
                    i32.const 8
                    i32.add
                    local.set 3
                    local.get 6
                    i32.const -1
                    i32.add
                    local.tee 6
                    br_if 0 (;@8;)
                  end
                end
                block  ;; label = @7
                  local.get 1
                  i32.const 12
                  i32.add
                  i32.load
                  i32.eqz
                  br_if 0 (;@7;)
                  local.get 5
                  i32.const 0
                  i32.lt_s
                  br_if 1 (;@6;)
                  local.get 5
                  i32.const 16
                  i32.lt_u
                  local.get 4
                  i32.load offset=4
                  i32.eqz
                  i32.and
                  br_if 1 (;@6;)
                  local.get 5
                  i32.const 1
                  i32.shl
                  local.set 5
                end
                local.get 5
                br_if 1 (;@5;)
              end
              i32.const 1
              local.set 3
              i32.const 0
              local.set 5
              br 1 (;@4;)
            end
            local.get 5
            i32.const -1
            i32.le_s
            br_if 1 (;@3;)
            i32.const 0
            i32.load8_u offset=1059320
            drop
            local.get 5
            i32.const 1
            call $__rust_alloc
            local.tee 3
            i32.eqz
            br_if 2 (;@2;)
          end
          local.get 2
          i32.const 0
          i32.store offset=8
          local.get 2
          local.get 5
          i32.store offset=4
          local.get 2
          local.get 3
          i32.store
          local.get 2
          local.get 2
          i32.store offset=12
          local.get 2
          i32.const 16
          i32.add
          i32.const 16
          i32.add
          local.get 1
          i32.const 16
          i32.add
          i64.load align=4
          i64.store
          local.get 2
          i32.const 16
          i32.add
          i32.const 8
          i32.add
          local.get 1
          i32.const 8
          i32.add
          i64.load align=4
          i64.store
          local.get 2
          local.get 1
          i64.load align=4
          i64.store offset=16
          local.get 2
          i32.const 12
          i32.add
          i32.const 1048596
          local.get 2
          i32.const 16
          i32.add
          call $_ZN4core3fmt5write17h8253e306f6bd0e19E
          i32.eqz
          br_if 2 (;@1;)
          i32.const 1048664
          i32.const 51
          local.get 2
          i32.const 40
          i32.add
          i32.const 1048716
          i32.const 1048756
          call $_ZN4core6result13unwrap_failed17hfefb3e75b68d8f8cE
          unreachable
        end
        call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
        unreachable
      end
      i32.const 1
      local.get 5
      call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
      unreachable
    end
    local.get 0
    local.get 2
    i64.load
    i64.store align=4
    local.get 0
    i32.const 8
    i32.add
    local.get 2
    i32.const 8
    i32.add
    i32.load
    i32.store
    local.get 2
    i32.const 48
    i32.add
    global.set $__stack_pointer)
  (func $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17hce6ec3cb0496d13dE (type 3) (param i32 i32)
    block  ;; label = @1
      local.get 1
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      call $free
    end)
  (func $_ZN89_$LT$base..strategy..BaseStrategy$LT$S$GT$$u20$as$u20$base..strategy..TradingStrategy$GT$4next17h814055e7e1141c1fE (type 4) (param i32 i32) (result i32 f32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 f32 f32 i32)
    global.get $__stack_pointer
    i32.const 144
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      local.get 0
      i32.load offset=12
      local.tee 3
      local.get 0
      i32.load offset=24
      local.tee 4
      i32.lt_u
      br_if 0 (;@1;)
      block  ;; label = @2
        local.get 3
        br_if 0 (;@2;)
        i32.const 0
        local.set 3
        br 1 (;@1;)
      end
      local.get 0
      local.get 3
      i32.const -1
      i32.add
      local.tee 3
      i32.store offset=12
      local.get 0
      local.get 0
      i32.load offset=8
      i32.const 1
      i32.add
      local.tee 5
      i32.const 0
      local.get 0
      i32.load offset=4
      local.tee 6
      local.get 5
      local.get 6
      i32.lt_u
      select
      i32.sub
      i32.store offset=8
    end
    i32.const 4
    local.set 7
    block  ;; label = @1
      local.get 3
      local.get 0
      i32.const 4
      i32.add
      i32.load
      local.tee 6
      i32.ne
      br_if 0 (;@1;)
      local.get 0
      call $_ZN5alloc11collections9vec_deque21VecDeque$LT$T$C$A$GT$4grow17hf36a8419da4188daE
      local.get 0
      i32.const 4
      i32.add
      i32.load
      local.set 6
      local.get 0
      i32.load offset=24
      local.set 4
      local.get 0
      i32.load offset=12
      local.set 3
    end
    local.get 0
    local.get 3
    i32.const 1
    i32.add
    local.tee 5
    i32.store offset=12
    local.get 0
    i32.load
    local.tee 8
    local.get 0
    i32.const 8
    i32.add
    i32.load
    local.tee 9
    local.get 3
    i32.add
    local.tee 3
    i32.const 0
    local.get 6
    local.get 3
    local.get 6
    i32.lt_u
    select
    i32.sub
    i32.const 20
    i32.mul
    i32.add
    local.tee 3
    local.get 1
    i64.load align=4
    i64.store align=4
    local.get 3
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store align=4
    local.get 3
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i32.load
    i32.store
    block  ;; label = @1
      local.get 5
      local.get 4
      i32.lt_u
      br_if 0 (;@1;)
      local.get 5
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h887a12da11f6a316E
      local.set 1
      local.set 3
      local.get 2
      i32.const 0
      i32.store offset=72
      local.get 2
      local.get 1
      i32.store offset=68
      local.get 2
      local.get 3
      i32.store offset=64
      local.get 5
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h887a12da11f6a316E
      local.set 1
      local.set 3
      local.get 2
      i32.const 0
      i32.store offset=88
      local.get 2
      local.get 1
      i32.store offset=84
      local.get 2
      local.get 3
      i32.store offset=80
      local.get 5
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h887a12da11f6a316E
      local.set 1
      local.set 3
      local.get 2
      i32.const 0
      i32.store offset=104
      local.get 2
      local.get 1
      i32.store offset=100
      local.get 2
      local.get 3
      i32.store offset=96
      local.get 5
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h887a12da11f6a316E
      local.set 1
      local.set 3
      local.get 2
      i32.const 0
      i32.store offset=120
      local.get 2
      local.get 1
      i32.store offset=116
      local.get 2
      local.get 3
      i32.store offset=112
      local.get 5
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h887a12da11f6a316E
      local.set 1
      local.set 3
      local.get 2
      i32.const 0
      i32.store offset=136
      local.get 2
      local.get 1
      i32.store offset=132
      local.get 2
      local.get 3
      i32.store offset=128
      local.get 2
      i32.const 8
      i32.add
      local.get 6
      local.get 9
      local.get 5
      call $_ZN5alloc11collections9vec_deque21VecDeque$LT$T$C$A$GT$12slice_ranges17h771185e4c206a015E
      local.get 8
      local.get 2
      i32.const 20
      i32.add
      i32.load
      i32.const 20
      i32.mul
      i32.add
      local.set 5
      local.get 8
      local.get 2
      i32.load offset=12
      i32.const 20
      i32.mul
      i32.add
      local.set 1
      local.get 8
      local.get 2
      i32.load offset=16
      i32.const 20
      i32.mul
      i32.add
      local.set 3
      local.get 8
      local.get 2
      i32.load offset=8
      i32.const 20
      i32.mul
      i32.add
      local.set 6
      block  ;; label = @2
        loop  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              local.get 6
              local.get 1
              i32.eq
              br_if 0 (;@5;)
              local.get 5
              local.set 8
              local.get 3
              local.set 4
              local.get 1
              local.set 5
              local.get 6
              local.set 3
              br 1 (;@4;)
            end
            local.get 1
            local.set 8
            local.get 1
            local.set 4
            local.get 3
            local.get 5
            i32.eq
            br_if 2 (;@2;)
          end
          local.get 5
          local.set 1
          local.get 2
          i32.const 64
          i32.add
          local.get 3
          f32.load
          call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$4push17h015b00d50b87b785E
          local.get 2
          i32.const 80
          i32.add
          local.get 3
          f32.load offset=4
          call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$4push17h015b00d50b87b785E
          local.get 2
          i32.const 96
          i32.add
          local.get 3
          f32.load offset=8
          call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$4push17h015b00d50b87b785E
          local.get 2
          i32.const 112
          i32.add
          local.get 3
          f32.load offset=12
          call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$4push17h015b00d50b87b785E
          local.get 2
          i32.const 128
          i32.add
          local.get 3
          f32.load offset=16
          call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$4push17h015b00d50b87b785E
          local.get 3
          i32.const 20
          i32.add
          local.set 6
          local.get 8
          local.set 5
          local.get 4
          local.set 3
          br 0 (;@3;)
        end
      end
      local.get 2
      i32.load offset=132
      local.set 10
      local.get 2
      i32.load offset=128
      local.set 11
      local.get 2
      i32.load offset=116
      local.set 12
      local.get 2
      i32.load offset=100
      local.set 13
      local.get 2
      i32.load offset=84
      local.set 14
      local.get 2
      i32.load offset=68
      local.set 15
      local.get 2
      i32.load offset=64
      local.set 16
      local.get 2
      i32.load offset=104
      local.set 4
      local.get 2
      i32.load offset=96
      local.set 17
      local.get 2
      i32.load offset=88
      local.set 7
      local.get 2
      i32.load offset=80
      local.set 18
      local.get 2
      i32.const 32
      i32.add
      local.get 2
      i32.load offset=112
      local.tee 9
      local.get 2
      i32.load offset=120
      local.tee 8
      local.get 0
      i32.load offset=16
      call $_ZN5trend3sma3sma17h7fceb42ba3154614E
      local.get 2
      i32.const 48
      i32.add
      local.get 9
      local.get 8
      local.get 0
      i32.const 20
      i32.add
      i32.load
      call $_ZN5trend3sma3sma17h7fceb42ba3154614E
      local.get 2
      i32.const 96
      i32.add
      local.get 2
      i32.load offset=32
      local.tee 3
      local.get 2
      i32.load offset=40
      local.tee 1
      local.get 2
      i32.load offset=48
      local.tee 5
      local.get 2
      i32.load offset=56
      local.tee 6
      call $_ZN4core4bool49_$LT$impl$u20$core..series..Series$LT$f32$GT$$GT$2gt17h1330ec5560ce6d0eE
      local.get 2
      i32.const 128
      i32.add
      local.get 3
      local.get 1
      call $_ZN4core6series15Series$LT$T$GT$5shift17h096cac452bc3fb0cE
      local.get 2
      i32.const 8
      i32.add
      local.get 5
      local.get 6
      call $_ZN4core6series15Series$LT$T$GT$5shift17h096cac452bc3fb0cE
      local.get 2
      i32.const 112
      i32.add
      local.get 2
      i32.load offset=128
      local.tee 0
      local.get 2
      i32.load offset=136
      local.get 2
      i32.load offset=8
      local.tee 19
      local.get 2
      i32.load offset=16
      call $_ZN4core4bool49_$LT$impl$u20$core..series..Series$LT$f32$GT$$GT$2lt17hea1df66b6255e5b8E
      local.get 2
      i32.const 64
      i32.add
      local.get 2
      i32.const 96
      i32.add
      local.get 2
      i32.const 112
      i32.add
      call $_ZN4core4bool85_$LT$impl$u20$core..ops..bit..BitAnd$u20$for$u20$core..series..Series$LT$bool$GT$$GT$6bitand17h9d98e97305c6c554E
      local.get 19
      local.get 2
      i32.load offset=12
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      local.get 0
      local.get 2
      i32.load offset=132
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      local.get 2
      i32.const 96
      i32.add
      local.get 3
      local.get 1
      local.get 5
      local.get 6
      call $_ZN4core4bool49_$LT$impl$u20$core..series..Series$LT$f32$GT$$GT$2lt17hea1df66b6255e5b8E
      local.get 2
      i32.const 128
      i32.add
      local.get 3
      local.get 1
      call $_ZN4core6series15Series$LT$T$GT$5shift17h096cac452bc3fb0cE
      local.get 2
      i32.const 8
      i32.add
      local.get 5
      local.get 6
      call $_ZN4core6series15Series$LT$T$GT$5shift17h096cac452bc3fb0cE
      local.get 2
      i32.const 112
      i32.add
      local.get 2
      i32.load offset=128
      local.tee 1
      local.get 2
      i32.load offset=136
      local.get 2
      i32.load offset=8
      local.tee 6
      local.get 2
      i32.load offset=16
      call $_ZN4core4bool49_$LT$impl$u20$core..series..Series$LT$f32$GT$$GT$2gt17h1330ec5560ce6d0eE
      local.get 2
      i32.const 80
      i32.add
      local.get 2
      i32.const 96
      i32.add
      local.get 2
      i32.const 112
      i32.add
      call $_ZN4core4bool85_$LT$impl$u20$core..ops..bit..BitAnd$u20$for$u20$core..series..Series$LT$bool$GT$$GT$6bitand17h9d98e97305c6c554E
      local.get 6
      local.get 2
      i32.load offset=12
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      local.get 1
      local.get 2
      i32.load offset=132
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      local.get 2
      i32.load offset=84
      local.set 0
      local.get 2
      i32.load offset=80
      local.set 1
      local.get 2
      i32.load offset=88
      local.set 19
      local.get 2
      i32.load offset=68
      local.set 20
      local.get 2
      i32.load offset=64
      local.set 6
      local.get 2
      i32.load offset=72
      local.set 21
      local.get 5
      local.get 2
      i32.load offset=52
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      local.get 3
      local.get 2
      i32.load offset=36
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      local.get 2
      i32.const 8
      i32.add
      call $_ZN4core6series15Series$LT$T$GT$5empty17h62d985689bde32feE
      local.get 2
      i32.const 20
      i32.add
      call $_ZN4core6series15Series$LT$T$GT$5empty17h62d985689bde32feE
      local.get 2
      i32.const 24
      i32.add
      i32.load
      local.set 22
      local.get 2
      i32.const 8
      i32.add
      i32.const 20
      i32.add
      i32.load
      local.set 23
      local.get 2
      i32.load offset=20
      local.set 3
      local.get 2
      i32.load offset=12
      local.set 24
      local.get 2
      i32.load offset=16
      local.set 25
      local.get 2
      i32.load offset=8
      local.set 5
      local.get 2
      i32.const 771
      i32.store16 offset=24
      local.get 2
      local.get 6
      local.get 21
      i32.add
      i32.store offset=20
      local.get 2
      local.get 6
      i32.store offset=16
      local.get 2
      local.get 20
      i32.store offset=12
      local.get 2
      local.get 6
      i32.store offset=8
      local.get 2
      i32.const 8
      i32.add
      call $_ZN106_$LT$core..iter..adapters..flatten..Flatten$LT$I$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$4last17h2bcb6d668b68b047E
      local.set 6
      local.get 2
      i32.const 771
      i32.store16 offset=24
      local.get 2
      local.get 1
      local.get 19
      i32.add
      i32.store offset=20
      local.get 2
      local.get 1
      i32.store offset=16
      local.get 2
      local.get 0
      i32.store offset=12
      local.get 2
      local.get 1
      i32.store offset=8
      local.get 2
      i32.const 8
      i32.add
      call $_ZN106_$LT$core..iter..adapters..flatten..Flatten$LT$I$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$4last17h2bcb6d668b68b047E
      local.set 1
      local.get 2
      i32.const 771
      i32.store16 offset=24
      local.get 2
      local.get 5
      local.get 25
      i32.add
      i32.store offset=20
      local.get 2
      local.get 5
      i32.store offset=16
      local.get 2
      local.get 24
      i32.store offset=12
      local.get 2
      local.get 5
      i32.store offset=8
      local.get 2
      i32.const 8
      i32.add
      call $_ZN106_$LT$core..iter..adapters..flatten..Flatten$LT$I$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$4last17h2bcb6d668b68b047E
      local.set 0
      local.get 2
      i32.const 771
      i32.store16 offset=24
      local.get 2
      local.get 3
      local.get 23
      i32.add
      i32.store offset=20
      local.get 2
      local.get 3
      i32.store offset=16
      local.get 2
      local.get 22
      i32.store offset=12
      local.get 2
      local.get 3
      i32.store offset=8
      local.get 2
      i32.const 8
      i32.add
      call $_ZN106_$LT$core..iter..adapters..flatten..Flatten$LT$I$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$4last17h2bcb6d668b68b047E
      local.set 19
      local.get 2
      i32.const 112
      i32.add
      local.get 18
      local.get 7
      call $_ZN80_$LT$core..series..Series$LT$f32$GT$$u20$as$u20$core..convert..From$LT$T$GT$$GT$4from17h2b5121aec93578c9E
      local.get 2
      i32.const 128
      i32.add
      local.get 17
      local.get 4
      call $_ZN80_$LT$core..series..Series$LT$f32$GT$$u20$as$u20$core..convert..From$LT$T$GT$$GT$4from17h2b5121aec93578c9E
      local.get 2
      i32.const 8
      i32.add
      local.get 9
      local.get 8
      call $_ZN80_$LT$core..series..Series$LT$f32$GT$$u20$as$u20$core..convert..From$LT$T$GT$$GT$4from17h2b5121aec93578c9E
      local.get 2
      i32.const 96
      i32.add
      local.get 2
      i32.const 112
      i32.add
      local.get 2
      i32.const 128
      i32.add
      call $_ZN4core3ops83_$LT$impl$u20$core..ops..arith..Add$u20$for$u20$core..series..Series$LT$f32$GT$$GT$3add17ha857ff2e7d42036bE
      local.get 2
      i32.const 128
      i32.add
      local.get 2
      i32.const 96
      i32.add
      local.get 2
      i32.const 8
      i32.add
      call $_ZN4core3ops83_$LT$impl$u20$core..ops..arith..Add$u20$for$u20$core..series..Series$LT$f32$GT$$GT$3add17ha857ff2e7d42036bE
      local.get 2
      i32.load offset=128
      local.set 7
      i32.const 0
      local.set 5
      local.get 2
      i32.load offset=136
      local.tee 3
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17ha2c1a859907dfec3E
      local.set 4
      local.set 8
      local.get 2
      i32.const 0
      i32.store offset=16
      local.get 2
      local.get 4
      i32.store offset=12
      local.get 2
      local.get 8
      i32.store offset=8
      local.get 2
      i32.const 8
      i32.add
      local.get 3
      call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h33b65ac2de0dd8f6E
      local.get 6
      i32.const 255
      i32.and
      local.tee 20
      i32.const 1
      i32.and
      local.set 21
      local.get 1
      i32.const 255
      i32.and
      local.tee 22
      i32.const 1
      i32.and
      local.set 23
      local.get 0
      i32.const 255
      i32.and
      local.tee 24
      i32.const 1
      i32.and
      local.set 25
      local.get 19
      i32.const 255
      i32.and
      local.tee 19
      i32.const 1
      i32.and
      local.set 26
      local.get 3
      i32.const 3
      i32.shl
      local.set 0
      local.get 2
      i32.load offset=16
      local.tee 1
      i32.const 3
      i32.shl
      local.set 3
      local.get 2
      i32.load offset=8
      local.set 4
      block  ;; label = @2
        loop  ;; label = @3
          local.get 0
          local.get 5
          i32.eq
          br_if 1 (;@2;)
          block  ;; label = @4
            block  ;; label = @5
              local.get 7
              local.get 5
              i32.add
              local.tee 6
              i32.load
              br_if 0 (;@5;)
              i32.const 0
              local.set 8
              br 1 (;@4;)
            end
            i32.const 1
            local.set 8
            f32.const inf (;=inf;)
            local.set 27
            local.get 6
            i32.const 4
            i32.add
            f32.load
            local.tee 28
            f32.const 0x0p+0 (;=0;)
            f32.eq
            br_if 0 (;@4;)
            local.get 28
            f32.const 0x1.8p+1 (;=3;)
            f32.div
            local.set 27
          end
          local.get 4
          local.get 3
          i32.add
          local.tee 6
          local.get 8
          i32.store
          local.get 6
          i32.const 4
          i32.add
          local.get 27
          f32.store
          local.get 5
          i32.const 8
          i32.add
          local.set 5
          local.get 3
          i32.const 8
          i32.add
          local.set 3
          local.get 1
          i32.const 1
          i32.add
          local.set 1
          br 0 (;@3;)
        end
      end
      local.get 2
      i32.load offset=12
      local.set 29
      local.get 7
      local.get 2
      i32.load offset=132
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      i32.const 0
      local.set 6
      local.get 1
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h887a12da11f6a316E
      local.set 5
      local.set 8
      local.get 2
      i32.const 0
      i32.store offset=16
      local.get 2
      local.get 5
      i32.store offset=12
      local.get 2
      local.get 8
      i32.store offset=8
      local.get 26
      i32.const 0
      i32.ne
      local.set 0
      local.get 19
      i32.const 2
      i32.ne
      local.set 7
      local.get 25
      i32.const 0
      i32.ne
      local.set 19
      local.get 24
      i32.const 2
      i32.ne
      local.set 24
      local.get 23
      i32.const 0
      i32.ne
      local.set 23
      local.get 22
      i32.const 2
      i32.ne
      local.set 22
      local.get 21
      i32.const 0
      i32.ne
      local.set 21
      local.get 20
      i32.const 2
      i32.ne
      local.set 20
      block  ;; label = @2
        local.get 5
        local.get 1
        i32.ge_u
        br_if 0 (;@2;)
        local.get 2
        i32.const 8
        i32.add
        i32.const 0
        local.get 1
        call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$14grow_amortized17he5e3ed0132096fa9E
        call $_ZN5alloc7raw_vec14handle_reserve17hc1b6427a824c2669E
        local.get 2
        i32.load offset=16
        local.set 6
        local.get 2
        i32.load offset=8
        local.set 8
      end
      local.get 7
      local.get 0
      i32.and
      local.set 7
      local.get 24
      local.get 19
      i32.and
      local.set 19
      local.get 22
      local.get 23
      i32.and
      local.set 22
      local.get 20
      local.get 21
      i32.and
      local.set 0
      local.get 6
      i32.const 2
      i32.shl
      local.set 1
      local.get 4
      local.set 5
      block  ;; label = @2
        loop  ;; label = @3
          local.get 3
          i32.eqz
          br_if 1 (;@2;)
          local.get 8
          local.get 1
          i32.add
          local.get 5
          f32.load offset=4
          f32.const 0x0p+0 (;=0;)
          local.get 5
          i32.load
          select
          f32.store
          local.get 1
          i32.const 4
          i32.add
          local.set 1
          local.get 3
          i32.const -8
          i32.add
          local.set 3
          local.get 6
          i32.const 1
          i32.add
          local.set 6
          local.get 5
          i32.const 8
          i32.add
          local.set 5
          br 0 (;@3;)
        end
      end
      local.get 4
      local.get 29
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      local.get 2
      i32.load offset=8
      local.tee 3
      local.get 1
      i32.add
      i32.const -4
      i32.add
      i32.const 1048592
      local.get 6
      select
      f32.load
      local.set 27
      local.get 3
      local.get 2
      i32.load offset=12
      call $_ZN4core3ptr47drop_in_place$LT$alloc..vec..Vec$LT$f32$GT$$GT$17h5ba05a9c2fc58ac5E
      local.get 16
      local.get 15
      call $_ZN4core3ptr47drop_in_place$LT$alloc..vec..Vec$LT$f32$GT$$GT$17h5ba05a9c2fc58ac5E
      local.get 18
      local.get 14
      call $_ZN4core3ptr47drop_in_place$LT$alloc..vec..Vec$LT$f32$GT$$GT$17h5ba05a9c2fc58ac5E
      local.get 17
      local.get 13
      call $_ZN4core3ptr47drop_in_place$LT$alloc..vec..Vec$LT$f32$GT$$GT$17h5ba05a9c2fc58ac5E
      local.get 9
      local.get 12
      call $_ZN4core3ptr47drop_in_place$LT$alloc..vec..Vec$LT$f32$GT$$GT$17h5ba05a9c2fc58ac5E
      local.get 11
      local.get 10
      call $_ZN4core3ptr47drop_in_place$LT$alloc..vec..Vec$LT$f32$GT$$GT$17h5ba05a9c2fc58ac5E
      local.get 0
      i32.const 1
      i32.xor
      local.tee 3
      local.get 3
      i32.const 2
      i32.const 3
      i32.const 4
      local.get 7
      select
      local.get 19
      select
      local.get 22
      select
      local.get 0
      select
      local.set 7
    end
    local.get 2
    i32.const 144
    i32.add
    global.set $__stack_pointer
    local.get 7
    local.get 27)
  (func $_ZN5alloc11collections9vec_deque21VecDeque$LT$T$C$A$GT$4grow17hf36a8419da4188daE (type 2) (param i32)
    (local i32 i32 i32 i32 i32)
    local.get 0
    local.get 0
    i32.load offset=4
    local.tee 1
    call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$16reserve_for_push17h0a6f59455e94d109E
    block  ;; label = @1
      local.get 0
      i32.load offset=8
      local.tee 2
      local.get 1
      local.get 0
      i32.load offset=12
      local.tee 3
      i32.sub
      i32.le_u
      br_if 0 (;@1;)
      local.get 0
      i32.load offset=4
      local.set 4
      block  ;; label = @2
        block  ;; label = @3
          local.get 1
          local.get 2
          i32.sub
          local.tee 5
          local.get 3
          local.get 5
          i32.sub
          local.tee 3
          i32.le_u
          br_if 0 (;@3;)
          local.get 4
          local.get 1
          i32.sub
          local.get 3
          i32.ge_u
          br_if 1 (;@2;)
        end
        local.get 0
        i32.load
        local.tee 1
        local.get 4
        local.get 5
        i32.sub
        local.tee 3
        i32.const 20
        i32.mul
        i32.add
        local.get 1
        local.get 2
        i32.const 20
        i32.mul
        i32.add
        local.get 5
        i32.const 20
        i32.mul
        call $memmove
        drop
        local.get 0
        local.get 3
        i32.store offset=8
        return
      end
      local.get 0
      i32.load
      local.tee 0
      local.get 1
      i32.const 20
      i32.mul
      i32.add
      local.get 0
      local.get 3
      i32.const 20
      i32.mul
      call $memcpy
      drop
    end)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h887a12da11f6a316E (type 7) (param i32) (result i32 i32)
    (local i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        br_if 0 (;@2;)
        i32.const 4
        local.set 1
        br 1 (;@1;)
      end
      block  ;; label = @2
        local.get 0
        i32.const 536870911
        i32.gt_u
        br_if 0 (;@2;)
        local.get 0
        i32.const 2
        i32.shl
        local.tee 2
        i32.const -1
        i32.le_s
        br_if 0 (;@2;)
        local.get 0
        i32.const 536870912
        i32.lt_u
        i32.const 2
        i32.shl
        local.tee 3
        local.get 2
        call $_ZN5alloc5alloc6Global10alloc_impl17h1e7c53651c78c03dE
        drop
        local.tee 1
        br_if 1 (;@1;)
        local.get 3
        local.get 2
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
      unreachable
    end
    local.get 1
    local.get 0)
  (func $_ZN5alloc11collections9vec_deque21VecDeque$LT$T$C$A$GT$12slice_ranges17h771185e4c206a015E (type 9) (param i32 i32 i32 i32)
    (local i32)
    block  ;; label = @1
      local.get 3
      br_if 0 (;@1;)
      local.get 0
      i64.const 0
      i64.store align=4
      local.get 0
      i32.const 8
      i32.add
      i64.const 0
      i64.store align=4
      return
    end
    local.get 0
    local.get 2
    i32.const 0
    local.get 1
    local.get 2
    local.get 1
    i32.lt_u
    select
    i32.sub
    local.tee 2
    i32.store
    block  ;; label = @1
      local.get 1
      local.get 2
      i32.sub
      local.tee 4
      local.get 3
      i32.ge_u
      br_if 0 (;@1;)
      local.get 0
      i32.const 0
      i32.store offset=8
      local.get 0
      local.get 1
      i32.store offset=4
      local.get 0
      i32.const 12
      i32.add
      local.get 3
      local.get 4
      i32.sub
      i32.store
      return
    end
    local.get 0
    i64.const 0
    i64.store offset=8 align=4
    local.get 0
    local.get 2
    local.get 3
    i32.add
    i32.store offset=4)
  (func $_ZN5alloc3vec16Vec$LT$T$C$A$GT$4push17h015b00d50b87b785E (type 10) (param i32 f32)
    (local i32)
    block  ;; label = @1
      local.get 0
      i32.load offset=8
      local.tee 2
      local.get 0
      i32.load offset=4
      i32.ne
      br_if 0 (;@1;)
      local.get 0
      local.get 2
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$16reserve_for_push17h18cc450d3e0f18d4E
      local.get 0
      i32.load offset=8
      local.set 2
    end
    local.get 0
    local.get 2
    i32.const 1
    i32.add
    i32.store offset=8
    local.get 0
    i32.load
    local.get 2
    i32.const 2
    i32.shl
    i32.add
    local.get 1
    f32.store)
  (func $_ZN5trend3sma3sma17h7fceb42ba3154614E (type 9) (param i32 i32 i32 i32)
    (local i32 i32 i32 i32 i32 f32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 4
    global.set $__stack_pointer
    local.get 2
    call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17ha2c1a859907dfec3E
    local.set 6
    local.set 5
    local.get 4
    i32.const 0
    i32.store offset=24
    local.get 4
    local.get 6
    i32.store offset=20
    local.get 4
    local.get 5
    i32.store offset=16
    local.get 4
    i32.const 16
    i32.add
    local.get 2
    call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h33b65ac2de0dd8f6E
    local.get 2
    i32.const 2
    i32.shl
    local.set 5
    local.get 4
    i32.load offset=16
    local.tee 7
    local.get 4
    i32.load offset=24
    local.tee 8
    i32.const 3
    i32.shl
    i32.add
    local.set 2
    block  ;; label = @1
      loop  ;; label = @2
        local.get 5
        i32.eqz
        br_if 1 (;@1;)
        local.get 2
        i32.const 4
        i32.add
        local.get 1
        f32.load
        local.tee 9
        f32.store
        local.get 2
        local.get 9
        local.get 9
        f32.eq
        i32.store
        local.get 5
        i32.const -4
        i32.add
        local.set 5
        local.get 2
        i32.const 8
        i32.add
        local.set 2
        local.get 8
        i32.const 1
        i32.add
        local.set 8
        local.get 1
        i32.const 4
        i32.add
        local.set 1
        br 0 (;@2;)
      end
    end
    local.get 4
    i32.load offset=20
    local.set 10
    local.get 4
    local.get 8
    call $_ZN5alloc3vec9from_elem17h110bc7265e9c9318E
    local.get 4
    i32.const 16
    i32.add
    local.get 3
    call $_ZN5alloc3vec9from_elem17h110bc7265e9c9318E
    i32.const 0
    local.set 1
    local.get 4
    i32.load offset=8
    local.set 11
    local.get 4
    i32.load
    local.set 12
    local.get 4
    i32.load offset=24
    local.set 13
    local.get 4
    i32.load offset=16
    local.set 14
    i32.const 1
    local.set 6
    i32.const 0
    local.set 15
    block  ;; label = @1
      block  ;; label = @2
        loop  ;; label = @3
          local.get 8
          local.get 1
          i32.eq
          br_if 1 (;@2;)
          local.get 7
          local.get 1
          i32.const 3
          i32.shl
          i32.add
          local.tee 2
          i32.load
          local.set 5
          local.get 2
          f32.load offset=4
          local.set 9
          local.get 14
          local.get 13
          local.get 15
          i32.const 1053420
          call $_ZN84_$LT$alloc..vec..Vec$LT$T$C$A$GT$$u20$as$u20$core..ops..index..IndexMut$LT$I$GT$$GT$9index_mut17hc7aabc19decee266E
          local.tee 2
          local.get 9
          f32.store offset=4
          local.get 2
          local.get 5
          i32.store
          local.get 13
          local.get 1
          i32.const 1
          i32.add
          local.tee 16
          local.get 3
          local.get 16
          local.get 3
          i32.lt_u
          select
          local.tee 17
          i32.lt_u
          br_if 2 (;@1;)
          local.get 3
          local.get 6
          local.get 3
          local.get 6
          i32.lt_u
          select
          i32.const 3
          i32.shl
          local.set 5
          f32.const 0x0p+0 (;=0;)
          local.set 9
          local.get 14
          local.set 2
          block  ;; label = @4
            loop  ;; label = @5
              local.get 5
              i32.eqz
              br_if 1 (;@4;)
              local.get 9
              local.get 2
              f32.load offset=4
              f32.const -0x0p+0 (;=-0;)
              local.get 2
              i32.load
              select
              f32.add
              local.set 9
              local.get 5
              i32.const -8
              i32.add
              local.set 5
              local.get 2
              i32.const 8
              i32.add
              local.set 2
              br 0 (;@5;)
            end
          end
          local.get 12
          local.get 11
          local.get 1
          i32.const 1053452
          call $_ZN84_$LT$alloc..vec..Vec$LT$T$C$A$GT$$u20$as$u20$core..ops..index..IndexMut$LT$I$GT$$GT$9index_mut17hc7aabc19decee266E
          local.tee 2
          i32.const 1
          i32.store
          local.get 2
          local.get 9
          local.get 17
          f32.convert_i32_u
          f32.div
          f32.store offset=4
          block  ;; label = @4
            local.get 3
            i32.eqz
            br_if 0 (;@4;)
            local.get 6
            i32.const 1
            i32.add
            local.set 6
            local.get 15
            i32.const 1
            i32.add
            local.get 3
            i32.rem_u
            local.set 15
            local.get 16
            local.set 1
            br 1 (;@3;)
          end
        end
        i32.const 1053488
        i32.const 57
        i32.const 1053468
        call $_ZN4core9panicking5panic17hcfcdcc589d164b16E
        unreachable
      end
      local.get 0
      local.get 4
      i64.load
      i64.store align=4
      local.get 0
      i32.const 8
      i32.add
      local.get 4
      i32.const 8
      i32.add
      i32.load
      i32.store
      local.get 14
      local.get 4
      i32.load offset=20
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      local.get 7
      local.get 10
      call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
      local.get 4
      i32.const 32
      i32.add
      global.set $__stack_pointer
      return
    end
    local.get 17
    local.get 13
    i32.const 1053436
    call $_ZN4core5slice5index24slice_end_index_len_fail17he1e55bf2616238f7E
    unreachable)
  (func $_ZN4core4bool49_$LT$impl$u20$core..series..Series$LT$f32$GT$$GT$2gt17h1330ec5560ce6d0eE (type 11) (param i32 i32 i32 i32 i32)
    (local i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 5
    global.set $__stack_pointer
    local.get 5
    local.get 1
    local.get 1
    local.get 2
    i32.const 3
    i32.shl
    i32.add
    local.get 3
    local.get 4
    call $_ZN4core4iter6traits8iterator8Iterator3zip17hde5ecd6693b43225E
    local.get 5
    i32.load offset=20
    local.tee 2
    local.get 5
    i32.load offset=16
    local.tee 6
    i32.sub
    local.tee 1
    call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h0e522760e9448a1bE
    local.set 3
    local.set 4
    local.get 5
    local.get 3
    i32.store offset=36
    local.get 5
    local.get 4
    i32.store offset=32
    local.get 5
    i32.const 0
    i32.store offset=40
    local.get 5
    i32.load
    local.set 4
    local.get 5
    i32.load offset=8
    local.set 3
    local.get 5
    i32.const 32
    i32.add
    local.get 1
    call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h490bca4ea1fbb57cE
    i32.const 0
    local.get 1
    local.get 1
    local.get 2
    i32.gt_u
    select
    local.set 1
    local.get 6
    i32.const 3
    i32.shl
    local.set 6
    local.get 5
    i32.load offset=40
    local.set 2
    local.get 5
    i32.load offset=32
    local.set 7
    block  ;; label = @1
      loop  ;; label = @2
        local.get 1
        i32.eqz
        br_if 1 (;@1;)
        local.get 7
        local.get 2
        i32.add
        local.get 4
        local.get 6
        i32.add
        local.tee 8
        i32.const 4
        i32.add
        f32.load
        local.get 3
        local.get 6
        i32.add
        local.tee 9
        i32.const 4
        i32.add
        f32.load
        f32.gt
        i32.const 2
        local.get 9
        i32.load
        select
        i32.const 2
        local.get 8
        i32.load
        select
        i32.store8
        local.get 1
        i32.const -1
        i32.add
        local.set 1
        local.get 3
        i32.const 8
        i32.add
        local.set 3
        local.get 4
        i32.const 8
        i32.add
        local.set 4
        local.get 2
        i32.const 1
        i32.add
        local.set 2
        br 0 (;@2;)
      end
    end
    local.get 0
    local.get 5
    i64.load offset=32
    i64.store align=4
    local.get 0
    i32.const 8
    i32.add
    local.get 2
    i32.store
    local.get 5
    i32.const 48
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core6series15Series$LT$T$GT$5shift17h096cac452bc3fb0cE (type 12) (param i32 i32 i32)
    (local i32 i32 i32 i32 i32 f32 i64)
    global.get $__stack_pointer
    i32.const 96
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    i32.const 1
    i32.store offset=16
    local.get 3
    i32.const 0
    i32.store offset=8
    local.get 3
    local.get 2
    i32.const -1
    i32.add
    i32.store offset=28
    local.get 3
    local.get 1
    i32.store offset=20
    local.get 3
    local.get 1
    local.get 2
    i32.const 3
    i32.shl
    i32.add
    i32.store offset=24
    local.get 3
    i32.const 48
    i32.add
    local.get 3
    i32.const 8
    i32.add
    call $_ZN106_$LT$core..iter..adapters..chain..Chain$LT$A$C$B$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$9size_hint17h832c7bd1307a22d7E
    block  ;; label = @1
      local.get 3
      i32.load offset=52
      i32.eqz
      br_if 0 (;@1;)
      local.get 3
      i32.const 48
      i32.add
      i32.const 8
      i32.add
      local.tee 2
      i32.load
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17ha2c1a859907dfec3E
      local.set 4
      local.set 1
      local.get 3
      i32.const 0
      i32.store offset=40
      local.get 3
      local.get 4
      i32.store offset=36
      local.get 3
      local.get 1
      i32.store offset=32
      local.get 3
      i32.const 48
      i32.add
      i32.const 16
      i32.add
      local.get 3
      i32.const 8
      i32.add
      i32.const 16
      i32.add
      i64.load
      i64.store
      local.get 2
      local.get 3
      i32.const 8
      i32.add
      i32.const 8
      i32.add
      i64.load
      i64.store
      local.get 3
      local.get 3
      i64.load offset=8
      i64.store offset=48
      local.get 3
      i32.const 72
      i32.add
      local.get 3
      i32.const 48
      i32.add
      call $_ZN106_$LT$core..iter..adapters..chain..Chain$LT$A$C$B$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$9size_hint17h832c7bd1307a22d7E
      block  ;; label = @2
        local.get 3
        i32.load offset=76
        i32.eqz
        br_if 0 (;@2;)
        local.get 3
        i32.const 32
        i32.add
        local.get 3
        i32.const 72
        i32.add
        i32.const 8
        i32.add
        i32.load
        call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h33b65ac2de0dd8f6E
        local.get 3
        i32.load offset=60
        local.set 4
        local.get 3
        i32.load offset=40
        local.set 1
        local.get 3
        i32.load offset=32
        local.set 5
        block  ;; label = @3
          local.get 3
          i32.load offset=48
          local.tee 6
          i32.const 2
          i32.eq
          br_if 0 (;@3;)
          local.get 3
          i32.load offset=56
          local.tee 7
          i32.eqz
          br_if 0 (;@3;)
          local.get 5
          local.get 1
          i32.const 3
          i32.shl
          i32.add
          local.set 2
          local.get 3
          f32.load offset=52
          local.set 8
          loop  ;; label = @4
            local.get 2
            local.get 6
            i32.store
            local.get 2
            i32.const 4
            i32.add
            local.get 8
            f32.store
            local.get 2
            i32.const 8
            i32.add
            local.set 2
            local.get 1
            i32.const 1
            i32.add
            local.set 1
            local.get 7
            i32.const -1
            i32.add
            local.tee 7
            br_if 0 (;@4;)
          end
        end
        block  ;; label = @3
          local.get 4
          i32.eqz
          br_if 0 (;@3;)
          local.get 3
          i64.load offset=64
          local.tee 9
          i64.const 32
          i64.shr_u
          i32.wrap_i64
          local.tee 7
          i32.eqz
          br_if 0 (;@3;)
          local.get 9
          i32.wrap_i64
          local.set 6
          local.get 5
          local.get 1
          i32.const 3
          i32.shl
          i32.add
          local.set 2
          loop  ;; label = @4
            local.get 4
            local.get 6
            i32.eq
            br_if 1 (;@3;)
            local.get 2
            local.get 4
            i32.load
            i32.store
            local.get 2
            i32.const 4
            i32.add
            local.get 4
            i32.const 4
            i32.add
            f32.load
            f32.store
            local.get 4
            i32.const 8
            i32.add
            local.set 4
            local.get 2
            i32.const 8
            i32.add
            local.set 2
            local.get 1
            i32.const 1
            i32.add
            local.set 1
            local.get 7
            i32.const -1
            i32.add
            local.tee 7
            br_if 0 (;@4;)
          end
        end
        local.get 3
        i32.const 32
        i32.add
        i32.const 8
        i32.add
        local.get 1
        i32.store
        local.get 0
        i32.const 8
        i32.add
        local.get 1
        i32.store
        local.get 0
        local.get 3
        i64.load offset=32
        i64.store align=4
        local.get 3
        i32.const 96
        i32.add
        global.set $__stack_pointer
        return
      end
      local.get 3
      i32.const 84
      i32.add
      i64.const 0
      i64.store align=4
      local.get 3
      i32.const 1
      i32.store offset=76
      local.get 3
      i32.const 1053564
      i32.store offset=72
      local.get 3
      i32.const 1054164
      i32.store offset=80
      local.get 3
      i32.const 72
      i32.add
      i32.const 1053760
      call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
      unreachable
    end
    local.get 3
    i32.const 84
    i32.add
    i64.const 0
    i64.store align=4
    local.get 3
    i32.const 1
    i32.store offset=76
    local.get 3
    i32.const 1053564
    i32.store offset=72
    local.get 3
    i32.const 1054164
    i32.store offset=80
    local.get 3
    i32.const 72
    i32.add
    i32.const 1053668
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN4core4bool49_$LT$impl$u20$core..series..Series$LT$f32$GT$$GT$2lt17hea1df66b6255e5b8E (type 11) (param i32 i32 i32 i32 i32)
    (local i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 5
    global.set $__stack_pointer
    local.get 5
    local.get 1
    local.get 1
    local.get 2
    i32.const 3
    i32.shl
    i32.add
    local.get 3
    local.get 4
    call $_ZN4core4iter6traits8iterator8Iterator3zip17hde5ecd6693b43225E
    local.get 5
    i32.load offset=20
    local.tee 2
    local.get 5
    i32.load offset=16
    local.tee 6
    i32.sub
    local.tee 1
    call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h0e522760e9448a1bE
    local.set 3
    local.set 4
    local.get 5
    local.get 3
    i32.store offset=36
    local.get 5
    local.get 4
    i32.store offset=32
    local.get 5
    i32.const 0
    i32.store offset=40
    local.get 5
    i32.load
    local.set 4
    local.get 5
    i32.load offset=8
    local.set 3
    local.get 5
    i32.const 32
    i32.add
    local.get 1
    call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h490bca4ea1fbb57cE
    i32.const 0
    local.get 1
    local.get 1
    local.get 2
    i32.gt_u
    select
    local.set 1
    local.get 6
    i32.const 3
    i32.shl
    local.set 6
    local.get 5
    i32.load offset=40
    local.set 2
    local.get 5
    i32.load offset=32
    local.set 7
    block  ;; label = @1
      loop  ;; label = @2
        local.get 1
        i32.eqz
        br_if 1 (;@1;)
        local.get 7
        local.get 2
        i32.add
        local.get 4
        local.get 6
        i32.add
        local.tee 8
        i32.const 4
        i32.add
        f32.load
        local.get 3
        local.get 6
        i32.add
        local.tee 9
        i32.const 4
        i32.add
        f32.load
        f32.lt
        i32.const 2
        local.get 9
        i32.load
        select
        i32.const 2
        local.get 8
        i32.load
        select
        i32.store8
        local.get 1
        i32.const -1
        i32.add
        local.set 1
        local.get 3
        i32.const 8
        i32.add
        local.set 3
        local.get 4
        i32.const 8
        i32.add
        local.set 4
        local.get 2
        i32.const 1
        i32.add
        local.set 2
        br 0 (;@2;)
      end
    end
    local.get 0
    local.get 5
    i64.load offset=32
    i64.store align=4
    local.get 0
    i32.const 8
    i32.add
    local.get 2
    i32.store
    local.get 5
    i32.const 48
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core4bool85_$LT$impl$u20$core..ops..bit..BitAnd$u20$for$u20$core..series..Series$LT$bool$GT$$GT$6bitand17h9d98e97305c6c554E (type 12) (param i32 i32 i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 2
    i32.load
    local.set 4
    local.get 1
    i32.load
    local.set 5
    local.get 1
    i32.load offset=8
    local.tee 6
    local.get 2
    i32.load offset=8
    local.tee 7
    local.get 6
    local.get 7
    i32.lt_u
    select
    local.tee 8
    call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h0e522760e9448a1bE
    local.set 7
    local.set 6
    local.get 3
    i32.const 0
    i32.store offset=8
    local.get 3
    local.get 7
    i32.store offset=4
    local.get 3
    local.get 6
    i32.store
    local.get 3
    local.get 8
    call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h490bca4ea1fbb57cE
    local.get 3
    i32.load
    local.get 3
    i32.load offset=8
    local.tee 9
    i32.add
    local.set 10
    i32.const 0
    local.set 6
    block  ;; label = @1
      loop  ;; label = @2
        local.get 8
        local.get 6
        i32.eq
        br_if 1 (;@1;)
        local.get 10
        local.get 6
        i32.add
        i32.const 2
        i32.const 2
        local.get 5
        local.get 6
        i32.add
        i32.load8_u
        local.tee 7
        i32.const 0
        i32.ne
        local.get 4
        local.get 6
        i32.add
        i32.load8_u
        local.tee 11
        i32.const 0
        i32.ne
        i32.and
        local.get 11
        i32.const 2
        i32.eq
        select
        local.get 7
        i32.const 2
        i32.eq
        select
        i32.store8
        local.get 6
        i32.const 1
        i32.add
        local.set 6
        br 0 (;@2;)
      end
    end
    local.get 0
    local.get 3
    i64.load
    i64.store align=4
    local.get 0
    i32.const 8
    i32.add
    local.get 9
    local.get 6
    i32.add
    i32.store
    local.get 4
    local.get 2
    i32.const 4
    i32.add
    i32.load
    call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h3ad717a5de7f5611E
    local.get 5
    local.get 1
    i32.const 4
    i32.add
    i32.load
    call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h3ad717a5de7f5611E
    local.get 3
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE (type 3) (param i32 i32)
    block  ;; label = @1
      local.get 1
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      i32.const 3
      i32.shl
      call $_ZN63_$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$10deallocate17h61bf6a4893a1c41aE
    end)
  (func $_ZN4core6series15Series$LT$T$GT$5empty17h62d985689bde32feE (type 2) (param i32)
    (local i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    i32.const 1
    call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h0e522760e9448a1bE
    local.set 3
    local.set 2
    local.get 1
    i32.const 8
    i32.add
    local.tee 4
    i32.const 0
    i32.store
    local.get 1
    local.get 3
    i32.store offset=4
    local.get 1
    local.get 2
    i32.store
    local.get 1
    i32.const 1
    call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h490bca4ea1fbb57cE
    local.get 0
    local.get 1
    i64.load
    i64.store align=4
    local.get 1
    i32.load
    local.get 4
    i32.load
    local.tee 2
    i32.add
    i32.const 2
    i32.store8
    local.get 0
    i32.const 8
    i32.add
    local.get 2
    i32.const 1
    i32.add
    i32.store
    local.get 1
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN80_$LT$core..series..Series$LT$f32$GT$$u20$as$u20$core..convert..From$LT$T$GT$$GT$4from17h2b5121aec93578c9E (type 12) (param i32 i32 i32)
    (local i32 i32 i32 f32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 2
    call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17ha2c1a859907dfec3E
    local.set 5
    local.set 4
    local.get 3
    i32.const 0
    i32.store offset=8
    local.get 3
    local.get 5
    i32.store offset=4
    local.get 3
    local.get 4
    i32.store
    local.get 3
    local.get 2
    call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h33b65ac2de0dd8f6E
    local.get 2
    i32.const 2
    i32.shl
    local.set 4
    local.get 3
    i32.load
    local.get 3
    i32.load offset=8
    local.tee 5
    i32.const 3
    i32.shl
    i32.add
    local.set 2
    block  ;; label = @1
      loop  ;; label = @2
        local.get 4
        i32.eqz
        br_if 1 (;@1;)
        local.get 2
        i32.const 4
        i32.add
        local.get 1
        f32.load
        local.tee 6
        f32.store
        local.get 2
        local.get 6
        local.get 6
        f32.eq
        i32.store
        local.get 4
        i32.const -4
        i32.add
        local.set 4
        local.get 2
        i32.const 8
        i32.add
        local.set 2
        local.get 5
        i32.const 1
        i32.add
        local.set 5
        local.get 1
        i32.const 4
        i32.add
        local.set 1
        br 0 (;@2;)
      end
    end
    local.get 0
    local.get 3
    i64.load
    i64.store align=4
    local.get 0
    i32.const 8
    i32.add
    local.get 5
    i32.store
    local.get 3
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core3ops83_$LT$impl$u20$core..ops..arith..Add$u20$for$u20$core..series..Series$LT$f32$GT$$GT$3add17ha857ff2e7d42036bE (type 12) (param i32 i32 i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 f32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    local.get 1
    i32.load
    local.tee 4
    local.get 4
    local.get 1
    i32.load offset=8
    i32.const 3
    i32.shl
    i32.add
    local.get 2
    i32.load
    local.tee 5
    local.get 2
    i32.const 8
    i32.add
    i32.load
    call $_ZN4core4iter6traits8iterator8Iterator3zip17hde5ecd6693b43225E
    i32.const 0
    local.set 6
    local.get 3
    i32.load offset=20
    local.tee 7
    local.get 3
    i32.load offset=16
    local.tee 8
    i32.sub
    local.tee 9
    call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17ha2c1a859907dfec3E
    local.set 11
    local.set 10
    local.get 3
    i32.const 0
    i32.store offset=40
    local.get 3
    local.get 11
    i32.store offset=36
    local.get 3
    local.get 10
    i32.store offset=32
    local.get 3
    i32.load
    local.set 10
    local.get 3
    i32.load offset=8
    local.set 11
    local.get 3
    i32.const 32
    i32.add
    local.get 9
    call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h33b65ac2de0dd8f6E
    i32.const 0
    local.get 9
    local.get 9
    local.get 7
    i32.gt_u
    select
    local.set 9
    local.get 11
    local.get 8
    i32.const 3
    i32.shl
    local.tee 7
    i32.add
    local.set 12
    local.get 10
    local.get 7
    i32.add
    local.set 13
    local.get 3
    i32.load offset=32
    local.get 3
    i32.load offset=40
    local.tee 8
    i32.const 3
    i32.shl
    i32.add
    local.set 14
    block  ;; label = @1
      loop  ;; label = @2
        local.get 9
        i32.eqz
        br_if 1 (;@1;)
        i32.const 0
        local.set 7
        block  ;; label = @3
          block  ;; label = @4
            local.get 13
            local.get 6
            i32.add
            local.tee 10
            i32.load
            br_if 0 (;@4;)
            br 1 (;@3;)
          end
          local.get 12
          local.get 6
          i32.add
          local.tee 11
          i32.load
          i32.eqz
          br_if 0 (;@3;)
          local.get 10
          i32.const 4
          i32.add
          f32.load
          local.get 11
          i32.const 4
          i32.add
          f32.load
          f32.add
          local.set 15
          i32.const 1
          local.set 7
        end
        local.get 14
        local.get 6
        i32.add
        local.tee 10
        local.get 7
        i32.store
        local.get 10
        i32.const 4
        i32.add
        local.get 15
        f32.store
        local.get 9
        i32.const -1
        i32.add
        local.set 9
        local.get 6
        i32.const 8
        i32.add
        local.set 6
        local.get 8
        i32.const 1
        i32.add
        local.set 8
        br 0 (;@2;)
      end
    end
    local.get 0
    local.get 3
    i64.load offset=32
    i64.store align=4
    local.get 0
    i32.const 8
    i32.add
    local.get 8
    i32.store
    local.get 5
    local.get 2
    i32.const 4
    i32.add
    i32.load
    call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
    local.get 4
    local.get 1
    i32.const 4
    i32.add
    i32.load
    call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h556756e990b4e89eE
    local.get 3
    i32.const 48
    i32.add
    global.set $__stack_pointer)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17ha2c1a859907dfec3E (type 7) (param i32) (result i32 i32)
    (local i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        br_if 0 (;@2;)
        i32.const 4
        local.set 1
        br 1 (;@1;)
      end
      block  ;; label = @2
        local.get 0
        i32.const 268435455
        i32.gt_u
        br_if 0 (;@2;)
        local.get 0
        i32.const 3
        i32.shl
        local.tee 2
        i32.const -1
        i32.le_s
        br_if 0 (;@2;)
        local.get 0
        i32.const 268435456
        i32.lt_u
        i32.const 2
        i32.shl
        local.tee 3
        local.get 2
        call $_ZN5alloc5alloc6Global10alloc_impl17h1e7c53651c78c03dE
        drop
        local.tee 1
        br_if 1 (;@1;)
        local.get 3
        local.get 2
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
      unreachable
    end
    local.get 1
    local.get 0)
  (func $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h33b65ac2de0dd8f6E (type 3) (param i32 i32)
    (local i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      local.get 0
      i32.load offset=4
      local.tee 3
      local.get 0
      i32.load offset=8
      local.tee 4
      i32.sub
      local.get 1
      i32.ge_u
      br_if 0 (;@1;)
      i32.const 0
      local.set 5
      block  ;; label = @2
        local.get 4
        local.get 1
        i32.add
        local.tee 1
        local.get 4
        i32.lt_u
        br_if 0 (;@2;)
        local.get 3
        i32.const 1
        i32.shl
        local.tee 4
        local.get 1
        local.get 4
        local.get 1
        i32.gt_u
        select
        local.tee 1
        i32.const 4
        local.get 1
        i32.const 4
        i32.gt_u
        select
        local.tee 1
        i32.const 3
        i32.shl
        local.set 4
        local.get 1
        i32.const 268435456
        i32.lt_u
        i32.const 2
        i32.shl
        local.set 5
        block  ;; label = @3
          block  ;; label = @4
            local.get 3
            i32.eqz
            br_if 0 (;@4;)
            local.get 2
            i32.const 4
            i32.store offset=20
            local.get 2
            local.get 3
            i32.const 3
            i32.shl
            i32.store offset=24
            local.get 2
            local.get 0
            i32.load
            i32.store offset=16
            br 1 (;@3;)
          end
          local.get 2
          i32.const 0
          i32.store offset=20
        end
        local.get 2
        local.get 5
        local.get 4
        local.get 2
        i32.const 16
        i32.add
        call $_ZN5alloc7raw_vec11finish_grow17h4de5cd6636d1bdb9E
        local.get 2
        i32.load offset=4
        local.set 5
        block  ;; label = @3
          local.get 2
          i32.load
          i32.eqz
          br_if 0 (;@3;)
          local.get 2
          i32.const 8
          i32.add
          i32.load
          local.set 1
          br 1 (;@2;)
        end
        local.get 0
        local.get 1
        i32.store offset=4
        local.get 0
        local.get 5
        i32.store
        i32.const -2147483647
        local.set 5
      end
      local.get 5
      local.get 1
      call $_ZN5alloc7raw_vec14handle_reserve17hc1b6427a824c2669E
    end
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$14grow_amortized17he5e3ed0132096fa9E (type 13) (param i32 i32 i32) (result i32 i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    i32.const 0
    local.set 4
    block  ;; label = @1
      local.get 1
      local.get 2
      i32.add
      local.tee 2
      local.get 1
      i32.lt_u
      br_if 0 (;@1;)
      local.get 0
      i32.load offset=4
      local.tee 1
      i32.const 1
      i32.shl
      local.tee 4
      local.get 2
      local.get 4
      local.get 2
      i32.gt_u
      select
      local.tee 2
      i32.const 4
      local.get 2
      i32.const 4
      i32.gt_u
      select
      local.tee 2
      i32.const 2
      i32.shl
      local.set 4
      local.get 2
      i32.const 536870912
      i32.lt_u
      i32.const 2
      i32.shl
      local.set 5
      block  ;; label = @2
        block  ;; label = @3
          local.get 1
          i32.eqz
          br_if 0 (;@3;)
          local.get 3
          i32.const 4
          i32.store offset=20
          local.get 3
          local.get 1
          i32.const 2
          i32.shl
          i32.store offset=24
          local.get 3
          local.get 0
          i32.load
          i32.store offset=16
          br 1 (;@2;)
        end
        local.get 3
        i32.const 0
        i32.store offset=20
      end
      local.get 3
      local.get 5
      local.get 4
      local.get 3
      i32.const 16
      i32.add
      call $_ZN5alloc7raw_vec11finish_grow17h4de5cd6636d1bdb9E
      local.get 3
      i32.load offset=4
      local.set 4
      block  ;; label = @2
        local.get 3
        i32.load
        i32.eqz
        br_if 0 (;@2;)
        local.get 3
        i32.const 8
        i32.add
        i32.load
        local.set 2
        br 1 (;@1;)
      end
      local.get 0
      local.get 2
      i32.store offset=4
      local.get 0
      local.get 4
      i32.store
      i32.const -2147483647
      local.set 4
    end
    local.get 3
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 4
    local.get 2)
  (func $_ZN5alloc7raw_vec14handle_reserve17hc1b6427a824c2669E (type 3) (param i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.const -2147483647
        i32.eq
        br_if 0 (;@2;)
        local.get 0
        i32.eqz
        br_if 1 (;@1;)
        local.get 0
        local.get 1
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      return
    end
    call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
    unreachable)
  (func $__rust_alloc (type 1) (param i32 i32) (result i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 8
        i32.gt_u
        br_if 0 (;@2;)
        local.get 1
        local.get 0
        i32.le_u
        br_if 1 (;@1;)
      end
      local.get 1
      local.get 0
      call $aligned_alloc
      return
    end
    local.get 0
    call $malloc)
  (func $__rust_realloc (type 8) (param i32 i32 i32 i32) (result i32)
    block  ;; label = @1
      local.get 2
      local.get 3
      i32.le_u
      br_if 0 (;@1;)
      block  ;; label = @2
        local.get 2
        local.get 3
        call $aligned_alloc
        local.tee 2
        br_if 0 (;@2;)
        i32.const 0
        return
      end
      local.get 2
      local.get 0
      local.get 1
      local.get 3
      local.get 1
      local.get 3
      i32.lt_u
      select
      call $memcpy
      local.set 3
      local.get 0
      call $free
      local.get 3
      return
    end
    local.get 0
    local.get 3
    call $realloc)
  (func $__rust_alloc_error_handler (type 3) (param i32 i32)
    local.get 0
    local.get 1
    call $__rg_oom
    unreachable)
  (func $__rg_oom (type 3) (param i32 i32)
    local.get 1
    local.get 0
    call $_ZN3std5alloc8rust_oom17hb6ef0decd08a2b9fE
    unreachable)
  (func $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE (type 14)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 0
    global.set $__stack_pointer
    local.get 0
    i32.const 20
    i32.add
    i64.const 0
    i64.store align=4
    local.get 0
    i32.const 1
    i32.store offset=12
    local.get 0
    i32.const 1053564
    i32.store offset=8
    local.get 0
    i32.const 1054164
    i32.store offset=16
    local.get 0
    i32.const 8
    i32.add
    i32.const 1048648
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE (type 3) (param i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    local.get 0
    i32.store offset=20
    local.get 2
    i32.const 1049872
    i32.store offset=12
    local.get 2
    i32.const 1054164
    i32.store offset=8
    local.get 2
    i32.const 1
    i32.store8 offset=24
    local.get 2
    local.get 1
    i32.store offset=16
    local.get 2
    i32.const 8
    i32.add
    call $rust_begin_unwind
    unreachable)
  (func $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E (type 3) (param i32 i32)
    local.get 0
    local.get 1
    call $_ZN5alloc5alloc18handle_alloc_error8rt_error17hb1ca29683faa63daE
    unreachable)
  (func $_ZN5alloc5alloc18handle_alloc_error8rt_error17hb1ca29683faa63daE (type 3) (param i32 i32)
    local.get 1
    local.get 0
    call $__rust_alloc_error_handler
    unreachable)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$7reserve21do_reserve_and_handle17ha08d108f93397c99E (type 12) (param i32 i32 i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        local.get 2
        i32.add
        local.tee 2
        local.get 1
        i32.lt_u
        br_if 0 (;@2;)
        local.get 0
        i32.const 4
        i32.add
        i32.load
        local.tee 1
        i32.const 1
        i32.shl
        local.tee 4
        local.get 2
        local.get 4
        local.get 2
        i32.gt_u
        select
        local.tee 2
        i32.const 8
        local.get 2
        i32.const 8
        i32.gt_u
        select
        local.tee 2
        i32.const -1
        i32.xor
        i32.const 31
        i32.shr_u
        local.set 4
        block  ;; label = @3
          block  ;; label = @4
            local.get 1
            i32.eqz
            br_if 0 (;@4;)
            local.get 3
            local.get 1
            i32.store offset=24
            local.get 3
            i32.const 1
            i32.store offset=20
            local.get 3
            local.get 0
            i32.load
            i32.store offset=16
            br 1 (;@3;)
          end
          local.get 3
          i32.const 0
          i32.store offset=20
        end
        local.get 3
        local.get 4
        local.get 2
        local.get 3
        i32.const 16
        i32.add
        call $_ZN5alloc7raw_vec11finish_grow17h194894b6c287375cE
        local.get 3
        i32.load offset=4
        local.set 1
        block  ;; label = @3
          local.get 3
          i32.load
          br_if 0 (;@3;)
          local.get 0
          local.get 1
          i32.store
          local.get 0
          i32.const 4
          i32.add
          local.get 2
          i32.store
          br 2 (;@1;)
        end
        local.get 1
        i32.const -2147483647
        i32.eq
        br_if 1 (;@1;)
        local.get 1
        i32.eqz
        br_if 0 (;@2;)
        local.get 1
        local.get 3
        i32.const 8
        i32.add
        i32.load
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
      unreachable
    end
    local.get 3
    i32.const 32
    i32.add
    global.set $__stack_pointer)
  (func $_ZN5alloc7raw_vec11finish_grow17h194894b6c287375cE (type 9) (param i32 i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.eqz
        br_if 0 (;@2;)
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    local.get 2
                    i32.const -1
                    i32.le_s
                    br_if 0 (;@8;)
                    local.get 3
                    i32.load offset=4
                    br_if 1 (;@7;)
                    local.get 2
                    br_if 2 (;@6;)
                    i32.const 1
                    local.set 1
                    br 4 (;@4;)
                  end
                  local.get 0
                  i32.const 0
                  i32.store offset=4
                  br 6 (;@1;)
                end
                block  ;; label = @7
                  local.get 3
                  i32.const 8
                  i32.add
                  i32.load
                  local.tee 1
                  br_if 0 (;@7;)
                  block  ;; label = @8
                    local.get 2
                    br_if 0 (;@8;)
                    i32.const 1
                    local.set 1
                    br 4 (;@4;)
                  end
                  i32.const 0
                  i32.load8_u offset=1059320
                  drop
                  local.get 2
                  i32.const 1
                  call $__rust_alloc
                  local.set 1
                  br 2 (;@5;)
                end
                local.get 3
                i32.load
                local.get 1
                i32.const 1
                local.get 2
                call $__rust_realloc
                local.set 1
                br 1 (;@5;)
              end
              i32.const 0
              i32.load8_u offset=1059320
              drop
              local.get 2
              i32.const 1
              call $__rust_alloc
              local.set 1
            end
            local.get 1
            i32.eqz
            br_if 1 (;@3;)
          end
          local.get 0
          local.get 1
          i32.store offset=4
          local.get 0
          i32.const 8
          i32.add
          local.get 2
          i32.store
          local.get 0
          i32.const 0
          i32.store
          return
        end
        local.get 0
        i32.const 1
        i32.store offset=4
        local.get 0
        i32.const 8
        i32.add
        local.get 2
        i32.store
        local.get 0
        i32.const 1
        i32.store
        return
      end
      local.get 0
      i32.const 0
      i32.store offset=4
      local.get 0
      i32.const 8
      i32.add
      local.get 2
      i32.store
    end
    local.get 0
    i32.const 1
    i32.store)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$16reserve_for_push17h9a10d9e751dc77acE (type 3) (param i32 i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 1
        i32.add
        local.tee 1
        i32.eqz
        br_if 0 (;@2;)
        local.get 0
        i32.const 4
        i32.add
        i32.load
        local.tee 3
        i32.const 1
        i32.shl
        local.tee 4
        local.get 1
        local.get 4
        local.get 1
        i32.gt_u
        select
        local.tee 1
        i32.const 8
        local.get 1
        i32.const 8
        i32.gt_u
        select
        local.tee 1
        i32.const -1
        i32.xor
        i32.const 31
        i32.shr_u
        local.set 4
        block  ;; label = @3
          block  ;; label = @4
            local.get 3
            i32.eqz
            br_if 0 (;@4;)
            local.get 2
            local.get 3
            i32.store offset=24
            local.get 2
            i32.const 1
            i32.store offset=20
            local.get 2
            local.get 0
            i32.load
            i32.store offset=16
            br 1 (;@3;)
          end
          local.get 2
          i32.const 0
          i32.store offset=20
        end
        local.get 2
        local.get 4
        local.get 1
        local.get 2
        i32.const 16
        i32.add
        call $_ZN5alloc7raw_vec11finish_grow17h194894b6c287375cE
        local.get 2
        i32.load offset=4
        local.set 3
        block  ;; label = @3
          local.get 2
          i32.load
          br_if 0 (;@3;)
          local.get 0
          local.get 3
          i32.store
          local.get 0
          i32.const 4
          i32.add
          local.get 1
          i32.store
          br 2 (;@1;)
        end
        local.get 3
        i32.const -2147483647
        i32.eq
        br_if 1 (;@1;)
        local.get 3
        i32.eqz
        br_if 0 (;@2;)
        local.get 3
        local.get 2
        i32.const 8
        i32.add
        i32.load
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
      unreachable
    end
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core3fmt5write17h8253e306f6bd0e19E (type 0) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    i32.const 32
    i32.add
    local.get 1
    i32.store
    local.get 3
    i32.const 3
    i32.store8 offset=40
    local.get 3
    i32.const 32
    i32.store offset=24
    i32.const 0
    local.set 4
    local.get 3
    i32.const 0
    i32.store offset=36
    local.get 3
    local.get 0
    i32.store offset=28
    local.get 3
    i32.const 0
    i32.store offset=16
    local.get 3
    i32.const 0
    i32.store offset=8
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            local.get 2
            i32.load offset=16
            local.tee 5
            br_if 0 (;@4;)
            local.get 2
            i32.const 12
            i32.add
            i32.load
            local.tee 0
            i32.eqz
            br_if 1 (;@3;)
            local.get 2
            i32.load offset=8
            local.set 1
            local.get 0
            i32.const 3
            i32.shl
            local.set 6
            local.get 0
            i32.const -1
            i32.add
            i32.const 536870911
            i32.and
            i32.const 1
            i32.add
            local.set 4
            local.get 2
            i32.load
            local.set 0
            loop  ;; label = @5
              block  ;; label = @6
                local.get 0
                i32.const 4
                i32.add
                i32.load
                local.tee 7
                i32.eqz
                br_if 0 (;@6;)
                local.get 3
                i32.load offset=28
                local.get 0
                i32.load
                local.get 7
                local.get 3
                i32.load offset=32
                i32.load offset=12
                call_indirect (type 0)
                br_if 4 (;@2;)
              end
              local.get 1
              i32.load
              local.get 3
              i32.const 8
              i32.add
              local.get 1
              i32.const 4
              i32.add
              i32.load
              call_indirect (type 1)
              br_if 3 (;@2;)
              local.get 1
              i32.const 8
              i32.add
              local.set 1
              local.get 0
              i32.const 8
              i32.add
              local.set 0
              local.get 6
              i32.const -8
              i32.add
              local.tee 6
              br_if 0 (;@5;)
              br 2 (;@3;)
            end
          end
          local.get 2
          i32.const 20
          i32.add
          i32.load
          local.tee 1
          i32.eqz
          br_if 0 (;@3;)
          local.get 1
          i32.const 5
          i32.shl
          local.set 8
          local.get 1
          i32.const -1
          i32.add
          i32.const 134217727
          i32.and
          i32.const 1
          i32.add
          local.set 4
          local.get 2
          i32.load
          local.set 0
          i32.const 0
          local.set 6
          loop  ;; label = @4
            block  ;; label = @5
              local.get 0
              i32.const 4
              i32.add
              i32.load
              local.tee 1
              i32.eqz
              br_if 0 (;@5;)
              local.get 3
              i32.load offset=28
              local.get 0
              i32.load
              local.get 1
              local.get 3
              i32.load offset=32
              i32.load offset=12
              call_indirect (type 0)
              br_if 3 (;@2;)
            end
            local.get 3
            local.get 5
            local.get 6
            i32.add
            local.tee 1
            i32.const 16
            i32.add
            i32.load
            i32.store offset=24
            local.get 3
            local.get 1
            i32.const 28
            i32.add
            i32.load8_u
            i32.store8 offset=40
            local.get 3
            local.get 1
            i32.const 24
            i32.add
            i32.load
            i32.store offset=36
            local.get 1
            i32.const 12
            i32.add
            i32.load
            local.set 9
            local.get 2
            i32.load offset=8
            local.set 10
            i32.const 0
            local.set 11
            i32.const 0
            local.set 7
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  local.get 1
                  i32.const 8
                  i32.add
                  i32.load
                  br_table 1 (;@6;) 0 (;@7;) 2 (;@5;) 1 (;@6;)
                end
                local.get 9
                i32.const 3
                i32.shl
                local.set 12
                i32.const 0
                local.set 7
                local.get 10
                local.get 12
                i32.add
                local.tee 12
                i32.load offset=4
                i32.const 3
                i32.ne
                br_if 1 (;@5;)
                local.get 12
                i32.load
                i32.load
                local.set 9
              end
              i32.const 1
              local.set 7
            end
            local.get 3
            local.get 9
            i32.store offset=12
            local.get 3
            local.get 7
            i32.store offset=8
            local.get 1
            i32.const 4
            i32.add
            i32.load
            local.set 7
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  local.get 1
                  i32.load
                  br_table 1 (;@6;) 0 (;@7;) 2 (;@5;) 1 (;@6;)
                end
                local.get 7
                i32.const 3
                i32.shl
                local.set 9
                local.get 10
                local.get 9
                i32.add
                local.tee 9
                i32.load offset=4
                i32.const 3
                i32.ne
                br_if 1 (;@5;)
                local.get 9
                i32.load
                i32.load
                local.set 7
              end
              i32.const 1
              local.set 11
            end
            local.get 3
            local.get 7
            i32.store offset=20
            local.get 3
            local.get 11
            i32.store offset=16
            local.get 10
            local.get 1
            i32.const 20
            i32.add
            i32.load
            i32.const 3
            i32.shl
            i32.add
            local.tee 1
            i32.load
            local.get 3
            i32.const 8
            i32.add
            local.get 1
            i32.load offset=4
            call_indirect (type 1)
            br_if 2 (;@2;)
            local.get 0
            i32.const 8
            i32.add
            local.set 0
            local.get 8
            local.get 6
            i32.const 32
            i32.add
            local.tee 6
            i32.ne
            br_if 0 (;@4;)
          end
        end
        block  ;; label = @3
          local.get 4
          local.get 2
          i32.load offset=4
          i32.ge_u
          br_if 0 (;@3;)
          local.get 3
          i32.load offset=28
          local.get 2
          i32.load
          local.get 4
          i32.const 3
          i32.shl
          i32.add
          local.tee 1
          i32.load
          local.get 1
          i32.load offset=4
          local.get 3
          i32.load offset=32
          i32.load offset=12
          call_indirect (type 0)
          br_if 1 (;@2;)
        end
        i32.const 0
        local.set 1
        br 1 (;@1;)
      end
      i32.const 1
      local.set 1
    end
    local.get 3
    i32.const 48
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core6result13unwrap_failed17hfefb3e75b68d8f8cE (type 11) (param i32 i32 i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 64
    i32.sub
    local.tee 5
    global.set $__stack_pointer
    local.get 5
    local.get 1
    i32.store offset=12
    local.get 5
    local.get 0
    i32.store offset=8
    local.get 5
    local.get 3
    i32.store offset=20
    local.get 5
    local.get 2
    i32.store offset=16
    local.get 5
    i32.const 24
    i32.add
    i32.const 12
    i32.add
    i64.const 2
    i64.store align=4
    local.get 5
    i32.const 48
    i32.add
    i32.const 12
    i32.add
    i32.const 4
    i32.store
    local.get 5
    i32.const 2
    i32.store offset=28
    local.get 5
    i32.const 1050088
    i32.store offset=24
    local.get 5
    i32.const 5
    i32.store offset=52
    local.get 5
    local.get 5
    i32.const 48
    i32.add
    i32.store offset=32
    local.get 5
    local.get 5
    i32.const 16
    i32.add
    i32.store offset=56
    local.get 5
    local.get 5
    i32.const 8
    i32.add
    i32.store offset=48
    local.get 5
    i32.const 24
    i32.add
    local.get 4
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h888e990a606ca8ccE (type 0) (param i32 i32 i32) (result i32)
    (local i32)
    block  ;; label = @1
      local.get 0
      i32.load
      local.tee 0
      i32.load offset=4
      local.get 0
      i32.load offset=8
      local.tee 3
      i32.sub
      local.get 2
      i32.ge_u
      br_if 0 (;@1;)
      local.get 0
      local.get 3
      local.get 2
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$7reserve21do_reserve_and_handle17ha08d108f93397c99E
      local.get 0
      i32.load offset=8
      local.set 3
    end
    local.get 0
    i32.load
    local.get 3
    i32.add
    local.get 1
    local.get 2
    call $memcpy
    drop
    local.get 0
    local.get 3
    local.get 2
    i32.add
    i32.store offset=8
    i32.const 0)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17h4767d155bdd14fe0E (type 1) (param i32 i32) (result i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 127
        i32.gt_u
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 0
          i32.load offset=8
          local.tee 3
          local.get 0
          i32.load offset=4
          i32.ne
          br_if 0 (;@3;)
          local.get 0
          local.get 3
          call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$16reserve_for_push17h9a10d9e751dc77acE
          local.get 0
          i32.load offset=8
          local.set 3
        end
        local.get 0
        local.get 3
        i32.const 1
        i32.add
        i32.store offset=8
        local.get 0
        i32.load
        local.get 3
        i32.add
        local.get 1
        i32.store8
        br 1 (;@1;)
      end
      local.get 2
      i32.const 0
      i32.store offset=12
      block  ;; label = @2
        block  ;; label = @3
          local.get 1
          i32.const 2048
          i32.lt_u
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 1
            i32.const 65536
            i32.lt_u
            br_if 0 (;@4;)
            local.get 2
            local.get 1
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=15
            local.get 2
            local.get 1
            i32.const 6
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=14
            local.get 2
            local.get 1
            i32.const 12
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=13
            local.get 2
            local.get 1
            i32.const 18
            i32.shr_u
            i32.const 7
            i32.and
            i32.const 240
            i32.or
            i32.store8 offset=12
            i32.const 4
            local.set 1
            br 2 (;@2;)
          end
          local.get 2
          local.get 1
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=14
          local.get 2
          local.get 1
          i32.const 12
          i32.shr_u
          i32.const 224
          i32.or
          i32.store8 offset=12
          local.get 2
          local.get 1
          i32.const 6
          i32.shr_u
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=13
          i32.const 3
          local.set 1
          br 1 (;@2;)
        end
        local.get 2
        local.get 1
        i32.const 63
        i32.and
        i32.const 128
        i32.or
        i32.store8 offset=13
        local.get 2
        local.get 1
        i32.const 6
        i32.shr_u
        i32.const 192
        i32.or
        i32.store8 offset=12
        i32.const 2
        local.set 1
      end
      block  ;; label = @2
        local.get 0
        i32.load offset=4
        local.get 0
        i32.load offset=8
        local.tee 3
        i32.sub
        local.get 1
        i32.ge_u
        br_if 0 (;@2;)
        local.get 0
        local.get 3
        local.get 1
        call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$7reserve21do_reserve_and_handle17ha08d108f93397c99E
        local.get 0
        i32.load offset=8
        local.set 3
      end
      local.get 0
      i32.load
      local.get 3
      i32.add
      local.get 2
      i32.const 12
      i32.add
      local.get 1
      call $memcpy
      drop
      local.get 0
      local.get 3
      local.get 1
      i32.add
      i32.store offset=8
    end
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer
    i32.const 0)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17hb6baedc2fce95264E (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    local.get 0
    i32.store offset=4
    local.get 2
    i32.const 4
    i32.add
    i32.const 1048596
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 1
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN9hashbrown3raw22RawTableInner$LT$A$GT$15allocation_info17hfe639f5aa4fa5af7E (type 12) (param i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    local.get 2
    i32.const 1
    i32.add
    call $_ZN9hashbrown3raw11TableLayout20calculate_layout_for17h19a4715bf615a86aE
    local.get 3
    i32.load offset=8
    local.set 2
    local.get 0
    local.get 3
    i64.load
    i64.store offset=4 align=4
    local.get 0
    local.get 1
    local.get 2
    i32.sub
    i32.store
    local.get 3
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN9hashbrown3raw11TableLayout20calculate_layout_for17h19a4715bf615a86aE (type 3) (param i32 i32)
    (local i64 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i64.extend_i32_u
        i64.const 12
        i64.mul
        local.tee 2
        i64.const 32
        i64.shr_u
        i32.wrap_i64
        br_if 0 (;@2;)
        local.get 2
        i32.wrap_i64
        local.tee 3
        i32.const 7
        i32.add
        local.tee 4
        local.get 3
        i32.ge_u
        br_if 1 (;@1;)
      end
      local.get 0
      i32.const 0
      i32.store
      return
    end
    block  ;; label = @1
      local.get 1
      local.get 4
      i32.const -8
      i32.and
      local.tee 3
      i32.add
      i32.const 8
      i32.add
      local.tee 1
      local.get 3
      i32.lt_u
      br_if 0 (;@1;)
      block  ;; label = @2
        local.get 1
        i32.const 2147483640
        i32.gt_u
        br_if 0 (;@2;)
        local.get 0
        local.get 3
        i32.store offset=8
        local.get 0
        local.get 1
        i32.store offset=4
        local.get 0
        i32.const 8
        i32.store
        return
      end
      local.get 0
      i32.const 0
      i32.store
      return
    end
    local.get 0
    i32.const 0
    i32.store)
  (func $_ZN9hashbrown3raw21RawTable$LT$T$C$A$GT$14reserve_rehash17h3de690f35e59502cE (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i64 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    local.get 1
    i32.store offset=12
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            local.get 0
            i32.load offset=12
            local.tee 3
            i32.const 1
            i32.add
            local.tee 1
            i32.eqz
            br_if 0 (;@4;)
            local.get 1
            local.get 0
            i32.const 4
            i32.add
            i32.load
            local.tee 4
            local.get 4
            i32.const 1
            i32.add
            local.tee 5
            i32.const 3
            i32.shr_u
            i32.const 7
            i32.mul
            local.get 4
            i32.const 8
            i32.lt_u
            select
            local.tee 6
            i32.const 1
            i32.shr_u
            i32.le_u
            br_if 2 (;@2;)
            block  ;; label = @5
              block  ;; label = @6
                local.get 1
                local.get 6
                i32.const 1
                i32.add
                local.tee 7
                local.get 1
                local.get 7
                i32.gt_u
                select
                local.tee 7
                i32.const 8
                i32.lt_u
                br_if 0 (;@6;)
                local.get 7
                i32.const 536870912
                i32.ge_u
                br_if 2 (;@4;)
                i32.const 1
                local.set 1
                local.get 7
                i32.const 3
                i32.shl
                local.tee 7
                i32.const 14
                i32.lt_u
                br_if 1 (;@5;)
                i32.const -1
                local.get 7
                i32.const 7
                i32.div_u
                i32.const -1
                i32.add
                i32.clz
                i32.shr_u
                i32.const 1
                i32.add
                local.set 1
                br 1 (;@5;)
              end
              i32.const 4
              i32.const 8
              local.get 7
              i32.const 4
              i32.lt_u
              select
              local.set 1
            end
            local.get 2
            i32.const 16
            i32.add
            local.get 1
            call $_ZN9hashbrown3raw11TableLayout20calculate_layout_for17h19a4715bf615a86aE
            local.get 2
            i32.load offset=16
            local.tee 8
            i32.eqz
            br_if 0 (;@4;)
            local.get 2
            i32.load offset=24
            local.set 9
            block  ;; label = @5
              block  ;; label = @6
                local.get 2
                i32.load offset=20
                local.tee 10
                br_if 0 (;@6;)
                local.get 8
                local.set 7
                br 1 (;@5;)
              end
              i32.const 0
              i32.load8_u offset=1059320
              drop
              local.get 10
              local.get 8
              call $__rust_alloc
              local.set 7
            end
            local.get 7
            i32.eqz
            br_if 1 (;@3;)
            local.get 7
            local.get 9
            i32.add
            i32.const 255
            local.get 1
            i32.const 8
            i32.add
            call $memset
            local.set 8
            local.get 1
            i32.const -1
            i32.add
            local.tee 11
            local.get 1
            i32.const 3
            i32.shr_u
            i32.const 7
            i32.mul
            local.get 11
            i32.const 8
            i32.lt_u
            select
            local.set 5
            local.get 4
            i32.const 1
            i32.add
            local.set 12
            local.get 0
            i32.load
            local.set 9
            i32.const -12
            local.set 7
            i32.const 0
            local.set 1
            loop  ;; label = @5
              block  ;; label = @6
                local.get 12
                local.get 1
                i32.ne
                br_if 0 (;@6;)
                local.get 0
                local.get 8
                i32.store
                local.get 0
                local.get 5
                local.get 3
                i32.sub
                i32.store offset=8
                local.get 0
                i32.const 4
                i32.add
                local.get 11
                i32.store
                local.get 4
                i32.eqz
                br_if 5 (;@1;)
                local.get 2
                i32.const 16
                i32.add
                local.get 9
                local.get 4
                call $_ZN9hashbrown3raw22RawTableInner$LT$A$GT$15allocation_info17hfe639f5aa4fa5af7E
                local.get 2
                i32.load offset=16
                local.get 2
                i32.const 24
                i32.add
                i32.load
                call $_ZN63_$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$10deallocate17h61bf6a4893a1c41aE
                br 5 (;@1;)
              end
              block  ;; label = @6
                local.get 9
                local.get 1
                i32.add
                i32.load8_s
                i32.const 0
                i32.lt_s
                br_if 0 (;@6;)
                local.get 8
                local.get 8
                local.get 11
                local.get 2
                i32.const 12
                i32.add
                local.get 9
                local.get 1
                call $_ZN9hashbrown3raw21RawTable$LT$T$C$A$GT$14reserve_rehash28_$u7b$$u7b$closure$u7d$$u7d$17h00e9adfcff15ac28E
                local.tee 13
                call $_ZN9hashbrown3raw22RawTableInner$LT$A$GT$16find_insert_slot17hebb2e2228b09aef2E
                local.tee 10
                i32.add
                local.get 13
                i32.wrap_i64
                i32.const 25
                i32.shr_u
                local.tee 14
                i32.store8
                local.get 11
                local.get 10
                i32.const -8
                i32.add
                i32.and
                local.get 8
                i32.add
                i32.const 8
                i32.add
                local.get 14
                i32.store8
                local.get 10
                i32.const -12
                i32.mul
                local.get 8
                i32.add
                i32.const -12
                i32.add
                local.tee 10
                i32.const 8
                i32.add
                local.get 9
                local.get 7
                i32.add
                local.tee 14
                i32.const 8
                i32.add
                i32.load align=1
                i32.store align=1
                local.get 10
                local.get 14
                i64.load align=1
                i64.store align=1
              end
              local.get 1
              i32.const 1
              i32.add
              local.set 1
              local.get 7
              i32.const -12
              i32.add
              local.set 7
              br 0 (;@5;)
            end
          end
          call $_ZN9hashbrown3raw11Fallibility17capacity_overflow17he65d9ac21e057104E
          unreachable
        end
        local.get 8
        local.get 10
        call $_ZN9hashbrown3raw11Fallibility9alloc_err17h220ae99cd37bad82E
        unreachable
      end
      local.get 0
      i32.load
      local.set 14
      i32.const 0
      local.set 7
      i32.const 0
      local.set 1
      block  ;; label = @2
        loop  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              local.get 7
              i32.const 1
              i32.and
              i32.eqz
              br_if 0 (;@5;)
              local.get 1
              i32.const 7
              i32.add
              local.tee 7
              local.get 1
              i32.lt_u
              br_if 3 (;@2;)
              local.get 7
              local.get 5
              i32.ge_u
              br_if 3 (;@2;)
              local.get 1
              i32.const 8
              i32.add
              local.set 1
              br 1 (;@4;)
            end
            local.get 1
            local.get 5
            i32.lt_u
            local.tee 8
            i32.eqz
            br_if 2 (;@2;)
            local.get 1
            local.set 7
            local.get 1
            local.get 8
            i32.add
            local.set 1
          end
          local.get 14
          local.get 7
          i32.add
          local.tee 7
          local.get 7
          i64.load
          local.tee 13
          i64.const -1
          i64.xor
          i64.const 7
          i64.shr_u
          i64.const 72340172838076673
          i64.and
          local.get 13
          i64.const 9187201950435737471
          i64.or
          i64.add
          i64.store
          i32.const 1
          local.set 7
          br 0 (;@3;)
        end
      end
      block  ;; label = @2
        block  ;; label = @3
          local.get 5
          i32.const 8
          i32.lt_u
          br_if 0 (;@3;)
          local.get 14
          local.get 5
          i32.add
          local.get 14
          i64.load align=1
          i64.store align=1
          br 1 (;@2;)
        end
        local.get 14
        i32.const 8
        i32.add
        local.get 14
        local.get 5
        call $memmove
        drop
      end
      i32.const 0
      local.set 12
      local.get 14
      local.set 11
      loop  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              local.get 12
              local.get 5
              i32.eq
              br_if 0 (;@5;)
              local.get 14
              local.get 12
              i32.add
              local.tee 15
              i32.load8_u
              i32.const 128
              i32.ne
              br_if 2 (;@3;)
              local.get 12
              i32.const -12
              i32.mul
              local.get 14
              i32.add
              i32.const -12
              i32.add
              local.set 16
              loop  ;; label = @6
                local.get 12
                local.get 4
                local.get 2
                i32.const 12
                i32.add
                local.get 14
                local.get 12
                call $_ZN9hashbrown3raw21RawTable$LT$T$C$A$GT$14reserve_rehash28_$u7b$$u7b$closure$u7d$$u7d$17h00e9adfcff15ac28E
                local.tee 13
                i32.wrap_i64
                local.tee 7
                i32.and
                local.tee 8
                i32.sub
                local.get 14
                local.get 4
                local.get 13
                call $_ZN9hashbrown3raw22RawTableInner$LT$A$GT$16find_insert_slot17hebb2e2228b09aef2E
                local.tee 1
                local.get 8
                i32.sub
                i32.xor
                local.get 4
                i32.and
                i32.const 8
                i32.lt_u
                br_if 2 (;@4;)
                local.get 14
                local.get 1
                i32.add
                local.tee 8
                i32.load8_u
                local.set 9
                local.get 8
                local.get 7
                i32.const 25
                i32.shr_u
                local.tee 7
                i32.store8
                local.get 1
                i32.const -8
                i32.add
                local.get 4
                i32.and
                local.get 14
                i32.add
                i32.const 8
                i32.add
                local.get 7
                i32.store8
                local.get 1
                i32.const -12
                i32.mul
                local.get 14
                i32.add
                local.set 10
                block  ;; label = @7
                  local.get 9
                  i32.const 255
                  i32.eq
                  br_if 0 (;@7;)
                  i32.const -12
                  local.set 1
                  loop  ;; label = @8
                    local.get 1
                    i32.eqz
                    br_if 2 (;@6;)
                    local.get 11
                    local.get 1
                    i32.add
                    local.tee 7
                    i32.load8_u
                    local.set 8
                    local.get 7
                    local.get 10
                    local.get 1
                    i32.add
                    local.tee 9
                    i32.load8_u
                    i32.store8
                    local.get 9
                    local.get 8
                    i32.store8
                    local.get 1
                    i32.const 1
                    i32.add
                    local.set 1
                    br 0 (;@8;)
                  end
                end
              end
              local.get 15
              i32.const 255
              i32.store8
              local.get 12
              i32.const -8
              i32.add
              local.get 4
              i32.and
              local.get 14
              i32.add
              i32.const 8
              i32.add
              i32.const 255
              i32.store8
              local.get 10
              i32.const -12
              i32.add
              local.tee 1
              i32.const 8
              i32.add
              local.get 16
              i32.const 8
              i32.add
              i32.load align=1
              i32.store align=1
              local.get 1
              local.get 16
              i64.load align=1
              i64.store align=1
              br 2 (;@3;)
            end
            local.get 0
            local.get 6
            local.get 3
            i32.sub
            i32.store offset=8
            br 3 (;@1;)
          end
          local.get 15
          local.get 7
          i32.const 25
          i32.shr_u
          local.tee 1
          i32.store8
          local.get 12
          i32.const -8
          i32.add
          local.get 4
          i32.and
          local.get 14
          i32.add
          i32.const 8
          i32.add
          local.get 1
          i32.store8
        end
        local.get 12
        i32.const 1
        i32.add
        local.set 12
        local.get 11
        i32.const -12
        i32.add
        local.set 11
        br 0 (;@2;)
      end
    end
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    i32.const -2147483647)
  (func $_ZN9hashbrown3raw21RawTable$LT$T$C$A$GT$14reserve_rehash28_$u7b$$u7b$closure$u7d$$u7d$17h00e9adfcff15ac28E (type 15) (param i32 i32 i32) (result i64)
    local.get 0
    i32.load
    local.tee 0
    i64.load
    local.get 0
    i32.const 8
    i32.add
    i64.load
    local.get 1
    i32.const 0
    local.get 2
    i32.sub
    i32.const 12
    i32.mul
    i32.add
    i32.const -12
    i32.add
    i32.load
    call $_ZN4core4hash11BuildHasher8hash_one17haaa56a5ededbb8abE)
  (func $_ZN9hashbrown3raw22RawTableInner$LT$A$GT$16find_insert_slot17hebb2e2228b09aef2E (type 16) (param i32 i32 i64) (result i32)
    (local i32 i32)
    local.get 2
    i32.wrap_i64
    local.set 3
    i32.const 8
    local.set 4
    loop (result i32)  ;; label = @1
      block  ;; label = @2
        local.get 0
        local.get 3
        local.get 1
        i32.and
        local.tee 3
        i32.add
        i64.load align=1
        i64.const -9187201950435737472
        i64.and
        local.tee 2
        i64.eqz
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 0
          local.get 2
          i64.ctz
          i32.wrap_i64
          i32.const 3
          i32.shr_u
          local.get 3
          i32.add
          local.get 1
          i32.and
          local.tee 4
          i32.add
          i32.load8_s
          i32.const -1
          i32.le_s
          br_if 0 (;@3;)
          local.get 0
          i64.load
          i64.const -9187201950435737472
          i64.and
          i64.ctz
          i32.wrap_i64
          i32.const 3
          i32.shr_u
          local.set 4
        end
        local.get 4
        return
      end
      local.get 4
      local.get 3
      i32.add
      local.set 3
      local.get 4
      i32.const 8
      i32.add
      local.set 4
      br 0 (;@1;)
    end)
  (func $_ZN9hashbrown3raw11Fallibility17capacity_overflow17he65d9ac21e057104E (type 14)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 0
    global.set $__stack_pointer
    local.get 0
    i32.const 20
    i32.add
    i64.const 0
    i64.store align=4
    local.get 0
    i32.const 1
    i32.store offset=12
    local.get 0
    i32.const 1053804
    i32.store offset=8
    local.get 0
    i32.const 1054164
    i32.store offset=16
    local.get 0
    i32.const 8
    i32.add
    i32.const 1053896
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN9hashbrown3raw11Fallibility9alloc_err17h220ae99cd37bad82E (type 3) (param i32 i32)
    local.get 0
    local.get 1
    call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
    unreachable)
  (func $_ZN4core4hash11BuildHasher8hash_one17haaa56a5ededbb8abE (type 17) (param i64 i64 i32) (result i64)
    (local i64 i64 i64 i64)
    local.get 2
    i64.extend_i32_u
    i64.const 288230376151711744
    i64.or
    local.tee 3
    local.get 1
    i64.xor
    i64.const 8387220255154660723
    i64.xor
    local.tee 4
    i64.const 16
    i64.rotl
    local.get 4
    local.get 0
    i64.const 7816392313619706465
    i64.xor
    i64.add
    local.tee 4
    i64.xor
    local.tee 5
    i64.const 21
    i64.rotl
    local.get 5
    local.get 1
    i64.const 7237128888997146477
    i64.xor
    local.tee 1
    local.get 0
    i64.const 8317987319222330741
    i64.xor
    i64.add
    local.tee 0
    i64.const 32
    i64.rotl
    i64.add
    local.tee 5
    i64.xor
    local.tee 6
    local.get 4
    local.get 1
    i64.const 13
    i64.rotl
    local.get 0
    i64.xor
    local.tee 0
    i64.add
    local.tee 1
    i64.const 32
    i64.rotl
    i64.const 255
    i64.xor
    i64.add
    local.tee 4
    local.get 1
    local.get 0
    i64.const 17
    i64.rotl
    i64.xor
    local.tee 0
    i64.const 13
    i64.rotl
    local.get 0
    local.get 5
    local.get 3
    i64.xor
    i64.add
    local.tee 0
    i64.xor
    local.tee 1
    i64.add
    local.tee 3
    local.get 1
    i64.const 17
    i64.rotl
    i64.xor
    local.tee 1
    i64.const 13
    i64.rotl
    local.get 6
    i64.const 16
    i64.rotl
    local.get 4
    i64.xor
    local.tee 4
    local.get 0
    i64.const 32
    i64.rotl
    i64.add
    local.tee 0
    local.get 1
    i64.add
    local.tee 1
    i64.xor
    local.tee 5
    i64.const 17
    i64.rotl
    local.get 4
    i64.const 21
    i64.rotl
    local.get 0
    i64.xor
    local.tee 0
    local.get 3
    i64.const 32
    i64.rotl
    i64.add
    local.tee 3
    local.get 5
    i64.add
    local.tee 4
    i64.xor
    local.tee 5
    i64.const 13
    i64.rotl
    local.get 0
    i64.const 16
    i64.rotl
    local.get 3
    i64.xor
    local.tee 0
    local.get 1
    i64.const 32
    i64.rotl
    i64.add
    local.tee 1
    local.get 5
    i64.add
    i64.xor
    local.tee 3
    i64.const 17
    i64.rotl
    local.get 0
    i64.const 21
    i64.rotl
    local.get 1
    i64.xor
    local.tee 0
    local.get 4
    i64.const 32
    i64.rotl
    i64.add
    local.tee 1
    local.get 3
    i64.add
    local.tee 3
    i64.const 32
    i64.rotl
    i64.xor
    local.get 0
    i64.const 16
    i64.rotl
    local.get 1
    i64.xor
    i64.const 21
    i64.rotl
    i64.xor
    local.get 3
    i64.xor)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$16reserve_for_push17h18cc450d3e0f18d4E (type 3) (param i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        local.get 1
        i32.const 1
        call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$14grow_amortized17he5e3ed0132096fa9E
        local.set 0
        local.tee 1
        i32.const -2147483647
        i32.eq
        br_if 0 (;@2;)
        local.get 1
        i32.eqz
        br_if 1 (;@1;)
        local.get 1
        local.get 0
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      return
    end
    call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
    unreachable)
  (func $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17h0eeb836dede051ecE (type 1) (param i32 i32) (result i32)
    (local i32)
    local.get 0
    i32.load
    local.set 0
    block  ;; label = @1
      local.get 1
      i32.load offset=28
      local.tee 2
      i32.const 16
      i32.and
      br_if 0 (;@1;)
      block  ;; label = @2
        local.get 2
        i32.const 32
        i32.and
        br_if 0 (;@2;)
        local.get 0
        i32.load
        local.tee 0
        i64.extend_i32_u
        i64.const 0
        local.get 0
        i64.extend_i32_s
        i64.sub
        local.get 0
        i32.const -1
        i32.gt_s
        local.tee 0
        select
        local.get 0
        local.get 1
        call $_ZN4core3fmt3num3imp7fmt_u6417ha30186d55e58ac6fE
        return
      end
      local.get 0
      local.get 1
      call $_ZN4core3fmt3num53_$LT$impl$u20$core..fmt..UpperHex$u20$for$u20$i32$GT$3fmt17h58537b696dc0bd30E
      return
    end
    local.get 0
    local.get 1
    call $_ZN4core3fmt3num53_$LT$impl$u20$core..fmt..LowerHex$u20$for$u20$i32$GT$3fmt17h2e0d8f65cc6bfe78E)
  (func $_ZN4core3fmt3num3imp7fmt_u6417ha30186d55e58ac6fE (type 18) (param i64 i32 i32) (result i32)
    (local i32 i32 i64 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    i32.const 39
    local.set 4
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i64.const 10000
        i64.ge_u
        br_if 0 (;@2;)
        local.get 0
        local.set 5
        br 1 (;@1;)
      end
      i32.const 39
      local.set 4
      loop  ;; label = @2
        local.get 3
        i32.const 9
        i32.add
        local.get 4
        i32.add
        local.tee 6
        i32.const -4
        i32.add
        local.get 0
        i64.const 10000
        i64.div_u
        local.tee 5
        i64.const 55536
        i64.mul
        local.get 0
        i64.add
        i32.wrap_i64
        local.tee 7
        i32.const 65535
        i32.and
        i32.const 100
        i32.div_u
        local.tee 8
        i32.const 1
        i32.shl
        i32.const 1050206
        i32.add
        i32.load16_u align=1
        i32.store16 align=1
        local.get 6
        i32.const -2
        i32.add
        local.get 8
        i32.const -100
        i32.mul
        local.get 7
        i32.add
        i32.const 65535
        i32.and
        i32.const 1
        i32.shl
        i32.const 1050206
        i32.add
        i32.load16_u align=1
        i32.store16 align=1
        local.get 4
        i32.const -4
        i32.add
        local.set 4
        local.get 0
        i64.const 99999999
        i64.gt_u
        local.set 6
        local.get 5
        local.set 0
        local.get 6
        br_if 0 (;@2;)
      end
    end
    block  ;; label = @1
      local.get 5
      i32.wrap_i64
      local.tee 6
      i32.const 99
      i32.le_u
      br_if 0 (;@1;)
      local.get 3
      i32.const 9
      i32.add
      local.get 4
      i32.const -2
      i32.add
      local.tee 4
      i32.add
      local.get 5
      i32.wrap_i64
      local.tee 7
      i32.const 65535
      i32.and
      i32.const 100
      i32.div_u
      local.tee 6
      i32.const -100
      i32.mul
      local.get 7
      i32.add
      i32.const 65535
      i32.and
      i32.const 1
      i32.shl
      i32.const 1050206
      i32.add
      i32.load16_u align=1
      i32.store16 align=1
    end
    block  ;; label = @1
      block  ;; label = @2
        local.get 6
        i32.const 10
        i32.lt_u
        br_if 0 (;@2;)
        local.get 3
        i32.const 9
        i32.add
        local.get 4
        i32.const -2
        i32.add
        local.tee 4
        i32.add
        local.get 6
        i32.const 1
        i32.shl
        i32.const 1050206
        i32.add
        i32.load16_u align=1
        i32.store16 align=1
        br 1 (;@1;)
      end
      local.get 3
      i32.const 9
      i32.add
      local.get 4
      i32.const -1
      i32.add
      local.tee 4
      i32.add
      local.get 6
      i32.const 48
      i32.add
      i32.store8
    end
    local.get 2
    local.get 1
    i32.const 1054164
    i32.const 0
    local.get 3
    i32.const 9
    i32.add
    local.get 4
    i32.add
    i32.const 39
    local.get 4
    i32.sub
    call $_ZN4core3fmt9Formatter12pad_integral17h840ce31caaa4dc56E
    local.set 4
    local.get 3
    i32.const 48
    i32.add
    global.set $__stack_pointer
    local.get 4)
  (func $_ZN4core3fmt3num53_$LT$impl$u20$core..fmt..UpperHex$u20$for$u20$i32$GT$3fmt17h58537b696dc0bd30E (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 128
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    i32.const 0
    local.set 3
    loop  ;; label = @1
      local.get 2
      local.get 3
      i32.add
      i32.const 127
      i32.add
      i32.const 48
      i32.const 55
      local.get 0
      i32.const 15
      i32.and
      local.tee 4
      i32.const 10
      i32.lt_u
      select
      local.get 4
      i32.add
      i32.store8
      local.get 3
      i32.const -1
      i32.add
      local.set 3
      local.get 0
      i32.const 15
      i32.gt_u
      local.set 4
      local.get 0
      i32.const 4
      i32.shr_u
      local.set 0
      local.get 4
      br_if 0 (;@1;)
    end
    block  ;; label = @1
      local.get 3
      i32.const 128
      i32.add
      local.tee 0
      i32.const 129
      i32.lt_u
      br_if 0 (;@1;)
      local.get 0
      i32.const 128
      i32.const 1050188
      call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
      unreachable
    end
    local.get 1
    i32.const 1
    i32.const 1050204
    i32.const 2
    local.get 2
    local.get 3
    i32.add
    i32.const 128
    i32.add
    i32.const 0
    local.get 3
    i32.sub
    call $_ZN4core3fmt9Formatter12pad_integral17h840ce31caaa4dc56E
    local.set 0
    local.get 2
    i32.const 128
    i32.add
    global.set $__stack_pointer
    local.get 0)
  (func $_ZN4core3fmt3num53_$LT$impl$u20$core..fmt..LowerHex$u20$for$u20$i32$GT$3fmt17h2e0d8f65cc6bfe78E (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 128
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    i32.const 0
    local.set 3
    loop  ;; label = @1
      local.get 2
      local.get 3
      i32.add
      i32.const 127
      i32.add
      i32.const 48
      i32.const 87
      local.get 0
      i32.const 15
      i32.and
      local.tee 4
      i32.const 10
      i32.lt_u
      select
      local.get 4
      i32.add
      i32.store8
      local.get 3
      i32.const -1
      i32.add
      local.set 3
      local.get 0
      i32.const 15
      i32.gt_u
      local.set 4
      local.get 0
      i32.const 4
      i32.shr_u
      local.set 0
      local.get 4
      br_if 0 (;@1;)
    end
    block  ;; label = @1
      local.get 3
      i32.const 128
      i32.add
      local.tee 0
      i32.const 129
      i32.lt_u
      br_if 0 (;@1;)
      local.get 0
      i32.const 128
      i32.const 1050188
      call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
      unreachable
    end
    local.get 1
    i32.const 1
    i32.const 1050204
    i32.const 2
    local.get 2
    local.get 3
    i32.add
    i32.const 128
    i32.add
    i32.const 0
    local.get 3
    i32.sub
    call $_ZN4core3fmt9Formatter12pad_integral17h840ce31caaa4dc56E
    local.set 0
    local.get 2
    i32.const 128
    i32.add
    global.set $__stack_pointer
    local.get 0)
  (func $_ZN4core3ptr52drop_in_place$LT$std..thread..local..AccessError$GT$17h57a975f821e6c1ebE (type 2) (param i32))
  (func $_ZN4core9panicking13assert_failed17h9fdb338402711657E (type 3) (param i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    i32.const 1049496
    i32.store offset=4
    local.get 2
    local.get 0
    i32.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    i32.const 1048956
    local.get 2
    i32.const 4
    i32.add
    i32.const 1048956
    local.get 2
    i32.const 8
    i32.add
    i32.const 1049604
    call $_ZN4core9panicking19assert_failed_inner17h85f6c6a47372e3aaE
    unreachable)
  (func $_ZN4core9panicking19assert_failed_inner17h85f6c6a47372e3aaE (type 19) (param i32 i32 i32 i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 112
    i32.sub
    local.tee 6
    global.set $__stack_pointer
    local.get 6
    local.get 1
    i32.store offset=12
    local.get 6
    local.get 0
    i32.store offset=8
    local.get 6
    local.get 3
    i32.store offset=20
    local.get 6
    local.get 2
    i32.store offset=16
    local.get 6
    i32.const 2
    i32.store offset=28
    local.get 6
    i32.const 1049956
    i32.store offset=24
    block  ;; label = @1
      local.get 4
      i32.load
      br_if 0 (;@1;)
      local.get 6
      i32.const 76
      i32.add
      i32.const 4
      i32.store
      local.get 6
      i32.const 56
      i32.add
      i32.const 12
      i32.add
      i32.const 4
      i32.store
      local.get 6
      i32.const 88
      i32.add
      i32.const 12
      i32.add
      i64.const 3
      i64.store align=4
      local.get 6
      i32.const 4
      i32.store offset=92
      local.get 6
      i32.const 1050052
      i32.store offset=88
      local.get 6
      i32.const 5
      i32.store offset=60
      local.get 6
      local.get 6
      i32.const 56
      i32.add
      i32.store offset=96
      local.get 6
      local.get 6
      i32.const 16
      i32.add
      i32.store offset=72
      local.get 6
      local.get 6
      i32.const 8
      i32.add
      i32.store offset=64
      local.get 6
      local.get 6
      i32.const 24
      i32.add
      i32.store offset=56
      local.get 6
      i32.const 88
      i32.add
      local.get 5
      call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
      unreachable
    end
    local.get 6
    i32.const 32
    i32.add
    i32.const 16
    i32.add
    local.get 4
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 6
    i32.const 32
    i32.add
    i32.const 8
    i32.add
    local.get 4
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 6
    local.get 4
    i64.load align=4
    i64.store offset=32
    local.get 6
    i32.const 88
    i32.add
    i32.const 12
    i32.add
    i64.const 4
    i64.store align=4
    local.get 6
    i32.const 84
    i32.add
    i32.const 6
    i32.store
    local.get 6
    i32.const 76
    i32.add
    i32.const 4
    i32.store
    local.get 6
    i32.const 56
    i32.add
    i32.const 12
    i32.add
    i32.const 4
    i32.store
    local.get 6
    i32.const 4
    i32.store offset=92
    local.get 6
    i32.const 1050016
    i32.store offset=88
    local.get 6
    i32.const 5
    i32.store offset=60
    local.get 6
    local.get 6
    i32.const 56
    i32.add
    i32.store offset=96
    local.get 6
    local.get 6
    i32.const 32
    i32.add
    i32.store offset=80
    local.get 6
    local.get 6
    i32.const 16
    i32.add
    i32.store offset=72
    local.get 6
    local.get 6
    i32.const 8
    i32.add
    i32.store offset=64
    local.get 6
    local.get 6
    i32.const 24
    i32.add
    i32.store offset=56
    local.get 6
    i32.const 88
    i32.add
    local.get 5
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN9hashbrown3raw21RawTable$LT$T$C$A$GT$7get_mut17hd6b26100c674bb12E (type 20) (param i32 i64 i32) (result i32)
    (local i32 i32 i64 i32 i32 i64 i64)
    local.get 0
    i32.load offset=4
    local.tee 3
    local.get 1
    i32.wrap_i64
    i32.and
    local.set 4
    local.get 1
    i64.const 25
    i64.shr_u
    i64.const 127
    i64.and
    i64.const 72340172838076673
    i64.mul
    local.set 5
    local.get 2
    i32.load
    local.set 6
    local.get 0
    i32.load
    local.set 0
    i32.const 0
    local.set 7
    loop  ;; label = @1
      local.get 0
      local.get 4
      i32.add
      i64.load align=1
      local.tee 8
      local.get 5
      i64.xor
      local.tee 1
      i64.const -1
      i64.xor
      local.get 1
      i64.const -72340172838076673
      i64.add
      i64.and
      i64.const -9187201950435737472
      i64.and
      local.set 9
      block  ;; label = @2
        loop  ;; label = @3
          block  ;; label = @4
            local.get 9
            local.tee 1
            i64.const 0
            i64.ne
            br_if 0 (;@4;)
            local.get 8
            local.get 8
            i64.const 1
            i64.shl
            i64.and
            i64.const -9187201950435737472
            i64.and
            i64.eqz
            i32.eqz
            br_if 2 (;@2;)
            local.get 4
            local.get 7
            i32.const 8
            i32.add
            local.tee 7
            i32.add
            local.get 3
            i32.and
            local.set 4
            br 3 (;@1;)
          end
          local.get 1
          i64.const -1
          i64.add
          local.get 1
          i64.and
          local.set 9
          local.get 6
          local.get 0
          i32.const 0
          local.get 1
          i64.ctz
          i32.wrap_i64
          i32.const 3
          i32.shr_u
          local.get 4
          i32.add
          local.get 3
          i32.and
          local.tee 2
          i32.sub
          i32.const 12
          i32.mul
          i32.add
          i32.const -12
          i32.add
          i32.load
          i32.ne
          br_if 0 (;@3;)
        end
      end
    end
    i32.const 0
    i32.const 0
    local.get 0
    i32.const 0
    local.get 2
    i32.sub
    i32.const 12
    i32.mul
    i32.add
    local.get 1
    i64.eqz
    local.tee 4
    select
    i32.const -12
    i32.add
    local.get 4
    select)
  (func $_ZN76_$LT$std..sync..poison..PoisonError$LT$T$GT$$u20$as$u20$core..fmt..Debug$GT$3fmt17h31b1c977533811acE (type 1) (param i32 i32) (result i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 1
    i32.load offset=20
    i32.const 1048972
    i32.const 11
    local.get 1
    i32.const 24
    i32.add
    i32.load
    i32.load offset=12
    call_indirect (type 0)
    local.set 3
    local.get 2
    i32.const 0
    i32.store8 offset=13
    local.get 2
    local.get 3
    i32.store8 offset=12
    local.get 2
    local.get 1
    i32.store offset=8
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt8builders11DebugStruct21finish_non_exhaustive17haea475a0d151f175E
    local.set 1
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core3fmt8builders11DebugStruct21finish_non_exhaustive17haea475a0d151f175E (type 5) (param i32) (result i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    i32.const 1
    local.set 2
    block  ;; label = @1
      local.get 0
      i32.load8_u offset=4
      br_if 0 (;@1;)
      local.get 0
      i32.load
      local.set 3
      block  ;; label = @2
        local.get 0
        i32.const 5
        i32.add
        i32.load8_u
        br_if 0 (;@2;)
        local.get 3
        i32.load offset=20
        i32.const 1050152
        i32.const 7
        local.get 3
        i32.const 24
        i32.add
        i32.load
        i32.load offset=12
        call_indirect (type 0)
        local.set 2
        br 1 (;@1;)
      end
      block  ;; label = @2
        local.get 3
        i32.load8_u offset=28
        i32.const 4
        i32.and
        br_if 0 (;@2;)
        local.get 3
        i32.load offset=20
        i32.const 1050146
        i32.const 6
        local.get 3
        i32.const 24
        i32.add
        i32.load
        i32.load offset=12
        call_indirect (type 0)
        local.set 2
        br 1 (;@1;)
      end
      i32.const 1
      local.set 2
      local.get 1
      i32.const 1
      i32.store8 offset=15
      local.get 1
      local.get 3
      i64.load offset=20 align=4
      i64.store
      local.get 1
      local.get 1
      i32.const 15
      i32.add
      i32.store offset=8
      local.get 1
      i32.const 1050142
      i32.const 3
      call $_ZN68_$LT$core..fmt..builders..PadAdapter$u20$as$u20$core..fmt..Write$GT$9write_str17hd4ac5b916bf4e0b0E
      br_if 0 (;@1;)
      local.get 3
      i32.load offset=20
      i32.const 1050145
      i32.const 1
      local.get 3
      i32.load offset=24
      i32.load offset=12
      call_indirect (type 0)
      local.set 2
    end
    local.get 0
    local.get 2
    i32.store8 offset=4
    local.get 1
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 2)
  (func $_ZN4core3ops8function6FnOnce40call_once$u7b$$u7b$vtable.shim$u7d$$u7d$17h803462a5d051c192E (type 5) (param i32) (result i32)
    local.get 0
    call $_ZN9once_cell3imp17OnceCell$LT$T$GT$10initialize28_$u7b$$u7b$closure$u7d$$u7d$17h08719884d15d3caaE
    drop
    i32.const 1)
  (func $_ZN9once_cell3imp17OnceCell$LT$T$GT$10initialize28_$u7b$$u7b$closure$u7d$$u7d$17h08719884d15d3caaE (type 5) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i64 i32 i32)
    global.get $__stack_pointer
    i32.const 64
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.tee 2
    i32.load
    local.set 3
    local.get 2
    i32.const 0
    i32.store
    local.get 3
    i32.load offset=56
    local.set 2
    local.get 3
    i32.const 0
    i32.store offset=56
    block  ;; label = @1
      local.get 2
      i32.eqz
      br_if 0 (;@1;)
      local.get 1
      i32.const 8
      i32.add
      local.get 2
      call_indirect (type 2)
      block  ;; label = @2
        local.get 0
        i32.load offset=4
        local.tee 4
        i32.load
        local.tee 5
        i64.load
        i64.eqz
        br_if 0 (;@2;)
        local.get 5
        i32.const 20
        i32.add
        i32.load
        local.tee 3
        i32.eqz
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 5
          i32.const 28
          i32.add
          i32.load
          local.tee 2
          i32.eqz
          br_if 0 (;@3;)
          local.get 5
          i32.load offset=16
          local.tee 0
          i32.const 8
          i32.add
          local.set 3
          local.get 0
          i64.load
          i64.const -1
          i64.xor
          i64.const -9187201950435737472
          i64.and
          local.set 6
          block  ;; label = @4
            loop  ;; label = @5
              local.get 2
              i32.eqz
              br_if 1 (;@4;)
              block  ;; label = @6
                loop  ;; label = @7
                  local.get 6
                  i64.const 0
                  i64.ne
                  br_if 1 (;@6;)
                  local.get 0
                  i32.const -96
                  i32.add
                  local.set 0
                  local.get 3
                  i64.load
                  i64.const -1
                  i64.xor
                  i64.const -9187201950435737472
                  i64.and
                  local.set 6
                  local.get 3
                  i32.const 8
                  i32.add
                  local.set 3
                  br 0 (;@7;)
                end
              end
              local.get 0
              local.get 6
              i64.ctz
              i32.wrap_i64
              i32.const 3
              i32.shr_u
              i32.const -12
              i32.mul
              i32.add
              local.tee 7
              i32.const -8
              i32.add
              i32.load
              local.tee 8
              local.get 7
              i32.const -4
              i32.add
              i32.load
              local.tee 7
              i32.load
              call_indirect (type 2)
              local.get 8
              local.get 7
              i32.load offset=4
              call $_ZN63_$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$10deallocate17h61bf6a4893a1c41aE
              local.get 2
              i32.const -1
              i32.add
              local.set 2
              local.get 6
              i64.const -1
              i64.add
              local.get 6
              i64.and
              local.set 6
              br 0 (;@5;)
            end
          end
          local.get 5
          i32.const 20
          i32.add
          i32.load
          local.set 3
        end
        local.get 1
        i32.const 48
        i32.add
        local.get 5
        i32.load offset=16
        local.get 3
        call $_ZN9hashbrown3raw22RawTableInner$LT$A$GT$15allocation_info17hfe639f5aa4fa5af7E
        local.get 1
        i32.load offset=48
        local.get 1
        i32.const 56
        i32.add
        i32.load
        call $_ZN63_$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$10deallocate17h61bf6a4893a1c41aE
        local.get 4
        i32.load
        local.set 5
      end
      local.get 5
      i64.const 1
      i64.store
      local.get 5
      i32.const 8
      i32.add
      local.get 1
      i32.const 8
      i32.add
      i32.const 40
      call $memcpy
      drop
      local.get 1
      i32.const 64
      i32.add
      global.set $__stack_pointer
      i32.const 1
      return
    end
    local.get 1
    i32.const 20
    i32.add
    i64.const 0
    i64.store align=4
    local.get 1
    i32.const 1
    i32.store offset=12
    local.get 1
    i32.const 1049068
    i32.store offset=8
    local.get 1
    i32.const 1054164
    i32.store offset=16
    local.get 1
    i32.const 8
    i32.add
    i32.const 1049180
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN4core3ops8function6FnOnce40call_once$u7b$$u7b$vtable.shim$u7d$$u7d$17h6534dce3e0201b30E (type 5) (param i32) (result i32)
    local.get 0
    call $_ZN9once_cell3imp17OnceCell$LT$T$GT$10initialize28_$u7b$$u7b$closure$u7d$$u7d$17hecb0bdfae7ba818bE
    drop
    i32.const 1)
  (func $_ZN9once_cell3imp17OnceCell$LT$T$GT$10initialize28_$u7b$$u7b$closure$u7d$$u7d$17hecb0bdfae7ba818bE (type 5) (param i32) (result i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.tee 2
    i32.load
    local.set 3
    local.get 2
    i32.const 0
    i32.store
    local.get 3
    i32.load offset=20
    local.set 2
    local.get 3
    i32.const 0
    i32.store offset=20
    block  ;; label = @1
      local.get 2
      br_if 0 (;@1;)
      local.get 1
      i32.const 20
      i32.add
      i64.const 0
      i64.store align=4
      local.get 1
      i32.const 1
      i32.store offset=12
      local.get 1
      i32.const 1049068
      i32.store offset=8
      local.get 1
      i32.const 1054164
      i32.store offset=16
      local.get 1
      i32.const 8
      i32.add
      i32.const 1049180
      call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
      unreachable
    end
    local.get 1
    i32.const 8
    i32.add
    local.get 2
    call_indirect (type 2)
    local.get 0
    i32.load offset=4
    i32.load
    local.tee 3
    i32.const 1
    i32.store
    local.get 3
    local.get 1
    i64.load offset=8 align=4
    i64.store offset=4 align=4
    local.get 3
    i32.const 12
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i32.load
    i32.store
    local.get 1
    i32.const 32
    i32.add
    global.set $__stack_pointer
    i32.const 1)
  (func $_ZN3std3sys4wasi5locks6rwlock6RwLock5write17hbe82db7de699f57cE (type 2) (param i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 2
    local.get 0
    i32.const -1
    i32.store
    block  ;; label = @1
      local.get 2
      br_if 0 (;@1;)
      local.get 1
      i32.const 48
      i32.add
      global.set $__stack_pointer
      return
    end
    local.get 1
    i32.const 28
    i32.add
    i64.const 0
    i64.store align=4
    local.get 1
    i32.const 1
    i32.store offset=20
    local.get 1
    i32.const 1049256
    i32.store offset=16
    local.get 1
    local.get 1
    i32.const 40
    i32.add
    i32.store offset=24
    local.get 1
    i32.const 8
    i32.add
    local.get 1
    i32.const 40
    i32.add
    local.get 1
    i32.const 16
    i32.add
    call $_ZN3std2io5Write9write_fmt17ha7e411ed63ede228E
    local.get 1
    i32.load8_u offset=8
    local.get 1
    i32.load offset=12
    call $_ZN4core3ptr81drop_in_place$LT$core..result..Result$LT$$LP$$RP$$C$std..io..error..Error$GT$$GT$17h3640ecbe50e7f3deE
    call $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E
    unreachable)
  (func $_ZN3std2io5Write9write_fmt17ha7e411ed63ede228E (type 12) (param i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    i32.const 4
    i32.store8 offset=8
    local.get 3
    local.get 1
    i32.store offset=16
    local.get 3
    i32.const 24
    i32.add
    i32.const 16
    i32.add
    local.get 2
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 3
    i32.const 24
    i32.add
    i32.const 8
    i32.add
    local.get 2
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 3
    local.get 2
    i64.load align=4
    i64.store offset=24
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 3
          i32.const 8
          i32.add
          i32.const 1049712
          local.get 3
          i32.const 24
          i32.add
          call $_ZN4core3fmt5write17h8253e306f6bd0e19E
          br_if 0 (;@3;)
          local.get 0
          i32.const 4
          i32.store8
          local.get 3
          i32.load8_u offset=8
          local.set 2
          br 1 (;@2;)
        end
        block  ;; label = @3
          local.get 3
          i32.load8_u offset=8
          i32.const 4
          i32.ne
          br_if 0 (;@3;)
          local.get 0
          i32.const 1054500
          i32.store offset=4
          local.get 0
          i32.const 2
          i32.store8
          i32.const 4
          local.set 2
          br 1 (;@2;)
        end
        local.get 0
        local.get 3
        i64.load offset=8
        i64.store align=4
        br 1 (;@1;)
      end
      local.get 2
      local.get 3
      i32.load offset=12
      call $_ZN4core3ptr81drop_in_place$LT$core..result..Result$LT$$LP$$RP$$C$std..io..error..Error$GT$$GT$17h3640ecbe50e7f3deE.57
    end
    local.get 3
    i32.const 48
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core3ptr81drop_in_place$LT$core..result..Result$LT$$LP$$RP$$C$std..io..error..Error$GT$$GT$17h3640ecbe50e7f3deE (type 3) (param i32 i32)
    (local i32)
    block  ;; label = @1
      local.get 0
      i32.const 255
      i32.and
      i32.const 3
      i32.ne
      br_if 0 (;@1;)
      local.get 1
      i32.load
      local.tee 0
      local.get 1
      i32.load offset=4
      local.tee 2
      i32.load
      call_indirect (type 2)
      local.get 0
      local.get 2
      i32.load offset=4
      call $_ZN63_$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$10deallocate17h61bf6a4893a1c41aE
      local.get 1
      call $free
    end)
  (func $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E (type 14)
    call $abort
    unreachable)
  (func $_ZN3std4sync6rwlock15RwLock$LT$T$GT$5write17h55db55ec8afe36b5E (type 3) (param i32 i32)
    (local i32 i32)
    local.get 1
    call $_ZN3std3sys4wasi5locks6rwlock6RwLock5write17hbe82db7de699f57cE
    local.get 1
    i32.const 4
    i32.add
    call $_ZN3std4sync6poison4Flag5guard17h8f6284c0743aa497E
    local.set 3
    local.set 2
    local.get 0
    local.get 1
    i32.store offset=4
    local.get 0
    i32.const 8
    i32.add
    local.get 3
    i32.const 1
    i32.and
    i32.store8
    local.get 0
    local.get 2
    i32.const 1
    i32.and
    i32.store)
  (func $_ZN3std4sync6poison4Flag5guard17h8f6284c0743aa497E (type 7) (param i32) (result i32 i32)
    (local i32)
    call $_ZN3std9panicking11panic_count13count_is_zero17hd357b03b426d5e54E
    local.set 1
    local.get 0
    i32.load8_u
    i32.const 0
    i32.ne
    local.get 1
    i32.const 1
    i32.xor)
  (func $_ZN4core6result19Result$LT$T$C$E$GT$6unwrap17h14230750cec305d5E (type 21) (param i32 i32) (result i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      local.get 0
      i32.load
      br_if 0 (;@1;)
      local.get 0
      i32.const 8
      i32.add
      i32.load8_u
      local.set 1
      local.get 0
      i32.load offset=4
      local.set 0
      local.get 2
      i32.const 16
      i32.add
      global.set $__stack_pointer
      local.get 0
      local.get 1
      return
    end
    local.get 2
    local.get 0
    i32.load offset=4
    i32.store offset=8
    local.get 2
    local.get 0
    i32.const 8
    i32.add
    i32.load8_u
    i32.store8 offset=12
    i32.const 1049264
    i32.const 43
    local.get 2
    i32.const 8
    i32.add
    i32.const 1049340
    local.get 1
    call $_ZN4core6result13unwrap_failed17hfefb3e75b68d8f8cE
    unreachable)
  (func $_ZN4core3ptr159drop_in_place$LT$core..option..Option$LT$alloc..boxed..Box$LT$dyn$u20$base..strategy..TradingStrategy$u2b$core..marker..Sync$u2b$core..marker..Send$GT$$GT$$GT$17ha9b7ed211c79f172E (type 3) (param i32 i32)
    block  ;; label = @1
      local.get 0
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      i32.load
      call_indirect (type 2)
      local.get 0
      local.get 1
      i32.load offset=4
      call $_ZN63_$LT$alloc..alloc..Global$u20$as$u20$core..alloc..Allocator$GT$10deallocate17h61bf6a4893a1c41aE
    end)
  (func $_ZN4core3ops8function6FnOnce9call_once17h2296aeb300a7e9bdE (type 2) (param i32)
    (local i32 i32 i64)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    block  ;; label = @1
      i32.const 0
      call $_ZN3std11collections4hash3map11RandomState3new4KEYS7__getit17h0b53c3a427dad1f1E
      local.tee 2
      br_if 0 (;@1;)
      i32.const 1048772
      i32.const 70
      local.get 1
      i32.const 8
      i32.add
      i32.const 1048844
      i32.const 1048940
      call $_ZN4core6result13unwrap_failed17hfefb3e75b68d8f8cE
      unreachable
    end
    local.get 2
    local.get 2
    i64.load
    local.tee 3
    i64.const 1
    i64.add
    i64.store
    local.get 0
    i32.const 32
    i32.add
    local.get 2
    i64.load offset=8
    i64.store
    local.get 0
    i32.const 24
    i32.add
    local.get 3
    i64.store
    local.get 0
    i32.const 20
    i32.add
    i32.const 0
    i32.store
    local.get 0
    i32.const 12
    i32.add
    i64.const 0
    i64.store align=4
    local.get 0
    i32.const 1049200
    i32.store offset=8
    local.get 0
    i32.const 0
    i32.store8 offset=4
    local.get 0
    i32.const 0
    i32.store
    local.get 1
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN3std11collections4hash3map11RandomState3new4KEYS7__getit17h0b53c3a427dad1f1E (type 5) (param i32) (result i32)
    (local i32 i64 i32 i64)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          i32.const 0
          i64.load offset=1059296
          local.tee 2
          i64.const 0
          i64.eq
          br_if 0 (;@3;)
          i32.const 0
          i32.const 1059304
          local.get 2
          i64.eqz
          select
          local.set 0
          br 1 (;@2;)
        end
        block  ;; label = @3
          block  ;; label = @4
            local.get 0
            i32.eqz
            br_if 0 (;@4;)
            local.get 0
            i32.load
            local.set 3
            local.get 0
            i64.const 0
            i64.store
            local.get 3
            i32.const 1
            i32.ne
            br_if 0 (;@4;)
            local.get 0
            i64.load offset=16
            local.set 2
            local.get 0
            i64.load offset=8
            local.set 4
            br 1 (;@3;)
          end
          local.get 1
          i32.const 16
          i32.add
          i64.const 0
          i64.store
          local.get 1
          i64.const 0
          i64.store offset=8
          local.get 1
          i32.const 8
          i32.add
          i32.const 16
          call $_ZN4wasi13lib_generated22wasi_snapshot_preview110random_get17h9e4fa943327627f2E
          local.tee 0
          br_if 2 (;@1;)
          local.get 1
          i64.load offset=16
          local.set 2
          local.get 1
          i64.load offset=8
          local.set 4
        end
        i32.const 0
        local.get 2
        i64.store offset=1059312
        i32.const 0
        local.get 4
        i64.store offset=1059304
        i32.const 0
        i64.const 1
        i64.store offset=1059296
        i32.const 1059304
        local.set 0
      end
      local.get 1
      i32.const 32
      i32.add
      global.set $__stack_pointer
      local.get 0
      return
    end
    local.get 1
    local.get 0
    i32.store16 offset=30
    i32.const 1055544
    i32.const 18
    local.get 1
    i32.const 30
    i32.add
    i32.const 1055528
    i32.const 1055596
    call $_ZN4core6result13unwrap_failed17hfefb3e75b68d8f8cE
    unreachable)
  (func $_ZN4core3ptr105drop_in_place$LT$std..sync..poison..PoisonError$LT$std..sync..rwlock..RwLockWriteGuard$LT$i32$GT$$GT$$GT$17heec6d4163f504738E (type 2) (param i32)
    local.get 0
    i32.load
    local.get 0
    i32.const 4
    i32.add
    i32.load8_u
    call $_ZN86_$LT$std..sync..rwlock..RwLockWriteGuard$LT$T$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h0c6c9fd4b72761f4E)
  (func $_ZN86_$LT$std..sync..rwlock..RwLockWriteGuard$LT$T$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h0c6c9fd4b72761f4E (type 3) (param i32 i32)
    local.get 0
    i32.const 4
    i32.add
    local.get 1
    call $_ZN3std4sync6poison4Flag4done17h80178340b661c814E
    local.get 0
    call $_ZN3std3sys4wasi5locks6rwlock6RwLock12write_unlock17h1257998f30f57970E)
  (func $_ZN4core3ops8function6FnOnce9call_once17hced0e244dbb5386bE (type 2) (param i32)
    local.get 0
    i32.const 0
    i32.store offset=8
    local.get 0
    i32.const 0
    i32.store8 offset=4
    local.get 0
    i32.const 0
    i32.store)
  (func $unregister_strategy (type 5) (param i32) (result i32)
    (local i32 i32 i32 i32 i64 i32 i64 i32 i32 i64 i64 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    local.get 1
    call $_ZN78_$LT$once_cell..sync..Lazy$LT$T$C$F$GT$$u20$as$u20$core..ops..deref..Deref$GT$5deref17h0320017a3b91974eE
    call $_ZN3std4sync6rwlock15RwLock$LT$T$GT$5write17h55db55ec8afe36b5E
    local.get 1
    i32.const 1049432
    call $_ZN4core6result19Result$LT$T$C$E$GT$6unwrap17h14230750cec305d5E
    local.set 2
    local.tee 3
    i32.const 12
    i32.add
    i32.load
    local.tee 4
    local.get 3
    i32.const 24
    i32.add
    i64.load
    local.get 3
    i32.const 32
    i32.add
    i64.load
    local.get 0
    call $_ZN4core4hash11BuildHasher8hash_one17haaa56a5ededbb8abE
    local.tee 5
    i32.wrap_i64
    i32.and
    local.set 6
    local.get 5
    i64.const 25
    i64.shr_u
    i64.const 127
    i64.and
    i64.const 72340172838076673
    i64.mul
    local.set 7
    local.get 3
    i32.const 8
    i32.add
    i32.load
    local.set 8
    i32.const 0
    local.set 9
    block  ;; label = @1
      loop  ;; label = @2
        local.get 8
        local.get 6
        i32.add
        i64.load align=1
        local.tee 10
        local.get 7
        i64.xor
        local.tee 5
        i64.const -1
        i64.xor
        local.get 5
        i64.const -72340172838076673
        i64.add
        i64.and
        i64.const -9187201950435737472
        i64.and
        local.set 5
        loop  ;; label = @3
          block  ;; label = @4
            local.get 5
            i64.const 0
            i64.ne
            br_if 0 (;@4;)
            block  ;; label = @5
              local.get 10
              local.get 10
              i64.const 1
              i64.shl
              i64.and
              i64.const -9187201950435737472
              i64.and
              i64.eqz
              br_if 0 (;@5;)
              i32.const 0
              local.set 6
              br 4 (;@1;)
            end
            local.get 6
            local.get 9
            i32.const 8
            i32.add
            local.tee 9
            i32.add
            local.get 4
            i32.and
            local.set 6
            br 2 (;@2;)
          end
          local.get 5
          i64.ctz
          local.set 11
          local.get 5
          i64.const -1
          i64.add
          local.get 5
          i64.and
          local.set 5
          local.get 8
          i32.const 0
          local.get 11
          i32.wrap_i64
          i32.const 3
          i32.shr_u
          local.get 6
          i32.add
          local.get 4
          i32.and
          local.tee 12
          i32.sub
          i32.const 12
          i32.mul
          i32.add
          i32.const -12
          i32.add
          local.tee 13
          i32.load
          local.get 0
          i32.ne
          br_if 0 (;@3;)
        end
      end
      i32.const 128
      local.set 6
      block  ;; label = @2
        local.get 8
        local.get 12
        i32.const 12
        i32.mul
        i32.const 12
        i32.div_s
        local.tee 0
        i32.add
        local.tee 12
        i64.load align=1
        local.tee 5
        local.get 5
        i64.const 1
        i64.shl
        i64.and
        i64.const -9187201950435737472
        i64.and
        i64.ctz
        i32.wrap_i64
        i32.const 3
        i32.shr_u
        local.get 8
        local.get 0
        i32.const -8
        i32.add
        local.get 4
        i32.and
        i32.add
        local.tee 8
        i64.load align=1
        local.tee 5
        local.get 5
        i64.const 1
        i64.shl
        i64.and
        i64.const -9187201950435737472
        i64.and
        i64.clz
        i32.wrap_i64
        i32.const 3
        i32.shr_u
        i32.add
        i32.const 7
        i32.gt_u
        br_if 0 (;@2;)
        local.get 3
        i32.const 16
        i32.add
        local.tee 6
        local.get 6
        i32.load
        i32.const 1
        i32.add
        i32.store
        i32.const 255
        local.set 6
      end
      local.get 12
      local.get 6
      i32.store8
      local.get 8
      i32.const 8
      i32.add
      local.get 6
      i32.store8
      local.get 3
      i32.const 20
      i32.add
      local.tee 6
      local.get 6
      i32.load
      i32.const -1
      i32.add
      i32.store
      local.get 13
      i32.load offset=8
      local.set 8
      local.get 13
      i32.load offset=4
      local.set 6
    end
    local.get 3
    local.get 2
    call $_ZN86_$LT$std..sync..rwlock..RwLockWriteGuard$LT$T$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h0c6c9fd4b72761f4E
    local.get 6
    local.get 8
    call $_ZN4core3ptr159drop_in_place$LT$core..option..Option$LT$alloc..boxed..Box$LT$dyn$u20$base..strategy..TradingStrategy$u2b$core..marker..Sync$u2b$core..marker..Send$GT$$GT$$GT$17ha9b7ed211c79f172E
    local.get 1
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 6
    i32.const 0
    i32.ne)
  (func $_ZN78_$LT$once_cell..sync..Lazy$LT$T$C$F$GT$$u20$as$u20$core..ops..deref..Deref$GT$5deref17h0320017a3b91974eE (type 22) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 0
    global.set $__stack_pointer
    block  ;; label = @1
      i32.const 0
      i32.load offset=1059200
      i32.const 2
      i32.eq
      br_if 0 (;@1;)
      local.get 0
      i32.const 1059152
      i32.store
      local.get 0
      i32.const 1059152
      i32.store offset=4
      local.get 0
      local.get 0
      i32.const 24
      i32.add
      i32.store offset=16
      local.get 0
      local.get 0
      i32.const 4
      i32.add
      i32.store offset=12
      local.get 0
      local.get 0
      i32.store offset=8
      i32.const 1059200
      local.get 0
      i32.const 8
      i32.add
      i32.const 1048984
      call $_ZN9once_cell3imp18initialize_or_wait17h555185a2b5de84ceE
    end
    local.get 0
    i32.const 32
    i32.add
    global.set $__stack_pointer
    i32.const 1059160)
  (func $strategy_parameters (type 7) (param i32) (result i32 i32)
    (local i32 i32 i32 i32 i32 i64 i32 i64 i32 i32 i64 i64 i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              call $_ZN78_$LT$once_cell..sync..Lazy$LT$T$C$F$GT$$u20$as$u20$core..ops..deref..Deref$GT$5deref17h0320017a3b91974eE
              local.tee 2
              i32.load
              local.tee 3
              i32.const -1
              i32.le_s
              br_if 0 (;@5;)
              local.get 2
              local.get 3
              i32.const 1
              i32.add
              i32.store
              local.get 2
              i32.load8_u offset=4
              br_if 1 (;@4;)
              i32.const -1
              local.set 4
              local.get 2
              i32.const 20
              i32.add
              i32.load
              i32.eqz
              br_if 3 (;@2;)
              local.get 2
              i32.const 12
              i32.add
              i32.load
              local.tee 5
              local.get 2
              i32.const 24
              i32.add
              i64.load
              local.get 2
              i32.const 32
              i32.add
              i64.load
              local.get 0
              call $_ZN4core4hash11BuildHasher8hash_one17haaa56a5ededbb8abE
              local.tee 6
              i32.wrap_i64
              i32.and
              local.set 7
              local.get 6
              i64.const 25
              i64.shr_u
              i64.const 127
              i64.and
              i64.const 72340172838076673
              i64.mul
              local.set 8
              local.get 2
              i32.const 8
              i32.add
              i32.load
              local.set 9
              i32.const 0
              local.set 10
              loop  ;; label = @6
                local.get 9
                local.get 7
                i32.add
                i64.load align=1
                local.tee 11
                local.get 8
                i64.xor
                local.tee 6
                i64.const -1
                i64.xor
                local.get 6
                i64.const -72340172838076673
                i64.add
                i64.and
                i64.const -9187201950435737472
                i64.and
                local.set 6
                loop  ;; label = @7
                  block  ;; label = @8
                    local.get 6
                    i64.const 0
                    i64.ne
                    br_if 0 (;@8;)
                    local.get 11
                    local.get 11
                    i64.const 1
                    i64.shl
                    i64.and
                    i64.const -9187201950435737472
                    i64.and
                    i64.eqz
                    i32.eqz
                    br_if 6 (;@2;)
                    local.get 7
                    local.get 10
                    i32.const 8
                    i32.add
                    local.tee 10
                    i32.add
                    local.get 5
                    i32.and
                    local.set 7
                    br 2 (;@6;)
                  end
                  local.get 6
                  i64.ctz
                  local.set 12
                  local.get 6
                  i64.const -1
                  i64.add
                  local.get 6
                  i64.and
                  local.set 6
                  local.get 9
                  i32.const 0
                  local.get 12
                  i32.wrap_i64
                  i32.const 3
                  i32.shr_u
                  local.get 7
                  i32.add
                  local.get 5
                  i32.and
                  i32.sub
                  i32.const 12
                  i32.mul
                  i32.add
                  i32.const -12
                  i32.add
                  local.tee 13
                  i32.load
                  local.get 0
                  i32.ne
                  br_if 0 (;@7;)
                end
              end
              local.get 1
              i32.const 16
              i32.add
              local.get 13
              i32.load offset=4
              local.get 13
              i32.const 8
              i32.add
              i32.load
              i32.load offset=12
              call_indirect (type 3)
              local.get 1
              i32.load offset=24
              local.tee 4
              i32.const -1
              i32.le_s
              br_if 2 (;@3;)
              local.get 1
              i32.load offset=16
              local.set 9
              i32.const 0
              i32.load8_u offset=1059320
              drop
              local.get 4
              i32.const 1
              call $__rust_alloc
              local.tee 7
              local.get 9
              local.get 4
              call $memcpy
              drop
              local.get 9
              local.get 1
              i32.load offset=20
              call $_ZN77_$LT$alloc..raw_vec..RawVec$LT$T$C$A$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17hce6ec3cb0496d13dE
              local.get 2
              i32.load
              i32.const -1
              i32.add
              local.set 3
              br 4 (;@1;)
            end
            local.get 1
            i32.const 28
            i32.add
            i64.const 0
            i64.store align=4
            local.get 1
            i32.const 1
            i32.store offset=20
            local.get 1
            i32.const 1055520
            i32.store offset=16
            local.get 1
            local.get 1
            i32.const 40
            i32.add
            i32.store offset=24
            local.get 1
            i32.const 8
            i32.add
            local.get 1
            i32.const 40
            i32.add
            local.get 1
            i32.const 16
            i32.add
            call $_ZN3std2io5Write9write_fmt17ha7e411ed63ede228E
            local.get 1
            i32.load8_u offset=8
            local.get 1
            i32.load offset=12
            call $_ZN4core3ptr81drop_in_place$LT$core..result..Result$LT$$LP$$RP$$C$std..io..error..Error$GT$$GT$17h3640ecbe50e7f3deE
            call $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E
            unreachable
          end
          local.get 1
          local.get 2
          i32.store offset=20
          local.get 1
          local.get 2
          i32.const 8
          i32.add
          i32.store offset=16
          i32.const 1049264
          i32.const 43
          local.get 1
          i32.const 16
          i32.add
          i32.const 1049356
          i32.const 1049448
          call $_ZN4core6result13unwrap_failed17hfefb3e75b68d8f8cE
          unreachable
        end
        i32.const 1049264
        i32.const 43
        local.get 1
        i32.const 40
        i32.add
        i32.const 1049308
        i32.const 1049464
        call $_ZN4core6result13unwrap_failed17hfefb3e75b68d8f8cE
        unreachable
      end
      i32.const -1
      local.set 7
    end
    local.get 2
    local.get 3
    i32.store
    local.get 1
    i32.const 48
    i32.add
    global.set $__stack_pointer
    local.get 7
    local.get 4)
  (func $_ZN4core3ptr261drop_in_place$LT$std..sync..poison..PoisonError$LT$std..sync..rwlock..RwLockReadGuard$LT$std..collections..hash..map..HashMap$LT$i32$C$alloc..boxed..Box$LT$dyn$u20$base..strategy..TradingStrategy$u2b$core..marker..Sync$u2b$core..marker..Send$GT$$GT$$GT$$GT$$GT$17h30417aeeed91d393E (type 2) (param i32)
    local.get 0
    i32.load offset=4
    local.tee 0
    local.get 0
    i32.load
    i32.const -1
    i32.add
    i32.store)
  (func $strategy_next (type 23) (param i32 i32 f32 f32 f32 f32 f32)
    (local i32 f32 f32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 7
    global.set $__stack_pointer
    local.get 7
    local.get 1
    i32.store offset=4
    local.get 7
    i32.const 8
    i32.add
    call $_ZN78_$LT$once_cell..sync..Lazy$LT$T$C$F$GT$$u20$as$u20$core..ops..deref..Deref$GT$5deref17h0320017a3b91974eE
    call $_ZN3std4sync6rwlock15RwLock$LT$T$GT$5write17h55db55ec8afe36b5E
    f32.const 0x0p+0 (;=0;)
    local.set 8
    f32.const -0x1p+0 (;=-1;)
    local.set 9
    block  ;; label = @1
      block  ;; label = @2
        local.get 7
        i32.const 8
        i32.add
        i32.const 1049480
        call $_ZN4core6result19Result$LT$T$C$E$GT$6unwrap17h14230750cec305d5E
        local.set 10
        local.tee 11
        i32.const 20
        i32.add
        i32.load
        i32.eqz
        br_if 0 (;@2;)
        local.get 11
        i32.const 8
        i32.add
        local.get 11
        i32.const 24
        i32.add
        i64.load
        local.get 11
        i32.const 32
        i32.add
        i64.load
        local.get 1
        call $_ZN4core4hash11BuildHasher8hash_one17haaa56a5ededbb8abE
        local.get 7
        i32.const 4
        i32.add
        call $_ZN9hashbrown3raw21RawTable$LT$T$C$A$GT$7get_mut17hd6b26100c674bb12E
        local.tee 1
        i32.eqz
        br_if 0 (;@2;)
        local.get 1
        i32.const 8
        i32.add
        i32.load
        i32.load offset=16
        local.set 12
        local.get 1
        i32.load offset=4
        local.set 1
        local.get 7
        local.get 6
        f32.store offset=24
        local.get 7
        local.get 5
        f32.store offset=20
        local.get 7
        local.get 4
        f32.store offset=16
        local.get 7
        local.get 3
        f32.store offset=12
        local.get 7
        local.get 2
        f32.store offset=8
        f32.const 0x1.ccccccp-1 (;=0.9;)
        local.set 6
        f32.const 0x1p+0 (;=1;)
        local.set 9
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  local.get 1
                  local.get 7
                  i32.const 8
                  i32.add
                  local.get 12
                  call_indirect (type 4)
                  local.set 8
                  br_table 6 (;@1;) 0 (;@7;) 1 (;@6;) 2 (;@5;) 3 (;@4;) 6 (;@1;)
                end
                f32.const 0x1p+1 (;=2;)
                local.set 9
                br 5 (;@1;)
              end
              f32.const 0x1.8p+1 (;=3;)
              local.set 9
              br 2 (;@3;)
            end
            f32.const 0x1p+2 (;=4;)
            local.set 9
            br 1 (;@3;)
          end
          f32.const 0x0p+0 (;=0;)
          local.set 9
        end
        f32.const 0x0p+0 (;=0;)
        local.set 8
      end
      f32.const 0x0p+0 (;=0;)
      local.set 6
    end
    local.get 0
    local.get 6
    f32.store offset=8
    local.get 0
    local.get 8
    f32.store offset=4
    local.get 0
    local.get 9
    f32.store
    local.get 11
    local.get 10
    call $_ZN86_$LT$std..sync..rwlock..RwLockWriteGuard$LT$T$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h0c6c9fd4b72761f4E
    local.get 7
    i32.const 32
    i32.add
    global.set $__stack_pointer)
  (func $_ZN3std9panicking11panic_count13count_is_zero17hd357b03b426d5e54E (type 22) (result i32)
    (local i32)
    i32.const 1
    local.set 0
    block  ;; label = @1
      i32.const 0
      i32.load offset=1059268
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if 0 (;@1;)
      call $_ZN3std9panicking11panic_count17is_zero_slow_path17h75908fc4564b8b9eE
      local.set 0
    end
    local.get 0)
  (func $_ZN3std9panicking11panic_count17is_zero_slow_path17h75908fc4564b8b9eE (type 22) (result i32)
    i32.const 0
    i32.load offset=1059280
    i32.eqz)
  (func $_ZN3std4sync6poison4Flag4done17h80178340b661c814E (type 3) (param i32 i32)
    block  ;; label = @1
      local.get 1
      i32.const 255
      i32.and
      br_if 0 (;@1;)
      call $_ZN3std9panicking11panic_count13count_is_zero17hd357b03b426d5e54E
      br_if 0 (;@1;)
      local.get 0
      i32.const 1
      i32.store8
    end)
  (func $_ZN3std3sys4wasi5locks6rwlock6RwLock12write_unlock17h1257998f30f57970E (type 2) (param i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 2
    local.get 0
    i32.const 0
    i32.store
    local.get 1
    local.get 2
    i32.store offset=4
    block  ;; label = @1
      local.get 2
      i32.const -1
      i32.ne
      br_if 0 (;@1;)
      local.get 1
      i32.const 32
      i32.add
      global.set $__stack_pointer
      return
    end
    local.get 1
    i32.const 0
    i32.store offset=8
    local.get 1
    i32.const 4
    i32.add
    local.get 1
    i32.const 8
    i32.add
    call $_ZN4core9panicking13assert_failed17h9fdb338402711657E
    unreachable)
  (func $_ZN9once_cell3imp18initialize_or_wait17h555185a2b5de84ceE (type 12) (param i32 i32 i32)
    (local i32 i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 4
    loop  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    local.get 4
                    i32.const 3
                    i32.and
                    local.tee 5
                    br_table 0 (;@8;) 1 (;@7;) 3 (;@5;) 7 (;@1;)
                  end
                  local.get 1
                  br_if 1 (;@6;)
                end
                local.get 3
                i32.const 8
                i32.add
                local.get 5
                i32.or
                local.set 6
                block  ;; label = @7
                  loop  ;; label = @8
                    call $_ZN3std10sys_common11thread_info14current_thread17h2d20a3c7c082bda6E
                    local.set 7
                    local.get 0
                    local.get 6
                    local.get 0
                    i32.load
                    local.tee 8
                    local.get 8
                    local.get 4
                    i32.eq
                    select
                    i32.store
                    local.get 3
                    i32.const 0
                    i32.store8 offset=16
                    local.get 3
                    local.get 7
                    i32.store offset=8
                    local.get 3
                    local.get 4
                    i32.const -4
                    i32.and
                    i32.store offset=12
                    local.get 8
                    local.get 4
                    i32.eq
                    br_if 1 (;@7;)
                    local.get 3
                    i32.const 8
                    i32.add
                    call $_ZN4core3ptr43drop_in_place$LT$once_cell..imp..Waiter$GT$17h7a61f04626115bb4E
                    local.get 8
                    local.set 4
                    local.get 8
                    i32.const 3
                    i32.and
                    local.get 5
                    i32.eq
                    br_if 0 (;@8;)
                    br 6 (;@2;)
                  end
                end
                loop  ;; label = @7
                  block  ;; label = @8
                    local.get 3
                    i32.load8_u offset=16
                    i32.eqz
                    br_if 0 (;@8;)
                    local.get 3
                    i32.const 8
                    i32.add
                    call $_ZN4core3ptr43drop_in_place$LT$once_cell..imp..Waiter$GT$17h7a61f04626115bb4E
                    br 6 (;@2;)
                  end
                  call $_ZN3std10sys_common11thread_info14current_thread17h2d20a3c7c082bda6E
                  local.tee 8
                  local.get 8
                  i32.load
                  local.tee 4
                  i32.const -1
                  i32.add
                  i32.store
                  local.get 4
                  i32.const 1
                  i32.ne
                  br_if 0 (;@7;)
                  local.get 8
                  call $_ZN5alloc4sync12Arc$LT$T$GT$9drop_slow17hfead2a7a1440e4b8E
                  br 0 (;@7;)
                end
              end
              local.get 0
              local.get 4
              i32.const -4
              i32.and
              i32.const 1
              i32.or
              local.get 0
              i32.load
              local.tee 8
              local.get 8
              local.get 4
              i32.eq
              select
              i32.store
              local.get 8
              local.get 4
              i32.ne
              local.set 7
              local.get 8
              local.set 4
              local.get 7
              br_if 4 (;@1;)
              local.get 1
              local.get 2
              i32.load offset=16
              call_indirect (type 5)
              local.set 4
              local.get 0
              i32.load
              local.set 8
              local.get 0
              i32.const 2
              i32.const 0
              local.get 4
              select
              i32.store
              local.get 3
              local.get 8
              i32.const 3
              i32.and
              local.tee 4
              i32.store offset=4
              local.get 4
              i32.const 1
              i32.ne
              br_if 1 (;@4;)
              local.get 8
              i32.const -1
              i32.add
              local.set 8
              loop  ;; label = @6
                local.get 8
                i32.eqz
                br_if 1 (;@5;)
                local.get 8
                i32.load offset=4
                local.set 0
                local.get 8
                i32.load
                local.set 4
                local.get 8
                i32.const 0
                i32.store
                local.get 4
                i32.eqz
                br_if 3 (;@3;)
                local.get 8
                i32.const 1
                i32.store8 offset=8
                local.get 3
                local.get 4
                i32.store offset=8
                local.get 3
                i32.const 8
                i32.add
                call $_ZN4core3ptr40drop_in_place$LT$std..thread..Thread$GT$17h164b0697484aa5b2E
                local.get 0
                local.set 8
                br 0 (;@6;)
              end
            end
            local.get 3
            i32.const 32
            i32.add
            global.set $__stack_pointer
            return
          end
          local.get 3
          i32.const 0
          i32.store offset=8
          local.get 3
          i32.const 4
          i32.add
          local.get 3
          i32.const 8
          i32.add
          call $_ZN4core9panicking13assert_failed17hfa364ad86727fdaaE
          unreachable
        end
        i32.const 1054072
        i32.const 43
        i32.const 1054040
        call $_ZN4core9panicking5panic17hcfcdcc589d164b16E
        unreachable
      end
      local.get 0
      i32.load
      local.set 4
      br 0 (;@1;)
    end)
  (func $_ZN4core3ptr42drop_in_place$LT$std..io..error..Error$GT$17h168ffd97fd3ea3c7E (type 3) (param i32 i32)
    (local i32)
    block  ;; label = @1
      local.get 0
      i32.const 255
      i32.and
      i32.const 3
      i32.ne
      br_if 0 (;@1;)
      local.get 1
      i32.load
      local.tee 2
      local.get 1
      i32.load offset=4
      local.tee 0
      i32.load
      call_indirect (type 2)
      block  ;; label = @2
        local.get 0
        i32.load offset=4
        i32.eqz
        br_if 0 (;@2;)
        local.get 2
        call $free
      end
      local.get 1
      call $free
    end)
  (func $_ZN4core3ptr81drop_in_place$LT$core..result..Result$LT$$LP$$RP$$C$std..io..error..Error$GT$$GT$17h3640ecbe50e7f3deE.57 (type 3) (param i32 i32)
    block  ;; label = @1
      local.get 0
      i32.const 255
      i32.and
      i32.const 4
      i32.eq
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      call $_ZN4core3ptr42drop_in_place$LT$std..io..error..Error$GT$17h168ffd97fd3ea3c7E
    end)
  (func $_ZN4core3ptr92drop_in_place$LT$std..io..Write..write_fmt..Adapter$LT$std..sys..wasi..stdio..Stderr$GT$$GT$17h82f1e3f018af5003E (type 2) (param i32)
    local.get 0
    i32.load8_u
    local.get 0
    i32.const 4
    i32.add
    i32.load
    call $_ZN4core3ptr81drop_in_place$LT$core..result..Result$LT$$LP$$RP$$C$std..io..error..Error$GT$$GT$17h3640ecbe50e7f3deE.57)
  (func $_ZN4core3fmt5Write10write_char17h1167d2a5cfccbbddE (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    i32.const 0
    i32.store offset=12
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 128
        i32.lt_u
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 1
          i32.const 2048
          i32.lt_u
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 1
            i32.const 65536
            i32.lt_u
            br_if 0 (;@4;)
            local.get 2
            local.get 1
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=15
            local.get 2
            local.get 1
            i32.const 6
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=14
            local.get 2
            local.get 1
            i32.const 12
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=13
            local.get 2
            local.get 1
            i32.const 18
            i32.shr_u
            i32.const 7
            i32.and
            i32.const 240
            i32.or
            i32.store8 offset=12
            i32.const 4
            local.set 1
            br 3 (;@1;)
          end
          local.get 2
          local.get 1
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=14
          local.get 2
          local.get 1
          i32.const 12
          i32.shr_u
          i32.const 224
          i32.or
          i32.store8 offset=12
          local.get 2
          local.get 1
          i32.const 6
          i32.shr_u
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=13
          i32.const 3
          local.set 1
          br 2 (;@1;)
        end
        local.get 2
        local.get 1
        i32.const 63
        i32.and
        i32.const 128
        i32.or
        i32.store8 offset=13
        local.get 2
        local.get 1
        i32.const 6
        i32.shr_u
        i32.const 192
        i32.or
        i32.store8 offset=12
        i32.const 2
        local.set 1
        br 1 (;@1;)
      end
      local.get 2
      local.get 1
      i32.store8 offset=12
      i32.const 1
      local.set 1
    end
    local.get 0
    local.get 2
    i32.const 12
    i32.add
    local.get 1
    call $_ZN80_$LT$std..io..Write..write_fmt..Adapter$LT$T$GT$$u20$as$u20$core..fmt..Write$GT$9write_str17ha20c17e383239b1fE
    local.set 1
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN80_$LT$std..io..Write..write_fmt..Adapter$LT$T$GT$$u20$as$u20$core..fmt..Write$GT$9write_str17ha20c17e383239b1fE (type 0) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          loop  ;; label = @4
            i32.const 0
            local.set 4
            local.get 2
            i32.eqz
            br_if 2 (;@2;)
            local.get 3
            i32.const 8
            i32.add
            local.get 3
            local.get 1
            local.get 2
            call $_ZN64_$LT$std..sys..wasi..stdio..Stderr$u20$as$u20$std..io..Write$GT$5write17hc56ef5c390ae78f2E
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  local.get 3
                  i32.load8_u offset=8
                  local.tee 5
                  i32.const 4
                  i32.ne
                  br_if 0 (;@7;)
                  local.get 3
                  i32.load offset=12
                  local.tee 5
                  br_if 1 (;@6;)
                  i32.const 2
                  local.set 2
                  i32.const 1054472
                  local.set 1
                  br 4 (;@3;)
                end
                block  ;; label = @7
                  block  ;; label = @8
                    block  ;; label = @9
                      block  ;; label = @10
                        block  ;; label = @11
                          local.get 5
                          br_table 0 (;@11;) 1 (;@10;) 2 (;@9;) 3 (;@8;) 0 (;@11;)
                        end
                        local.get 3
                        i32.load offset=12
                        call $_ZN3std3sys4wasi17decode_error_kind17hc0f82157747eae67E
                        i32.const 255
                        i32.and
                        local.set 5
                        br 3 (;@7;)
                      end
                      local.get 3
                      i32.load8_u offset=9
                      local.set 5
                      br 2 (;@7;)
                    end
                    local.get 3
                    i32.load offset=12
                    i32.load8_u offset=8
                    local.set 5
                    br 1 (;@7;)
                  end
                  local.get 3
                  i32.load offset=12
                  i32.load8_u offset=8
                  local.set 5
                end
                local.get 5
                i32.const 255
                i32.and
                i32.const 35
                i32.ne
                br_if 1 (;@5;)
                local.get 3
                i32.load8_u offset=8
                local.get 3
                i32.load offset=12
                call $_ZN4core3ptr42drop_in_place$LT$std..io..error..Error$GT$17h168ffd97fd3ea3c7E
                br 2 (;@4;)
              end
              local.get 2
              local.get 5
              i32.lt_u
              br_if 4 (;@1;)
              local.get 1
              local.get 5
              i32.add
              local.set 1
              local.get 2
              local.get 5
              i32.sub
              local.set 2
              br 1 (;@4;)
            end
          end
          local.get 3
          i32.load offset=8
          local.tee 2
          i32.const 255
          i32.and
          i32.const 4
          i32.eq
          br_if 1 (;@2;)
          local.get 3
          i32.load offset=12
          local.set 1
        end
        block  ;; label = @3
          local.get 0
          i32.load8_u
          local.tee 5
          i32.const 4
          i32.eq
          br_if 0 (;@3;)
          local.get 5
          i32.const 3
          i32.ne
          br_if 0 (;@3;)
          local.get 0
          i32.load offset=4
          local.tee 5
          i32.load
          local.tee 6
          local.get 5
          i32.load offset=4
          local.tee 4
          i32.load
          call_indirect (type 2)
          block  ;; label = @4
            local.get 4
            i32.load offset=4
            i32.eqz
            br_if 0 (;@4;)
            local.get 6
            call $free
          end
          local.get 5
          call $free
        end
        local.get 0
        local.get 1
        i32.store offset=4
        local.get 0
        local.get 2
        i32.store
        i32.const 1
        local.set 4
      end
      local.get 3
      i32.const 16
      i32.add
      global.set $__stack_pointer
      local.get 4
      return
    end
    local.get 5
    local.get 2
    i32.const 1049696
    call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
    unreachable)
  (func $_ZN64_$LT$std..sys..wasi..stdio..Stderr$u20$as$u20$std..io..Write$GT$5write17hc56ef5c390ae78f2E (type 9) (param i32 i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 4
    global.set $__stack_pointer
    local.get 4
    local.get 3
    i32.store offset=4
    local.get 4
    local.get 2
    i32.store
    local.get 4
    i32.const 8
    i32.add
    local.get 4
    i32.const 1
    call $_ZN4wasi13lib_generated8fd_write17h775ab5e87c956e2cE
    block  ;; label = @1
      block  ;; label = @2
        local.get 4
        i32.load16_u offset=8
        br_if 0 (;@2;)
        local.get 0
        local.get 4
        i32.load offset=12
        i32.store offset=4
        local.get 0
        i32.const 4
        i32.store8
        br 1 (;@1;)
      end
      local.get 0
      local.get 4
      i64.load16_u offset=10
      i64.const 32
      i64.shl
      i64.store align=4
    end
    local.get 4
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN3std3sys4wasi17decode_error_kind17hc0f82157747eae67E (type 5) (param i32) (result i32)
    (local i32)
    i32.const 40
    local.set 1
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.const 65535
        i32.gt_u
        br_if 0 (;@2;)
        i32.const 2
        local.set 1
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    block  ;; label = @9
                      block  ;; label = @10
                        block  ;; label = @11
                          block  ;; label = @12
                            block  ;; label = @13
                              block  ;; label = @14
                                block  ;; label = @15
                                  block  ;; label = @16
                                    local.get 0
                                    i32.const -2
                                    i32.add
                                    br_table 1 (;@15;) 6 (;@10;) 5 (;@11;) 15 (;@1;) 12 (;@4;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 4 (;@12;) 14 (;@2;) 0 (;@16;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 11 (;@5;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 8 (;@8;) 9 (;@7;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 7 (;@9;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 13 (;@3;) 3 (;@13;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 1 (;@15;) 2 (;@14;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 15 (;@1;) 10 (;@6;) 15 (;@1;)
                                  end
                                  i32.const 3
                                  return
                                end
                                i32.const 1
                                return
                              end
                              i32.const 11
                              return
                            end
                            i32.const 7
                            return
                          end
                          i32.const 6
                          return
                        end
                        i32.const 9
                        return
                      end
                      i32.const 8
                      return
                    end
                    i32.const 0
                    return
                  end
                  i32.const 35
                  return
                end
                i32.const 20
                return
              end
              i32.const 22
              return
            end
            i32.const 12
            return
          end
          i32.const 13
          return
        end
        i32.const 36
        local.set 1
      end
      local.get 1
      return
    end
    i32.const 38
    i32.const 40
    local.get 0
    i32.const 48
    i32.eq
    select)
  (func $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE (type 12) (param i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    local.get 0
    i32.store
    local.get 3
    local.get 1
    i32.store offset=4
    local.get 3
    i32.const 8
    i32.add
    i32.const 12
    i32.add
    i64.const 2
    i64.store align=4
    local.get 3
    i32.const 32
    i32.add
    i32.const 12
    i32.add
    i32.const 1
    i32.store
    local.get 3
    i32.const 2
    i32.store offset=12
    local.get 3
    i32.const 1050528
    i32.store offset=8
    local.get 3
    i32.const 1
    i32.store offset=36
    local.get 3
    local.get 3
    i32.const 32
    i32.add
    i32.store offset=16
    local.get 3
    local.get 3
    i32.const 4
    i32.add
    i32.store offset=40
    local.get 3
    local.get 3
    i32.store offset=32
    local.get 3
    i32.const 8
    i32.add
    local.get 2
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN4core3fmt5Write9write_fmt17hea1dcd8ca86a27a6E (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    local.get 0
    i32.store offset=4
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    i32.const 4
    i32.add
    i32.const 1049736
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 1
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core3ptr104drop_in_place$LT$$RF$mut$u20$std..io..Write..write_fmt..Adapter$LT$std..sys..wasi..stdio..Stderr$GT$$GT$17h653c62b9b22bc166E (type 2) (param i32))
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h594ada18edc2cc2aE (type 0) (param i32 i32 i32) (result i32)
    local.get 0
    i32.load
    local.get 1
    local.get 2
    call $_ZN80_$LT$std..io..Write..write_fmt..Adapter$LT$T$GT$$u20$as$u20$core..fmt..Write$GT$9write_str17ha20c17e383239b1fE)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17hd153e54c623bbe7bE (type 1) (param i32 i32) (result i32)
    local.get 0
    i32.load
    local.get 1
    call $_ZN4core3fmt5Write10write_char17h1167d2a5cfccbbddE)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17h2960215ccf17f2d3E (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 0
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt5Write9write_fmt17hea1dcd8ca86a27a6E
    local.set 1
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core3ops8function6FnOnce9call_once17h55447dbbde76805eE (type 1) (param i32 i32) (result i32)
    local.get 0
    i32.load
    drop
    loop (result i32)  ;; label = @1
      br 0 (;@1;)
    end)
  (func $rust_begin_unwind (type 2) (param i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    block  ;; label = @1
      local.get 0
      i32.load offset=12
      local.tee 2
      br_if 0 (;@1;)
      i32.const 1054072
      i32.const 43
      i32.const 1055072
      call $_ZN4core9panicking5panic17hcfcdcc589d164b16E
      unreachable
    end
    local.get 1
    local.get 0
    i32.load offset=8
    i32.store offset=8
    local.get 1
    local.get 0
    i32.store offset=4
    local.get 1
    local.get 2
    i32.store
    local.get 1
    call $_ZN3std10sys_common9backtrace26__rust_end_short_backtrace17hffd60a674bcf0795E
    unreachable)
  (func $_ZN4core9panicking18panic_bounds_check17h7eef07023fe9cc87E (type 12) (param i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    local.get 1
    i32.store offset=4
    local.get 3
    local.get 0
    i32.store
    local.get 3
    i32.const 8
    i32.add
    i32.const 12
    i32.add
    i64.const 2
    i64.store align=4
    local.get 3
    i32.const 32
    i32.add
    i32.const 12
    i32.add
    i32.const 1
    i32.store
    local.get 3
    i32.const 2
    i32.store offset=12
    local.get 3
    i32.const 1049940
    i32.store offset=8
    local.get 3
    i32.const 1
    i32.store offset=36
    local.get 3
    local.get 3
    i32.const 32
    i32.add
    i32.store offset=16
    local.get 3
    local.get 3
    i32.store offset=40
    local.get 3
    local.get 3
    i32.const 4
    i32.add
    i32.store offset=32
    local.get 3
    i32.const 8
    i32.add
    local.get 2
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN4core3fmt9Formatter12pad_integral17h840ce31caaa4dc56E (type 24) (param i32 i32 i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.eqz
        br_if 0 (;@2;)
        i32.const 43
        i32.const 1114112
        local.get 0
        i32.load offset=28
        local.tee 6
        i32.const 1
        i32.and
        local.tee 1
        select
        local.set 7
        local.get 1
        local.get 5
        i32.add
        local.set 8
        br 1 (;@1;)
      end
      local.get 5
      i32.const 1
      i32.add
      local.set 8
      local.get 0
      i32.load offset=28
      local.set 6
      i32.const 45
      local.set 7
    end
    block  ;; label = @1
      block  ;; label = @2
        local.get 6
        i32.const 4
        i32.and
        br_if 0 (;@2;)
        i32.const 0
        local.set 2
        br 1 (;@1;)
      end
      block  ;; label = @2
        block  ;; label = @3
          local.get 3
          br_if 0 (;@3;)
          i32.const 0
          local.set 9
          br 1 (;@2;)
        end
        block  ;; label = @3
          local.get 3
          i32.const 3
          i32.and
          local.tee 10
          br_if 0 (;@3;)
          br 1 (;@2;)
        end
        i32.const 0
        local.set 9
        local.get 2
        local.set 1
        loop  ;; label = @3
          local.get 9
          local.get 1
          i32.load8_s
          i32.const -65
          i32.gt_s
          i32.add
          local.set 9
          local.get 1
          i32.const 1
          i32.add
          local.set 1
          local.get 10
          i32.const -1
          i32.add
          local.tee 10
          br_if 0 (;@3;)
        end
      end
      local.get 9
      local.get 8
      i32.add
      local.set 8
    end
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.load
        br_if 0 (;@2;)
        i32.const 1
        local.set 1
        local.get 0
        i32.const 20
        i32.add
        i32.load
        local.tee 9
        local.get 0
        i32.const 24
        i32.add
        i32.load
        local.tee 10
        local.get 7
        local.get 2
        local.get 3
        call $_ZN4core3fmt9Formatter12pad_integral12write_prefix17hb93099e3a54c5cfdE
        br_if 1 (;@1;)
        local.get 9
        local.get 4
        local.get 5
        local.get 10
        i32.load offset=12
        call_indirect (type 0)
        return
      end
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                local.get 0
                i32.load offset=4
                local.tee 11
                local.get 8
                i32.le_u
                br_if 0 (;@6;)
                local.get 6
                i32.const 8
                i32.and
                br_if 4 (;@2;)
                local.get 11
                local.get 8
                i32.sub
                local.tee 9
                local.set 6
                local.get 0
                i32.load8_u offset=32
                local.tee 1
                br_table 3 (;@3;) 1 (;@5;) 2 (;@4;) 1 (;@5;) 3 (;@3;)
              end
              i32.const 1
              local.set 1
              local.get 0
              i32.const 20
              i32.add
              i32.load
              local.tee 9
              local.get 0
              i32.const 24
              i32.add
              i32.load
              local.tee 10
              local.get 7
              local.get 2
              local.get 3
              call $_ZN4core3fmt9Formatter12pad_integral12write_prefix17hb93099e3a54c5cfdE
              br_if 4 (;@1;)
              local.get 9
              local.get 4
              local.get 5
              local.get 10
              i32.load offset=12
              call_indirect (type 0)
              return
            end
            i32.const 0
            local.set 6
            local.get 9
            local.set 1
            br 1 (;@3;)
          end
          local.get 9
          i32.const 1
          i32.shr_u
          local.set 1
          local.get 9
          i32.const 1
          i32.add
          i32.const 1
          i32.shr_u
          local.set 6
        end
        local.get 1
        i32.const 1
        i32.add
        local.set 1
        local.get 0
        i32.const 24
        i32.add
        i32.load
        local.set 10
        local.get 0
        i32.const 20
        i32.add
        i32.load
        local.set 8
        local.get 0
        i32.load offset=16
        local.set 9
        block  ;; label = @3
          loop  ;; label = @4
            local.get 1
            i32.const -1
            i32.add
            local.tee 1
            i32.eqz
            br_if 1 (;@3;)
            local.get 8
            local.get 9
            local.get 10
            i32.load offset=16
            call_indirect (type 1)
            i32.eqz
            br_if 0 (;@4;)
          end
          i32.const 1
          return
        end
        i32.const 1
        local.set 1
        local.get 9
        i32.const 1114112
        i32.eq
        br_if 1 (;@1;)
        local.get 8
        local.get 10
        local.get 7
        local.get 2
        local.get 3
        call $_ZN4core3fmt9Formatter12pad_integral12write_prefix17hb93099e3a54c5cfdE
        br_if 1 (;@1;)
        local.get 8
        local.get 4
        local.get 5
        local.get 10
        i32.load offset=12
        call_indirect (type 0)
        br_if 1 (;@1;)
        i32.const 0
        local.set 1
        block  ;; label = @3
          loop  ;; label = @4
            block  ;; label = @5
              local.get 6
              local.get 1
              i32.ne
              br_if 0 (;@5;)
              local.get 6
              local.set 1
              br 2 (;@3;)
            end
            local.get 1
            i32.const 1
            i32.add
            local.set 1
            local.get 8
            local.get 9
            local.get 10
            i32.load offset=16
            call_indirect (type 1)
            i32.eqz
            br_if 0 (;@4;)
          end
          local.get 1
          i32.const -1
          i32.add
          local.set 1
        end
        local.get 1
        local.get 6
        i32.lt_u
        local.set 1
        br 1 (;@1;)
      end
      local.get 0
      i32.load offset=16
      local.set 6
      local.get 0
      i32.const 48
      i32.store offset=16
      local.get 0
      i32.load8_u offset=32
      local.set 12
      i32.const 1
      local.set 1
      local.get 0
      i32.const 1
      i32.store8 offset=32
      local.get 0
      i32.const 20
      i32.add
      i32.load
      local.tee 9
      local.get 0
      i32.const 24
      i32.add
      i32.load
      local.tee 10
      local.get 7
      local.get 2
      local.get 3
      call $_ZN4core3fmt9Formatter12pad_integral12write_prefix17hb93099e3a54c5cfdE
      br_if 0 (;@1;)
      local.get 11
      local.get 8
      i32.sub
      i32.const 1
      i32.add
      local.set 1
      block  ;; label = @2
        loop  ;; label = @3
          local.get 1
          i32.const -1
          i32.add
          local.tee 1
          i32.eqz
          br_if 1 (;@2;)
          local.get 9
          i32.const 48
          local.get 10
          i32.load offset=16
          call_indirect (type 1)
          i32.eqz
          br_if 0 (;@3;)
        end
        i32.const 1
        return
      end
      i32.const 1
      local.set 1
      local.get 9
      local.get 4
      local.get 5
      local.get 10
      i32.load offset=12
      call_indirect (type 0)
      br_if 0 (;@1;)
      local.get 0
      local.get 12
      i32.store8 offset=32
      local.get 0
      local.get 6
      i32.store offset=16
      i32.const 0
      return
    end
    local.get 1)
  (func $_ZN4core3fmt9Formatter12pad_integral12write_prefix17hb93099e3a54c5cfdE (type 25) (param i32 i32 i32 i32 i32) (result i32)
    (local i32)
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 2
          i32.const 1114112
          i32.eq
          br_if 0 (;@3;)
          i32.const 1
          local.set 5
          local.get 0
          local.get 2
          local.get 1
          i32.load offset=16
          call_indirect (type 1)
          br_if 1 (;@2;)
        end
        local.get 3
        br_if 1 (;@1;)
        i32.const 0
        local.set 5
      end
      local.get 5
      return
    end
    local.get 0
    local.get 3
    local.get 4
    local.get 1
    i32.load offset=12
    call_indirect (type 0))
  (func $_ZN4core5slice5index24slice_end_index_len_fail17he1e55bf2616238f7E (type 12) (param i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    local.get 0
    i32.store
    local.get 3
    local.get 1
    i32.store offset=4
    local.get 3
    i32.const 8
    i32.add
    i32.const 12
    i32.add
    i64.const 2
    i64.store align=4
    local.get 3
    i32.const 32
    i32.add
    i32.const 12
    i32.add
    i32.const 1
    i32.store
    local.get 3
    i32.const 2
    i32.store offset=12
    local.get 3
    i32.const 1050560
    i32.store offset=8
    local.get 3
    i32.const 1
    i32.store offset=36
    local.get 3
    local.get 3
    i32.const 32
    i32.add
    i32.store offset=16
    local.get 3
    local.get 3
    i32.const 4
    i32.add
    i32.store offset=40
    local.get 3
    local.get 3
    i32.store offset=32
    local.get 3
    i32.const 8
    i32.add
    local.get 2
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN4core9panicking5panic17hcfcdcc589d164b16E (type 12) (param i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    i32.const 12
    i32.add
    i64.const 0
    i64.store align=4
    local.get 3
    i32.const 1
    i32.store offset=4
    local.get 3
    i32.const 1054164
    i32.store offset=8
    local.get 3
    local.get 1
    i32.store offset=28
    local.get 3
    local.get 0
    i32.store offset=24
    local.get 3
    local.get 3
    i32.const 24
    i32.add
    i32.store
    local.get 3
    local.get 2
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17he1e3e02f5fc28a55E (type 1) (param i32 i32) (result i32)
    local.get 0
    i32.load
    local.get 1
    local.get 0
    i32.load offset=4
    i32.load offset=12
    call_indirect (type 1))
  (func $_ZN44_$LT$$RF$T$u20$as$u20$core..fmt..Display$GT$3fmt17h3efcc4100aab223eE (type 1) (param i32 i32) (result i32)
    local.get 1
    local.get 0
    i32.load
    local.get 0
    i32.load offset=4
    call $_ZN4core3fmt9Formatter3pad17h2cd94e1fc1b5b777E)
  (func $_ZN59_$LT$core..fmt..Arguments$u20$as$u20$core..fmt..Display$GT$3fmt17h2a7274ab74be954aE (type 1) (param i32 i32) (result i32)
    local.get 1
    i32.load offset=20
    local.get 1
    i32.const 24
    i32.add
    i32.load
    local.get 0
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E)
  (func $_ZN4core5slice5index22slice_index_order_fail17h677b88984b8b522bE (type 12) (param i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    local.get 0
    i32.store
    local.get 3
    local.get 1
    i32.store offset=4
    local.get 3
    i32.const 8
    i32.add
    i32.const 12
    i32.add
    i64.const 2
    i64.store align=4
    local.get 3
    i32.const 32
    i32.add
    i32.const 12
    i32.add
    i32.const 1
    i32.store
    local.get 3
    i32.const 2
    i32.store offset=12
    local.get 3
    i32.const 1050612
    i32.store offset=8
    local.get 3
    i32.const 1
    i32.store offset=36
    local.get 3
    local.get 3
    i32.const 32
    i32.add
    i32.store offset=16
    local.get 3
    local.get 3
    i32.const 4
    i32.add
    i32.store offset=40
    local.get 3
    local.get 3
    i32.store offset=32
    local.get 3
    i32.const 8
    i32.add
    local.get 2
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN4core3fmt3num50_$LT$impl$u20$core..fmt..Debug$u20$for$u20$u32$GT$3fmt17hd7e872357038b7c4E (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 128
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              local.get 1
              i32.load offset=28
              local.tee 3
              i32.const 16
              i32.and
              br_if 0 (;@5;)
              local.get 3
              i32.const 32
              i32.and
              br_if 1 (;@4;)
              local.get 0
              i64.extend_i32_u
              i32.const 1
              local.get 1
              call $_ZN4core3fmt3num3imp7fmt_u6417ha30186d55e58ac6fE
              local.set 0
              br 4 (;@1;)
            end
            i32.const 0
            local.set 3
            loop  ;; label = @5
              local.get 2
              local.get 3
              i32.add
              i32.const 127
              i32.add
              i32.const 48
              i32.const 87
              local.get 0
              i32.const 15
              i32.and
              local.tee 4
              i32.const 10
              i32.lt_u
              select
              local.get 4
              i32.add
              i32.store8
              local.get 3
              i32.const -1
              i32.add
              local.set 3
              local.get 0
              i32.const 15
              i32.gt_u
              local.set 4
              local.get 0
              i32.const 4
              i32.shr_u
              local.set 0
              local.get 4
              br_if 0 (;@5;)
            end
            local.get 3
            i32.const 128
            i32.add
            local.tee 0
            i32.const 129
            i32.ge_u
            br_if 1 (;@3;)
            local.get 1
            i32.const 1
            i32.const 1050204
            i32.const 2
            local.get 2
            local.get 3
            i32.add
            i32.const 128
            i32.add
            i32.const 0
            local.get 3
            i32.sub
            call $_ZN4core3fmt9Formatter12pad_integral17h840ce31caaa4dc56E
            local.set 0
            br 3 (;@1;)
          end
          i32.const 0
          local.set 3
          loop  ;; label = @4
            local.get 2
            local.get 3
            i32.add
            i32.const 127
            i32.add
            i32.const 48
            i32.const 55
            local.get 0
            i32.const 15
            i32.and
            local.tee 4
            i32.const 10
            i32.lt_u
            select
            local.get 4
            i32.add
            i32.store8
            local.get 3
            i32.const -1
            i32.add
            local.set 3
            local.get 0
            i32.const 15
            i32.gt_u
            local.set 4
            local.get 0
            i32.const 4
            i32.shr_u
            local.set 0
            local.get 4
            br_if 0 (;@4;)
          end
          local.get 3
          i32.const 128
          i32.add
          local.tee 0
          i32.const 129
          i32.ge_u
          br_if 1 (;@2;)
          local.get 1
          i32.const 1
          i32.const 1050204
          i32.const 2
          local.get 2
          local.get 3
          i32.add
          i32.const 128
          i32.add
          i32.const 0
          local.get 3
          i32.sub
          call $_ZN4core3fmt9Formatter12pad_integral17h840ce31caaa4dc56E
          local.set 0
          br 2 (;@1;)
        end
        local.get 0
        i32.const 128
        i32.const 1050188
        call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
        unreachable
      end
      local.get 0
      i32.const 128
      i32.const 1050188
      call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
      unreachable
    end
    local.get 2
    i32.const 128
    i32.add
    global.set $__stack_pointer
    local.get 0)
  (func $_ZN63_$LT$core..cell..BorrowMutError$u20$as$u20$core..fmt..Debug$GT$3fmt17h5ce61f4bcde0325cE (type 1) (param i32 i32) (result i32)
    local.get 1
    i32.load offset=20
    i32.const 1049800
    i32.const 14
    local.get 1
    i32.const 24
    i32.add
    i32.load
    i32.load offset=12
    call_indirect (type 0))
  (func $_ZN4core3ffi5c_str4CStr19from_bytes_with_nul17h9450f87e6dcc5836E (type 3) (param i32 i32)
    (local i32 i32)
    i32.const 0
    local.set 2
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 3
        i32.add
        i32.const -4
        i32.and
        local.tee 3
        local.get 1
        i32.eq
        br_if 0 (;@2;)
        local.get 3
        local.get 1
        i32.sub
        local.tee 3
        i32.eqz
        br_if 0 (;@2;)
        i32.const 0
        local.set 2
        loop  ;; label = @3
          local.get 1
          local.get 2
          i32.add
          i32.load8_u
          i32.eqz
          br_if 2 (;@1;)
          local.get 3
          local.get 2
          i32.const 1
          i32.add
          local.tee 2
          i32.ne
          br_if 0 (;@3;)
        end
        local.get 3
        local.set 2
      end
      block  ;; label = @2
        local.get 1
        local.get 2
        i32.add
        i32.load
        local.tee 3
        i32.const -1
        i32.xor
        local.get 3
        i32.const -16843009
        i32.add
        i32.and
        i32.const -2139062144
        i32.and
        br_if 0 (;@2;)
        local.get 2
        local.get 2
        i32.const 8
        i32.or
        local.get 1
        local.get 2
        i32.const 4
        i32.or
        i32.add
        i32.load
        local.tee 3
        i32.const -1
        i32.xor
        local.get 3
        i32.const -16843009
        i32.add
        i32.and
        i32.const -2139062144
        i32.and
        select
        local.set 2
      end
      loop  ;; label = @2
        local.get 1
        local.get 2
        i32.add
        i32.load8_u
        i32.eqz
        br_if 1 (;@1;)
        local.get 2
        i32.const 1
        i32.add
        local.tee 2
        i32.const 15
        i32.ne
        br_if 0 (;@2;)
      end
      local.get 0
      i32.const 1
      i32.store offset=4
      local.get 0
      i32.const 1
      i32.store
      return
    end
    block  ;; label = @1
      local.get 2
      i32.const 14
      i32.eq
      br_if 0 (;@1;)
      local.get 0
      i32.const 0
      i32.store offset=4
      local.get 0
      i32.const 8
      i32.add
      local.get 2
      i32.store
      local.get 0
      i32.const 1
      i32.store
      return
    end
    local.get 0
    local.get 1
    i32.store offset=4
    local.get 0
    i32.const 8
    i32.add
    i32.const 15
    i32.store
    local.get 0
    i32.const 0
    i32.store)
  (func $_ZN53_$LT$core..fmt..Error$u20$as$u20$core..fmt..Debug$GT$3fmt17h8ca99f446535e2f5E (type 1) (param i32 i32) (result i32)
    local.get 1
    i32.load offset=20
    i32.const 1052492
    i32.const 5
    local.get 1
    i32.const 24
    i32.add
    i32.load
    i32.load offset=12
    call_indirect (type 0))
  (func $_ZN73_$LT$core..panic..panic_info..PanicInfo$u20$as$u20$core..fmt..Display$GT$3fmt17hcc3487ec06dc686aE (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 64
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    i32.const 1
    local.set 3
    block  ;; label = @1
      local.get 1
      i32.load offset=20
      local.tee 4
      i32.const 1049840
      i32.const 12
      local.get 1
      i32.const 24
      i32.add
      i32.load
      local.tee 1
      i32.load offset=12
      call_indirect (type 0)
      br_if 0 (;@1;)
      block  ;; label = @2
        block  ;; label = @3
          local.get 0
          i32.load offset=12
          local.tee 5
          i32.eqz
          br_if 0 (;@3;)
          local.get 2
          local.get 5
          i32.store offset=12
          local.get 2
          i32.const 7
          i32.store offset=20
          local.get 2
          local.get 2
          i32.const 12
          i32.add
          i32.store offset=16
          local.get 2
          i64.const 1
          i64.store offset=52 align=4
          local.get 2
          i32.const 2
          i32.store offset=44
          local.get 2
          i32.const 1049856
          i32.store offset=40
          local.get 2
          local.get 2
          i32.const 16
          i32.add
          i32.store offset=48
          local.get 4
          local.get 1
          local.get 2
          i32.const 40
          i32.add
          call $_ZN4core3fmt5write17h8253e306f6bd0e19E
          i32.eqz
          br_if 1 (;@2;)
          br 2 (;@1;)
        end
        local.get 0
        i32.load
        local.tee 5
        local.get 0
        i32.load offset=4
        i32.const 12
        i32.add
        i32.load
        call_indirect (type 6)
        i64.const -4493808902380553279
        i64.ne
        br_if 0 (;@2;)
        local.get 2
        local.get 5
        i32.store offset=12
        local.get 2
        i32.const 8
        i32.store offset=20
        local.get 2
        local.get 2
        i32.const 12
        i32.add
        i32.store offset=16
        local.get 2
        i64.const 1
        i64.store offset=52 align=4
        local.get 2
        i32.const 2
        i32.store offset=44
        local.get 2
        i32.const 1049856
        i32.store offset=40
        local.get 2
        local.get 2
        i32.const 16
        i32.add
        i32.store offset=48
        local.get 4
        local.get 1
        local.get 2
        i32.const 40
        i32.add
        call $_ZN4core3fmt5write17h8253e306f6bd0e19E
        br_if 1 (;@1;)
      end
      local.get 0
      i32.load offset=8
      local.set 3
      local.get 2
      i32.const 36
      i32.add
      i32.const 1
      i32.store
      local.get 2
      i32.const 16
      i32.add
      i32.const 12
      i32.add
      i32.const 1
      i32.store
      local.get 2
      local.get 3
      i32.const 12
      i32.add
      i32.store offset=32
      local.get 2
      local.get 3
      i32.const 8
      i32.add
      i32.store offset=24
      local.get 2
      i32.const 5
      i32.store offset=20
      local.get 2
      local.get 3
      i32.store offset=16
      local.get 2
      i64.const 3
      i64.store offset=52 align=4
      local.get 2
      i32.const 3
      i32.store offset=44
      local.get 2
      i32.const 1049816
      i32.store offset=40
      local.get 2
      local.get 2
      i32.const 16
      i32.add
      i32.store offset=48
      local.get 4
      local.get 1
      local.get 2
      i32.const 40
      i32.add
      call $_ZN4core3fmt5write17h8253e306f6bd0e19E
      local.set 3
    end
    local.get 2
    i32.const 64
    i32.add
    global.set $__stack_pointer
    local.get 3)
  (func $_ZN44_$LT$$RF$T$u20$as$u20$core..fmt..Display$GT$3fmt17hf33a8949ac184540E (type 1) (param i32 i32) (result i32)
    local.get 1
    i32.load offset=20
    local.get 1
    i32.const 24
    i32.add
    i32.load
    local.get 0
    i32.load
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E)
  (func $_ZN44_$LT$$RF$T$u20$as$u20$core..fmt..Display$GT$3fmt17h6d756373b98cd7c1E (type 1) (param i32 i32) (result i32)
    local.get 1
    local.get 0
    i32.load
    local.tee 0
    i32.load
    local.get 0
    i32.load offset=4
    call $_ZN4core3fmt9Formatter3pad17h2cd94e1fc1b5b777E)
  (func $_ZN68_$LT$core..fmt..builders..PadAdapter$u20$as$u20$core..fmt..Write$GT$9write_str17hd4ac5b916bf4e0b0E (type 0) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    local.get 0
    i32.load offset=4
    local.set 3
    local.get 0
    i32.load
    local.set 4
    local.get 0
    i32.load offset=8
    local.set 5
    i32.const 0
    local.set 6
    i32.const 0
    local.set 7
    i32.const 0
    local.set 8
    i32.const 0
    local.set 9
    block  ;; label = @1
      loop  ;; label = @2
        local.get 9
        i32.const 255
        i32.and
        br_if 1 (;@1;)
        block  ;; label = @3
          block  ;; label = @4
            local.get 8
            local.get 2
            i32.gt_u
            br_if 0 (;@4;)
            loop  ;; label = @5
              local.get 1
              local.get 8
              i32.add
              local.set 10
              block  ;; label = @6
                block  ;; label = @7
                  local.get 2
                  local.get 8
                  i32.sub
                  local.tee 11
                  i32.const 8
                  i32.lt_u
                  br_if 0 (;@7;)
                  block  ;; label = @8
                    block  ;; label = @9
                      block  ;; label = @10
                        local.get 10
                        i32.const 3
                        i32.add
                        i32.const -4
                        i32.and
                        local.tee 0
                        local.get 10
                        i32.eq
                        br_if 0 (;@10;)
                        local.get 0
                        local.get 10
                        i32.sub
                        local.tee 12
                        i32.eqz
                        br_if 0 (;@10;)
                        i32.const 0
                        local.set 0
                        loop  ;; label = @11
                          local.get 10
                          local.get 0
                          i32.add
                          i32.load8_u
                          i32.const 10
                          i32.eq
                          br_if 5 (;@6;)
                          local.get 12
                          local.get 0
                          i32.const 1
                          i32.add
                          local.tee 0
                          i32.ne
                          br_if 0 (;@11;)
                        end
                        local.get 12
                        local.get 11
                        i32.const -8
                        i32.add
                        local.tee 13
                        i32.le_u
                        br_if 1 (;@9;)
                        br 2 (;@8;)
                      end
                      local.get 11
                      i32.const -8
                      i32.add
                      local.set 13
                      i32.const 0
                      local.set 12
                    end
                    loop  ;; label = @9
                      local.get 10
                      local.get 12
                      i32.add
                      local.tee 9
                      i32.load
                      local.tee 0
                      i32.const -1
                      i32.xor
                      local.get 0
                      i32.const 168430090
                      i32.xor
                      i32.const -16843009
                      i32.add
                      i32.and
                      i32.const -2139062144
                      i32.and
                      br_if 1 (;@8;)
                      local.get 9
                      i32.const 4
                      i32.add
                      i32.load
                      local.tee 0
                      i32.const -1
                      i32.xor
                      local.get 0
                      i32.const 168430090
                      i32.xor
                      i32.const -16843009
                      i32.add
                      i32.and
                      i32.const -2139062144
                      i32.and
                      br_if 1 (;@8;)
                      local.get 12
                      i32.const 8
                      i32.add
                      local.tee 12
                      local.get 13
                      i32.le_u
                      br_if 0 (;@9;)
                    end
                  end
                  block  ;; label = @8
                    local.get 11
                    local.get 12
                    i32.ne
                    br_if 0 (;@8;)
                    local.get 2
                    local.set 8
                    br 4 (;@4;)
                  end
                  loop  ;; label = @8
                    block  ;; label = @9
                      local.get 10
                      local.get 12
                      i32.add
                      i32.load8_u
                      i32.const 10
                      i32.ne
                      br_if 0 (;@9;)
                      local.get 12
                      local.set 0
                      br 3 (;@6;)
                    end
                    local.get 11
                    local.get 12
                    i32.const 1
                    i32.add
                    local.tee 12
                    i32.ne
                    br_if 0 (;@8;)
                  end
                  local.get 2
                  local.set 8
                  br 3 (;@4;)
                end
                block  ;; label = @7
                  local.get 8
                  local.get 2
                  i32.ne
                  br_if 0 (;@7;)
                  local.get 2
                  local.set 8
                  br 3 (;@4;)
                end
                i32.const 0
                local.set 0
                loop  ;; label = @7
                  local.get 10
                  local.get 0
                  i32.add
                  i32.load8_u
                  i32.const 10
                  i32.eq
                  br_if 1 (;@6;)
                  local.get 11
                  local.get 0
                  i32.const 1
                  i32.add
                  local.tee 0
                  i32.ne
                  br_if 0 (;@7;)
                end
                local.get 2
                local.set 8
                br 2 (;@4;)
              end
              local.get 8
              local.get 0
              i32.add
              local.tee 0
              i32.const 1
              i32.add
              local.set 8
              block  ;; label = @6
                local.get 0
                local.get 2
                i32.ge_u
                br_if 0 (;@6;)
                local.get 1
                local.get 0
                i32.add
                i32.load8_u
                i32.const 10
                i32.ne
                br_if 0 (;@6;)
                i32.const 0
                local.set 9
                local.get 8
                local.set 13
                local.get 8
                local.set 0
                br 3 (;@3;)
              end
              local.get 8
              local.get 2
              i32.le_u
              br_if 0 (;@5;)
            end
          end
          i32.const 1
          local.set 9
          local.get 7
          local.set 13
          local.get 2
          local.set 0
          local.get 7
          local.get 2
          i32.eq
          br_if 2 (;@1;)
        end
        block  ;; label = @3
          block  ;; label = @4
            local.get 5
            i32.load8_u
            i32.eqz
            br_if 0 (;@4;)
            local.get 4
            i32.const 1050128
            i32.const 4
            local.get 3
            i32.load offset=12
            call_indirect (type 0)
            br_if 1 (;@3;)
          end
          local.get 1
          local.get 7
          i32.add
          local.set 12
          local.get 0
          local.get 7
          i32.sub
          local.set 10
          i32.const 0
          local.set 11
          block  ;; label = @4
            local.get 0
            local.get 7
            i32.eq
            br_if 0 (;@4;)
            local.get 10
            local.get 12
            i32.add
            i32.const -1
            i32.add
            i32.load8_u
            i32.const 10
            i32.eq
            local.set 11
          end
          local.get 5
          local.get 11
          i32.store8
          local.get 13
          local.set 7
          local.get 4
          local.get 12
          local.get 10
          local.get 3
          i32.load offset=12
          call_indirect (type 0)
          i32.eqz
          br_if 1 (;@2;)
        end
      end
      i32.const 1
      local.set 6
    end
    local.get 6)
  (func $_ZN4core3fmt8builders11DebugStruct5field17h52a4d0d1d2d279aeE (type 25) (param i32 i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i64)
    global.get $__stack_pointer
    i32.const 64
    i32.sub
    local.tee 5
    global.set $__stack_pointer
    i32.const 1
    local.set 6
    block  ;; label = @1
      local.get 0
      i32.load8_u offset=4
      br_if 0 (;@1;)
      local.get 0
      i32.load8_u offset=5
      local.set 7
      block  ;; label = @2
        local.get 0
        i32.load
        local.tee 8
        i32.load offset=28
        local.tee 9
        i32.const 4
        i32.and
        br_if 0 (;@2;)
        i32.const 1
        local.set 6
        local.get 8
        i32.load offset=20
        i32.const 1050137
        i32.const 1050139
        local.get 7
        i32.const 255
        i32.and
        local.tee 7
        select
        i32.const 2
        i32.const 3
        local.get 7
        select
        local.get 8
        i32.const 24
        i32.add
        i32.load
        i32.load offset=12
        call_indirect (type 0)
        br_if 1 (;@1;)
        i32.const 1
        local.set 6
        local.get 8
        i32.load offset=20
        local.get 1
        local.get 2
        local.get 8
        i32.load offset=24
        i32.load offset=12
        call_indirect (type 0)
        br_if 1 (;@1;)
        i32.const 1
        local.set 6
        local.get 8
        i32.load offset=20
        i32.const 1050084
        i32.const 2
        local.get 8
        i32.load offset=24
        i32.load offset=12
        call_indirect (type 0)
        br_if 1 (;@1;)
        local.get 3
        local.get 8
        local.get 4
        call_indirect (type 1)
        local.set 6
        br 1 (;@1;)
      end
      block  ;; label = @2
        local.get 7
        i32.const 255
        i32.and
        br_if 0 (;@2;)
        i32.const 1
        local.set 6
        local.get 8
        i32.load offset=20
        i32.const 1050132
        i32.const 3
        local.get 8
        i32.const 24
        i32.add
        i32.load
        i32.load offset=12
        call_indirect (type 0)
        br_if 1 (;@1;)
        local.get 8
        i32.load offset=28
        local.set 9
      end
      i32.const 1
      local.set 6
      local.get 5
      i32.const 1
      i32.store8 offset=23
      local.get 5
      i32.const 48
      i32.add
      i32.const 1050104
      i32.store
      local.get 5
      local.get 8
      i64.load offset=20 align=4
      i64.store offset=8
      local.get 5
      local.get 5
      i32.const 23
      i32.add
      i32.store offset=16
      local.get 5
      local.get 8
      i64.load offset=8 align=4
      i64.store offset=32
      local.get 8
      i64.load align=4
      local.set 10
      local.get 5
      local.get 9
      i32.store offset=52
      local.get 5
      local.get 8
      i32.load offset=16
      i32.store offset=40
      local.get 5
      local.get 8
      i32.load8_u offset=32
      i32.store8 offset=56
      local.get 5
      local.get 10
      i64.store offset=24
      local.get 5
      local.get 5
      i32.const 8
      i32.add
      i32.store offset=44
      local.get 5
      i32.const 8
      i32.add
      local.get 1
      local.get 2
      call $_ZN68_$LT$core..fmt..builders..PadAdapter$u20$as$u20$core..fmt..Write$GT$9write_str17hd4ac5b916bf4e0b0E
      br_if 0 (;@1;)
      local.get 5
      i32.const 8
      i32.add
      i32.const 1050084
      i32.const 2
      call $_ZN68_$LT$core..fmt..builders..PadAdapter$u20$as$u20$core..fmt..Write$GT$9write_str17hd4ac5b916bf4e0b0E
      br_if 0 (;@1;)
      local.get 3
      local.get 5
      i32.const 24
      i32.add
      local.get 4
      call_indirect (type 1)
      br_if 0 (;@1;)
      local.get 5
      i32.load offset=44
      i32.const 1050135
      i32.const 2
      local.get 5
      i32.load offset=48
      i32.load offset=12
      call_indirect (type 0)
      local.set 6
    end
    local.get 0
    i32.const 1
    i32.store8 offset=5
    local.get 0
    local.get 6
    i32.store8 offset=4
    local.get 5
    i32.const 64
    i32.add
    global.set $__stack_pointer
    local.get 0)
  (func $_ZN4core3fmt5Write10write_char17ha7c13b4705496bbdE (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    i32.const 0
    i32.store offset=12
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 128
        i32.lt_u
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 1
          i32.const 2048
          i32.lt_u
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 1
            i32.const 65536
            i32.lt_u
            br_if 0 (;@4;)
            local.get 2
            local.get 1
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=15
            local.get 2
            local.get 1
            i32.const 6
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=14
            local.get 2
            local.get 1
            i32.const 12
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=13
            local.get 2
            local.get 1
            i32.const 18
            i32.shr_u
            i32.const 7
            i32.and
            i32.const 240
            i32.or
            i32.store8 offset=12
            i32.const 4
            local.set 1
            br 3 (;@1;)
          end
          local.get 2
          local.get 1
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=14
          local.get 2
          local.get 1
          i32.const 12
          i32.shr_u
          i32.const 224
          i32.or
          i32.store8 offset=12
          local.get 2
          local.get 1
          i32.const 6
          i32.shr_u
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=13
          i32.const 3
          local.set 1
          br 2 (;@1;)
        end
        local.get 2
        local.get 1
        i32.const 63
        i32.and
        i32.const 128
        i32.or
        i32.store8 offset=13
        local.get 2
        local.get 1
        i32.const 6
        i32.shr_u
        i32.const 192
        i32.or
        i32.store8 offset=12
        i32.const 2
        local.set 1
        br 1 (;@1;)
      end
      local.get 2
      local.get 1
      i32.store8 offset=12
      i32.const 1
      local.set 1
    end
    local.get 0
    local.get 2
    i32.const 12
    i32.add
    local.get 1
    call $_ZN68_$LT$core..fmt..builders..PadAdapter$u20$as$u20$core..fmt..Write$GT$9write_str17hd4ac5b916bf4e0b0E
    local.set 1
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core3fmt5Write9write_fmt17h99728a0a28fde9f9E (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    local.get 0
    i32.store offset=4
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    i32.const 4
    i32.add
    i32.const 1050408
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 1
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h3bfd604354950662E (type 0) (param i32 i32 i32) (result i32)
    local.get 0
    i32.load
    local.get 1
    local.get 2
    call $_ZN68_$LT$core..fmt..builders..PadAdapter$u20$as$u20$core..fmt..Write$GT$9write_str17hd4ac5b916bf4e0b0E)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17heffbb38722d0b741E (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    local.get 2
    i32.const 0
    i32.store offset=12
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 128
        i32.lt_u
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 1
          i32.const 2048
          i32.lt_u
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 1
            i32.const 65536
            i32.lt_u
            br_if 0 (;@4;)
            local.get 2
            local.get 1
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=15
            local.get 2
            local.get 1
            i32.const 6
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=14
            local.get 2
            local.get 1
            i32.const 12
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=13
            local.get 2
            local.get 1
            i32.const 18
            i32.shr_u
            i32.const 7
            i32.and
            i32.const 240
            i32.or
            i32.store8 offset=12
            i32.const 4
            local.set 1
            br 3 (;@1;)
          end
          local.get 2
          local.get 1
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=14
          local.get 2
          local.get 1
          i32.const 12
          i32.shr_u
          i32.const 224
          i32.or
          i32.store8 offset=12
          local.get 2
          local.get 1
          i32.const 6
          i32.shr_u
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=13
          i32.const 3
          local.set 1
          br 2 (;@1;)
        end
        local.get 2
        local.get 1
        i32.const 63
        i32.and
        i32.const 128
        i32.or
        i32.store8 offset=13
        local.get 2
        local.get 1
        i32.const 6
        i32.shr_u
        i32.const 192
        i32.or
        i32.store8 offset=12
        i32.const 2
        local.set 1
        br 1 (;@1;)
      end
      local.get 2
      local.get 1
      i32.store8 offset=12
      i32.const 1
      local.set 1
    end
    local.get 0
    local.get 2
    i32.const 12
    i32.add
    local.get 1
    call $_ZN68_$LT$core..fmt..builders..PadAdapter$u20$as$u20$core..fmt..Write$GT$9write_str17hd4ac5b916bf4e0b0E
    local.set 1
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17hbdaf748e5c297b7aE (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    local.get 0
    i32.store offset=4
    local.get 2
    i32.const 4
    i32.add
    i32.const 1050408
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 1
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core3fmt8builders11DebugStruct6finish17h24c6b68ba16e2ce0E (type 5) (param i32) (result i32)
    (local i32 i32)
    local.get 0
    i32.load8_u offset=4
    local.set 1
    block  ;; label = @1
      local.get 0
      i32.load8_u offset=5
      br_if 0 (;@1;)
      local.get 1
      i32.const 255
      i32.and
      i32.const 0
      i32.ne
      return
    end
    i32.const 1
    local.set 2
    block  ;; label = @1
      local.get 1
      i32.const 255
      i32.and
      br_if 0 (;@1;)
      block  ;; label = @2
        local.get 0
        i32.load
        local.tee 1
        i32.load8_u offset=28
        i32.const 4
        i32.and
        br_if 0 (;@2;)
        local.get 0
        local.get 1
        i32.load offset=20
        i32.const 1050159
        i32.const 2
        local.get 1
        i32.const 24
        i32.add
        i32.load
        i32.load offset=12
        call_indirect (type 0)
        local.tee 1
        i32.store8 offset=4
        local.get 1
        return
      end
      local.get 1
      i32.load offset=20
      i32.const 1050145
      i32.const 1
      local.get 1
      i32.const 24
      i32.add
      i32.load
      i32.load offset=12
      call_indirect (type 0)
      local.set 2
    end
    local.get 0
    local.get 2
    i32.store8 offset=4
    local.get 2)
  (func $_ZN4core3fmt9Formatter9write_fmt17h5cc4795932e82988E (type 0) (param i32 i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 2
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 3
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 2
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 3
    local.get 2
    i64.load align=4
    i64.store offset=8
    local.get 0
    local.get 1
    local.get 3
    i32.const 8
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 2
    local.get 3
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 2)
  (func $_ZN4core3str16slice_error_fail17h9100964d4f03db1dE (type 11) (param i32 i32 i32 i32 i32)
    local.get 0
    local.get 1
    local.get 2
    local.get 3
    local.get 4
    call $_ZN4core3str19slice_error_fail_rt17hed5fe7020735bfc1E
    unreachable)
  (func $_ZN4core3str19slice_error_fail_rt17hed5fe7020735bfc1E (type 11) (param i32 i32 i32 i32 i32)
    (local i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 112
    i32.sub
    local.tee 5
    global.set $__stack_pointer
    local.get 5
    local.get 3
    i32.store offset=12
    local.get 5
    local.get 2
    i32.store offset=8
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 1
          i32.const 257
          i32.lt_u
          br_if 0 (;@3;)
          i32.const 256
          local.set 6
          block  ;; label = @4
            local.get 0
            i32.load8_s offset=256
            i32.const -65
            i32.gt_s
            br_if 0 (;@4;)
            i32.const 255
            local.set 6
            local.get 0
            i32.load8_s offset=255
            i32.const -65
            i32.gt_s
            br_if 0 (;@4;)
            i32.const 254
            local.set 6
            local.get 0
            i32.load8_s offset=254
            i32.const -65
            i32.gt_s
            br_if 0 (;@4;)
            i32.const 253
            local.set 6
            local.get 0
            i32.load8_s offset=253
            i32.const -65
            i32.le_s
            br_if 2 (;@2;)
          end
          local.get 5
          local.get 6
          i32.store offset=20
          local.get 5
          local.get 0
          i32.store offset=16
          i32.const 5
          local.set 6
          i32.const 1050628
          local.set 7
          br 2 (;@1;)
        end
        local.get 5
        local.get 1
        i32.store offset=20
        local.get 5
        local.get 0
        i32.store offset=16
        i32.const 0
        local.set 6
        i32.const 1054164
        local.set 7
        br 1 (;@1;)
      end
      local.get 0
      local.get 1
      i32.const 0
      i32.const 253
      local.get 4
      call $_ZN4core3str16slice_error_fail17h9100964d4f03db1dE
      unreachable
    end
    local.get 5
    local.get 6
    i32.store offset=28
    local.get 5
    local.get 7
    i32.store offset=24
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            local.get 2
            local.get 1
            i32.gt_u
            local.tee 6
            br_if 0 (;@4;)
            local.get 3
            local.get 1
            i32.gt_u
            br_if 0 (;@4;)
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    local.get 2
                    local.get 3
                    i32.gt_u
                    br_if 0 (;@8;)
                    block  ;; label = @9
                      block  ;; label = @10
                        local.get 2
                        i32.eqz
                        br_if 0 (;@10;)
                        block  ;; label = @11
                          local.get 2
                          local.get 1
                          i32.lt_u
                          br_if 0 (;@11;)
                          local.get 2
                          local.get 1
                          i32.eq
                          br_if 1 (;@10;)
                          br 2 (;@9;)
                        end
                        local.get 0
                        local.get 2
                        i32.add
                        i32.load8_s
                        i32.const -64
                        i32.lt_s
                        br_if 1 (;@9;)
                      end
                      local.get 3
                      local.set 2
                    end
                    local.get 5
                    local.get 2
                    i32.store offset=32
                    local.get 1
                    local.set 3
                    block  ;; label = @9
                      local.get 2
                      local.get 1
                      i32.ge_u
                      br_if 0 (;@9;)
                      local.get 2
                      i32.const 1
                      i32.add
                      local.tee 6
                      i32.const 0
                      local.get 2
                      i32.const -3
                      i32.add
                      local.tee 3
                      local.get 3
                      local.get 2
                      i32.gt_u
                      select
                      local.tee 3
                      i32.lt_u
                      br_if 6 (;@3;)
                      block  ;; label = @10
                        local.get 3
                        local.get 6
                        i32.eq
                        br_if 0 (;@10;)
                        local.get 0
                        local.get 6
                        i32.add
                        local.get 0
                        local.get 3
                        i32.add
                        local.tee 8
                        i32.sub
                        local.set 6
                        block  ;; label = @11
                          local.get 0
                          local.get 2
                          i32.add
                          local.tee 9
                          i32.load8_s
                          i32.const -65
                          i32.le_s
                          br_if 0 (;@11;)
                          local.get 6
                          i32.const -1
                          i32.add
                          local.set 7
                          br 1 (;@10;)
                        end
                        local.get 3
                        local.get 2
                        i32.eq
                        br_if 0 (;@10;)
                        block  ;; label = @11
                          local.get 9
                          i32.const -1
                          i32.add
                          local.tee 2
                          i32.load8_s
                          i32.const -65
                          i32.le_s
                          br_if 0 (;@11;)
                          local.get 6
                          i32.const -2
                          i32.add
                          local.set 7
                          br 1 (;@10;)
                        end
                        local.get 8
                        local.get 2
                        i32.eq
                        br_if 0 (;@10;)
                        block  ;; label = @11
                          local.get 2
                          i32.const -1
                          i32.add
                          local.tee 2
                          i32.load8_s
                          i32.const -65
                          i32.le_s
                          br_if 0 (;@11;)
                          local.get 6
                          i32.const -3
                          i32.add
                          local.set 7
                          br 1 (;@10;)
                        end
                        local.get 8
                        local.get 2
                        i32.eq
                        br_if 0 (;@10;)
                        block  ;; label = @11
                          local.get 2
                          i32.const -1
                          i32.add
                          local.tee 2
                          i32.load8_s
                          i32.const -65
                          i32.le_s
                          br_if 0 (;@11;)
                          local.get 6
                          i32.const -4
                          i32.add
                          local.set 7
                          br 1 (;@10;)
                        end
                        local.get 8
                        local.get 2
                        i32.eq
                        br_if 0 (;@10;)
                        local.get 6
                        i32.const -5
                        i32.add
                        local.set 7
                      end
                      local.get 7
                      local.get 3
                      i32.add
                      local.set 3
                    end
                    block  ;; label = @9
                      local.get 3
                      i32.eqz
                      br_if 0 (;@9;)
                      block  ;; label = @10
                        block  ;; label = @11
                          local.get 3
                          local.get 1
                          i32.lt_u
                          br_if 0 (;@11;)
                          local.get 1
                          local.get 3
                          i32.eq
                          br_if 1 (;@10;)
                          br 10 (;@1;)
                        end
                        local.get 0
                        local.get 3
                        i32.add
                        i32.load8_s
                        i32.const -65
                        i32.le_s
                        br_if 9 (;@1;)
                      end
                      local.get 1
                      local.get 3
                      i32.sub
                      local.set 1
                    end
                    local.get 1
                    i32.eqz
                    br_if 6 (;@2;)
                    block  ;; label = @9
                      block  ;; label = @10
                        local.get 0
                        local.get 3
                        i32.add
                        local.tee 1
                        i32.load8_s
                        local.tee 2
                        i32.const -1
                        i32.gt_s
                        br_if 0 (;@10;)
                        local.get 1
                        i32.load8_u offset=1
                        i32.const 63
                        i32.and
                        local.set 0
                        local.get 2
                        i32.const 31
                        i32.and
                        local.set 6
                        local.get 2
                        i32.const -33
                        i32.gt_u
                        br_if 1 (;@9;)
                        local.get 6
                        i32.const 6
                        i32.shl
                        local.get 0
                        i32.or
                        local.set 1
                        br 4 (;@6;)
                      end
                      local.get 5
                      local.get 2
                      i32.const 255
                      i32.and
                      i32.store offset=36
                      i32.const 1
                      local.set 2
                      br 4 (;@5;)
                    end
                    local.get 0
                    i32.const 6
                    i32.shl
                    local.get 1
                    i32.load8_u offset=2
                    i32.const 63
                    i32.and
                    i32.or
                    local.set 0
                    local.get 2
                    i32.const -16
                    i32.ge_u
                    br_if 1 (;@7;)
                    local.get 0
                    local.get 6
                    i32.const 12
                    i32.shl
                    i32.or
                    local.set 1
                    br 2 (;@6;)
                  end
                  local.get 5
                  i32.const 100
                  i32.add
                  i32.const 5
                  i32.store
                  local.get 5
                  i32.const 92
                  i32.add
                  i32.const 5
                  i32.store
                  local.get 5
                  i32.const 72
                  i32.add
                  i32.const 12
                  i32.add
                  i32.const 1
                  i32.store
                  local.get 5
                  i32.const 48
                  i32.add
                  i32.const 12
                  i32.add
                  i64.const 4
                  i64.store align=4
                  local.get 5
                  i32.const 4
                  i32.store offset=52
                  local.get 5
                  i32.const 1050728
                  i32.store offset=48
                  local.get 5
                  i32.const 1
                  i32.store offset=76
                  local.get 5
                  local.get 5
                  i32.const 72
                  i32.add
                  i32.store offset=56
                  local.get 5
                  local.get 5
                  i32.const 24
                  i32.add
                  i32.store offset=96
                  local.get 5
                  local.get 5
                  i32.const 16
                  i32.add
                  i32.store offset=88
                  local.get 5
                  local.get 5
                  i32.const 12
                  i32.add
                  i32.store offset=80
                  local.get 5
                  local.get 5
                  i32.const 8
                  i32.add
                  i32.store offset=72
                  local.get 5
                  i32.const 48
                  i32.add
                  local.get 4
                  call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
                  unreachable
                end
                local.get 0
                i32.const 6
                i32.shl
                local.get 1
                i32.load8_u offset=3
                i32.const 63
                i32.and
                i32.or
                local.get 6
                i32.const 18
                i32.shl
                i32.const 1835008
                i32.and
                i32.or
                local.tee 1
                i32.const 1114112
                i32.eq
                br_if 4 (;@2;)
              end
              local.get 5
              local.get 1
              i32.store offset=36
              i32.const 1
              local.set 2
              local.get 1
              i32.const 128
              i32.lt_u
              br_if 0 (;@5;)
              i32.const 2
              local.set 2
              local.get 1
              i32.const 2047
              i32.le_u
              br_if 0 (;@5;)
              i32.const 3
              i32.const 4
              local.get 1
              i32.const 65536
              i32.lt_u
              select
              local.set 2
            end
            local.get 5
            local.get 3
            i32.store offset=40
            local.get 5
            local.get 2
            local.get 3
            i32.add
            i32.store offset=44
            local.get 5
            i32.const 48
            i32.add
            i32.const 12
            i32.add
            i64.const 5
            i64.store align=4
            local.get 5
            i32.const 108
            i32.add
            i32.const 5
            i32.store
            local.get 5
            i32.const 100
            i32.add
            i32.const 5
            i32.store
            local.get 5
            i32.const 92
            i32.add
            i32.const 9
            i32.store
            local.get 5
            i32.const 72
            i32.add
            i32.const 12
            i32.add
            i32.const 10
            i32.store
            local.get 5
            i32.const 5
            i32.store offset=52
            local.get 5
            i32.const 1050812
            i32.store offset=48
            local.get 5
            i32.const 1
            i32.store offset=76
            local.get 5
            local.get 5
            i32.const 72
            i32.add
            i32.store offset=56
            local.get 5
            local.get 5
            i32.const 24
            i32.add
            i32.store offset=104
            local.get 5
            local.get 5
            i32.const 16
            i32.add
            i32.store offset=96
            local.get 5
            local.get 5
            i32.const 40
            i32.add
            i32.store offset=88
            local.get 5
            local.get 5
            i32.const 36
            i32.add
            i32.store offset=80
            local.get 5
            local.get 5
            i32.const 32
            i32.add
            i32.store offset=72
            local.get 5
            i32.const 48
            i32.add
            local.get 4
            call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
            unreachable
          end
          local.get 5
          local.get 2
          local.get 3
          local.get 6
          select
          i32.store offset=40
          local.get 5
          i32.const 48
          i32.add
          i32.const 12
          i32.add
          i64.const 3
          i64.store align=4
          local.get 5
          i32.const 92
          i32.add
          i32.const 5
          i32.store
          local.get 5
          i32.const 72
          i32.add
          i32.const 12
          i32.add
          i32.const 5
          i32.store
          local.get 5
          i32.const 3
          i32.store offset=52
          local.get 5
          i32.const 1050668
          i32.store offset=48
          local.get 5
          i32.const 1
          i32.store offset=76
          local.get 5
          local.get 5
          i32.const 72
          i32.add
          i32.store offset=56
          local.get 5
          local.get 5
          i32.const 24
          i32.add
          i32.store offset=88
          local.get 5
          local.get 5
          i32.const 16
          i32.add
          i32.store offset=80
          local.get 5
          local.get 5
          i32.const 40
          i32.add
          i32.store offset=72
          local.get 5
          i32.const 48
          i32.add
          local.get 4
          call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
          unreachable
        end
        local.get 3
        local.get 6
        i32.const 1050880
        call $_ZN4core5slice5index22slice_index_order_fail17h677b88984b8b522bE
        unreachable
      end
      i32.const 1054072
      i32.const 43
      local.get 4
      call $_ZN4core9panicking5panic17hcfcdcc589d164b16E
      unreachable
    end
    local.get 0
    local.get 1
    local.get 3
    local.get 1
    local.get 4
    call $_ZN4core3str16slice_error_fail17h9100964d4f03db1dE
    unreachable)
  (func $_ZN4core4char7methods22_$LT$impl$u20$char$GT$16escape_debug_ext17h35ef25b93b9973daE (type 12) (param i32 i32 i32)
    (local i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    block  ;; label = @9
                      block  ;; label = @10
                        local.get 1
                        br_table 1 (;@9;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 2 (;@8;) 4 (;@6;) 8 (;@2;) 8 (;@2;) 3 (;@7;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 7 (;@3;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 8 (;@2;) 6 (;@4;) 0 (;@10;)
                      end
                      local.get 1
                      i32.const 92
                      i32.eq
                      br_if 4 (;@5;)
                      br 7 (;@2;)
                    end
                    local.get 0
                    i32.const 512
                    i32.store16 offset=10
                    local.get 0
                    i64.const 0
                    i64.store offset=2 align=2
                    local.get 0
                    i32.const 12380
                    i32.store16
                    br 7 (;@1;)
                  end
                  local.get 0
                  i32.const 512
                  i32.store16 offset=10
                  local.get 0
                  i64.const 0
                  i64.store offset=2 align=2
                  local.get 0
                  i32.const 29788
                  i32.store16
                  br 6 (;@1;)
                end
                local.get 0
                i32.const 512
                i32.store16 offset=10
                local.get 0
                i64.const 0
                i64.store offset=2 align=2
                local.get 0
                i32.const 29276
                i32.store16
                br 5 (;@1;)
              end
              local.get 0
              i32.const 512
              i32.store16 offset=10
              local.get 0
              i64.const 0
              i64.store offset=2 align=2
              local.get 0
              i32.const 28252
              i32.store16
              br 4 (;@1;)
            end
            local.get 0
            i32.const 512
            i32.store16 offset=10
            local.get 0
            i64.const 0
            i64.store offset=2 align=2
            local.get 0
            i32.const 23644
            i32.store16
            br 3 (;@1;)
          end
          local.get 2
          i32.const 256
          i32.and
          i32.eqz
          br_if 1 (;@2;)
          local.get 0
          i32.const 512
          i32.store16 offset=10
          local.get 0
          i64.const 0
          i64.store offset=2 align=2
          local.get 0
          i32.const 10076
          i32.store16
          br 2 (;@1;)
        end
        local.get 2
        i32.const 65536
        i32.and
        i32.eqz
        br_if 0 (;@2;)
        local.get 0
        i32.const 512
        i32.store16 offset=10
        local.get 0
        i64.const 0
        i64.store offset=2 align=2
        local.get 0
        i32.const 8796
        i32.store16
        br 1 (;@1;)
      end
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              local.get 2
              i32.const 1
              i32.and
              i32.eqz
              br_if 0 (;@5;)
              local.get 1
              i32.const 11
              i32.shl
              local.set 4
              i32.const 0
              local.set 2
              i32.const 33
              local.set 5
              i32.const 33
              local.set 6
              block  ;; label = @6
                block  ;; label = @7
                  loop  ;; label = @8
                    block  ;; label = @9
                      block  ;; label = @10
                        i32.const -1
                        local.get 5
                        i32.const 1
                        i32.shr_u
                        local.get 2
                        i32.add
                        local.tee 5
                        i32.const 2
                        i32.shl
                        i32.const 1052532
                        i32.add
                        i32.load
                        i32.const 11
                        i32.shl
                        local.tee 7
                        local.get 4
                        i32.ne
                        local.get 7
                        local.get 4
                        i32.lt_u
                        select
                        local.tee 7
                        i32.const 1
                        i32.ne
                        br_if 0 (;@10;)
                        local.get 5
                        local.set 6
                        br 1 (;@9;)
                      end
                      local.get 7
                      i32.const 255
                      i32.and
                      i32.const 255
                      i32.ne
                      br_if 2 (;@7;)
                      local.get 5
                      i32.const 1
                      i32.add
                      local.set 2
                    end
                    local.get 6
                    local.get 2
                    i32.sub
                    local.set 5
                    local.get 6
                    local.get 2
                    i32.gt_u
                    br_if 0 (;@8;)
                    br 2 (;@6;)
                  end
                end
                local.get 5
                i32.const 1
                i32.add
                local.set 2
              end
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    block  ;; label = @9
                      block  ;; label = @10
                        local.get 2
                        i32.const 32
                        i32.gt_u
                        br_if 0 (;@10;)
                        local.get 2
                        i32.const 2
                        i32.shl
                        local.tee 4
                        i32.const 1052532
                        i32.add
                        i32.load
                        i32.const 21
                        i32.shr_u
                        local.set 6
                        local.get 2
                        i32.const 32
                        i32.ne
                        br_if 1 (;@9;)
                        i32.const 727
                        local.set 7
                        i32.const 31
                        local.set 2
                        br 2 (;@8;)
                      end
                      i32.const 33
                      i32.const 33
                      i32.const 1052500
                      call $_ZN4core9panicking18panic_bounds_check17h7eef07023fe9cc87E
                      unreachable
                    end
                    local.get 4
                    i32.const 1052536
                    i32.add
                    i32.load
                    i32.const 21
                    i32.shr_u
                    local.set 7
                    local.get 2
                    i32.eqz
                    br_if 1 (;@7;)
                    local.get 2
                    i32.const -1
                    i32.add
                    local.set 2
                  end
                  local.get 2
                  i32.const 2
                  i32.shl
                  i32.const 1052532
                  i32.add
                  i32.load
                  i32.const 2097151
                  i32.and
                  local.set 2
                  br 1 (;@6;)
                end
                i32.const 0
                local.set 2
              end
              block  ;; label = @6
                local.get 7
                local.get 6
                i32.const -1
                i32.xor
                i32.add
                i32.eqz
                br_if 0 (;@6;)
                local.get 1
                local.get 2
                i32.sub
                local.set 5
                local.get 6
                i32.const 727
                local.get 6
                i32.const 727
                i32.gt_u
                select
                local.set 4
                local.get 7
                i32.const -1
                i32.add
                local.set 7
                i32.const 0
                local.set 2
                loop  ;; label = @7
                  local.get 4
                  local.get 6
                  i32.eq
                  br_if 3 (;@4;)
                  local.get 2
                  local.get 6
                  i32.const 1052664
                  i32.add
                  i32.load8_u
                  i32.add
                  local.tee 2
                  local.get 5
                  i32.gt_u
                  br_if 1 (;@6;)
                  local.get 7
                  local.get 6
                  i32.const 1
                  i32.add
                  local.tee 6
                  i32.ne
                  br_if 0 (;@7;)
                end
                local.get 7
                local.set 6
              end
              local.get 6
              i32.const 1
              i32.and
              i32.eqz
              br_if 0 (;@5;)
              local.get 3
              i32.const 6
              i32.add
              i32.const 2
              i32.add
              i32.const 0
              i32.store8
              local.get 3
              i32.const 0
              i32.store16 offset=6
              local.get 3
              i32.const 125
              i32.store8 offset=15
              local.get 3
              local.get 1
              i32.const 15
              i32.and
              i32.const 1052412
              i32.add
              i32.load8_u
              i32.store8 offset=14
              local.get 3
              local.get 1
              i32.const 4
              i32.shr_u
              i32.const 15
              i32.and
              i32.const 1052412
              i32.add
              i32.load8_u
              i32.store8 offset=13
              local.get 3
              local.get 1
              i32.const 8
              i32.shr_u
              i32.const 15
              i32.and
              i32.const 1052412
              i32.add
              i32.load8_u
              i32.store8 offset=12
              local.get 3
              local.get 1
              i32.const 12
              i32.shr_u
              i32.const 15
              i32.and
              i32.const 1052412
              i32.add
              i32.load8_u
              i32.store8 offset=11
              local.get 3
              local.get 1
              i32.const 16
              i32.shr_u
              i32.const 15
              i32.and
              i32.const 1052412
              i32.add
              i32.load8_u
              i32.store8 offset=10
              local.get 3
              local.get 1
              i32.const 20
              i32.shr_u
              i32.const 15
              i32.and
              i32.const 1052412
              i32.add
              i32.load8_u
              i32.store8 offset=9
              local.get 1
              i32.const 1
              i32.or
              i32.clz
              i32.const 2
              i32.shr_u
              i32.const -2
              i32.add
              local.tee 2
              i32.const 11
              i32.ge_u
              br_if 2 (;@3;)
              local.get 3
              i32.const 6
              i32.add
              local.get 2
              i32.add
              local.tee 6
              i32.const 0
              i32.load16_u offset=1052472 align=1
              i32.store16 align=1
              local.get 6
              i32.const 2
              i32.add
              i32.const 0
              i32.load8_u offset=1052474
              i32.store8
              local.get 0
              local.get 3
              i64.load offset=6 align=2
              i64.store align=1
              local.get 0
              i32.const 8
              i32.add
              local.get 3
              i32.const 6
              i32.add
              i32.const 8
              i32.add
              i32.load16_u
              i32.store16 align=1
              local.get 0
              i32.const 10
              i32.store8 offset=11
              local.get 0
              local.get 2
              i32.store8 offset=10
              br 4 (;@1;)
            end
            local.get 1
            i32.const 32
            i32.lt_u
            br_if 2 (;@2;)
            block  ;; label = @5
              local.get 1
              i32.const 127
              i32.lt_u
              br_if 0 (;@5;)
              block  ;; label = @6
                local.get 1
                i32.const 65536
                i32.lt_u
                br_if 0 (;@6;)
                block  ;; label = @7
                  local.get 1
                  i32.const 131072
                  i32.lt_u
                  br_if 0 (;@7;)
                  local.get 1
                  i32.const -918000
                  i32.add
                  i32.const 196112
                  i32.lt_u
                  br_if 5 (;@2;)
                  local.get 1
                  i32.const -205744
                  i32.add
                  i32.const 712016
                  i32.lt_u
                  br_if 5 (;@2;)
                  local.get 1
                  i32.const -201547
                  i32.add
                  i32.const 5
                  i32.lt_u
                  br_if 5 (;@2;)
                  local.get 1
                  i32.const -195102
                  i32.add
                  i32.const 1506
                  i32.lt_u
                  br_if 5 (;@2;)
                  local.get 1
                  i32.const -191457
                  i32.add
                  i32.const 3103
                  i32.lt_u
                  br_if 5 (;@2;)
                  local.get 1
                  i32.const -183970
                  i32.add
                  i32.const 14
                  i32.lt_u
                  br_if 5 (;@2;)
                  local.get 1
                  i32.const -2
                  i32.and
                  i32.const 178206
                  i32.eq
                  br_if 5 (;@2;)
                  local.get 1
                  i32.const -32
                  i32.and
                  i32.const 173792
                  i32.eq
                  br_if 5 (;@2;)
                  local.get 1
                  i32.const -177978
                  i32.add
                  i32.const 6
                  i32.lt_u
                  br_if 5 (;@2;)
                  br 2 (;@5;)
                end
                local.get 1
                i32.const 1051638
                i32.const 44
                i32.const 1051726
                i32.const 196
                i32.const 1051922
                i32.const 450
                call $_ZN4core7unicode9printable5check17h27038d57ba2a6c2dE
                br_if 1 (;@5;)
                br 4 (;@2;)
              end
              local.get 1
              i32.const 1050968
              i32.const 40
              i32.const 1051048
              i32.const 287
              i32.const 1051335
              i32.const 303
              call $_ZN4core7unicode9printable5check17h27038d57ba2a6c2dE
              i32.eqz
              br_if 3 (;@2;)
            end
            local.get 0
            local.get 1
            i32.store offset=4
            local.get 0
            i32.const 128
            i32.store8
            br 3 (;@1;)
          end
          local.get 4
          i32.const 727
          i32.const 1052516
          call $_ZN4core9panicking18panic_bounds_check17h7eef07023fe9cc87E
          unreachable
        end
        local.get 2
        i32.const 10
        i32.const 1052456
        call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
        unreachable
      end
      local.get 3
      i32.const 6
      i32.add
      i32.const 2
      i32.add
      i32.const 0
      i32.store8
      local.get 3
      i32.const 0
      i32.store16 offset=6
      local.get 3
      i32.const 125
      i32.store8 offset=15
      local.get 3
      local.get 1
      i32.const 15
      i32.and
      i32.const 1052412
      i32.add
      i32.load8_u
      i32.store8 offset=14
      local.get 3
      local.get 1
      i32.const 4
      i32.shr_u
      i32.const 15
      i32.and
      i32.const 1052412
      i32.add
      i32.load8_u
      i32.store8 offset=13
      local.get 3
      local.get 1
      i32.const 8
      i32.shr_u
      i32.const 15
      i32.and
      i32.const 1052412
      i32.add
      i32.load8_u
      i32.store8 offset=12
      local.get 3
      local.get 1
      i32.const 12
      i32.shr_u
      i32.const 15
      i32.and
      i32.const 1052412
      i32.add
      i32.load8_u
      i32.store8 offset=11
      local.get 3
      local.get 1
      i32.const 16
      i32.shr_u
      i32.const 15
      i32.and
      i32.const 1052412
      i32.add
      i32.load8_u
      i32.store8 offset=10
      local.get 3
      local.get 1
      i32.const 20
      i32.shr_u
      i32.const 15
      i32.and
      i32.const 1052412
      i32.add
      i32.load8_u
      i32.store8 offset=9
      block  ;; label = @2
        local.get 1
        i32.const 1
        i32.or
        i32.clz
        i32.const 2
        i32.shr_u
        i32.const -2
        i32.add
        local.tee 2
        i32.const 11
        i32.ge_u
        br_if 0 (;@2;)
        local.get 3
        i32.const 6
        i32.add
        local.get 2
        i32.add
        local.tee 6
        i32.const 0
        i32.load16_u offset=1052472 align=1
        i32.store16 align=1
        local.get 6
        i32.const 2
        i32.add
        i32.const 0
        i32.load8_u offset=1052474
        i32.store8
        local.get 0
        local.get 3
        i64.load offset=6 align=2
        i64.store align=1
        local.get 0
        i32.const 8
        i32.add
        local.get 3
        i32.const 6
        i32.add
        i32.const 8
        i32.add
        i32.load16_u
        i32.store16 align=1
        local.get 0
        i32.const 10
        i32.store8 offset=11
        local.get 0
        local.get 2
        i32.store8 offset=10
        br 1 (;@1;)
      end
      local.get 2
      i32.const 10
      i32.const 1052456
      call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
      unreachable
    end
    local.get 3
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core7unicode9printable5check17h27038d57ba2a6c2dE (type 26) (param i32 i32 i32 i32 i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32)
    local.get 1
    local.get 2
    i32.const 1
    i32.shl
    i32.add
    local.set 7
    local.get 0
    i32.const 65280
    i32.and
    i32.const 8
    i32.shr_u
    local.set 8
    i32.const 0
    local.set 9
    local.get 0
    i32.const 255
    i32.and
    local.set 10
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          loop  ;; label = @4
            local.get 1
            i32.const 2
            i32.add
            local.set 11
            local.get 9
            local.get 1
            i32.load8_u offset=1
            local.tee 2
            i32.add
            local.set 12
            block  ;; label = @5
              local.get 1
              i32.load8_u
              local.tee 1
              local.get 8
              i32.eq
              br_if 0 (;@5;)
              local.get 1
              local.get 8
              i32.gt_u
              br_if 3 (;@2;)
              local.get 12
              local.set 9
              local.get 11
              local.set 1
              local.get 11
              local.get 7
              i32.ne
              br_if 1 (;@4;)
              br 3 (;@2;)
            end
            block  ;; label = @5
              local.get 12
              local.get 9
              i32.lt_u
              br_if 0 (;@5;)
              local.get 12
              local.get 4
              i32.gt_u
              br_if 2 (;@3;)
              local.get 3
              local.get 9
              i32.add
              local.set 1
              block  ;; label = @6
                loop  ;; label = @7
                  local.get 2
                  i32.eqz
                  br_if 1 (;@6;)
                  local.get 2
                  i32.const -1
                  i32.add
                  local.set 2
                  local.get 1
                  i32.load8_u
                  local.set 9
                  local.get 1
                  i32.const 1
                  i32.add
                  local.set 1
                  local.get 9
                  local.get 10
                  i32.ne
                  br_if 0 (;@7;)
                end
                i32.const 0
                local.set 2
                br 5 (;@1;)
              end
              local.get 12
              local.set 9
              local.get 11
              local.set 1
              local.get 11
              local.get 7
              i32.ne
              br_if 1 (;@4;)
              br 3 (;@2;)
            end
          end
          local.get 9
          local.get 12
          i32.const 1050936
          call $_ZN4core5slice5index22slice_index_order_fail17h677b88984b8b522bE
          unreachable
        end
        local.get 12
        local.get 4
        i32.const 1050936
        call $_ZN4core5slice5index24slice_end_index_len_fail17he1e55bf2616238f7E
        unreachable
      end
      local.get 0
      i32.const 65535
      i32.and
      local.set 9
      local.get 5
      local.get 6
      i32.add
      local.set 12
      i32.const 1
      local.set 2
      block  ;; label = @2
        loop  ;; label = @3
          local.get 5
          i32.const 1
          i32.add
          local.set 10
          block  ;; label = @4
            block  ;; label = @5
              local.get 5
              i32.load8_u
              local.tee 1
              i32.extend8_s
              local.tee 11
              i32.const 0
              i32.lt_s
              br_if 0 (;@5;)
              local.get 10
              local.set 5
              br 1 (;@4;)
            end
            local.get 10
            local.get 12
            i32.eq
            br_if 2 (;@2;)
            local.get 11
            i32.const 127
            i32.and
            i32.const 8
            i32.shl
            local.get 5
            i32.load8_u offset=1
            i32.or
            local.set 1
            local.get 5
            i32.const 2
            i32.add
            local.set 5
          end
          local.get 9
          local.get 1
          i32.sub
          local.tee 9
          i32.const 0
          i32.lt_s
          br_if 2 (;@1;)
          local.get 2
          i32.const 1
          i32.xor
          local.set 2
          local.get 5
          local.get 12
          i32.ne
          br_if 0 (;@3;)
          br 2 (;@1;)
        end
      end
      i32.const 1054072
      i32.const 43
      i32.const 1050952
      call $_ZN4core9panicking5panic17hcfcdcc589d164b16E
      unreachable
    end
    local.get 2
    i32.const 1
    i32.and)
  (func $_ZN71_$LT$core..ops..range..Range$LT$Idx$GT$$u20$as$u20$core..fmt..Debug$GT$3fmt17ha38900d092035ca2E (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    i32.const 1
    local.set 3
    block  ;; label = @1
      local.get 0
      i32.load
      local.get 1
      call $_ZN4core3fmt3num50_$LT$impl$u20$core..fmt..Debug$u20$for$u20$u32$GT$3fmt17hd7e872357038b7c4E
      br_if 0 (;@1;)
      local.get 1
      i32.const 24
      i32.add
      i32.load
      local.set 4
      local.get 1
      i32.load offset=20
      local.set 5
      local.get 2
      i64.const 0
      i64.store offset=20 align=4
      local.get 2
      i32.const 1054164
      i32.store offset=16
      i32.const 1
      local.set 3
      local.get 2
      i32.const 1
      i32.store offset=12
      local.get 2
      i32.const 1049792
      i32.store offset=8
      local.get 5
      local.get 4
      local.get 2
      i32.const 8
      i32.add
      call $_ZN4core3fmt5write17h8253e306f6bd0e19E
      br_if 0 (;@1;)
      local.get 0
      i32.load offset=4
      local.get 1
      call $_ZN4core3fmt3num50_$LT$impl$u20$core..fmt..Debug$u20$for$u20$u32$GT$3fmt17hd7e872357038b7c4E
      local.set 3
    end
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 3)
  (func $_ZN41_$LT$char$u20$as$u20$core..fmt..Debug$GT$3fmt17h23bf9b2886472963E (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    i32.const 1
    local.set 3
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.load offset=20
        local.tee 4
        i32.const 39
        local.get 1
        i32.const 24
        i32.add
        i32.load
        i32.load offset=16
        local.tee 5
        call_indirect (type 1)
        br_if 0 (;@2;)
        local.get 2
        local.get 0
        i32.load
        i32.const 257
        call $_ZN4core4char7methods22_$LT$impl$u20$char$GT$16escape_debug_ext17h35ef25b93b9973daE
        block  ;; label = @3
          block  ;; label = @4
            local.get 2
            i32.load8_u
            i32.const 128
            i32.ne
            br_if 0 (;@4;)
            local.get 2
            i32.const 8
            i32.add
            local.set 6
            i32.const 128
            local.set 7
            loop  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  local.get 7
                  i32.const 255
                  i32.and
                  i32.const 128
                  i32.eq
                  br_if 0 (;@7;)
                  local.get 2
                  i32.load8_u offset=10
                  local.tee 0
                  local.get 2
                  i32.load8_u offset=11
                  i32.ge_u
                  br_if 4 (;@3;)
                  local.get 2
                  local.get 0
                  i32.const 1
                  i32.add
                  i32.store8 offset=10
                  local.get 0
                  i32.const 10
                  i32.ge_u
                  br_if 6 (;@1;)
                  local.get 2
                  local.get 0
                  i32.add
                  i32.load8_u
                  local.set 1
                  br 1 (;@6;)
                end
                i32.const 0
                local.set 7
                local.get 6
                i32.const 0
                i32.store
                local.get 2
                i32.load offset=4
                local.set 1
                local.get 2
                i64.const 0
                i64.store
              end
              local.get 4
              local.get 1
              local.get 5
              call_indirect (type 1)
              i32.eqz
              br_if 0 (;@5;)
              br 3 (;@2;)
            end
          end
          local.get 2
          i32.load8_u offset=10
          local.tee 1
          i32.const 10
          local.get 1
          i32.const 10
          i32.gt_u
          select
          local.set 0
          local.get 2
          i32.load8_u offset=11
          local.tee 7
          local.get 1
          local.get 7
          local.get 1
          i32.gt_u
          select
          local.set 8
          loop  ;; label = @4
            local.get 8
            local.get 1
            i32.eq
            br_if 1 (;@3;)
            local.get 2
            local.get 1
            i32.const 1
            i32.add
            local.tee 7
            i32.store8 offset=10
            local.get 0
            local.get 1
            i32.eq
            br_if 3 (;@1;)
            local.get 2
            local.get 1
            i32.add
            local.set 6
            local.get 7
            local.set 1
            local.get 4
            local.get 6
            i32.load8_u
            local.get 5
            call_indirect (type 1)
            i32.eqz
            br_if 0 (;@4;)
            br 2 (;@2;)
          end
        end
        local.get 4
        i32.const 39
        local.get 5
        call_indirect (type 1)
        local.set 3
      end
      local.get 2
      i32.const 16
      i32.add
      global.set $__stack_pointer
      local.get 3
      return
    end
    local.get 0
    i32.const 10
    i32.const 1052476
    call $_ZN4core9panicking18panic_bounds_check17h7eef07023fe9cc87E
    unreachable)
  (func $_ZN69_$LT$core..alloc..layout..LayoutError$u20$as$u20$core..fmt..Debug$GT$3fmt17h8c527b937ccb019eE (type 1) (param i32 i32) (result i32)
    local.get 1
    i32.load offset=20
    i32.const 1053391
    i32.const 11
    local.get 1
    i32.const 24
    i32.add
    i32.load
    i32.load offset=12
    call_indirect (type 0))
  (func $_ZN5alloc7raw_vec11finish_grow17h4de5cd6636d1bdb9E (type 9) (param i32 i32 i32 i32)
    (local i32)
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 1
          i32.eqz
          br_if 0 (;@3;)
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                local.get 2
                i32.const -1
                i32.le_s
                br_if 0 (;@6;)
                block  ;; label = @7
                  local.get 3
                  i32.load offset=4
                  i32.eqz
                  br_if 0 (;@7;)
                  local.get 3
                  i32.const 8
                  i32.add
                  i32.load
                  local.tee 4
                  br_if 2 (;@5;)
                end
                local.get 1
                local.get 2
                call $_ZN5alloc5alloc6Global10alloc_impl17h1e7c53651c78c03dE
                local.set 4
                local.set 3
                br 2 (;@4;)
              end
              local.get 0
              i32.const 0
              i32.store offset=4
              br 3 (;@2;)
            end
            local.get 3
            i32.load
            local.get 4
            local.get 1
            local.get 2
            call $__rust_realloc
            local.set 3
            local.get 2
            local.set 4
          end
          block  ;; label = @4
            local.get 3
            i32.eqz
            br_if 0 (;@4;)
            local.get 0
            local.get 3
            i32.store offset=4
            local.get 0
            i32.const 8
            i32.add
            local.get 4
            i32.store
            i32.const 0
            local.set 2
            br 3 (;@1;)
          end
          local.get 0
          local.get 1
          i32.store offset=4
          local.get 0
          i32.const 8
          i32.add
          local.get 2
          i32.store
          br 1 (;@2;)
        end
        local.get 0
        i32.const 0
        i32.store offset=4
        local.get 0
        i32.const 8
        i32.add
        local.get 2
        i32.store
      end
      i32.const 1
      local.set 2
    end
    local.get 0
    local.get 2
    i32.store)
  (func $_ZN5alloc5alloc6Global10alloc_impl17h1e7c53651c78c03dE (type 21) (param i32 i32) (result i32 i32)
    block  ;; label = @1
      local.get 1
      i32.eqz
      br_if 0 (;@1;)
      i32.const 0
      i32.load8_u offset=1059320
      drop
      local.get 1
      local.get 0
      call $__rust_alloc
      local.set 0
    end
    local.get 0
    local.get 1)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17h0e522760e9448a1bE (type 7) (param i32) (result i32 i32)
    (local i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        br_if 0 (;@2;)
        i32.const 1
        local.set 1
        br 1 (;@1;)
      end
      block  ;; label = @2
        local.get 0
        i32.const -1
        i32.gt_s
        local.tee 2
        i32.eqz
        br_if 0 (;@2;)
        local.get 2
        local.get 0
        call $_ZN5alloc5alloc6Global10alloc_impl17h1e7c53651c78c03dE
        drop
        local.tee 1
        br_if 1 (;@1;)
        local.get 2
        local.get 0
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
      unreachable
    end
    local.get 1
    local.get 0)
  (func $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h490bca4ea1fbb57cE (type 3) (param i32 i32)
    (local i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      local.get 0
      i32.load offset=4
      local.tee 3
      local.get 0
      i32.load offset=8
      local.tee 4
      i32.sub
      local.get 1
      i32.ge_u
      br_if 0 (;@1;)
      i32.const 0
      local.set 5
      block  ;; label = @2
        local.get 4
        local.get 1
        i32.add
        local.tee 1
        local.get 4
        i32.lt_u
        br_if 0 (;@2;)
        local.get 3
        i32.const 1
        i32.shl
        local.tee 4
        local.get 1
        local.get 4
        local.get 1
        i32.gt_u
        select
        local.tee 1
        i32.const 8
        local.get 1
        i32.const 8
        i32.gt_u
        select
        local.tee 1
        i32.const -1
        i32.xor
        i32.const 31
        i32.shr_u
        local.set 4
        block  ;; label = @3
          block  ;; label = @4
            local.get 3
            i32.eqz
            br_if 0 (;@4;)
            local.get 2
            local.get 3
            i32.store offset=24
            local.get 2
            i32.const 1
            i32.store offset=20
            local.get 2
            local.get 0
            i32.load
            i32.store offset=16
            br 1 (;@3;)
          end
          local.get 2
          i32.const 0
          i32.store offset=20
        end
        local.get 2
        local.get 4
        local.get 1
        local.get 2
        i32.const 16
        i32.add
        call $_ZN5alloc7raw_vec11finish_grow17h4de5cd6636d1bdb9E
        local.get 2
        i32.load offset=4
        local.set 5
        block  ;; label = @3
          local.get 2
          i32.load
          i32.eqz
          br_if 0 (;@3;)
          local.get 2
          i32.const 8
          i32.add
          i32.load
          local.set 1
          br 1 (;@2;)
        end
        local.get 0
        local.get 1
        i32.store offset=4
        local.get 0
        local.get 5
        i32.store
        i32.const -2147483647
        local.set 5
      end
      local.get 5
      local.get 1
      call $_ZN5alloc7raw_vec14handle_reserve17hc1b6427a824c2669E
    end
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core4iter6traits8iterator8Iterator3zip17hde5ecd6693b43225E (type 11) (param i32 i32 i32 i32 i32)
    local.get 0
    i32.const 0
    i32.store offset=16
    local.get 0
    local.get 3
    i32.store offset=8
    local.get 0
    local.get 2
    i32.store offset=4
    local.get 0
    local.get 1
    i32.store
    local.get 0
    local.get 2
    local.get 1
    i32.sub
    i32.const 3
    i32.shr_u
    local.tee 2
    i32.store offset=24
    local.get 0
    i32.const 12
    i32.add
    local.get 3
    local.get 4
    i32.const 3
    i32.shl
    i32.add
    i32.store
    local.get 0
    local.get 2
    local.get 4
    local.get 2
    local.get 4
    i32.lt_u
    select
    i32.store offset=20)
  (func $_ZN106_$LT$core..iter..adapters..chain..Chain$LT$A$C$B$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$9size_hint17h832c7bd1307a22d7E (type 3) (param i32 i32)
    (local i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 1
    i32.const 12
    i32.add
    local.set 3
    local.get 1
    i32.load offset=12
    local.set 4
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 1
          i32.load
          i32.const 2
          i32.ne
          br_if 0 (;@3;)
          local.get 4
          br_if 1 (;@2;)
          local.get 0
          i64.const 4294967296
          i64.store align=4
          local.get 0
          i32.const 8
          i32.add
          i32.const 0
          i32.store
          br 2 (;@1;)
        end
        block  ;; label = @3
          local.get 4
          br_if 0 (;@3;)
          local.get 0
          i32.const 1
          i32.store offset=4
          local.get 0
          i32.const 8
          i32.add
          local.get 1
          i32.load offset=8
          local.tee 1
          i32.store
          local.get 0
          local.get 1
          i32.store
          br 2 (;@1;)
        end
        local.get 1
        i32.load offset=8
        local.set 1
        local.get 2
        local.get 3
        call $_ZN100_$LT$core..iter..adapters..take..Take$LT$I$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$9size_hint17h9d6acb87643c5e3eE
        local.get 2
        i32.load
        local.set 4
        local.get 2
        i32.load offset=4
        local.set 3
        local.get 0
        i32.const 8
        i32.add
        local.get 1
        local.get 2
        i32.const 8
        i32.add
        i32.load
        i32.add
        local.tee 5
        i32.store
        local.get 0
        local.get 3
        i32.const 0
        i32.ne
        local.get 5
        local.get 1
        i32.ge_u
        i32.and
        i32.store offset=4
        local.get 0
        i32.const -1
        local.get 1
        local.get 4
        i32.add
        local.tee 4
        local.get 4
        local.get 1
        i32.lt_u
        select
        i32.store
        br 1 (;@1;)
      end
      local.get 0
      local.get 3
      call $_ZN100_$LT$core..iter..adapters..take..Take$LT$I$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$9size_hint17h9d6acb87643c5e3eE
    end
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN84_$LT$alloc..vec..Vec$LT$T$C$A$GT$$u20$as$u20$core..ops..index..IndexMut$LT$I$GT$$GT$9index_mut17hc7aabc19decee266E (type 8) (param i32 i32 i32 i32) (result i32)
    block  ;; label = @1
      local.get 1
      local.get 2
      i32.gt_u
      br_if 0 (;@1;)
      local.get 2
      local.get 1
      local.get 3
      call $_ZN4core9panicking18panic_bounds_check17h7eef07023fe9cc87E
      unreachable
    end
    local.get 0
    local.get 2
    i32.const 3
    i32.shl
    i32.add)
  (func $_ZN100_$LT$core..iter..adapters..take..Take$LT$I$GT$$u20$as$u20$core..iter..traits..iterator..Iterator$GT$9size_hint17h9d6acb87643c5e3eE (type 3) (param i32 i32)
    (local i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.load offset=8
        local.tee 2
        br_if 0 (;@2;)
        i32.const 0
        local.set 1
        br 1 (;@1;)
      end
      local.get 1
      i32.load offset=4
      local.get 1
      i32.load
      i32.sub
      i32.const 3
      i32.shr_u
      local.tee 1
      local.get 2
      local.get 1
      local.get 2
      i32.lt_u
      select
      local.set 1
    end
    local.get 0
    i32.const 1
    i32.store offset=4
    local.get 0
    local.get 1
    i32.store
    local.get 0
    i32.const 8
    i32.add
    local.get 1
    i32.store)
  (func $_ZN5alloc3vec9from_elem17h110bc7265e9c9318E (type 3) (param i32 i32)
    (local i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 1
    call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$11allocate_in17ha2c1a859907dfec3E
    local.set 4
    local.set 3
    local.get 2
    i32.const 0
    i32.store offset=8
    local.get 2
    local.get 4
    i32.store offset=4
    local.get 2
    local.get 3
    i32.store
    local.get 2
    local.get 1
    call $_ZN5alloc3vec16Vec$LT$T$C$A$GT$7reserve17h33b65ac2de0dd8f6E
    local.get 1
    i32.const 1
    local.get 1
    i32.const 1
    i32.gt_u
    select
    local.tee 5
    i32.const -1
    i32.add
    local.set 3
    local.get 2
    i32.load
    local.get 2
    i32.load offset=8
    local.tee 6
    i32.const 3
    i32.shl
    i32.add
    local.set 4
    block  ;; label = @1
      block  ;; label = @2
        loop  ;; label = @3
          block  ;; label = @4
            local.get 3
            br_if 0 (;@4;)
            local.get 6
            local.get 5
            i32.add
            local.set 3
            local.get 1
            br_if 2 (;@2;)
            local.get 3
            i32.const -1
            i32.add
            local.set 3
            br 3 (;@1;)
          end
          local.get 4
          i32.const 0
          i32.store
          local.get 3
          i32.const -1
          i32.add
          local.set 3
          local.get 4
          i32.const 8
          i32.add
          local.set 4
          br 0 (;@3;)
        end
      end
      local.get 4
      i32.const 0
      i32.store
    end
    local.get 0
    local.get 2
    i64.load
    i64.store align=4
    local.get 0
    i32.const 8
    i32.add
    local.get 3
    i32.store
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN5alloc4sync12Arc$LT$T$GT$9drop_slow17h3538528ce2076bdcE (type 2) (param i32)
    (local i32)
    block  ;; label = @1
      local.get 0
      i32.const 16
      i32.add
      i32.load
      local.tee 1
      i32.eqz
      br_if 0 (;@1;)
      local.get 1
      i32.const 0
      i32.store8
      local.get 0
      i32.const 20
      i32.add
      i32.load
      i32.eqz
      br_if 0 (;@1;)
      local.get 1
      call $free
    end
    block  ;; label = @1
      local.get 0
      i32.const -1
      i32.eq
      br_if 0 (;@1;)
      local.get 0
      local.get 0
      i32.load offset=4
      local.tee 1
      i32.const -1
      i32.add
      i32.store offset=4
      local.get 1
      i32.const 1
      i32.ne
      br_if 0 (;@1;)
      local.get 0
      call $free
    end)
  (func $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17hfa244fbfe149e5b0E (type 1) (param i32 i32) (result i32)
    (local i32)
    local.get 0
    i32.load
    local.set 0
    block  ;; label = @1
      local.get 1
      i32.load offset=28
      local.tee 2
      i32.const 16
      i32.and
      br_if 0 (;@1;)
      block  ;; label = @2
        local.get 2
        i32.const 32
        i32.and
        br_if 0 (;@2;)
        local.get 0
        local.get 1
        call $_ZN4core3fmt3num3imp52_$LT$impl$u20$core..fmt..Display$u20$for$u20$u32$GT$3fmt17h4be59bab036c1886E
        return
      end
      local.get 0
      local.get 1
      call $_ZN4core3fmt3num53_$LT$impl$u20$core..fmt..UpperHex$u20$for$u20$i32$GT$3fmt17h58537b696dc0bd30E
      return
    end
    local.get 0
    local.get 1
    call $_ZN4core3fmt3num53_$LT$impl$u20$core..fmt..LowerHex$u20$for$u20$i32$GT$3fmt17h2e0d8f65cc6bfe78E)
  (func $_ZN4core3ptr40drop_in_place$LT$std..thread..Thread$GT$17h164b0697484aa5b2E (type 2) (param i32)
    (local i32)
    local.get 0
    i32.load
    local.tee 1
    local.get 1
    i32.load
    local.tee 1
    i32.const -1
    i32.add
    i32.store
    block  ;; label = @1
      local.get 1
      i32.const 1
      i32.ne
      br_if 0 (;@1;)
      local.get 0
      i32.load
      call $_ZN5alloc4sync12Arc$LT$T$GT$9drop_slow17h3538528ce2076bdcE
    end)
  (func $_ZN3std10sys_common11thread_info14current_thread17h2d20a3c7c082bda6E (type 22) (result i32)
    (local i32 i32 i64 i64 i64 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 0
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            i32.const 0
            i32.load offset=1059288
            br_if 0 (;@4;)
            i32.const 0
            i32.const -1
            i32.store offset=1059288
            block  ;; label = @5
              i32.const 0
              i32.load offset=1059292
              local.tee 1
              br_if 0 (;@5;)
              i32.const 0
              i32.load8_u offset=1059320
              drop
              i32.const 24
              call $malloc
              local.tee 1
              i32.eqz
              br_if 3 (;@2;)
              local.get 1
              i64.const 4294967297
              i64.store align=4
              local.get 1
              i32.const 16
              i32.add
              i32.const 0
              i32.store
              i32.const 0
              i64.load offset=1059272
              local.set 2
              loop  ;; label = @6
                local.get 2
                i64.const 1
                i64.add
                local.tee 3
                i64.eqz
                br_if 5 (;@1;)
                i32.const 0
                local.get 3
                i32.const 0
                i64.load offset=1059272
                local.tee 4
                local.get 4
                local.get 2
                i64.eq
                local.tee 5
                select
                i64.store offset=1059272
                local.get 4
                local.set 2
                local.get 5
                i32.eqz
                br_if 0 (;@6;)
              end
              i32.const 0
              local.get 1
              i32.store offset=1059292
              local.get 1
              local.get 3
              i64.store offset=8
            end
            local.get 1
            local.get 1
            i32.load
            local.tee 5
            i32.const 1
            i32.add
            i32.store
            local.get 5
            i32.const -1
            i32.gt_s
            br_if 1 (;@3;)
            unreachable
            unreachable
          end
          i32.const 1054368
          i32.const 16
          local.get 0
          i32.const 8
          i32.add
          i32.const 1054384
          i32.const 1054808
          call $_ZN4core6result13unwrap_failed17hfefb3e75b68d8f8cE
          unreachable
        end
        i32.const 0
        i32.const 0
        i32.store offset=1059288
        local.get 0
        i32.const 16
        i32.add
        global.set $__stack_pointer
        local.get 1
        return
      end
      i32.const 8
      i32.const 24
      call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
      unreachable
    end
    call $_ZN3std6thread8ThreadId3new9exhausted17h77632c58c47c47fcE
    unreachable)
  (func $_ZN4core3ptr43drop_in_place$LT$once_cell..imp..Waiter$GT$17h7a61f04626115bb4E (type 2) (param i32)
    block  ;; label = @1
      local.get 0
      i32.load
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      call $_ZN4core3ptr40drop_in_place$LT$std..thread..Thread$GT$17h164b0697484aa5b2E
    end)
  (func $_ZN5alloc4sync12Arc$LT$T$GT$9drop_slow17hfead2a7a1440e4b8E (type 2) (param i32)
    (local i32 i32)
    block  ;; label = @1
      local.get 0
      i32.const 16
      i32.add
      i32.load
      local.tee 1
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      i32.const 20
      i32.add
      i32.load
      local.set 2
      local.get 1
      i32.const 0
      i32.store8
      local.get 2
      i32.eqz
      br_if 0 (;@1;)
      local.get 1
      call $free
    end
    block  ;; label = @1
      local.get 0
      i32.const -1
      i32.eq
      br_if 0 (;@1;)
      local.get 0
      local.get 0
      i32.load offset=4
      local.tee 1
      i32.const -1
      i32.add
      i32.store offset=4
      local.get 1
      i32.const 1
      i32.ne
      br_if 0 (;@1;)
      local.get 0
      call $free
    end)
  (func $_ZN4core9panicking13assert_failed17hfa364ad86727fdaaE (type 3) (param i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    i32.const 1053912
    i32.store offset=4
    local.get 2
    local.get 0
    i32.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    i32.const 1054056
    local.get 2
    i32.const 4
    i32.add
    i32.const 1054056
    local.get 2
    i32.const 8
    i32.add
    i32.const 1054024
    call $_ZN4core9panicking19assert_failed_inner17h85f6c6a47372e3aaE
    unreachable)
  (func $_ZN3std6thread8ThreadId3new9exhausted17h77632c58c47c47fcE (type 14)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 0
    global.set $__stack_pointer
    local.get 0
    i32.const 20
    i32.add
    i64.const 0
    i64.store align=4
    local.get 0
    i32.const 1
    i32.store offset=12
    local.get 0
    i32.const 1054320
    i32.store offset=8
    local.get 0
    i32.const 1054164
    i32.store offset=16
    local.get 0
    i32.const 8
    i32.add
    i32.const 1054328
    call $_ZN4core9panicking9panic_fmt17h0bff5abeb2912aefE
    unreachable)
  (func $_ZN3std2io5Write9write_fmt17hab21973df7a26b7dE (type 12) (param i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    local.get 3
    i32.const 4
    i32.store8 offset=8
    local.get 3
    local.get 1
    i32.store offset=16
    local.get 3
    i32.const 24
    i32.add
    i32.const 16
    i32.add
    local.get 2
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 3
    i32.const 24
    i32.add
    i32.const 8
    i32.add
    local.get 2
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 3
    local.get 2
    i64.load align=4
    i64.store offset=24
    block  ;; label = @1
      block  ;; label = @2
        local.get 3
        i32.const 8
        i32.add
        i32.const 1054512
        local.get 3
        i32.const 24
        i32.add
        call $_ZN4core3fmt5write17h8253e306f6bd0e19E
        i32.eqz
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 3
          i32.load8_u offset=8
          i32.const 4
          i32.ne
          br_if 0 (;@3;)
          local.get 0
          i32.const 1054500
          i32.store offset=4
          local.get 0
          i32.const 2
          i32.store8
          br 2 (;@1;)
        end
        local.get 0
        local.get 3
        i64.load offset=8
        i64.store align=4
        br 1 (;@1;)
      end
      local.get 0
      i32.const 4
      i32.store8
      local.get 3
      i32.load offset=12
      local.set 0
      block  ;; label = @2
        local.get 3
        i32.load8_u offset=8
        local.tee 2
        i32.const 4
        i32.gt_u
        br_if 0 (;@2;)
        local.get 2
        i32.const 3
        i32.ne
        br_if 1 (;@1;)
      end
      local.get 0
      i32.load
      local.tee 1
      local.get 0
      i32.const 4
      i32.add
      i32.load
      local.tee 2
      i32.load
      call_indirect (type 2)
      block  ;; label = @2
        local.get 2
        i32.const 4
        i32.add
        i32.load
        i32.eqz
        br_if 0 (;@2;)
        local.get 1
        call $free
      end
      local.get 0
      call $free
    end
    local.get 3
    i32.const 48
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core3ptr81drop_in_place$LT$core..result..Result$LT$$LP$$RP$$C$std..io..error..Error$GT$$GT$17hb85f686a3328dc58E (type 3) (param i32 i32)
    (local i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.const 255
        i32.and
        local.tee 0
        i32.const 4
        i32.gt_u
        br_if 0 (;@2;)
        local.get 0
        i32.const 3
        i32.ne
        br_if 1 (;@1;)
      end
      local.get 1
      i32.load
      local.tee 2
      local.get 1
      i32.const 4
      i32.add
      i32.load
      local.tee 0
      i32.load
      call_indirect (type 2)
      block  ;; label = @2
        local.get 0
        i32.const 4
        i32.add
        i32.load
        i32.eqz
        br_if 0 (;@2;)
        local.get 2
        call $free
      end
      local.get 1
      call $free
    end)
  (func $_ZN4core3ptr29drop_in_place$LT$$LP$$RP$$GT$17h83ff458eb0202b31E (type 2) (param i32))
  (func $_ZN4core3ptr88drop_in_place$LT$std..io..Write..write_fmt..Adapter$LT$alloc..vec..Vec$LT$u8$GT$$GT$$GT$17hca98a9d3138cd957E (type 2) (param i32)
    (local i32 i32)
    local.get 0
    i32.const 4
    i32.add
    i32.load
    local.set 1
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.load8_u
        local.tee 0
        i32.const 4
        i32.gt_u
        br_if 0 (;@2;)
        local.get 0
        i32.const 3
        i32.ne
        br_if 1 (;@1;)
      end
      local.get 1
      i32.load
      local.tee 2
      local.get 1
      i32.const 4
      i32.add
      i32.load
      local.tee 0
      i32.load
      call_indirect (type 2)
      block  ;; label = @2
        local.get 0
        i32.const 4
        i32.add
        i32.load
        i32.eqz
        br_if 0 (;@2;)
        local.get 2
        call $free
      end
      local.get 1
      call $free
    end)
  (func $_ZN80_$LT$std..io..Write..write_fmt..Adapter$LT$T$GT$$u20$as$u20$core..fmt..Write$GT$9write_str17hffeb84cbbad34c0bE (type 0) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    i32.const 0
    local.set 4
    block  ;; label = @1
      local.get 2
      i32.eqz
      br_if 0 (;@1;)
      block  ;; label = @2
        block  ;; label = @3
          loop  ;; label = @4
            local.get 3
            local.get 2
            i32.store offset=4
            local.get 3
            local.get 1
            i32.store
            local.get 3
            i32.const 8
            i32.add
            local.get 3
            i32.const 1
            call $_ZN4wasi13lib_generated8fd_write17h775ab5e87c956e2cE
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  local.get 3
                  i32.load16_u offset=8
                  br_if 0 (;@7;)
                  local.get 3
                  i32.load offset=12
                  local.tee 5
                  br_if 1 (;@6;)
                  i32.const 2
                  local.set 2
                  i32.const 1054472
                  local.set 5
                  br 5 (;@2;)
                end
                local.get 3
                i32.load16_u offset=10
                local.tee 5
                call $_ZN3std3sys4wasi17decode_error_kind17hc0f82157747eae67E
                i32.const 255
                i32.and
                i32.const 35
                i32.eq
                br_if 1 (;@5;)
                i32.const 0
                local.set 2
                br 4 (;@2;)
              end
              local.get 2
              local.get 5
              i32.lt_u
              br_if 2 (;@3;)
              local.get 1
              local.get 5
              i32.add
              local.set 1
              local.get 2
              local.get 5
              i32.sub
              local.set 2
            end
            local.get 2
            br_if 0 (;@4;)
            br 3 (;@1;)
          end
        end
        local.get 5
        local.get 2
        i32.const 1054428
        call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
        unreachable
      end
      local.get 0
      i32.const 4
      i32.add
      i32.load
      local.set 4
      block  ;; label = @2
        block  ;; label = @3
          local.get 0
          i32.load8_u
          local.tee 1
          i32.const 4
          i32.gt_u
          br_if 0 (;@3;)
          local.get 1
          i32.const 3
          i32.ne
          br_if 1 (;@2;)
        end
        local.get 4
        i32.load
        local.tee 6
        local.get 4
        i32.const 4
        i32.add
        i32.load
        local.tee 1
        i32.load
        call_indirect (type 2)
        block  ;; label = @3
          local.get 1
          i32.const 4
          i32.add
          i32.load
          i32.eqz
          br_if 0 (;@3;)
          local.get 6
          call $free
        end
        local.get 4
        call $free
      end
      local.get 0
      local.get 2
      i32.store
      local.get 0
      i32.const 4
      i32.add
      local.get 5
      i32.store
      i32.const 1
      local.set 4
    end
    local.get 3
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 4)
  (func $_ZN4wasi13lib_generated8fd_write17h775ab5e87c956e2cE (type 12) (param i32 i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        i32.const 2
        local.get 1
        local.get 2
        local.get 3
        i32.const 12
        i32.add
        call $_ZN4wasi13lib_generated22wasi_snapshot_preview18fd_write17h82bd99e8a5fb7244E
        local.tee 2
        br_if 0 (;@2;)
        local.get 0
        local.get 3
        i32.load offset=12
        i32.store offset=4
        i32.const 0
        local.set 2
        br 1 (;@1;)
      end
      local.get 0
      local.get 2
      i32.store16 offset=2
      i32.const 1
      local.set 2
    end
    local.get 0
    local.get 2
    i32.store16
    local.get 3
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $_ZN4core3fmt5Write10write_char17h35bf3a19560abc4fE (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    i32.const 0
    i32.store offset=12
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 128
        i32.lt_u
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 1
          i32.const 2048
          i32.lt_u
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 1
            i32.const 65536
            i32.lt_u
            br_if 0 (;@4;)
            local.get 2
            local.get 1
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=15
            local.get 2
            local.get 1
            i32.const 6
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=14
            local.get 2
            local.get 1
            i32.const 12
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=13
            local.get 2
            local.get 1
            i32.const 18
            i32.shr_u
            i32.const 7
            i32.and
            i32.const 240
            i32.or
            i32.store8 offset=12
            i32.const 4
            local.set 1
            br 3 (;@1;)
          end
          local.get 2
          local.get 1
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=14
          local.get 2
          local.get 1
          i32.const 12
          i32.shr_u
          i32.const 224
          i32.or
          i32.store8 offset=12
          local.get 2
          local.get 1
          i32.const 6
          i32.shr_u
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=13
          i32.const 3
          local.set 1
          br 2 (;@1;)
        end
        local.get 2
        local.get 1
        i32.const 63
        i32.and
        i32.const 128
        i32.or
        i32.store8 offset=13
        local.get 2
        local.get 1
        i32.const 6
        i32.shr_u
        i32.const 192
        i32.or
        i32.store8 offset=12
        i32.const 2
        local.set 1
        br 1 (;@1;)
      end
      local.get 2
      local.get 1
      i32.store8 offset=12
      i32.const 1
      local.set 1
    end
    local.get 0
    local.get 2
    i32.const 12
    i32.add
    local.get 1
    call $_ZN80_$LT$std..io..Write..write_fmt..Adapter$LT$T$GT$$u20$as$u20$core..fmt..Write$GT$9write_str17hffeb84cbbad34c0bE
    local.set 1
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core3fmt5Write9write_fmt17hd267ee56f623e382E (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    local.get 0
    i32.store offset=4
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    i32.const 4
    i32.add
    i32.const 1054140
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 1
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core3ptr100drop_in_place$LT$$RF$mut$u20$std..io..Write..write_fmt..Adapter$LT$alloc..vec..Vec$LT$u8$GT$$GT$$GT$17hdd0e3e29f1eafbe5E (type 2) (param i32))
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h1cfe241be326fd2fE (type 0) (param i32 i32 i32) (result i32)
    local.get 0
    i32.load
    local.get 1
    local.get 2
    call $_ZN80_$LT$std..io..Write..write_fmt..Adapter$LT$T$GT$$u20$as$u20$core..fmt..Write$GT$9write_str17hffeb84cbbad34c0bE)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17he4fbd911983151ddE (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    local.get 2
    i32.const 0
    i32.store offset=12
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 128
        i32.lt_u
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 1
          i32.const 2048
          i32.lt_u
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 1
            i32.const 65536
            i32.lt_u
            br_if 0 (;@4;)
            local.get 2
            local.get 1
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=15
            local.get 2
            local.get 1
            i32.const 6
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=14
            local.get 2
            local.get 1
            i32.const 12
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=13
            local.get 2
            local.get 1
            i32.const 18
            i32.shr_u
            i32.const 7
            i32.and
            i32.const 240
            i32.or
            i32.store8 offset=12
            i32.const 4
            local.set 1
            br 3 (;@1;)
          end
          local.get 2
          local.get 1
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=14
          local.get 2
          local.get 1
          i32.const 12
          i32.shr_u
          i32.const 224
          i32.or
          i32.store8 offset=12
          local.get 2
          local.get 1
          i32.const 6
          i32.shr_u
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=13
          i32.const 3
          local.set 1
          br 2 (;@1;)
        end
        local.get 2
        local.get 1
        i32.const 63
        i32.and
        i32.const 128
        i32.or
        i32.store8 offset=13
        local.get 2
        local.get 1
        i32.const 6
        i32.shr_u
        i32.const 192
        i32.or
        i32.store8 offset=12
        i32.const 2
        local.set 1
        br 1 (;@1;)
      end
      local.get 2
      local.get 1
      i32.store8 offset=12
      i32.const 1
      local.set 1
    end
    local.get 0
    local.get 2
    i32.const 12
    i32.add
    local.get 1
    call $_ZN80_$LT$std..io..Write..write_fmt..Adapter$LT$T$GT$$u20$as$u20$core..fmt..Write$GT$9write_str17hffeb84cbbad34c0bE
    local.set 1
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17h0ac08c1e052d4e5eE (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    local.get 0
    i32.store offset=4
    local.get 2
    i32.const 4
    i32.add
    i32.const 1054140
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 1
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN68_$LT$std..thread..local..AccessError$u20$as$u20$core..fmt..Debug$GT$3fmt17h2a97b2ac10eb69a0E (type 1) (param i32 i32) (result i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 1
    i32.load offset=20
    i32.const 1054225
    i32.const 11
    local.get 1
    i32.const 24
    i32.add
    i32.load
    i32.load offset=12
    call_indirect (type 0)
    local.set 3
    local.get 2
    i32.const 0
    i32.store8 offset=13
    local.get 2
    local.get 3
    i32.store8 offset=12
    local.get 2
    local.get 1
    i32.store offset=8
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt8builders11DebugStruct6finish17h24c6b68ba16e2ce0E
    local.set 1
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core9panicking13assert_failed17h574f7db4222bb7e6E (type 3) (param i32 i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    i32.const 1054164
    i32.store offset=4
    local.get 2
    local.get 0
    i32.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    i32.const 1054168
    local.get 2
    i32.const 4
    i32.add
    i32.const 1054168
    local.get 2
    i32.const 8
    i32.add
    i32.const 1055456
    call $_ZN4core9panicking19assert_failed_inner17h85f6c6a47372e3aaE
    unreachable)
  (func $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17h60f47e1d406afabfE (type 1) (param i32 i32) (result i32)
    block  ;; label = @1
      local.get 0
      i32.load
      i32.load8_u
      br_if 0 (;@1;)
      local.get 1
      i32.const 1050436
      i32.const 5
      call $_ZN4core3fmt9Formatter3pad17h2cd94e1fc1b5b777E
      return
    end
    local.get 1
    i32.const 1050432
    i32.const 4
    call $_ZN4core3fmt9Formatter3pad17h2cd94e1fc1b5b777E)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$7reserve21do_reserve_and_handle17h2174b82f11d991afE (type 12) (param i32 i32 i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        local.get 2
        i32.add
        local.tee 2
        local.get 1
        i32.lt_u
        br_if 0 (;@2;)
        local.get 0
        i32.const 4
        i32.add
        i32.load
        local.tee 1
        i32.const 1
        i32.shl
        local.tee 4
        local.get 2
        local.get 4
        local.get 2
        i32.gt_u
        select
        local.tee 2
        i32.const 8
        local.get 2
        i32.const 8
        i32.gt_u
        select
        local.tee 2
        i32.const -1
        i32.xor
        i32.const 31
        i32.shr_u
        local.set 4
        block  ;; label = @3
          block  ;; label = @4
            local.get 1
            i32.eqz
            br_if 0 (;@4;)
            local.get 3
            local.get 1
            i32.store offset=24
            local.get 3
            i32.const 1
            i32.store offset=20
            local.get 3
            local.get 0
            i32.load
            i32.store offset=16
            br 1 (;@3;)
          end
          local.get 3
          i32.const 0
          i32.store offset=20
        end
        local.get 3
        local.get 4
        local.get 2
        local.get 3
        i32.const 16
        i32.add
        call $_ZN5alloc7raw_vec11finish_grow17h7f10e140e73363beE
        local.get 3
        i32.load offset=4
        local.set 1
        block  ;; label = @3
          local.get 3
          i32.load
          br_if 0 (;@3;)
          local.get 0
          local.get 1
          i32.store
          local.get 0
          i32.const 4
          i32.add
          local.get 2
          i32.store
          br 2 (;@1;)
        end
        local.get 1
        i32.const -2147483647
        i32.eq
        br_if 1 (;@1;)
        local.get 1
        i32.eqz
        br_if 0 (;@2;)
        local.get 1
        local.get 3
        i32.const 8
        i32.add
        i32.load
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
      unreachable
    end
    local.get 3
    i32.const 32
    i32.add
    global.set $__stack_pointer)
  (func $_ZN5alloc7raw_vec11finish_grow17h7f10e140e73363beE (type 9) (param i32 i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.eqz
        br_if 0 (;@2;)
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              local.get 2
              i32.const -1
              i32.le_s
              br_if 0 (;@5;)
              local.get 3
              i32.load offset=4
              br_if 1 (;@4;)
              i32.const 0
              i32.load8_u offset=1059320
              drop
              local.get 2
              i32.const 1
              call $__rust_alloc
              local.set 1
              br 2 (;@3;)
            end
            local.get 0
            i32.const 0
            i32.store offset=4
            br 3 (;@1;)
          end
          block  ;; label = @4
            local.get 3
            i32.const 8
            i32.add
            i32.load
            local.tee 1
            br_if 0 (;@4;)
            i32.const 0
            i32.load8_u offset=1059320
            drop
            local.get 2
            i32.const 1
            call $__rust_alloc
            local.set 1
            br 1 (;@3;)
          end
          local.get 3
          i32.load
          local.get 1
          i32.const 1
          local.get 2
          call $__rust_realloc
          local.set 1
        end
        block  ;; label = @3
          local.get 1
          i32.eqz
          br_if 0 (;@3;)
          local.get 0
          local.get 1
          i32.store offset=4
          local.get 0
          i32.const 8
          i32.add
          local.get 2
          i32.store
          local.get 0
          i32.const 0
          i32.store
          return
        end
        local.get 0
        i32.const 1
        i32.store offset=4
        local.get 0
        i32.const 8
        i32.add
        local.get 2
        i32.store
        local.get 0
        i32.const 1
        i32.store
        return
      end
      local.get 0
      i32.const 0
      i32.store offset=4
      local.get 0
      i32.const 8
      i32.add
      local.get 2
      i32.store
    end
    local.get 0
    i32.const 1
    i32.store)
  (func $_ZN4core3ptr39drop_in_place$LT$std..path..PathBuf$GT$17h6b2ac406cb2d3acfE (type 2) (param i32)
    block  ;; label = @1
      local.get 0
      i32.const 4
      i32.add
      i32.load
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      i32.load
      call $free
    end)
  (func $rust_panic (type 14)
    unreachable
    unreachable)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$16reserve_for_push17haff08c7ab95aead1E (type 3) (param i32 i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 1
        i32.add
        local.tee 1
        i32.eqz
        br_if 0 (;@2;)
        local.get 0
        i32.const 4
        i32.add
        i32.load
        local.tee 3
        i32.const 1
        i32.shl
        local.tee 4
        local.get 1
        local.get 4
        local.get 1
        i32.gt_u
        select
        local.tee 1
        i32.const 8
        local.get 1
        i32.const 8
        i32.gt_u
        select
        local.tee 1
        i32.const -1
        i32.xor
        i32.const 31
        i32.shr_u
        local.set 4
        block  ;; label = @3
          block  ;; label = @4
            local.get 3
            i32.eqz
            br_if 0 (;@4;)
            local.get 2
            local.get 3
            i32.store offset=24
            local.get 2
            i32.const 1
            i32.store offset=20
            local.get 2
            local.get 0
            i32.load
            i32.store offset=16
            br 1 (;@3;)
          end
          local.get 2
          i32.const 0
          i32.store offset=20
        end
        local.get 2
        local.get 4
        local.get 1
        local.get 2
        i32.const 16
        i32.add
        call $_ZN5alloc7raw_vec11finish_grow17h7f10e140e73363beE
        local.get 2
        i32.load offset=4
        local.set 3
        block  ;; label = @3
          local.get 2
          i32.load
          br_if 0 (;@3;)
          local.get 0
          local.get 3
          i32.store
          local.get 0
          i32.const 4
          i32.add
          local.get 1
          i32.store
          br 2 (;@1;)
        end
        local.get 3
        i32.const -2147483647
        i32.eq
        br_if 1 (;@1;)
        local.get 3
        i32.eqz
        br_if 0 (;@2;)
        local.get 3
        local.get 2
        i32.const 8
        i32.add
        i32.load
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
      unreachable
    end
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer)
  (func $_ZN3std7process5abort17hef6a1f4cde1d025cE (type 14)
    call $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E
    unreachable)
  (func $_ZN4core3ptr24drop_in_place$LT$u16$GT$17hb2b91af30d5c58eeE (type 2) (param i32))
  (func $_ZN91_$LT$std..sys_common..backtrace.._print..DisplayBacktrace$u20$as$u20$core..fmt..Display$GT$3fmt17h65a078f2606287d9E (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32 i32 i64 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    i32.const 0
    i32.load8_u offset=1059320
    drop
    local.get 0
    i32.load8_u
    local.set 3
    i32.const 512
    local.set 4
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              i32.const 512
              call $malloc
              local.tee 0
              i32.eqz
              br_if 0 (;@5;)
              local.get 2
              i32.const 512
              i32.store offset=12
              local.get 2
              local.get 0
              i32.store offset=8
              local.get 0
              i32.const 512
              call $getcwd
              br_if 1 (;@4;)
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    i32.const 0
                    i32.load offset=1059820
                    local.tee 4
                    i32.const 68
                    i32.ne
                    br_if 0 (;@8;)
                    i32.const 512
                    local.set 4
                    loop  ;; label = @9
                      local.get 2
                      local.get 4
                      i32.store offset=16
                      local.get 2
                      i32.const 8
                      i32.add
                      local.get 4
                      i32.const 1
                      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$7reserve21do_reserve_and_handle17h2174b82f11d991afE
                      local.get 2
                      i32.load offset=8
                      local.tee 0
                      local.get 2
                      i32.load offset=12
                      local.tee 4
                      call $getcwd
                      br_if 5 (;@4;)
                      i32.const 0
                      i32.load offset=1059820
                      local.tee 5
                      i32.const 68
                      i32.eq
                      br_if 0 (;@9;)
                    end
                    local.get 5
                    i64.extend_i32_u
                    i64.const 32
                    i64.shl
                    local.set 6
                    local.get 4
                    br_if 1 (;@7;)
                    br 2 (;@6;)
                  end
                  local.get 4
                  i64.extend_i32_u
                  i64.const 32
                  i64.shl
                  local.set 6
                end
                local.get 0
                call $free
              end
              i32.const 0
              local.set 0
              br 2 (;@3;)
            end
            i32.const 1
            i32.const 512
            call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
            unreachable
          end
          local.get 2
          local.get 0
          call $strlen
          local.tee 5
          i32.store offset=16
          block  ;; label = @4
            local.get 4
            local.get 5
            i32.le_u
            br_if 0 (;@4;)
            block  ;; label = @5
              block  ;; label = @6
                local.get 5
                br_if 0 (;@6;)
                local.get 0
                call $free
                i32.const 1
                local.set 0
                br 1 (;@5;)
              end
              local.get 0
              local.get 4
              i32.const 1
              local.get 5
              call $__rust_realloc
              local.tee 0
              i32.eqz
              br_if 3 (;@2;)
            end
            local.get 2
            local.get 5
            i32.store offset=12
          end
          local.get 2
          i64.load offset=12 align=4
          local.set 6
        end
        local.get 0
        br_if 1 (;@1;)
        local.get 6
        i64.const 255
        i64.and
        i64.const 3
        i64.ne
        br_if 1 (;@1;)
        local.get 6
        i64.const 32
        i64.shr_u
        i32.wrap_i64
        local.tee 4
        i32.load
        local.tee 7
        local.get 4
        i32.const 4
        i32.add
        i32.load
        local.tee 5
        i32.load
        call_indirect (type 2)
        block  ;; label = @3
          local.get 5
          i32.const 4
          i32.add
          i32.load
          i32.eqz
          br_if 0 (;@3;)
          local.get 7
          call $free
        end
        local.get 4
        call $free
        br 1 (;@1;)
      end
      i32.const 1
      local.get 5
      call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
      unreachable
    end
    local.get 2
    i32.const 20
    i32.add
    i64.const 0
    i64.store align=4
    i32.const 1
    local.set 4
    local.get 2
    i32.const 1
    i32.store offset=12
    local.get 2
    i32.const 1054660
    i32.store offset=8
    local.get 2
    i32.const 1054164
    i32.store offset=16
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            local.get 1
            i32.const 20
            i32.add
            i32.load
            local.tee 5
            local.get 1
            i32.const 24
            i32.add
            i32.load
            local.tee 1
            local.get 2
            i32.const 8
            i32.add
            call $_ZN4core3fmt9Formatter9write_fmt17h5cc4795932e82988E
            br_if 0 (;@4;)
            local.get 3
            i32.const 255
            i32.and
            br_if 1 (;@3;)
            local.get 2
            i32.const 20
            i32.add
            i64.const 0
            i64.store align=4
            local.get 2
            i32.const 1
            i32.store offset=12
            local.get 2
            i32.const 1054756
            i32.store offset=8
            local.get 2
            i32.const 1054164
            i32.store offset=16
            local.get 5
            local.get 1
            local.get 2
            i32.const 8
            i32.add
            call $_ZN4core3fmt9Formatter9write_fmt17h5cc4795932e82988E
            i32.eqz
            br_if 1 (;@3;)
          end
          local.get 0
          i32.eqz
          br_if 2 (;@1;)
          local.get 6
          i64.const 4294967295
          i64.and
          i64.eqz
          br_if 2 (;@1;)
          br 1 (;@2;)
        end
        i32.const 0
        local.set 4
        local.get 0
        i32.eqz
        br_if 1 (;@1;)
        local.get 6
        i64.const 4294967295
        i64.and
        i64.eqz
        br_if 1 (;@1;)
      end
      local.get 0
      call $free
    end
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 4)
  (func $_ZN3std5alloc24default_alloc_error_hook17h1f56ab869b311cf1E (type 3) (param i32 i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 64
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 2
    i32.const 1
    i32.store offset=4
    local.get 2
    local.get 1
    i32.store offset=12
    local.get 2
    local.get 2
    i32.const 12
    i32.add
    i32.store
    local.get 2
    i32.const 4
    i32.store8 offset=16
    local.get 2
    local.get 2
    i32.const 56
    i32.add
    i32.store offset=24
    local.get 2
    i64.const 1
    i64.store offset=44 align=4
    local.get 2
    i32.const 2
    i32.store offset=36
    local.get 2
    i32.const 1054860
    i32.store offset=32
    local.get 2
    local.get 2
    i32.store offset=40
    local.get 2
    i32.const 16
    i32.add
    i32.const 1054512
    local.get 2
    i32.const 32
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 3
    local.get 2
    i32.load8_u offset=16
    local.set 1
    block  ;; label = @1
      block  ;; label = @2
        local.get 3
        i32.eqz
        br_if 0 (;@2;)
        local.get 1
        i32.const 4
        i32.eq
        br_if 1 (;@1;)
        local.get 2
        i32.load offset=20
        local.set 3
        block  ;; label = @3
          local.get 2
          i32.load8_u offset=16
          local.tee 1
          i32.const 4
          i32.gt_u
          br_if 0 (;@3;)
          local.get 1
          i32.const 3
          i32.ne
          br_if 2 (;@1;)
        end
        local.get 3
        i32.load
        local.tee 4
        local.get 3
        i32.const 4
        i32.add
        i32.load
        local.tee 1
        i32.load
        call_indirect (type 2)
        block  ;; label = @3
          local.get 1
          i32.const 4
          i32.add
          i32.load
          i32.eqz
          br_if 0 (;@3;)
          local.get 4
          call $free
        end
        local.get 3
        call $free
        br 1 (;@1;)
      end
      local.get 2
      i32.load offset=20
      local.set 3
      block  ;; label = @2
        local.get 1
        i32.const 4
        i32.gt_u
        br_if 0 (;@2;)
        local.get 1
        i32.const 3
        i32.ne
        br_if 1 (;@1;)
      end
      local.get 3
      i32.load
      local.tee 4
      local.get 3
      i32.const 4
      i32.add
      i32.load
      local.tee 1
      i32.load
      call_indirect (type 2)
      block  ;; label = @2
        local.get 1
        i32.const 4
        i32.add
        i32.load
        i32.eqz
        br_if 0 (;@2;)
        local.get 4
        call $free
      end
      local.get 3
      call $free
    end
    local.get 2
    i32.const 64
    i32.add
    global.set $__stack_pointer)
  (func $_ZN44_$LT$$RF$T$u20$as$u20$core..fmt..Display$GT$3fmt17h3cd999b848d69bd1E (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    local.get 2
    i32.const 20
    i32.add
    i32.const 1
    i32.store
    local.get 2
    i32.const 12
    i32.add
    i32.const 1
    i32.store
    local.get 2
    local.get 0
    i32.const 12
    i32.add
    i32.store offset=16
    local.get 2
    local.get 0
    i32.const 8
    i32.add
    i32.store offset=8
    local.get 2
    i32.const 5
    i32.store offset=4
    local.get 2
    local.get 0
    i32.store
    local.get 1
    i32.const 24
    i32.add
    i32.load
    local.set 0
    local.get 1
    i32.load offset=20
    local.set 1
    local.get 2
    i64.const 3
    i64.store offset=36 align=4
    local.get 2
    i32.const 3
    i32.store offset=28
    local.get 2
    i32.const 1049816
    i32.store offset=24
    local.get 2
    local.get 2
    i32.store offset=32
    local.get 1
    local.get 0
    local.get 2
    i32.const 24
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 0
    local.get 2
    i32.const 48
    i32.add
    global.set $__stack_pointer
    local.get 0)
  (func $_ZN3std10sys_common9backtrace5print17h9d7796a319bcb766E (type 12) (param i32 i32 i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 3
    global.set $__stack_pointer
    i32.const 0
    i32.load8_u offset=1059260
    local.set 4
    i32.const 1
    local.set 5
    i32.const 0
    i32.const 1
    i32.store8 offset=1059260
    local.get 3
    local.get 4
    i32.store8 offset=32
    block  ;; label = @1
      local.get 4
      br_if 0 (;@1;)
      block  ;; label = @2
        i32.const 0
        i32.load offset=1059268
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if 0 (;@2;)
        call $_ZN3std9panicking11panic_count17is_zero_slow_path17h75908fc4564b8b9eE
        local.set 5
      end
      local.get 3
      i32.const 20
      i32.add
      i64.const 1
      i64.store align=4
      local.get 3
      i32.const 1
      i32.store offset=12
      local.get 3
      i32.const 1054360
      i32.store offset=8
      local.get 3
      i32.const 11
      i32.store offset=36
      local.get 3
      local.get 2
      i32.store8 offset=47
      local.get 3
      local.get 3
      i32.const 32
      i32.add
      i32.store offset=16
      local.get 3
      local.get 3
      i32.const 47
      i32.add
      i32.store offset=32
      local.get 0
      local.get 1
      local.get 3
      i32.const 8
      i32.add
      call $_ZN3std2io5Write9write_fmt17hab21973df7a26b7dE
      block  ;; label = @2
        local.get 5
        i32.eqz
        br_if 0 (;@2;)
        i32.const 0
        i32.load offset=1059268
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if 0 (;@2;)
        call $_ZN3std9panicking11panic_count17is_zero_slow_path17h75908fc4564b8b9eE
        br_if 0 (;@2;)
        i32.const 0
        i32.const 1
        i32.store8 offset=1059261
      end
      i32.const 0
      i32.const 0
      i32.store8 offset=1059260
      local.get 3
      i32.const 48
      i32.add
      global.set $__stack_pointer
      return
    end
    local.get 3
    i64.const 0
    i64.store offset=20 align=4
    local.get 3
    i32.const 1054164
    i32.store offset=16
    local.get 3
    i32.const 1
    i32.store offset=12
    local.get 3
    i32.const 1055392
    i32.store offset=8
    local.get 3
    i32.const 32
    i32.add
    local.get 3
    i32.const 8
    i32.add
    call $_ZN4core9panicking13assert_failed17h574f7db4222bb7e6E
    unreachable)
  (func $_ZN3std10sys_common9backtrace26__rust_end_short_backtrace17hffd60a674bcf0795E (type 2) (param i32)
    local.get 0
    call $_ZN3std9panicking19begin_panic_handler28_$u7b$$u7b$closure$u7d$$u7d$17h21734c0d3e1fd911E
    unreachable)
  (func $_ZN3std9panicking19begin_panic_handler28_$u7b$$u7b$closure$u7d$$u7d$17h21734c0d3e1fd911E (type 2) (param i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.tee 2
    i32.const 12
    i32.add
    i32.load
    local.set 3
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            local.get 2
            i32.load offset=4
            br_table 0 (;@4;) 1 (;@3;) 3 (;@1;)
          end
          local.get 3
          br_if 2 (;@1;)
          i32.const 1054164
          local.set 2
          i32.const 0
          local.set 3
          br 1 (;@2;)
        end
        local.get 3
        br_if 1 (;@1;)
        local.get 2
        i32.load
        local.tee 2
        i32.load offset=4
        local.set 3
        local.get 2
        i32.load
        local.set 2
      end
      local.get 1
      local.get 3
      i32.store offset=4
      local.get 1
      local.get 2
      i32.store
      local.get 1
      i32.const 1055140
      local.get 0
      i32.load offset=4
      local.tee 2
      i32.load offset=12
      local.get 0
      i32.load offset=8
      local.get 2
      i32.load8_u offset=16
      call $_ZN3std9panicking20rust_panic_with_hook17h9ac9df70df6ab297E
      unreachable
    end
    local.get 1
    i32.const 0
    i32.store offset=4
    local.get 1
    local.get 2
    i32.store
    local.get 1
    i32.const 1055120
    local.get 0
    i32.load offset=4
    local.tee 2
    i32.load offset=12
    local.get 0
    i32.load offset=8
    local.get 2
    i32.load8_u offset=16
    call $_ZN3std9panicking20rust_panic_with_hook17h9ac9df70df6ab297E
    unreachable)
  (func $_ZN3std9panicking20rust_panic_with_hook17h9ac9df70df6ab297E (type 11) (param i32 i32 i32 i32 i32)
    (local i32 i32 i64 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 448
    i32.sub
    local.tee 5
    global.set $__stack_pointer
    i32.const 0
    i32.const 0
    i32.load offset=1059268
    local.tee 6
    i32.const 1
    i32.add
    i32.store offset=1059268
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    block  ;; label = @9
                      block  ;; label = @10
                        local.get 6
                        i32.const 0
                        i32.lt_s
                        br_if 0 (;@10;)
                        i32.const 0
                        i32.load8_u offset=1059284
                        br_if 1 (;@9;)
                        i32.const 1
                        local.set 6
                        i32.const 0
                        i32.const 1
                        i32.store8 offset=1059284
                        i32.const 0
                        i32.const 0
                        i32.load offset=1059280
                        i32.const 1
                        i32.add
                        i32.store offset=1059280
                        i32.const 0
                        i32.load offset=1059264
                        local.tee 2
                        i32.const -1
                        i32.le_s
                        br_if 3 (;@7;)
                        i32.const 0
                        local.get 2
                        i32.const 1
                        i32.add
                        i32.store offset=1059264
                        local.get 0
                        local.get 1
                        i32.load offset=16
                        call_indirect (type 7)
                        local.set 1
                        local.set 2
                        i32.const 0
                        i32.load offset=1059280
                        i32.const 1
                        i32.gt_u
                        br_if 6 (;@4;)
                        i32.const 0
                        local.set 6
                        block  ;; label = @11
                          block  ;; label = @12
                            block  ;; label = @13
                              block  ;; label = @14
                                i32.const 0
                                i32.load offset=1059256
                                br_table 3 (;@11;) 10 (;@4;) 1 (;@13;) 2 (;@12;) 0 (;@14;)
                              end
                              i32.const 1054184
                              i32.const 40
                              i32.const 1054560
                              call $_ZN4core9panicking5panic17hcfcdcc589d164b16E
                              unreachable
                            end
                            i32.const 1
                            local.set 6
                            br 8 (;@4;)
                          end
                          i32.const 2
                          local.set 6
                          br 7 (;@4;)
                        end
                        local.get 5
                        i32.const 0
                        i32.store8 offset=70
                        local.get 5
                        i32.const 0
                        i64.load offset=1054350 align=1
                        i64.store offset=62 align=2
                        local.get 5
                        i32.const 0
                        i64.load offset=1054344 align=1
                        i64.store offset=56
                        local.get 5
                        i32.const 32
                        i32.add
                        local.get 5
                        i32.const 56
                        i32.add
                        call $_ZN4core3ffi5c_str4CStr19from_bytes_with_nul17h9450f87e6dcc5836E
                        block  ;; label = @11
                          local.get 5
                          i32.load offset=32
                          br_if 0 (;@11;)
                          local.get 5
                          i32.load offset=36
                          call $getenv
                          local.set 0
                          br 5 (;@6;)
                        end
                        i32.const 0
                        i64.load offset=1054632
                        local.tee 7
                        i64.const 32
                        i64.shr_u
                        i32.wrap_i64
                        local.set 0
                        local.get 7
                        i32.wrap_i64
                        i32.const 255
                        i32.and
                        local.tee 8
                        i32.const 4
                        i32.eq
                        br_if 4 (;@6;)
                        i32.const 3
                        local.set 9
                        i32.const 2
                        local.set 6
                        local.get 8
                        i32.const 3
                        i32.lt_u
                        br_if 5 (;@5;)
                        local.get 0
                        i32.load
                        local.tee 10
                        local.get 0
                        i32.const 4
                        i32.add
                        i32.load
                        local.tee 8
                        i32.load
                        call_indirect (type 2)
                        block  ;; label = @11
                          local.get 8
                          i32.const 4
                          i32.add
                          i32.load
                          i32.eqz
                          br_if 0 (;@11;)
                          local.get 10
                          call $free
                        end
                        local.get 0
                        call $free
                        br 5 (;@5;)
                      end
                      local.get 5
                      local.get 2
                      i32.store offset=44
                      local.get 5
                      i32.const 1055160
                      i32.store offset=36
                      local.get 5
                      i32.const 1054164
                      i32.store offset=32
                      local.get 5
                      local.get 4
                      i32.store8 offset=48
                      local.get 5
                      local.get 3
                      i32.store offset=40
                      local.get 5
                      i32.const 12
                      i32.store offset=28
                      local.get 5
                      local.get 5
                      i32.const 32
                      i32.add
                      i32.store offset=24
                      local.get 5
                      i32.const 4
                      i32.store8
                      local.get 5
                      local.get 5
                      i32.const 440
                      i32.add
                      i32.store offset=8
                      local.get 5
                      i64.const 1
                      i64.store offset=68 align=4
                      local.get 5
                      i32.const 2
                      i32.store offset=60
                      local.get 5
                      i32.const 1055344
                      i32.store offset=56
                      local.get 5
                      local.get 5
                      i32.const 24
                      i32.add
                      i32.store offset=64
                      local.get 5
                      i32.const 1054512
                      local.get 5
                      i32.const 56
                      i32.add
                      call $_ZN4core3fmt5write17h8253e306f6bd0e19E
                      local.set 4
                      local.get 5
                      i32.load8_u
                      local.set 6
                      block  ;; label = @10
                        local.get 4
                        i32.eqz
                        br_if 0 (;@10;)
                        local.get 6
                        i32.const 4
                        i32.eq
                        br_if 2 (;@8;)
                        local.get 5
                        i32.load offset=4
                        local.set 6
                        block  ;; label = @11
                          local.get 5
                          i32.load8_u
                          local.tee 5
                          i32.const 4
                          i32.gt_u
                          br_if 0 (;@11;)
                          local.get 5
                          i32.const 3
                          i32.ne
                          br_if 3 (;@8;)
                        end
                        local.get 6
                        i32.load
                        local.tee 4
                        local.get 6
                        i32.const 4
                        i32.add
                        i32.load
                        local.tee 5
                        i32.load
                        call_indirect (type 2)
                        block  ;; label = @11
                          local.get 5
                          i32.const 4
                          i32.add
                          i32.load
                          i32.eqz
                          br_if 0 (;@11;)
                          local.get 4
                          call $free
                        end
                        local.get 6
                        call $free
                        call $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E
                        unreachable
                      end
                      local.get 5
                      i32.load offset=4
                      local.set 5
                      block  ;; label = @10
                        local.get 6
                        i32.const 4
                        i32.gt_u
                        br_if 0 (;@10;)
                        local.get 6
                        i32.const 3
                        i32.ne
                        br_if 2 (;@8;)
                      end
                      local.get 5
                      i32.load
                      local.tee 4
                      local.get 5
                      i32.const 4
                      i32.add
                      i32.load
                      local.tee 6
                      i32.load
                      call_indirect (type 2)
                      block  ;; label = @10
                        local.get 6
                        i32.const 4
                        i32.add
                        i32.load
                        i32.eqz
                        br_if 0 (;@10;)
                        local.get 4
                        call $free
                      end
                      local.get 5
                      call $free
                      call $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E
                      unreachable
                    end
                    local.get 5
                    i32.const 4
                    i32.store8 offset=32
                    local.get 5
                    local.get 5
                    i32.const 440
                    i32.add
                    i32.store offset=40
                    local.get 5
                    i64.const 0
                    i64.store offset=68 align=4
                    local.get 5
                    i32.const 1054164
                    i32.store offset=64
                    local.get 5
                    i32.const 1
                    i32.store offset=60
                    local.get 5
                    i32.const 1055284
                    i32.store offset=56
                    local.get 5
                    i32.const 32
                    i32.add
                    i32.const 1054512
                    local.get 5
                    i32.const 56
                    i32.add
                    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
                    local.set 4
                    local.get 5
                    i32.load8_u offset=32
                    local.set 6
                    block  ;; label = @9
                      local.get 4
                      i32.eqz
                      br_if 0 (;@9;)
                      local.get 6
                      i32.const 4
                      i32.eq
                      br_if 1 (;@8;)
                      local.get 5
                      i32.load offset=36
                      local.set 6
                      block  ;; label = @10
                        local.get 5
                        i32.load8_u offset=32
                        local.tee 5
                        i32.const 4
                        i32.gt_u
                        br_if 0 (;@10;)
                        local.get 5
                        i32.const 3
                        i32.ne
                        br_if 2 (;@8;)
                      end
                      local.get 6
                      i32.load
                      local.tee 4
                      local.get 6
                      i32.const 4
                      i32.add
                      i32.load
                      local.tee 5
                      i32.load
                      call_indirect (type 2)
                      block  ;; label = @10
                        local.get 5
                        i32.const 4
                        i32.add
                        i32.load
                        i32.eqz
                        br_if 0 (;@10;)
                        local.get 4
                        call $free
                      end
                      local.get 6
                      call $free
                      call $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E
                      unreachable
                    end
                    local.get 5
                    i32.load offset=36
                    local.set 5
                    block  ;; label = @9
                      local.get 6
                      i32.const 4
                      i32.gt_u
                      br_if 0 (;@9;)
                      local.get 6
                      i32.const 3
                      i32.ne
                      br_if 1 (;@8;)
                    end
                    local.get 5
                    i32.load
                    local.tee 4
                    local.get 5
                    i32.const 4
                    i32.add
                    i32.load
                    local.tee 6
                    i32.load
                    call_indirect (type 2)
                    block  ;; label = @9
                      local.get 6
                      i32.const 4
                      i32.add
                      i32.load
                      i32.eqz
                      br_if 0 (;@9;)
                      local.get 4
                      call $free
                    end
                    local.get 5
                    call $free
                  end
                  call $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E
                  unreachable
                end
                local.get 5
                i32.const 68
                i32.add
                i64.const 0
                i64.store align=4
                local.get 5
                i32.const 1
                i32.store offset=60
                local.get 5
                i32.const 1055520
                i32.store offset=56
                local.get 5
                local.get 5
                i32.const 440
                i32.add
                i32.store offset=64
                local.get 5
                i32.const 32
                i32.add
                local.get 5
                i32.const 440
                i32.add
                local.get 5
                i32.const 56
                i32.add
                call $_ZN3std2io5Write9write_fmt17hab21973df7a26b7dE
                local.get 5
                i32.load8_u offset=32
                local.get 5
                i32.load offset=36
                call $_ZN4core3ptr81drop_in_place$LT$core..result..Result$LT$$LP$$RP$$C$std..io..error..Error$GT$$GT$17hb85f686a3328dc58E
                call $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E
                unreachable
              end
              block  ;; label = @6
                local.get 0
                br_if 0 (;@6;)
                i32.const 3
                local.set 9
                i32.const 2
                local.set 6
                br 1 (;@5;)
              end
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    block  ;; label = @9
                      local.get 0
                      call $strlen
                      local.tee 9
                      i32.eqz
                      br_if 0 (;@9;)
                      local.get 9
                      i32.const -1
                      i32.gt_s
                      local.tee 8
                      i32.eqz
                      br_if 6 (;@3;)
                      i32.const 0
                      local.set 6
                      i32.const 0
                      i32.load8_u offset=1059320
                      drop
                      local.get 9
                      local.get 8
                      call $__rust_alloc
                      local.tee 10
                      i32.eqz
                      br_if 7 (;@2;)
                      local.get 10
                      local.get 0
                      local.get 9
                      call $memcpy
                      local.set 0
                      block  ;; label = @10
                        local.get 9
                        i32.const -1
                        i32.add
                        br_table 2 (;@8;) 3 (;@7;) 3 (;@7;) 0 (;@10;) 3 (;@7;)
                      end
                      local.get 0
                      i32.load align=1
                      i32.const 1819047270
                      i32.eq
                      local.set 6
                      br 2 (;@7;)
                    end
                    i32.const 1
                    local.get 0
                    local.get 9
                    call $memcpy
                    drop
                    i32.const 0
                    local.set 6
                    br 2 (;@6;)
                  end
                  local.get 0
                  i32.load8_u
                  i32.const 48
                  i32.eq
                  i32.const 1
                  i32.shl
                  local.set 6
                end
                local.get 0
                call $free
              end
              local.get 6
              i32.const 1
              i32.add
              local.set 9
            end
            i32.const 0
            local.get 9
            i32.store offset=1059256
          end
          local.get 5
          local.get 3
          i32.store offset=12
          i32.const 12
          local.set 3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                local.get 2
                local.get 1
                i32.const 12
                i32.add
                local.tee 0
                i32.load
                call_indirect (type 6)
                i64.const -4493808902380553279
                i64.eq
                br_if 0 (;@6;)
                i32.const 1054904
                local.set 1
                local.get 2
                local.get 0
                i32.load
                call_indirect (type 6)
                i64.const 1958613589856376022
                i64.ne
                br_if 2 (;@4;)
                local.get 2
                i32.const 8
                i32.add
                local.set 3
                br 1 (;@5;)
              end
              local.get 2
              i32.const 4
              i32.add
              local.set 3
            end
            local.get 3
            i32.load
            local.set 3
            local.get 2
            i32.load
            local.set 1
          end
          local.get 5
          local.get 3
          i32.store offset=20
          local.get 5
          local.get 1
          i32.store offset=16
          block  ;; label = @4
            block  ;; label = @5
              call $_ZN3std10sys_common11thread_info14current_thread17h2d20a3c7c082bda6E
              local.tee 3
              i32.const 16
              i32.add
              i32.load
              local.tee 2
              br_if 0 (;@5;)
              i32.const 9
              local.set 1
              i32.const 1054916
              local.set 2
              br 1 (;@4;)
            end
            local.get 3
            i32.const 20
            i32.add
            i32.load
            i32.const -1
            i32.add
            local.set 1
          end
          local.get 5
          local.get 1
          i32.store offset=28
          local.get 5
          local.get 2
          i32.store offset=24
          local.get 5
          i32.const 32
          i32.add
          i32.const 12
          i32.add
          i64.const 3
          i64.store align=4
          local.get 5
          i32.const 76
          i32.add
          i32.const 13
          i32.store
          local.get 5
          i32.const 56
          i32.add
          i32.const 12
          i32.add
          i32.const 5
          i32.store
          local.get 5
          i32.const 1054952
          i32.store offset=32
          local.get 5
          i32.const 5
          i32.store offset=60
          local.get 5
          local.get 5
          i32.const 56
          i32.add
          i32.store offset=40
          local.get 5
          local.get 5
          i32.const 12
          i32.add
          i32.store offset=72
          local.get 5
          local.get 5
          i32.const 16
          i32.add
          i32.store offset=64
          local.get 5
          local.get 5
          i32.const 24
          i32.add
          i32.store offset=56
          local.get 5
          i32.const 4
          i32.store offset=36
          local.get 5
          local.get 5
          i32.const 440
          i32.add
          local.get 5
          i32.const 32
          i32.add
          call $_ZN3std2io5Write9write_fmt17hab21973df7a26b7dE
          local.get 5
          i32.load offset=4
          local.set 1
          block  ;; label = @4
            block  ;; label = @5
              local.get 5
              i32.load8_u
              local.tee 2
              i32.const 4
              i32.gt_u
              br_if 0 (;@5;)
              local.get 2
              i32.const 3
              i32.ne
              br_if 1 (;@4;)
            end
            local.get 1
            i32.load
            local.tee 0
            local.get 1
            i32.const 4
            i32.add
            i32.load
            local.tee 2
            i32.load
            call_indirect (type 2)
            block  ;; label = @5
              local.get 2
              i32.const 4
              i32.add
              i32.load
              i32.eqz
              br_if 0 (;@5;)
              local.get 0
              call $free
            end
            local.get 1
            call $free
          end
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  local.get 6
                  br_table 0 (;@7;) 1 (;@6;) 2 (;@5;) 0 (;@7;)
                end
                local.get 5
                i32.const 56
                i32.add
                local.get 5
                i32.const 440
                i32.add
                i32.const 0
                call $_ZN3std10sys_common9backtrace5print17h9d7796a319bcb766E
                local.get 5
                i32.load offset=60
                local.set 2
                block  ;; label = @7
                  local.get 5
                  i32.load8_u offset=56
                  local.tee 6
                  i32.const 4
                  i32.gt_u
                  br_if 0 (;@7;)
                  local.get 6
                  i32.const 3
                  i32.ne
                  br_if 3 (;@4;)
                end
                local.get 2
                i32.load
                local.tee 1
                local.get 2
                i32.const 4
                i32.add
                i32.load
                local.tee 6
                i32.load
                call_indirect (type 2)
                block  ;; label = @7
                  local.get 6
                  i32.const 4
                  i32.add
                  i32.load
                  i32.eqz
                  br_if 0 (;@7;)
                  local.get 1
                  call $free
                end
                local.get 2
                call $free
                br 2 (;@4;)
              end
              local.get 5
              i32.const 56
              i32.add
              local.get 5
              i32.const 440
              i32.add
              i32.const 1
              call $_ZN3std10sys_common9backtrace5print17h9d7796a319bcb766E
              local.get 5
              i32.load offset=60
              local.set 2
              block  ;; label = @6
                local.get 5
                i32.load8_u offset=56
                local.tee 6
                i32.const 4
                i32.gt_u
                br_if 0 (;@6;)
                local.get 6
                i32.const 3
                i32.ne
                br_if 2 (;@4;)
              end
              local.get 2
              i32.load
              local.tee 1
              local.get 2
              i32.const 4
              i32.add
              i32.load
              local.tee 6
              i32.load
              call_indirect (type 2)
              block  ;; label = @6
                local.get 6
                i32.const 4
                i32.add
                i32.load
                i32.eqz
                br_if 0 (;@6;)
                local.get 1
                call $free
              end
              local.get 2
              call $free
              br 1 (;@4;)
            end
            i32.const 0
            i32.load8_u offset=1059240
            local.set 6
            i32.const 0
            i32.const 0
            i32.store8 offset=1059240
            local.get 6
            i32.eqz
            br_if 0 (;@4;)
            local.get 5
            i32.const 68
            i32.add
            i64.const 0
            i64.store align=4
            local.get 5
            i32.const 1
            i32.store offset=60
            local.get 5
            i32.const 1055064
            i32.store offset=56
            local.get 5
            i32.const 1054164
            i32.store offset=64
            local.get 5
            i32.const 32
            i32.add
            local.get 5
            i32.const 440
            i32.add
            local.get 5
            i32.const 56
            i32.add
            call $_ZN3std2io5Write9write_fmt17hab21973df7a26b7dE
            local.get 5
            i32.load offset=36
            local.set 2
            block  ;; label = @5
              local.get 5
              i32.load8_u offset=32
              local.tee 6
              i32.const 4
              i32.gt_u
              br_if 0 (;@5;)
              local.get 6
              i32.const 3
              i32.ne
              br_if 1 (;@4;)
            end
            local.get 2
            i32.load
            local.tee 1
            local.get 2
            i32.const 4
            i32.add
            i32.load
            local.tee 6
            i32.load
            call_indirect (type 2)
            block  ;; label = @5
              local.get 6
              i32.const 4
              i32.add
              i32.load
              i32.eqz
              br_if 0 (;@5;)
              local.get 1
              call $free
            end
            local.get 2
            call $free
          end
          local.get 3
          local.get 3
          i32.load
          local.tee 6
          i32.const -1
          i32.add
          i32.store
          block  ;; label = @4
            local.get 6
            i32.const 1
            i32.ne
            br_if 0 (;@4;)
            local.get 3
            call $_ZN5alloc4sync12Arc$LT$T$GT$9drop_slow17hfead2a7a1440e4b8E
          end
          i32.const 0
          i32.const 0
          i32.load offset=1059264
          i32.const -1
          i32.add
          i32.store offset=1059264
          i32.const 0
          i32.const 0
          i32.store8 offset=1059284
          local.get 4
          br_if 2 (;@1;)
          local.get 5
          i32.const 68
          i32.add
          i64.const 0
          i64.store align=4
          local.get 5
          i32.const 1
          i32.store offset=60
          local.get 5
          i32.const 1055224
          i32.store offset=56
          local.get 5
          i32.const 1054164
          i32.store offset=64
          local.get 5
          i32.const 32
          i32.add
          local.get 5
          i32.const 440
          i32.add
          local.get 5
          i32.const 56
          i32.add
          call $_ZN3std2io5Write9write_fmt17hab21973df7a26b7dE
          local.get 5
          i32.load8_u offset=32
          local.get 5
          i32.load offset=36
          call $_ZN4core3ptr81drop_in_place$LT$core..result..Result$LT$$LP$$RP$$C$std..io..error..Error$GT$$GT$17hb85f686a3328dc58E
          call $_ZN3std3sys4wasi14abort_internal17hc490932b728b6a87E
          unreachable
        end
        call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
        unreachable
      end
      local.get 8
      local.get 9
      call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
      unreachable
    end
    call $rust_panic
    unreachable)
  (func $_ZN4core3ptr70drop_in_place$LT$std..panicking..begin_panic_handler..PanicPayload$GT$17h017685081936aa35E (type 2) (param i32)
    (local i32)
    block  ;; label = @1
      local.get 0
      i32.const 4
      i32.add
      i32.load
      local.tee 1
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      i32.const 8
      i32.add
      i32.load
      i32.eqz
      br_if 0 (;@1;)
      local.get 1
      call $free
    end)
  (func $_ZN90_$LT$std..panicking..begin_panic_handler..PanicPayload$u20$as$u20$core..panic..BoxMeUp$GT$8take_box17h571d43091b181743E (type 7) (param i32) (result i32 i32)
    (local i32 i32 i32 i32 i64)
    global.get $__stack_pointer
    i32.const 48
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    local.get 0
    i32.const 4
    i32.add
    local.set 2
    block  ;; label = @1
      local.get 0
      i32.load offset=4
      br_if 0 (;@1;)
      local.get 0
      i32.load
      local.set 3
      local.get 1
      i32.const 32
      i32.add
      i32.const 8
      i32.add
      local.tee 4
      i32.const 0
      i32.store
      local.get 1
      i64.const 1
      i64.store offset=32
      local.get 1
      local.get 1
      i32.const 32
      i32.add
      i32.store offset=44
      local.get 1
      i32.const 44
      i32.add
      i32.const 1054116
      local.get 3
      call $_ZN4core3fmt5write17h8253e306f6bd0e19E
      drop
      local.get 1
      i32.const 16
      i32.add
      i32.const 8
      i32.add
      local.get 4
      i32.load
      local.tee 3
      i32.store
      local.get 1
      local.get 1
      i64.load offset=32
      local.tee 5
      i64.store offset=16
      local.get 2
      i32.const 8
      i32.add
      local.get 3
      i32.store
      local.get 2
      local.get 5
      i64.store align=4
    end
    local.get 1
    i32.const 8
    i32.add
    local.tee 3
    local.get 2
    i32.const 8
    i32.add
    i32.load
    i32.store
    local.get 0
    i32.const 12
    i32.add
    i32.const 0
    i32.store
    local.get 2
    i64.load align=4
    local.set 5
    local.get 0
    i64.const 1
    i64.store offset=4 align=4
    i32.const 0
    i32.load8_u offset=1059320
    drop
    local.get 1
    local.get 5
    i64.store
    block  ;; label = @1
      i32.const 12
      call $malloc
      local.tee 0
      br_if 0 (;@1;)
      i32.const 4
      i32.const 12
      call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
      unreachable
    end
    local.get 0
    local.get 1
    i64.load
    i64.store align=4
    local.get 0
    i32.const 8
    i32.add
    local.get 3
    i32.load
    i32.store
    local.get 1
    i32.const 48
    i32.add
    global.set $__stack_pointer
    local.get 0
    i32.const 1055088)
  (func $_ZN90_$LT$std..panicking..begin_panic_handler..PanicPayload$u20$as$u20$core..panic..BoxMeUp$GT$3get17h570121d24b9b06c6E (type 7) (param i32) (result i32 i32)
    (local i32 i32 i32 i64)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    local.get 0
    i32.const 4
    i32.add
    local.set 2
    block  ;; label = @1
      local.get 0
      i32.load offset=4
      br_if 0 (;@1;)
      local.get 0
      i32.load
      local.set 0
      local.get 1
      i32.const 16
      i32.add
      i32.const 8
      i32.add
      local.tee 3
      i32.const 0
      i32.store
      local.get 1
      i64.const 1
      i64.store offset=16
      local.get 1
      local.get 1
      i32.const 16
      i32.add
      i32.store offset=28
      local.get 1
      i32.const 28
      i32.add
      i32.const 1054116
      local.get 0
      call $_ZN4core3fmt5write17h8253e306f6bd0e19E
      drop
      local.get 1
      i32.const 8
      i32.add
      local.get 3
      i32.load
      local.tee 0
      i32.store
      local.get 1
      local.get 1
      i64.load offset=16
      local.tee 4
      i64.store
      local.get 2
      i32.const 8
      i32.add
      local.get 0
      i32.store
      local.get 2
      local.get 4
      i64.store align=4
    end
    local.get 1
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 2
    i32.const 1055088)
  (func $_ZN36_$LT$T$u20$as$u20$core..any..Any$GT$7type_id17h4c4ad1a2d5b40bf7E (type 6) (param i32) (result i64)
    i64.const 1958613589856376022)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h27459983c441be4dE (type 0) (param i32 i32 i32) (result i32)
    (local i32)
    block  ;; label = @1
      local.get 0
      i32.load
      local.tee 0
      i32.load offset=4
      local.get 0
      i32.load offset=8
      local.tee 3
      i32.sub
      local.get 2
      i32.ge_u
      br_if 0 (;@1;)
      local.get 0
      local.get 3
      local.get 2
      call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$7reserve21do_reserve_and_handle17h2174b82f11d991afE
      local.get 0
      i32.load offset=8
      local.set 3
    end
    local.get 0
    i32.load
    local.get 3
    i32.add
    local.get 1
    local.get 2
    call $memcpy
    drop
    local.get 0
    local.get 3
    local.get 2
    i32.add
    i32.store offset=8
    i32.const 0)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17hd182b41fe69b70caE (type 1) (param i32 i32) (result i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 127
        i32.gt_u
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 0
          i32.load offset=8
          local.tee 3
          local.get 0
          i32.load offset=4
          i32.ne
          br_if 0 (;@3;)
          local.get 0
          local.get 3
          call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$16reserve_for_push17haff08c7ab95aead1E
          local.get 0
          i32.load offset=8
          local.set 3
        end
        local.get 0
        local.get 3
        i32.const 1
        i32.add
        i32.store offset=8
        local.get 0
        i32.load
        local.get 3
        i32.add
        local.get 1
        i32.store8
        br 1 (;@1;)
      end
      local.get 2
      i32.const 0
      i32.store offset=12
      block  ;; label = @2
        block  ;; label = @3
          local.get 1
          i32.const 2048
          i32.lt_u
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 1
            i32.const 65536
            i32.lt_u
            br_if 0 (;@4;)
            local.get 2
            local.get 1
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=15
            local.get 2
            local.get 1
            i32.const 6
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=14
            local.get 2
            local.get 1
            i32.const 12
            i32.shr_u
            i32.const 63
            i32.and
            i32.const 128
            i32.or
            i32.store8 offset=13
            local.get 2
            local.get 1
            i32.const 18
            i32.shr_u
            i32.const 7
            i32.and
            i32.const 240
            i32.or
            i32.store8 offset=12
            i32.const 4
            local.set 1
            br 2 (;@2;)
          end
          local.get 2
          local.get 1
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=14
          local.get 2
          local.get 1
          i32.const 12
          i32.shr_u
          i32.const 224
          i32.or
          i32.store8 offset=12
          local.get 2
          local.get 1
          i32.const 6
          i32.shr_u
          i32.const 63
          i32.and
          i32.const 128
          i32.or
          i32.store8 offset=13
          i32.const 3
          local.set 1
          br 1 (;@2;)
        end
        local.get 2
        local.get 1
        i32.const 63
        i32.and
        i32.const 128
        i32.or
        i32.store8 offset=13
        local.get 2
        local.get 1
        i32.const 6
        i32.shr_u
        i32.const 192
        i32.or
        i32.store8 offset=12
        i32.const 2
        local.set 1
      end
      block  ;; label = @2
        local.get 0
        i32.load offset=4
        local.get 0
        i32.load offset=8
        local.tee 3
        i32.sub
        local.get 1
        i32.ge_u
        br_if 0 (;@2;)
        local.get 0
        local.get 3
        local.get 1
        call $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$7reserve21do_reserve_and_handle17h2174b82f11d991afE
        local.get 0
        i32.load offset=8
        local.set 3
      end
      local.get 0
      i32.load
      local.get 3
      i32.add
      local.get 2
      i32.const 12
      i32.add
      local.get 1
      call $memcpy
      drop
      local.get 0
      local.get 3
      local.get 1
      i32.add
      i32.store offset=8
    end
    local.get 2
    i32.const 16
    i32.add
    global.set $__stack_pointer
    i32.const 0)
  (func $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17h74d01cc6236fab0bE (type 1) (param i32 i32) (result i32)
    (local i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load
    local.set 0
    local.get 2
    i32.const 8
    i32.add
    i32.const 16
    i32.add
    local.get 1
    i32.const 16
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    i32.const 8
    i32.add
    i32.const 8
    i32.add
    local.get 1
    i32.const 8
    i32.add
    i64.load align=4
    i64.store
    local.get 2
    local.get 1
    i64.load align=4
    i64.store offset=8
    local.get 2
    local.get 0
    i32.store offset=4
    local.get 2
    i32.const 4
    i32.add
    i32.const 1054116
    local.get 2
    i32.const 8
    i32.add
    call $_ZN4core3fmt5write17h8253e306f6bd0e19E
    local.set 1
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN36_$LT$T$u20$as$u20$core..any..Any$GT$7type_id17h27298964b5ba96aaE (type 6) (param i32) (result i64)
    i64.const 1720412530605818077)
  (func $_ZN93_$LT$std..panicking..begin_panic_handler..StrPanicPayload$u20$as$u20$core..panic..BoxMeUp$GT$8take_box17hc0dcc5abb65c5495E (type 7) (param i32) (result i32 i32)
    (local i32 i32)
    i32.const 0
    i32.load8_u offset=1059320
    drop
    local.get 0
    i32.load offset=4
    local.set 1
    local.get 0
    i32.load
    local.set 2
    block  ;; label = @1
      i32.const 8
      call $malloc
      local.tee 0
      br_if 0 (;@1;)
      i32.const 4
      i32.const 8
      call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
      unreachable
    end
    local.get 0
    local.get 1
    i32.store offset=4
    local.get 0
    local.get 2
    i32.store
    local.get 0
    i32.const 1055104)
  (func $_ZN93_$LT$std..panicking..begin_panic_handler..StrPanicPayload$u20$as$u20$core..panic..BoxMeUp$GT$3get17hadfa6298e70556caE (type 7) (param i32) (result i32 i32)
    local.get 0
    i32.const 1055104)
  (func $_ZN36_$LT$T$u20$as$u20$core..any..Any$GT$7type_id17ha906ab4a92d8e02fE (type 6) (param i32) (result i64)
    i64.const -4493808902380553279)
  (func $_ZN3std5alloc8rust_oom17hb6ef0decd08a2b9fE (type 3) (param i32 i32)
    local.get 0
    local.get 1
    call $_ZN3std5alloc24default_alloc_error_hook17h1f56ab869b311cf1E
    call $_ZN3std7process5abort17hef6a1f4cde1d025cE
    unreachable)
  (func $_ZN5alloc7raw_vec19RawVec$LT$T$C$A$GT$16reserve_for_push17h0a6f59455e94d109E (type 3) (param i32 i32)
    (local i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        local.get 1
        i32.const 1
        i32.add
        local.tee 1
        i32.eqz
        br_if 0 (;@2;)
        local.get 0
        i32.load offset=4
        local.tee 3
        i32.const 1
        i32.shl
        local.tee 4
        local.get 1
        local.get 4
        local.get 1
        i32.gt_u
        select
        local.tee 1
        i32.const 4
        local.get 1
        i32.const 4
        i32.gt_u
        select
        local.tee 1
        i32.const 20
        i32.mul
        local.set 4
        local.get 1
        i32.const 107374183
        i32.lt_u
        i32.const 2
        i32.shl
        local.set 5
        block  ;; label = @3
          block  ;; label = @4
            local.get 3
            i32.eqz
            br_if 0 (;@4;)
            local.get 2
            i32.const 4
            i32.store offset=20
            local.get 2
            local.get 3
            i32.const 20
            i32.mul
            i32.store offset=24
            local.get 2
            local.get 0
            i32.load
            i32.store offset=16
            br 1 (;@3;)
          end
          local.get 2
          i32.const 0
          i32.store offset=20
        end
        local.get 2
        local.get 5
        local.get 4
        local.get 2
        i32.const 16
        i32.add
        call $_ZN5alloc7raw_vec11finish_grow17h4de5cd6636d1bdb9E
        local.get 2
        i32.load offset=4
        local.set 3
        block  ;; label = @3
          local.get 2
          i32.load
          br_if 0 (;@3;)
          local.get 0
          local.get 1
          i32.store offset=4
          local.get 0
          local.get 3
          i32.store
          br 2 (;@1;)
        end
        local.get 3
        i32.const -2147483647
        i32.eq
        br_if 1 (;@1;)
        local.get 3
        i32.eqz
        br_if 0 (;@2;)
        local.get 3
        local.get 2
        i32.const 8
        i32.add
        i32.load
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
      unreachable
    end
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer)
  (func $register_crossma (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i64 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            local.get 0
            local.get 1
            local.get 0
            local.get 1
            i32.gt_u
            select
            local.tee 3
            i32.const 55
            local.get 3
            i32.const 55
            i32.gt_u
            select
            local.tee 4
            i32.const 107374182
            i32.gt_u
            br_if 0 (;@4;)
            local.get 4
            i32.const 20
            i32.mul
            local.tee 3
            i32.const -1
            i32.le_s
            br_if 0 (;@4;)
            local.get 4
            i32.const 107374183
            i32.lt_u
            i32.const 2
            i32.shl
            local.set 5
            block  ;; label = @5
              block  ;; label = @6
                local.get 3
                br_if 0 (;@6;)
                local.get 5
                local.set 6
                br 1 (;@5;)
              end
              i32.const 0
              i32.load8_u offset=1059320
              drop
              local.get 3
              local.get 5
              call $__rust_alloc
              local.set 6
            end
            local.get 6
            i32.eqz
            br_if 1 (;@3;)
            i32.const 0
            i32.load8_u offset=1059320
            drop
            i32.const 28
            call $malloc
            local.tee 3
            i32.eqz
            br_if 2 (;@2;)
            local.get 3
            local.get 4
            i32.store offset=24
            local.get 3
            local.get 1
            i32.store offset=20
            local.get 3
            local.get 0
            i32.store offset=16
            local.get 3
            i64.const 0
            i64.store offset=8 align=4
            local.get 3
            local.get 4
            i32.store offset=4
            local.get 3
            local.get 6
            i32.store
            block  ;; label = @5
              i32.const 0
              i32.load offset=1059232
              i32.const 2
              i32.eq
              br_if 0 (;@5;)
              local.get 2
              i32.const 1059216
              i32.store
              local.get 2
              i32.const 1059216
              i32.store offset=4
              local.get 2
              local.get 2
              i32.const 24
              i32.add
              i32.store offset=16
              local.get 2
              local.get 2
              i32.const 4
              i32.add
              i32.store offset=12
              local.get 2
              local.get 2
              i32.store offset=8
              i32.const 1059232
              local.get 2
              i32.const 8
              i32.add
              i32.const 1049004
              call $_ZN9once_cell3imp18initialize_or_wait17h555185a2b5de84ceE
            end
            i32.const 1059220
            call $_ZN3std3sys4wasi5locks6rwlock6RwLock5write17hbe82db7de699f57cE
            i32.const 1059224
            call $_ZN3std4sync6poison4Flag5guard17h8f6284c0743aa497E
            local.set 6
            i32.const 1
            i32.and
            br_if 3 (;@1;)
            i32.const 0
            i32.const 0
            i32.load offset=1059228
            i32.const 1
            i32.add
            local.tee 1
            i32.store offset=1059228
            local.get 2
            i32.const 8
            i32.add
            call $_ZN78_$LT$once_cell..sync..Lazy$LT$T$C$F$GT$$u20$as$u20$core..ops..deref..Deref$GT$5deref17h0320017a3b91974eE
            call $_ZN3std4sync6rwlock15RwLock$LT$T$GT$5write17h55db55ec8afe36b5E
            local.get 2
            i32.const 8
            i32.add
            i32.const 1049416
            call $_ZN4core6result19Result$LT$T$C$E$GT$6unwrap17h14230750cec305d5E
            local.set 5
            local.set 4
            local.get 2
            local.get 1
            i32.store offset=8
            block  ;; label = @5
              block  ;; label = @6
                local.get 4
                i32.const 8
                i32.add
                local.tee 7
                local.get 4
                i32.const 24
                i32.add
                local.tee 8
                i64.load
                local.get 4
                i32.const 32
                i32.add
                i64.load
                local.get 1
                call $_ZN4core4hash11BuildHasher8hash_one17haaa56a5ededbb8abE
                local.tee 9
                local.get 2
                i32.const 8
                i32.add
                call $_ZN9hashbrown3raw21RawTable$LT$T$C$A$GT$7get_mut17hd6b26100c674bb12E
                local.tee 0
                i32.eqz
                br_if 0 (;@6;)
                local.get 0
                i32.load offset=4
                local.set 7
                local.get 0
                local.get 3
                i32.store offset=4
                local.get 0
                i32.const 8
                i32.add
                local.tee 3
                i32.load
                local.set 0
                br 1 (;@5;)
              end
              local.get 7
              i32.load
              local.set 0
              local.get 0
              local.get 0
              local.get 4
              i32.const 12
              i32.add
              i32.load
              local.tee 10
              local.get 9
              call $_ZN9hashbrown3raw22RawTableInner$LT$A$GT$16find_insert_slot17hebb2e2228b09aef2E
              local.tee 11
              i32.add
              i32.load8_u
              i32.const 1
              i32.and
              local.set 12
              block  ;; label = @6
                local.get 4
                i32.const 16
                i32.add
                i32.load
                local.tee 13
                br_if 0 (;@6;)
                local.get 12
                i32.eqz
                br_if 0 (;@6;)
                local.get 7
                local.get 8
                call $_ZN9hashbrown3raw21RawTable$LT$T$C$A$GT$14reserve_rehash17h3de690f35e59502cE
                drop
                local.get 4
                i32.load offset=8
                local.tee 0
                local.get 4
                i32.const 12
                i32.add
                i32.load
                local.tee 10
                local.get 9
                call $_ZN9hashbrown3raw22RawTableInner$LT$A$GT$16find_insert_slot17hebb2e2228b09aef2E
                local.set 11
                local.get 4
                i32.load offset=16
                local.set 13
              end
              local.get 0
              local.get 11
              i32.add
              local.get 9
              i32.wrap_i64
              i32.const 25
              i32.shr_u
              local.tee 7
              i32.store8
              local.get 10
              local.get 11
              i32.const -8
              i32.add
              i32.and
              local.get 0
              i32.add
              i32.const 8
              i32.add
              local.get 7
              i32.store8
              local.get 4
              local.get 13
              local.get 12
              i32.sub
              i32.store offset=16
              local.get 4
              i32.const 20
              i32.add
              local.tee 7
              local.get 7
              i32.load
              i32.const 1
              i32.add
              i32.store
              i32.const 0
              local.set 7
              local.get 0
              i32.const 0
              local.get 11
              i32.sub
              i32.const 12
              i32.mul
              i32.add
              local.tee 0
              i32.const -12
              i32.add
              local.tee 11
              local.get 1
              i32.store
              local.get 11
              local.get 3
              i32.store offset=4
              local.get 0
              i32.const -4
              i32.add
              local.set 3
            end
            local.get 3
            i32.const 1055640
            i32.store
            local.get 7
            local.get 0
            call $_ZN4core3ptr159drop_in_place$LT$core..option..Option$LT$alloc..boxed..Box$LT$dyn$u20$base..strategy..TradingStrategy$u2b$core..marker..Sync$u2b$core..marker..Send$GT$$GT$$GT$17ha9b7ed211c79f172E
            local.get 4
            local.get 5
            call $_ZN86_$LT$std..sync..rwlock..RwLockWriteGuard$LT$T$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h0c6c9fd4b72761f4E
            i32.const 1059220
            local.get 6
            i32.const 1
            i32.and
            call $_ZN86_$LT$std..sync..rwlock..RwLockWriteGuard$LT$T$GT$$u20$as$u20$core..ops..drop..Drop$GT$4drop17h0c6c9fd4b72761f4E
            local.get 2
            i32.const 32
            i32.add
            global.set $__stack_pointer
            local.get 1
            return
          end
          call $_ZN5alloc7raw_vec17capacity_overflow17hea43c759a13a8accE
          unreachable
        end
        local.get 5
        local.get 3
        call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
        unreachable
      end
      i32.const 4
      i32.const 28
      call $_ZN5alloc5alloc18handle_alloc_error17h6af4fa8aec2dc383E
      unreachable
    end
    local.get 2
    i32.const 1059220
    i32.store offset=8
    local.get 2
    local.get 6
    i32.const 1
    i32.and
    i32.store8 offset=12
    i32.const 1049264
    i32.const 43
    local.get 2
    i32.const 8
    i32.add
    i32.const 1049324
    i32.const 1049400
    call $_ZN4core6result13unwrap_failed17hfefb3e75b68d8f8cE
    unreachable)
  (func $_ZN4core3ptr96drop_in_place$LT$base..strategy..BaseStrategy$LT$trend_follow..cross_ma..CrossMAStrategy$GT$$GT$17h48bb8f367846860fE (type 2) (param i32)
    block  ;; label = @1
      local.get 0
      i32.const 4
      i32.add
      i32.load
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      i32.load
      call $free
    end)
  (func $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17h5e15663af5b05b89E (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i64 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 0
    i32.load offset=4
    local.set 3
    local.get 0
    i32.load
    local.set 4
    i32.const 1
    local.set 5
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 1
          i32.load offset=20
          local.tee 6
          i32.const 34
          local.get 1
          i32.const 24
          i32.add
          i32.load
          local.tee 7
          i32.load offset=16
          local.tee 8
          call_indirect (type 1)
          br_if 0 (;@3;)
          block  ;; label = @4
            block  ;; label = @5
              local.get 3
              br_if 0 (;@5;)
              i32.const 0
              local.set 1
              i32.const 0
              local.set 3
              br 1 (;@4;)
            end
            local.get 4
            local.get 3
            i32.add
            local.set 9
            i32.const 0
            local.set 1
            local.get 4
            local.set 10
            i32.const 0
            local.set 11
            block  ;; label = @5
              loop  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    local.get 10
                    local.tee 12
                    i32.load8_s
                    local.tee 0
                    i32.const -1
                    i32.le_s
                    br_if 0 (;@8;)
                    local.get 12
                    i32.const 1
                    i32.add
                    local.set 10
                    local.get 0
                    i32.const 255
                    i32.and
                    local.set 13
                    br 1 (;@7;)
                  end
                  local.get 12
                  i32.load8_u offset=1
                  i32.const 63
                  i32.and
                  local.set 14
                  local.get 0
                  i32.const 31
                  i32.and
                  local.set 15
                  block  ;; label = @8
                    local.get 0
                    i32.const -33
                    i32.gt_u
                    br_if 0 (;@8;)
                    local.get 15
                    i32.const 6
                    i32.shl
                    local.get 14
                    i32.or
                    local.set 13
                    local.get 12
                    i32.const 2
                    i32.add
                    local.set 10
                    br 1 (;@7;)
                  end
                  local.get 14
                  i32.const 6
                  i32.shl
                  local.get 12
                  i32.load8_u offset=2
                  i32.const 63
                  i32.and
                  i32.or
                  local.set 14
                  local.get 12
                  i32.const 3
                  i32.add
                  local.set 10
                  block  ;; label = @8
                    local.get 0
                    i32.const -16
                    i32.ge_u
                    br_if 0 (;@8;)
                    local.get 14
                    local.get 15
                    i32.const 12
                    i32.shl
                    i32.or
                    local.set 13
                    br 1 (;@7;)
                  end
                  local.get 14
                  i32.const 6
                  i32.shl
                  local.get 10
                  i32.load8_u
                  i32.const 63
                  i32.and
                  i32.or
                  local.get 15
                  i32.const 18
                  i32.shl
                  i32.const 1835008
                  i32.and
                  i32.or
                  local.tee 13
                  i32.const 1114112
                  i32.eq
                  br_if 2 (;@5;)
                  local.get 12
                  i32.const 4
                  i32.add
                  local.set 10
                end
                local.get 2
                local.get 13
                i32.const 65537
                call $_ZN4core4char7methods22_$LT$impl$u20$char$GT$16escape_debug_ext17h35ef25b93b9973daE
                block  ;; label = @7
                  block  ;; label = @8
                    local.get 2
                    i32.load8_u
                    i32.const 128
                    i32.eq
                    br_if 0 (;@8;)
                    local.get 2
                    i32.load8_u offset=11
                    local.get 2
                    i32.load8_u offset=10
                    i32.sub
                    i32.const 255
                    i32.and
                    i32.const 1
                    i32.eq
                    br_if 0 (;@8;)
                    local.get 11
                    local.get 1
                    i32.lt_u
                    br_if 7 (;@1;)
                    block  ;; label = @9
                      local.get 1
                      i32.eqz
                      br_if 0 (;@9;)
                      block  ;; label = @10
                        local.get 1
                        local.get 3
                        i32.lt_u
                        br_if 0 (;@10;)
                        local.get 1
                        local.get 3
                        i32.eq
                        br_if 1 (;@9;)
                        br 9 (;@1;)
                      end
                      local.get 4
                      local.get 1
                      i32.add
                      i32.load8_s
                      i32.const -64
                      i32.lt_s
                      br_if 8 (;@1;)
                    end
                    block  ;; label = @9
                      local.get 11
                      i32.eqz
                      br_if 0 (;@9;)
                      block  ;; label = @10
                        local.get 11
                        local.get 3
                        i32.lt_u
                        br_if 0 (;@10;)
                        local.get 11
                        local.get 3
                        i32.ne
                        br_if 9 (;@1;)
                        br 1 (;@9;)
                      end
                      local.get 4
                      local.get 11
                      i32.add
                      i32.load8_s
                      i32.const -65
                      i32.le_s
                      br_if 8 (;@1;)
                    end
                    block  ;; label = @9
                      block  ;; label = @10
                        local.get 6
                        local.get 4
                        local.get 1
                        i32.add
                        local.get 11
                        local.get 1
                        i32.sub
                        local.get 7
                        i32.load offset=12
                        call_indirect (type 0)
                        br_if 0 (;@10;)
                        local.get 2
                        i32.const 16
                        i32.add
                        i32.const 8
                        i32.add
                        local.tee 15
                        local.get 2
                        i32.const 8
                        i32.add
                        i32.load
                        i32.store
                        local.get 2
                        local.get 2
                        i64.load
                        local.tee 16
                        i64.store offset=16
                        block  ;; label = @11
                          local.get 16
                          i32.wrap_i64
                          i32.const 255
                          i32.and
                          i32.const 128
                          i32.ne
                          br_if 0 (;@11;)
                          i32.const 128
                          local.set 14
                          loop  ;; label = @12
                            block  ;; label = @13
                              block  ;; label = @14
                                local.get 14
                                i32.const 255
                                i32.and
                                i32.const 128
                                i32.eq
                                br_if 0 (;@14;)
                                local.get 2
                                i32.load8_u offset=26
                                local.tee 0
                                local.get 2
                                i32.load8_u offset=27
                                i32.ge_u
                                br_if 5 (;@9;)
                                local.get 2
                                local.get 0
                                i32.const 1
                                i32.add
                                i32.store8 offset=26
                                local.get 0
                                i32.const 10
                                i32.ge_u
                                br_if 7 (;@7;)
                                local.get 2
                                i32.const 16
                                i32.add
                                local.get 0
                                i32.add
                                i32.load8_u
                                local.set 1
                                br 1 (;@13;)
                              end
                              i32.const 0
                              local.set 14
                              local.get 15
                              i32.const 0
                              i32.store
                              local.get 2
                              i32.load offset=20
                              local.set 1
                              local.get 2
                              i64.const 0
                              i64.store offset=16
                            end
                            local.get 6
                            local.get 1
                            local.get 8
                            call_indirect (type 1)
                            i32.eqz
                            br_if 0 (;@12;)
                            br 2 (;@10;)
                          end
                        end
                        local.get 2
                        i32.load8_u offset=26
                        local.tee 1
                        i32.const 10
                        local.get 1
                        i32.const 10
                        i32.gt_u
                        select
                        local.set 0
                        local.get 2
                        i32.load8_u offset=27
                        local.tee 14
                        local.get 1
                        local.get 14
                        local.get 1
                        i32.gt_u
                        select
                        local.set 17
                        loop  ;; label = @11
                          local.get 17
                          local.get 1
                          i32.eq
                          br_if 2 (;@9;)
                          local.get 2
                          local.get 1
                          i32.const 1
                          i32.add
                          local.tee 14
                          i32.store8 offset=26
                          local.get 0
                          local.get 1
                          i32.eq
                          br_if 4 (;@7;)
                          local.get 2
                          i32.const 16
                          i32.add
                          local.get 1
                          i32.add
                          local.set 15
                          local.get 14
                          local.set 1
                          local.get 6
                          local.get 15
                          i32.load8_u
                          local.get 8
                          call_indirect (type 1)
                          i32.eqz
                          br_if 0 (;@11;)
                        end
                      end
                      i32.const 1
                      local.set 5
                      br 6 (;@3;)
                    end
                    i32.const 1
                    local.set 1
                    block  ;; label = @9
                      local.get 13
                      i32.const 128
                      i32.lt_u
                      br_if 0 (;@9;)
                      i32.const 2
                      local.set 1
                      local.get 13
                      i32.const 2047
                      i32.le_u
                      br_if 0 (;@9;)
                      i32.const 3
                      i32.const 4
                      local.get 13
                      i32.const 65536
                      i32.lt_u
                      select
                      local.set 1
                    end
                    local.get 1
                    local.get 11
                    i32.add
                    local.set 1
                  end
                  local.get 11
                  local.get 12
                  i32.sub
                  local.get 10
                  i32.add
                  local.set 11
                  local.get 10
                  local.get 9
                  i32.ne
                  br_if 1 (;@6;)
                  br 2 (;@5;)
                end
              end
              local.get 0
              i32.const 10
              i32.const 1052476
              call $_ZN4core9panicking18panic_bounds_check17h7eef07023fe9cc87E
              unreachable
            end
            block  ;; label = @5
              local.get 1
              br_if 0 (;@5;)
              i32.const 0
              local.set 1
              br 1 (;@4;)
            end
            block  ;; label = @5
              local.get 3
              local.get 1
              i32.gt_u
              br_if 0 (;@5;)
              local.get 3
              local.get 1
              i32.ne
              br_if 3 (;@2;)
              local.get 3
              local.get 1
              i32.sub
              local.set 0
              local.get 3
              local.set 1
              local.get 0
              local.set 3
              br 1 (;@4;)
            end
            local.get 4
            local.get 1
            i32.add
            i32.load8_s
            i32.const -65
            i32.le_s
            br_if 2 (;@2;)
            local.get 3
            local.get 1
            i32.sub
            local.set 3
          end
          local.get 6
          local.get 4
          local.get 1
          i32.add
          local.get 3
          local.get 7
          i32.load offset=12
          call_indirect (type 0)
          br_if 0 (;@3;)
          local.get 6
          i32.const 34
          local.get 8
          call_indirect (type 1)
          local.set 5
        end
        local.get 2
        i32.const 32
        i32.add
        global.set $__stack_pointer
        local.get 5
        return
      end
      local.get 4
      local.get 3
      local.get 1
      local.get 3
      i32.const 1050460
      call $_ZN4core3str16slice_error_fail17h9100964d4f03db1dE
      unreachable
    end
    local.get 4
    local.get 3
    local.get 1
    local.get 11
    i32.const 1050444
    call $_ZN4core3str16slice_error_fail17h9100964d4f03db1dE
    unreachable)
  (func $_ZN63_$LT$wasi..lib_generated..Errno$u20$as$u20$core..fmt..Debug$GT$3fmt17h6aa6cc5efc0069feE (type 1) (param i32 i32) (result i32)
    (local i32 i32)
    global.get $__stack_pointer
    i32.const 32
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    local.get 1
    i32.load offset=20
    i32.const 1057905
    i32.const 5
    local.get 1
    i32.const 24
    i32.add
    i32.load
    i32.load offset=12
    call_indirect (type 0)
    local.set 3
    local.get 2
    i32.const 0
    i32.store8 offset=13
    local.get 2
    local.get 3
    i32.store8 offset=12
    local.get 2
    local.get 1
    i32.store offset=8
    local.get 2
    i32.const 8
    i32.add
    i32.const 1055660
    i32.const 4
    local.get 0
    i32.const 14
    call $_ZN4core3fmt8builders11DebugStruct5field17h52a4d0d1d2d279aeE
    local.set 3
    local.get 2
    local.get 0
    i32.load16_s
    i32.const 2
    i32.shl
    local.tee 1
    i32.const 1057912
    i32.add
    i32.load
    i32.store offset=20
    local.get 2
    local.get 1
    i32.const 1058220
    i32.add
    i32.load
    i32.store offset=16
    local.get 1
    i32.const 1058528
    i32.add
    i32.load
    local.set 0
    local.get 3
    i32.const 1055664
    i32.const 4
    local.get 2
    i32.const 16
    i32.add
    i32.const 15
    call $_ZN4core3fmt8builders11DebugStruct5field17h52a4d0d1d2d279aeE
    local.set 3
    local.get 2
    local.get 0
    i32.store offset=28
    local.get 2
    local.get 1
    i32.const 1058836
    i32.add
    i32.load
    i32.store offset=24
    local.get 3
    i32.const 1055668
    i32.const 7
    local.get 2
    i32.const 24
    i32.add
    i32.const 15
    call $_ZN4core3fmt8builders11DebugStruct5field17h52a4d0d1d2d279aeE
    call $_ZN4core3fmt8builders11DebugStruct6finish17h24c6b68ba16e2ce0E
    local.set 1
    local.get 2
    i32.const 32
    i32.add
    global.set $__stack_pointer
    local.get 1)
  (func $_ZN4core3fmt3num50_$LT$impl$u20$core..fmt..Debug$u20$for$u20$u16$GT$3fmt17h860941a58acd0572E.524 (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 128
    i32.sub
    local.tee 2
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              local.get 1
              i32.load offset=28
              local.tee 3
              i32.const 16
              i32.and
              br_if 0 (;@5;)
              local.get 3
              i32.const 32
              i32.and
              br_if 1 (;@4;)
              local.get 0
              i64.load16_u
              i32.const 1
              local.get 1
              call $_ZN4core3fmt3num3imp7fmt_u6417ha30186d55e58ac6fE
              local.set 0
              br 4 (;@1;)
            end
            local.get 0
            i32.load16_u
            local.set 3
            i32.const 0
            local.set 0
            loop  ;; label = @5
              local.get 2
              local.get 0
              i32.add
              i32.const 127
              i32.add
              i32.const 48
              i32.const 87
              local.get 3
              i32.const 15
              i32.and
              local.tee 4
              i32.const 10
              i32.lt_u
              select
              local.get 4
              i32.add
              i32.store8
              local.get 0
              i32.const -1
              i32.add
              local.set 0
              local.get 3
              i32.const 65535
              i32.and
              local.tee 4
              i32.const 4
              i32.shr_u
              local.set 3
              local.get 4
              i32.const 15
              i32.gt_u
              br_if 0 (;@5;)
            end
            local.get 0
            i32.const 128
            i32.add
            local.tee 3
            i32.const 129
            i32.ge_u
            br_if 1 (;@3;)
            local.get 1
            i32.const 1
            i32.const 1050204
            i32.const 2
            local.get 2
            local.get 0
            i32.add
            i32.const 128
            i32.add
            i32.const 0
            local.get 0
            i32.sub
            call $_ZN4core3fmt9Formatter12pad_integral17h840ce31caaa4dc56E
            local.set 0
            br 3 (;@1;)
          end
          local.get 0
          i32.load16_u
          local.set 3
          i32.const 0
          local.set 0
          loop  ;; label = @4
            local.get 2
            local.get 0
            i32.add
            i32.const 127
            i32.add
            i32.const 48
            i32.const 55
            local.get 3
            i32.const 15
            i32.and
            local.tee 4
            i32.const 10
            i32.lt_u
            select
            local.get 4
            i32.add
            i32.store8
            local.get 0
            i32.const -1
            i32.add
            local.set 0
            local.get 3
            i32.const 65535
            i32.and
            local.tee 4
            i32.const 4
            i32.shr_u
            local.set 3
            local.get 4
            i32.const 15
            i32.gt_u
            br_if 0 (;@4;)
          end
          local.get 0
          i32.const 128
          i32.add
          local.tee 3
          i32.const 129
          i32.ge_u
          br_if 1 (;@2;)
          local.get 1
          i32.const 1
          i32.const 1050204
          i32.const 2
          local.get 2
          local.get 0
          i32.add
          i32.const 128
          i32.add
          i32.const 0
          local.get 0
          i32.sub
          call $_ZN4core3fmt9Formatter12pad_integral17h840ce31caaa4dc56E
          local.set 0
          br 2 (;@1;)
        end
        local.get 3
        i32.const 128
        i32.const 1050188
        call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
        unreachable
      end
      local.get 3
      i32.const 128
      i32.const 1050188
      call $_ZN4core5slice5index26slice_start_index_len_fail17h15c06d86cc517bbdE
      unreachable
    end
    local.get 2
    i32.const 128
    i32.add
    global.set $__stack_pointer
    local.get 0)
  (func $malloc (type 5) (param i32) (result i32)
    local.get 0
    call $dlmalloc)
  (func $dlmalloc (type 5) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 1
    global.set $__stack_pointer
    block  ;; label = @1
      i32.const 0
      i32.load offset=1059348
      local.tee 2
      br_if 0 (;@1;)
      block  ;; label = @2
        block  ;; label = @3
          i32.const 0
          i32.load offset=1059796
          local.tee 3
          i32.eqz
          br_if 0 (;@3;)
          i32.const 0
          i32.load offset=1059800
          local.set 4
          br 1 (;@2;)
        end
        i32.const 0
        i64.const -1
        i64.store offset=1059808 align=4
        i32.const 0
        i64.const 281474976776192
        i64.store offset=1059800 align=4
        i32.const 0
        local.get 1
        i32.const 8
        i32.add
        i32.const -16
        i32.and
        i32.const 1431655768
        i32.xor
        local.tee 3
        i32.store offset=1059796
        i32.const 0
        i32.const 0
        i32.store offset=1059816
        i32.const 0
        i32.const 0
        i32.store offset=1059768
        i32.const 65536
        local.set 4
      end
      i32.const 0
      local.set 2
      i32.const 1114112
      i32.const 1059840
      local.get 4
      i32.add
      i32.const -1
      i32.add
      i32.const 0
      local.get 4
      i32.sub
      i32.and
      i32.const 1114112
      select
      i32.const 1059840
      i32.sub
      local.tee 5
      i32.const 89
      i32.lt_u
      br_if 0 (;@1;)
      i32.const 0
      local.set 4
      i32.const 0
      local.get 5
      i32.store offset=1059776
      i32.const 0
      i32.const 1059840
      i32.store offset=1059772
      i32.const 0
      i32.const 1059840
      i32.store offset=1059340
      i32.const 0
      local.get 3
      i32.store offset=1059360
      i32.const 0
      i32.const -1
      i32.store offset=1059356
      loop  ;; label = @2
        local.get 4
        i32.const 1059384
        i32.add
        local.get 4
        i32.const 1059372
        i32.add
        local.tee 3
        i32.store
        local.get 3
        local.get 4
        i32.const 1059364
        i32.add
        local.tee 6
        i32.store
        local.get 4
        i32.const 1059376
        i32.add
        local.get 6
        i32.store
        local.get 4
        i32.const 1059392
        i32.add
        local.get 4
        i32.const 1059380
        i32.add
        local.tee 6
        i32.store
        local.get 6
        local.get 3
        i32.store
        local.get 4
        i32.const 1059400
        i32.add
        local.get 4
        i32.const 1059388
        i32.add
        local.tee 3
        i32.store
        local.get 3
        local.get 6
        i32.store
        local.get 4
        i32.const 1059396
        i32.add
        local.get 3
        i32.store
        local.get 4
        i32.const 32
        i32.add
        local.tee 4
        i32.const 256
        i32.ne
        br_if 0 (;@2;)
      end
      i32.const 1059840
      i32.const -8
      i32.const 1059840
      i32.sub
      i32.const 15
      i32.and
      i32.const 0
      i32.const 1059840
      i32.const 8
      i32.add
      i32.const 15
      i32.and
      select
      local.tee 4
      i32.add
      local.tee 2
      i32.const 4
      i32.add
      local.get 5
      i32.const -56
      i32.add
      local.tee 3
      local.get 4
      i32.sub
      local.tee 4
      i32.const 1
      i32.or
      i32.store
      i32.const 0
      i32.const 0
      i32.load offset=1059812
      i32.store offset=1059352
      i32.const 0
      local.get 4
      i32.store offset=1059336
      i32.const 0
      local.get 2
      i32.store offset=1059348
      i32.const 1059840
      local.get 3
      i32.add
      i32.const 56
      i32.store offset=4
    end
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    block  ;; label = @9
                      block  ;; label = @10
                        block  ;; label = @11
                          block  ;; label = @12
                            local.get 0
                            i32.const 236
                            i32.gt_u
                            br_if 0 (;@12;)
                            block  ;; label = @13
                              i32.const 0
                              i32.load offset=1059324
                              local.tee 7
                              i32.const 16
                              local.get 0
                              i32.const 19
                              i32.add
                              i32.const -16
                              i32.and
                              local.get 0
                              i32.const 11
                              i32.lt_u
                              select
                              local.tee 5
                              i32.const 3
                              i32.shr_u
                              local.tee 3
                              i32.shr_u
                              local.tee 4
                              i32.const 3
                              i32.and
                              i32.eqz
                              br_if 0 (;@13;)
                              block  ;; label = @14
                                block  ;; label = @15
                                  local.get 4
                                  i32.const 1
                                  i32.and
                                  local.get 3
                                  i32.or
                                  i32.const 1
                                  i32.xor
                                  local.tee 6
                                  i32.const 3
                                  i32.shl
                                  local.tee 3
                                  i32.const 1059364
                                  i32.add
                                  local.tee 4
                                  local.get 3
                                  i32.const 1059372
                                  i32.add
                                  i32.load
                                  local.tee 3
                                  i32.load offset=8
                                  local.tee 5
                                  i32.ne
                                  br_if 0 (;@15;)
                                  i32.const 0
                                  local.get 7
                                  i32.const -2
                                  local.get 6
                                  i32.rotl
                                  i32.and
                                  i32.store offset=1059324
                                  br 1 (;@14;)
                                end
                                local.get 4
                                local.get 5
                                i32.store offset=8
                                local.get 5
                                local.get 4
                                i32.store offset=12
                              end
                              local.get 3
                              i32.const 8
                              i32.add
                              local.set 4
                              local.get 3
                              local.get 6
                              i32.const 3
                              i32.shl
                              local.tee 6
                              i32.const 3
                              i32.or
                              i32.store offset=4
                              local.get 3
                              local.get 6
                              i32.add
                              local.tee 3
                              local.get 3
                              i32.load offset=4
                              i32.const 1
                              i32.or
                              i32.store offset=4
                              br 12 (;@1;)
                            end
                            local.get 5
                            i32.const 0
                            i32.load offset=1059332
                            local.tee 8
                            i32.le_u
                            br_if 1 (;@11;)
                            block  ;; label = @13
                              local.get 4
                              i32.eqz
                              br_if 0 (;@13;)
                              block  ;; label = @14
                                block  ;; label = @15
                                  local.get 4
                                  local.get 3
                                  i32.shl
                                  i32.const 2
                                  local.get 3
                                  i32.shl
                                  local.tee 4
                                  i32.const 0
                                  local.get 4
                                  i32.sub
                                  i32.or
                                  i32.and
                                  local.tee 4
                                  i32.const 0
                                  local.get 4
                                  i32.sub
                                  i32.and
                                  i32.const -1
                                  i32.add
                                  local.tee 4
                                  local.get 4
                                  i32.const 12
                                  i32.shr_u
                                  i32.const 16
                                  i32.and
                                  local.tee 4
                                  i32.shr_u
                                  local.tee 3
                                  i32.const 5
                                  i32.shr_u
                                  i32.const 8
                                  i32.and
                                  local.tee 6
                                  local.get 4
                                  i32.or
                                  local.get 3
                                  local.get 6
                                  i32.shr_u
                                  local.tee 4
                                  i32.const 2
                                  i32.shr_u
                                  i32.const 4
                                  i32.and
                                  local.tee 3
                                  i32.or
                                  local.get 4
                                  local.get 3
                                  i32.shr_u
                                  local.tee 4
                                  i32.const 1
                                  i32.shr_u
                                  i32.const 2
                                  i32.and
                                  local.tee 3
                                  i32.or
                                  local.get 4
                                  local.get 3
                                  i32.shr_u
                                  local.tee 4
                                  i32.const 1
                                  i32.shr_u
                                  i32.const 1
                                  i32.and
                                  local.tee 3
                                  i32.or
                                  local.get 4
                                  local.get 3
                                  i32.shr_u
                                  i32.add
                                  local.tee 3
                                  i32.const 3
                                  i32.shl
                                  local.tee 4
                                  i32.const 1059364
                                  i32.add
                                  local.tee 6
                                  local.get 4
                                  i32.const 1059372
                                  i32.add
                                  i32.load
                                  local.tee 4
                                  i32.load offset=8
                                  local.tee 0
                                  i32.ne
                                  br_if 0 (;@15;)
                                  i32.const 0
                                  local.get 7
                                  i32.const -2
                                  local.get 3
                                  i32.rotl
                                  i32.and
                                  local.tee 7
                                  i32.store offset=1059324
                                  br 1 (;@14;)
                                end
                                local.get 6
                                local.get 0
                                i32.store offset=8
                                local.get 0
                                local.get 6
                                i32.store offset=12
                              end
                              local.get 4
                              local.get 5
                              i32.const 3
                              i32.or
                              i32.store offset=4
                              local.get 4
                              local.get 3
                              i32.const 3
                              i32.shl
                              local.tee 3
                              i32.add
                              local.get 3
                              local.get 5
                              i32.sub
                              local.tee 6
                              i32.store
                              local.get 4
                              local.get 5
                              i32.add
                              local.tee 0
                              local.get 6
                              i32.const 1
                              i32.or
                              i32.store offset=4
                              block  ;; label = @14
                                local.get 8
                                i32.eqz
                                br_if 0 (;@14;)
                                local.get 8
                                i32.const -8
                                i32.and
                                i32.const 1059364
                                i32.add
                                local.set 5
                                i32.const 0
                                i32.load offset=1059344
                                local.set 3
                                block  ;; label = @15
                                  block  ;; label = @16
                                    local.get 7
                                    i32.const 1
                                    local.get 8
                                    i32.const 3
                                    i32.shr_u
                                    i32.shl
                                    local.tee 9
                                    i32.and
                                    br_if 0 (;@16;)
                                    i32.const 0
                                    local.get 7
                                    local.get 9
                                    i32.or
                                    i32.store offset=1059324
                                    local.get 5
                                    local.set 9
                                    br 1 (;@15;)
                                  end
                                  local.get 5
                                  i32.load offset=8
                                  local.set 9
                                end
                                local.get 9
                                local.get 3
                                i32.store offset=12
                                local.get 5
                                local.get 3
                                i32.store offset=8
                                local.get 3
                                local.get 5
                                i32.store offset=12
                                local.get 3
                                local.get 9
                                i32.store offset=8
                              end
                              local.get 4
                              i32.const 8
                              i32.add
                              local.set 4
                              i32.const 0
                              local.get 0
                              i32.store offset=1059344
                              i32.const 0
                              local.get 6
                              i32.store offset=1059332
                              br 12 (;@1;)
                            end
                            i32.const 0
                            i32.load offset=1059328
                            local.tee 10
                            i32.eqz
                            br_if 1 (;@11;)
                            local.get 10
                            i32.const 0
                            local.get 10
                            i32.sub
                            i32.and
                            i32.const -1
                            i32.add
                            local.tee 4
                            local.get 4
                            i32.const 12
                            i32.shr_u
                            i32.const 16
                            i32.and
                            local.tee 4
                            i32.shr_u
                            local.tee 3
                            i32.const 5
                            i32.shr_u
                            i32.const 8
                            i32.and
                            local.tee 6
                            local.get 4
                            i32.or
                            local.get 3
                            local.get 6
                            i32.shr_u
                            local.tee 4
                            i32.const 2
                            i32.shr_u
                            i32.const 4
                            i32.and
                            local.tee 3
                            i32.or
                            local.get 4
                            local.get 3
                            i32.shr_u
                            local.tee 4
                            i32.const 1
                            i32.shr_u
                            i32.const 2
                            i32.and
                            local.tee 3
                            i32.or
                            local.get 4
                            local.get 3
                            i32.shr_u
                            local.tee 4
                            i32.const 1
                            i32.shr_u
                            i32.const 1
                            i32.and
                            local.tee 3
                            i32.or
                            local.get 4
                            local.get 3
                            i32.shr_u
                            i32.add
                            i32.const 2
                            i32.shl
                            i32.const 1059628
                            i32.add
                            i32.load
                            local.tee 0
                            i32.load offset=4
                            i32.const -8
                            i32.and
                            local.get 5
                            i32.sub
                            local.set 3
                            local.get 0
                            local.set 6
                            block  ;; label = @13
                              loop  ;; label = @14
                                block  ;; label = @15
                                  local.get 6
                                  i32.load offset=16
                                  local.tee 4
                                  br_if 0 (;@15;)
                                  local.get 6
                                  i32.const 20
                                  i32.add
                                  i32.load
                                  local.tee 4
                                  i32.eqz
                                  br_if 2 (;@13;)
                                end
                                local.get 4
                                i32.load offset=4
                                i32.const -8
                                i32.and
                                local.get 5
                                i32.sub
                                local.tee 6
                                local.get 3
                                local.get 6
                                local.get 3
                                i32.lt_u
                                local.tee 6
                                select
                                local.set 3
                                local.get 4
                                local.get 0
                                local.get 6
                                select
                                local.set 0
                                local.get 4
                                local.set 6
                                br 0 (;@14;)
                              end
                            end
                            local.get 0
                            i32.load offset=24
                            local.set 11
                            block  ;; label = @13
                              local.get 0
                              i32.load offset=12
                              local.tee 9
                              local.get 0
                              i32.eq
                              br_if 0 (;@13;)
                              local.get 0
                              i32.load offset=8
                              local.tee 4
                              i32.const 0
                              i32.load offset=1059340
                              i32.lt_u
                              drop
                              local.get 9
                              local.get 4
                              i32.store offset=8
                              local.get 4
                              local.get 9
                              i32.store offset=12
                              br 11 (;@2;)
                            end
                            block  ;; label = @13
                              local.get 0
                              i32.const 20
                              i32.add
                              local.tee 6
                              i32.load
                              local.tee 4
                              br_if 0 (;@13;)
                              local.get 0
                              i32.load offset=16
                              local.tee 4
                              i32.eqz
                              br_if 3 (;@10;)
                              local.get 0
                              i32.const 16
                              i32.add
                              local.set 6
                            end
                            loop  ;; label = @13
                              local.get 6
                              local.set 2
                              local.get 4
                              local.tee 9
                              i32.const 20
                              i32.add
                              local.tee 6
                              i32.load
                              local.tee 4
                              br_if 0 (;@13;)
                              local.get 9
                              i32.const 16
                              i32.add
                              local.set 6
                              local.get 9
                              i32.load offset=16
                              local.tee 4
                              br_if 0 (;@13;)
                            end
                            local.get 2
                            i32.const 0
                            i32.store
                            br 10 (;@2;)
                          end
                          i32.const -1
                          local.set 5
                          local.get 0
                          i32.const -65
                          i32.gt_u
                          br_if 0 (;@11;)
                          local.get 0
                          i32.const 19
                          i32.add
                          local.tee 4
                          i32.const -16
                          i32.and
                          local.set 5
                          i32.const 0
                          i32.load offset=1059328
                          local.tee 10
                          i32.eqz
                          br_if 0 (;@11;)
                          i32.const 0
                          local.set 8
                          block  ;; label = @12
                            local.get 5
                            i32.const 256
                            i32.lt_u
                            br_if 0 (;@12;)
                            i32.const 31
                            local.set 8
                            local.get 5
                            i32.const 16777215
                            i32.gt_u
                            br_if 0 (;@12;)
                            local.get 4
                            i32.const 8
                            i32.shr_u
                            local.tee 4
                            local.get 4
                            i32.const 1048320
                            i32.add
                            i32.const 16
                            i32.shr_u
                            i32.const 8
                            i32.and
                            local.tee 4
                            i32.shl
                            local.tee 3
                            local.get 3
                            i32.const 520192
                            i32.add
                            i32.const 16
                            i32.shr_u
                            i32.const 4
                            i32.and
                            local.tee 3
                            i32.shl
                            local.tee 6
                            local.get 6
                            i32.const 245760
                            i32.add
                            i32.const 16
                            i32.shr_u
                            i32.const 2
                            i32.and
                            local.tee 6
                            i32.shl
                            i32.const 15
                            i32.shr_u
                            local.get 4
                            local.get 3
                            i32.or
                            local.get 6
                            i32.or
                            i32.sub
                            local.tee 4
                            i32.const 1
                            i32.shl
                            local.get 5
                            local.get 4
                            i32.const 21
                            i32.add
                            i32.shr_u
                            i32.const 1
                            i32.and
                            i32.or
                            i32.const 28
                            i32.add
                            local.set 8
                          end
                          i32.const 0
                          local.get 5
                          i32.sub
                          local.set 3
                          block  ;; label = @12
                            block  ;; label = @13
                              block  ;; label = @14
                                block  ;; label = @15
                                  local.get 8
                                  i32.const 2
                                  i32.shl
                                  i32.const 1059628
                                  i32.add
                                  i32.load
                                  local.tee 6
                                  br_if 0 (;@15;)
                                  i32.const 0
                                  local.set 4
                                  i32.const 0
                                  local.set 9
                                  br 1 (;@14;)
                                end
                                i32.const 0
                                local.set 4
                                local.get 5
                                i32.const 0
                                i32.const 25
                                local.get 8
                                i32.const 1
                                i32.shr_u
                                i32.sub
                                local.get 8
                                i32.const 31
                                i32.eq
                                select
                                i32.shl
                                local.set 0
                                i32.const 0
                                local.set 9
                                loop  ;; label = @15
                                  block  ;; label = @16
                                    local.get 6
                                    i32.load offset=4
                                    i32.const -8
                                    i32.and
                                    local.get 5
                                    i32.sub
                                    local.tee 7
                                    local.get 3
                                    i32.ge_u
                                    br_if 0 (;@16;)
                                    local.get 7
                                    local.set 3
                                    local.get 6
                                    local.set 9
                                    local.get 7
                                    br_if 0 (;@16;)
                                    i32.const 0
                                    local.set 3
                                    local.get 6
                                    local.set 9
                                    local.get 6
                                    local.set 4
                                    br 3 (;@13;)
                                  end
                                  local.get 4
                                  local.get 6
                                  i32.const 20
                                  i32.add
                                  i32.load
                                  local.tee 7
                                  local.get 7
                                  local.get 6
                                  local.get 0
                                  i32.const 29
                                  i32.shr_u
                                  i32.const 4
                                  i32.and
                                  i32.add
                                  i32.const 16
                                  i32.add
                                  i32.load
                                  local.tee 6
                                  i32.eq
                                  select
                                  local.get 4
                                  local.get 7
                                  select
                                  local.set 4
                                  local.get 0
                                  i32.const 1
                                  i32.shl
                                  local.set 0
                                  local.get 6
                                  br_if 0 (;@15;)
                                end
                              end
                              block  ;; label = @14
                                local.get 4
                                local.get 9
                                i32.or
                                br_if 0 (;@14;)
                                i32.const 0
                                local.set 9
                                i32.const 2
                                local.get 8
                                i32.shl
                                local.tee 4
                                i32.const 0
                                local.get 4
                                i32.sub
                                i32.or
                                local.get 10
                                i32.and
                                local.tee 4
                                i32.eqz
                                br_if 3 (;@11;)
                                local.get 4
                                i32.const 0
                                local.get 4
                                i32.sub
                                i32.and
                                i32.const -1
                                i32.add
                                local.tee 4
                                local.get 4
                                i32.const 12
                                i32.shr_u
                                i32.const 16
                                i32.and
                                local.tee 4
                                i32.shr_u
                                local.tee 6
                                i32.const 5
                                i32.shr_u
                                i32.const 8
                                i32.and
                                local.tee 0
                                local.get 4
                                i32.or
                                local.get 6
                                local.get 0
                                i32.shr_u
                                local.tee 4
                                i32.const 2
                                i32.shr_u
                                i32.const 4
                                i32.and
                                local.tee 6
                                i32.or
                                local.get 4
                                local.get 6
                                i32.shr_u
                                local.tee 4
                                i32.const 1
                                i32.shr_u
                                i32.const 2
                                i32.and
                                local.tee 6
                                i32.or
                                local.get 4
                                local.get 6
                                i32.shr_u
                                local.tee 4
                                i32.const 1
                                i32.shr_u
                                i32.const 1
                                i32.and
                                local.tee 6
                                i32.or
                                local.get 4
                                local.get 6
                                i32.shr_u
                                i32.add
                                i32.const 2
                                i32.shl
                                i32.const 1059628
                                i32.add
                                i32.load
                                local.set 4
                              end
                              local.get 4
                              i32.eqz
                              br_if 1 (;@12;)
                            end
                            loop  ;; label = @13
                              local.get 4
                              i32.load offset=4
                              i32.const -8
                              i32.and
                              local.get 5
                              i32.sub
                              local.tee 7
                              local.get 3
                              i32.lt_u
                              local.set 0
                              block  ;; label = @14
                                local.get 4
                                i32.load offset=16
                                local.tee 6
                                br_if 0 (;@14;)
                                local.get 4
                                i32.const 20
                                i32.add
                                i32.load
                                local.set 6
                              end
                              local.get 7
                              local.get 3
                              local.get 0
                              select
                              local.set 3
                              local.get 4
                              local.get 9
                              local.get 0
                              select
                              local.set 9
                              local.get 6
                              local.set 4
                              local.get 6
                              br_if 0 (;@13;)
                            end
                          end
                          local.get 9
                          i32.eqz
                          br_if 0 (;@11;)
                          local.get 3
                          i32.const 0
                          i32.load offset=1059332
                          local.get 5
                          i32.sub
                          i32.ge_u
                          br_if 0 (;@11;)
                          local.get 9
                          i32.load offset=24
                          local.set 2
                          block  ;; label = @12
                            local.get 9
                            i32.load offset=12
                            local.tee 0
                            local.get 9
                            i32.eq
                            br_if 0 (;@12;)
                            local.get 9
                            i32.load offset=8
                            local.tee 4
                            i32.const 0
                            i32.load offset=1059340
                            i32.lt_u
                            drop
                            local.get 0
                            local.get 4
                            i32.store offset=8
                            local.get 4
                            local.get 0
                            i32.store offset=12
                            br 9 (;@3;)
                          end
                          block  ;; label = @12
                            local.get 9
                            i32.const 20
                            i32.add
                            local.tee 6
                            i32.load
                            local.tee 4
                            br_if 0 (;@12;)
                            local.get 9
                            i32.load offset=16
                            local.tee 4
                            i32.eqz
                            br_if 3 (;@9;)
                            local.get 9
                            i32.const 16
                            i32.add
                            local.set 6
                          end
                          loop  ;; label = @12
                            local.get 6
                            local.set 7
                            local.get 4
                            local.tee 0
                            i32.const 20
                            i32.add
                            local.tee 6
                            i32.load
                            local.tee 4
                            br_if 0 (;@12;)
                            local.get 0
                            i32.const 16
                            i32.add
                            local.set 6
                            local.get 0
                            i32.load offset=16
                            local.tee 4
                            br_if 0 (;@12;)
                          end
                          local.get 7
                          i32.const 0
                          i32.store
                          br 8 (;@3;)
                        end
                        block  ;; label = @11
                          i32.const 0
                          i32.load offset=1059332
                          local.tee 4
                          local.get 5
                          i32.lt_u
                          br_if 0 (;@11;)
                          i32.const 0
                          i32.load offset=1059344
                          local.set 3
                          block  ;; label = @12
                            block  ;; label = @13
                              local.get 4
                              local.get 5
                              i32.sub
                              local.tee 6
                              i32.const 16
                              i32.lt_u
                              br_if 0 (;@13;)
                              local.get 3
                              local.get 5
                              i32.add
                              local.tee 0
                              local.get 6
                              i32.const 1
                              i32.or
                              i32.store offset=4
                              i32.const 0
                              local.get 6
                              i32.store offset=1059332
                              i32.const 0
                              local.get 0
                              i32.store offset=1059344
                              local.get 3
                              local.get 4
                              i32.add
                              local.get 6
                              i32.store
                              local.get 3
                              local.get 5
                              i32.const 3
                              i32.or
                              i32.store offset=4
                              br 1 (;@12;)
                            end
                            local.get 3
                            local.get 4
                            i32.const 3
                            i32.or
                            i32.store offset=4
                            local.get 3
                            local.get 4
                            i32.add
                            local.tee 4
                            local.get 4
                            i32.load offset=4
                            i32.const 1
                            i32.or
                            i32.store offset=4
                            i32.const 0
                            i32.const 0
                            i32.store offset=1059344
                            i32.const 0
                            i32.const 0
                            i32.store offset=1059332
                          end
                          local.get 3
                          i32.const 8
                          i32.add
                          local.set 4
                          br 10 (;@1;)
                        end
                        block  ;; label = @11
                          i32.const 0
                          i32.load offset=1059336
                          local.tee 6
                          local.get 5
                          i32.le_u
                          br_if 0 (;@11;)
                          local.get 2
                          local.get 5
                          i32.add
                          local.tee 4
                          local.get 6
                          local.get 5
                          i32.sub
                          local.tee 3
                          i32.const 1
                          i32.or
                          i32.store offset=4
                          i32.const 0
                          local.get 4
                          i32.store offset=1059348
                          i32.const 0
                          local.get 3
                          i32.store offset=1059336
                          local.get 2
                          local.get 5
                          i32.const 3
                          i32.or
                          i32.store offset=4
                          local.get 2
                          i32.const 8
                          i32.add
                          local.set 4
                          br 10 (;@1;)
                        end
                        block  ;; label = @11
                          block  ;; label = @12
                            i32.const 0
                            i32.load offset=1059796
                            i32.eqz
                            br_if 0 (;@12;)
                            i32.const 0
                            i32.load offset=1059804
                            local.set 3
                            br 1 (;@11;)
                          end
                          i32.const 0
                          i64.const -1
                          i64.store offset=1059808 align=4
                          i32.const 0
                          i64.const 281474976776192
                          i64.store offset=1059800 align=4
                          i32.const 0
                          local.get 1
                          i32.const 12
                          i32.add
                          i32.const -16
                          i32.and
                          i32.const 1431655768
                          i32.xor
                          i32.store offset=1059796
                          i32.const 0
                          i32.const 0
                          i32.store offset=1059816
                          i32.const 0
                          i32.const 0
                          i32.store offset=1059768
                          i32.const 65536
                          local.set 3
                        end
                        i32.const 0
                        local.set 4
                        block  ;; label = @11
                          local.get 3
                          local.get 5
                          i32.const 71
                          i32.add
                          local.tee 8
                          i32.add
                          local.tee 0
                          i32.const 0
                          local.get 3
                          i32.sub
                          local.tee 7
                          i32.and
                          local.tee 9
                          local.get 5
                          i32.gt_u
                          br_if 0 (;@11;)
                          i32.const 0
                          i32.const 48
                          i32.store offset=1059820
                          br 10 (;@1;)
                        end
                        block  ;; label = @11
                          i32.const 0
                          i32.load offset=1059764
                          local.tee 4
                          i32.eqz
                          br_if 0 (;@11;)
                          block  ;; label = @12
                            i32.const 0
                            i32.load offset=1059756
                            local.tee 3
                            local.get 9
                            i32.add
                            local.tee 10
                            local.get 3
                            i32.le_u
                            br_if 0 (;@12;)
                            local.get 10
                            local.get 4
                            i32.le_u
                            br_if 1 (;@11;)
                          end
                          i32.const 0
                          local.set 4
                          i32.const 0
                          i32.const 48
                          i32.store offset=1059820
                          br 10 (;@1;)
                        end
                        i32.const 0
                        i32.load8_u offset=1059768
                        i32.const 4
                        i32.and
                        br_if 4 (;@6;)
                        block  ;; label = @11
                          block  ;; label = @12
                            block  ;; label = @13
                              local.get 2
                              i32.eqz
                              br_if 0 (;@13;)
                              i32.const 1059772
                              local.set 4
                              loop  ;; label = @14
                                block  ;; label = @15
                                  local.get 4
                                  i32.load
                                  local.tee 3
                                  local.get 2
                                  i32.gt_u
                                  br_if 0 (;@15;)
                                  local.get 3
                                  local.get 4
                                  i32.load offset=4
                                  i32.add
                                  local.get 2
                                  i32.gt_u
                                  br_if 3 (;@12;)
                                end
                                local.get 4
                                i32.load offset=8
                                local.tee 4
                                br_if 0 (;@14;)
                              end
                            end
                            i32.const 0
                            call $sbrk
                            local.tee 0
                            i32.const -1
                            i32.eq
                            br_if 5 (;@7;)
                            local.get 9
                            local.set 7
                            block  ;; label = @13
                              i32.const 0
                              i32.load offset=1059800
                              local.tee 4
                              i32.const -1
                              i32.add
                              local.tee 3
                              local.get 0
                              i32.and
                              i32.eqz
                              br_if 0 (;@13;)
                              local.get 9
                              local.get 0
                              i32.sub
                              local.get 3
                              local.get 0
                              i32.add
                              i32.const 0
                              local.get 4
                              i32.sub
                              i32.and
                              i32.add
                              local.set 7
                            end
                            local.get 7
                            local.get 5
                            i32.le_u
                            br_if 5 (;@7;)
                            local.get 7
                            i32.const 2147483646
                            i32.gt_u
                            br_if 5 (;@7;)
                            block  ;; label = @13
                              i32.const 0
                              i32.load offset=1059764
                              local.tee 4
                              i32.eqz
                              br_if 0 (;@13;)
                              i32.const 0
                              i32.load offset=1059756
                              local.tee 3
                              local.get 7
                              i32.add
                              local.tee 6
                              local.get 3
                              i32.le_u
                              br_if 6 (;@7;)
                              local.get 6
                              local.get 4
                              i32.gt_u
                              br_if 6 (;@7;)
                            end
                            local.get 7
                            call $sbrk
                            local.tee 4
                            local.get 0
                            i32.ne
                            br_if 1 (;@11;)
                            br 7 (;@5;)
                          end
                          local.get 0
                          local.get 6
                          i32.sub
                          local.get 7
                          i32.and
                          local.tee 7
                          i32.const 2147483646
                          i32.gt_u
                          br_if 4 (;@7;)
                          local.get 7
                          call $sbrk
                          local.tee 0
                          local.get 4
                          i32.load
                          local.get 4
                          i32.load offset=4
                          i32.add
                          i32.eq
                          br_if 3 (;@8;)
                          local.get 0
                          local.set 4
                        end
                        block  ;; label = @11
                          local.get 4
                          i32.const -1
                          i32.eq
                          br_if 0 (;@11;)
                          local.get 5
                          i32.const 72
                          i32.add
                          local.get 7
                          i32.le_u
                          br_if 0 (;@11;)
                          block  ;; label = @12
                            local.get 8
                            local.get 7
                            i32.sub
                            i32.const 0
                            i32.load offset=1059804
                            local.tee 3
                            i32.add
                            i32.const 0
                            local.get 3
                            i32.sub
                            i32.and
                            local.tee 3
                            i32.const 2147483646
                            i32.le_u
                            br_if 0 (;@12;)
                            local.get 4
                            local.set 0
                            br 7 (;@5;)
                          end
                          block  ;; label = @12
                            local.get 3
                            call $sbrk
                            i32.const -1
                            i32.eq
                            br_if 0 (;@12;)
                            local.get 3
                            local.get 7
                            i32.add
                            local.set 7
                            local.get 4
                            local.set 0
                            br 7 (;@5;)
                          end
                          i32.const 0
                          local.get 7
                          i32.sub
                          call $sbrk
                          drop
                          br 4 (;@7;)
                        end
                        local.get 4
                        local.set 0
                        local.get 4
                        i32.const -1
                        i32.ne
                        br_if 5 (;@5;)
                        br 3 (;@7;)
                      end
                      i32.const 0
                      local.set 9
                      br 7 (;@2;)
                    end
                    i32.const 0
                    local.set 0
                    br 5 (;@3;)
                  end
                  local.get 0
                  i32.const -1
                  i32.ne
                  br_if 2 (;@5;)
                end
                i32.const 0
                i32.const 0
                i32.load offset=1059768
                i32.const 4
                i32.or
                i32.store offset=1059768
              end
              local.get 9
              i32.const 2147483646
              i32.gt_u
              br_if 1 (;@4;)
              local.get 9
              call $sbrk
              local.set 0
              i32.const 0
              call $sbrk
              local.set 4
              local.get 0
              i32.const -1
              i32.eq
              br_if 1 (;@4;)
              local.get 4
              i32.const -1
              i32.eq
              br_if 1 (;@4;)
              local.get 0
              local.get 4
              i32.ge_u
              br_if 1 (;@4;)
              local.get 4
              local.get 0
              i32.sub
              local.tee 7
              local.get 5
              i32.const 56
              i32.add
              i32.le_u
              br_if 1 (;@4;)
            end
            i32.const 0
            i32.const 0
            i32.load offset=1059756
            local.get 7
            i32.add
            local.tee 4
            i32.store offset=1059756
            block  ;; label = @5
              local.get 4
              i32.const 0
              i32.load offset=1059760
              i32.le_u
              br_if 0 (;@5;)
              i32.const 0
              local.get 4
              i32.store offset=1059760
            end
            block  ;; label = @5
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    i32.const 0
                    i32.load offset=1059348
                    local.tee 3
                    i32.eqz
                    br_if 0 (;@8;)
                    i32.const 1059772
                    local.set 4
                    loop  ;; label = @9
                      local.get 0
                      local.get 4
                      i32.load
                      local.tee 6
                      local.get 4
                      i32.load offset=4
                      local.tee 9
                      i32.add
                      i32.eq
                      br_if 2 (;@7;)
                      local.get 4
                      i32.load offset=8
                      local.tee 4
                      br_if 0 (;@9;)
                      br 3 (;@6;)
                    end
                  end
                  block  ;; label = @8
                    block  ;; label = @9
                      i32.const 0
                      i32.load offset=1059340
                      local.tee 4
                      i32.eqz
                      br_if 0 (;@9;)
                      local.get 0
                      local.get 4
                      i32.ge_u
                      br_if 1 (;@8;)
                    end
                    i32.const 0
                    local.get 0
                    i32.store offset=1059340
                  end
                  i32.const 0
                  local.set 4
                  i32.const 0
                  local.get 7
                  i32.store offset=1059776
                  i32.const 0
                  local.get 0
                  i32.store offset=1059772
                  i32.const 0
                  i32.const -1
                  i32.store offset=1059356
                  i32.const 0
                  i32.const 0
                  i32.load offset=1059796
                  i32.store offset=1059360
                  i32.const 0
                  i32.const 0
                  i32.store offset=1059784
                  loop  ;; label = @8
                    local.get 4
                    i32.const 1059384
                    i32.add
                    local.get 4
                    i32.const 1059372
                    i32.add
                    local.tee 3
                    i32.store
                    local.get 3
                    local.get 4
                    i32.const 1059364
                    i32.add
                    local.tee 6
                    i32.store
                    local.get 4
                    i32.const 1059376
                    i32.add
                    local.get 6
                    i32.store
                    local.get 4
                    i32.const 1059392
                    i32.add
                    local.get 4
                    i32.const 1059380
                    i32.add
                    local.tee 6
                    i32.store
                    local.get 6
                    local.get 3
                    i32.store
                    local.get 4
                    i32.const 1059400
                    i32.add
                    local.get 4
                    i32.const 1059388
                    i32.add
                    local.tee 3
                    i32.store
                    local.get 3
                    local.get 6
                    i32.store
                    local.get 4
                    i32.const 1059396
                    i32.add
                    local.get 3
                    i32.store
                    local.get 4
                    i32.const 32
                    i32.add
                    local.tee 4
                    i32.const 256
                    i32.ne
                    br_if 0 (;@8;)
                  end
                  local.get 0
                  i32.const -8
                  local.get 0
                  i32.sub
                  i32.const 15
                  i32.and
                  i32.const 0
                  local.get 0
                  i32.const 8
                  i32.add
                  i32.const 15
                  i32.and
                  select
                  local.tee 4
                  i32.add
                  local.tee 3
                  local.get 7
                  i32.const -56
                  i32.add
                  local.tee 6
                  local.get 4
                  i32.sub
                  local.tee 4
                  i32.const 1
                  i32.or
                  i32.store offset=4
                  i32.const 0
                  i32.const 0
                  i32.load offset=1059812
                  i32.store offset=1059352
                  i32.const 0
                  local.get 4
                  i32.store offset=1059336
                  i32.const 0
                  local.get 3
                  i32.store offset=1059348
                  local.get 0
                  local.get 6
                  i32.add
                  i32.const 56
                  i32.store offset=4
                  br 2 (;@5;)
                end
                local.get 4
                i32.load8_u offset=12
                i32.const 8
                i32.and
                br_if 0 (;@6;)
                local.get 3
                local.get 6
                i32.lt_u
                br_if 0 (;@6;)
                local.get 3
                local.get 0
                i32.ge_u
                br_if 0 (;@6;)
                local.get 3
                i32.const -8
                local.get 3
                i32.sub
                i32.const 15
                i32.and
                i32.const 0
                local.get 3
                i32.const 8
                i32.add
                i32.const 15
                i32.and
                select
                local.tee 6
                i32.add
                local.tee 0
                i32.const 0
                i32.load offset=1059336
                local.get 7
                i32.add
                local.tee 2
                local.get 6
                i32.sub
                local.tee 6
                i32.const 1
                i32.or
                i32.store offset=4
                local.get 4
                local.get 9
                local.get 7
                i32.add
                i32.store offset=4
                i32.const 0
                i32.const 0
                i32.load offset=1059812
                i32.store offset=1059352
                i32.const 0
                local.get 6
                i32.store offset=1059336
                i32.const 0
                local.get 0
                i32.store offset=1059348
                local.get 3
                local.get 2
                i32.add
                i32.const 56
                i32.store offset=4
                br 1 (;@5;)
              end
              block  ;; label = @6
                local.get 0
                i32.const 0
                i32.load offset=1059340
                local.tee 9
                i32.ge_u
                br_if 0 (;@6;)
                i32.const 0
                local.get 0
                i32.store offset=1059340
                local.get 0
                local.set 9
              end
              local.get 0
              local.get 7
              i32.add
              local.set 6
              i32.const 1059772
              local.set 4
              block  ;; label = @6
                block  ;; label = @7
                  block  ;; label = @8
                    block  ;; label = @9
                      block  ;; label = @10
                        block  ;; label = @11
                          block  ;; label = @12
                            loop  ;; label = @13
                              local.get 4
                              i32.load
                              local.get 6
                              i32.eq
                              br_if 1 (;@12;)
                              local.get 4
                              i32.load offset=8
                              local.tee 4
                              br_if 0 (;@13;)
                              br 2 (;@11;)
                            end
                          end
                          local.get 4
                          i32.load8_u offset=12
                          i32.const 8
                          i32.and
                          i32.eqz
                          br_if 1 (;@10;)
                        end
                        i32.const 1059772
                        local.set 4
                        loop  ;; label = @11
                          block  ;; label = @12
                            local.get 4
                            i32.load
                            local.tee 6
                            local.get 3
                            i32.gt_u
                            br_if 0 (;@12;)
                            local.get 6
                            local.get 4
                            i32.load offset=4
                            i32.add
                            local.tee 6
                            local.get 3
                            i32.gt_u
                            br_if 3 (;@9;)
                          end
                          local.get 4
                          i32.load offset=8
                          local.set 4
                          br 0 (;@11;)
                        end
                      end
                      local.get 4
                      local.get 0
                      i32.store
                      local.get 4
                      local.get 4
                      i32.load offset=4
                      local.get 7
                      i32.add
                      i32.store offset=4
                      local.get 0
                      i32.const -8
                      local.get 0
                      i32.sub
                      i32.const 15
                      i32.and
                      i32.const 0
                      local.get 0
                      i32.const 8
                      i32.add
                      i32.const 15
                      i32.and
                      select
                      i32.add
                      local.tee 2
                      local.get 5
                      i32.const 3
                      i32.or
                      i32.store offset=4
                      local.get 6
                      i32.const -8
                      local.get 6
                      i32.sub
                      i32.const 15
                      i32.and
                      i32.const 0
                      local.get 6
                      i32.const 8
                      i32.add
                      i32.const 15
                      i32.and
                      select
                      i32.add
                      local.tee 7
                      local.get 2
                      local.get 5
                      i32.add
                      local.tee 5
                      i32.sub
                      local.set 4
                      block  ;; label = @10
                        local.get 7
                        local.get 3
                        i32.ne
                        br_if 0 (;@10;)
                        i32.const 0
                        local.get 5
                        i32.store offset=1059348
                        i32.const 0
                        i32.const 0
                        i32.load offset=1059336
                        local.get 4
                        i32.add
                        local.tee 4
                        i32.store offset=1059336
                        local.get 5
                        local.get 4
                        i32.const 1
                        i32.or
                        i32.store offset=4
                        br 3 (;@7;)
                      end
                      block  ;; label = @10
                        local.get 7
                        i32.const 0
                        i32.load offset=1059344
                        i32.ne
                        br_if 0 (;@10;)
                        i32.const 0
                        local.get 5
                        i32.store offset=1059344
                        i32.const 0
                        i32.const 0
                        i32.load offset=1059332
                        local.get 4
                        i32.add
                        local.tee 4
                        i32.store offset=1059332
                        local.get 5
                        local.get 4
                        i32.const 1
                        i32.or
                        i32.store offset=4
                        local.get 5
                        local.get 4
                        i32.add
                        local.get 4
                        i32.store
                        br 3 (;@7;)
                      end
                      block  ;; label = @10
                        local.get 7
                        i32.load offset=4
                        local.tee 3
                        i32.const 3
                        i32.and
                        i32.const 1
                        i32.ne
                        br_if 0 (;@10;)
                        local.get 3
                        i32.const -8
                        i32.and
                        local.set 8
                        block  ;; label = @11
                          block  ;; label = @12
                            local.get 3
                            i32.const 255
                            i32.gt_u
                            br_if 0 (;@12;)
                            local.get 7
                            i32.load offset=8
                            local.tee 6
                            local.get 3
                            i32.const 3
                            i32.shr_u
                            local.tee 9
                            i32.const 3
                            i32.shl
                            i32.const 1059364
                            i32.add
                            local.tee 0
                            i32.eq
                            drop
                            block  ;; label = @13
                              local.get 7
                              i32.load offset=12
                              local.tee 3
                              local.get 6
                              i32.ne
                              br_if 0 (;@13;)
                              i32.const 0
                              i32.const 0
                              i32.load offset=1059324
                              i32.const -2
                              local.get 9
                              i32.rotl
                              i32.and
                              i32.store offset=1059324
                              br 2 (;@11;)
                            end
                            local.get 3
                            local.get 0
                            i32.eq
                            drop
                            local.get 3
                            local.get 6
                            i32.store offset=8
                            local.get 6
                            local.get 3
                            i32.store offset=12
                            br 1 (;@11;)
                          end
                          local.get 7
                          i32.load offset=24
                          local.set 10
                          block  ;; label = @12
                            block  ;; label = @13
                              local.get 7
                              i32.load offset=12
                              local.tee 0
                              local.get 7
                              i32.eq
                              br_if 0 (;@13;)
                              local.get 7
                              i32.load offset=8
                              local.tee 3
                              local.get 9
                              i32.lt_u
                              drop
                              local.get 0
                              local.get 3
                              i32.store offset=8
                              local.get 3
                              local.get 0
                              i32.store offset=12
                              br 1 (;@12;)
                            end
                            block  ;; label = @13
                              local.get 7
                              i32.const 20
                              i32.add
                              local.tee 3
                              i32.load
                              local.tee 6
                              br_if 0 (;@13;)
                              local.get 7
                              i32.const 16
                              i32.add
                              local.tee 3
                              i32.load
                              local.tee 6
                              br_if 0 (;@13;)
                              i32.const 0
                              local.set 0
                              br 1 (;@12;)
                            end
                            loop  ;; label = @13
                              local.get 3
                              local.set 9
                              local.get 6
                              local.tee 0
                              i32.const 20
                              i32.add
                              local.tee 3
                              i32.load
                              local.tee 6
                              br_if 0 (;@13;)
                              local.get 0
                              i32.const 16
                              i32.add
                              local.set 3
                              local.get 0
                              i32.load offset=16
                              local.tee 6
                              br_if 0 (;@13;)
                            end
                            local.get 9
                            i32.const 0
                            i32.store
                          end
                          local.get 10
                          i32.eqz
                          br_if 0 (;@11;)
                          block  ;; label = @12
                            block  ;; label = @13
                              local.get 7
                              local.get 7
                              i32.load offset=28
                              local.tee 6
                              i32.const 2
                              i32.shl
                              i32.const 1059628
                              i32.add
                              local.tee 3
                              i32.load
                              i32.ne
                              br_if 0 (;@13;)
                              local.get 3
                              local.get 0
                              i32.store
                              local.get 0
                              br_if 1 (;@12;)
                              i32.const 0
                              i32.const 0
                              i32.load offset=1059328
                              i32.const -2
                              local.get 6
                              i32.rotl
                              i32.and
                              i32.store offset=1059328
                              br 2 (;@11;)
                            end
                            local.get 10
                            i32.const 16
                            i32.const 20
                            local.get 10
                            i32.load offset=16
                            local.get 7
                            i32.eq
                            select
                            i32.add
                            local.get 0
                            i32.store
                            local.get 0
                            i32.eqz
                            br_if 1 (;@11;)
                          end
                          local.get 0
                          local.get 10
                          i32.store offset=24
                          block  ;; label = @12
                            local.get 7
                            i32.load offset=16
                            local.tee 3
                            i32.eqz
                            br_if 0 (;@12;)
                            local.get 0
                            local.get 3
                            i32.store offset=16
                            local.get 3
                            local.get 0
                            i32.store offset=24
                          end
                          local.get 7
                          i32.load offset=20
                          local.tee 3
                          i32.eqz
                          br_if 0 (;@11;)
                          local.get 0
                          i32.const 20
                          i32.add
                          local.get 3
                          i32.store
                          local.get 3
                          local.get 0
                          i32.store offset=24
                        end
                        local.get 8
                        local.get 4
                        i32.add
                        local.set 4
                        local.get 7
                        local.get 8
                        i32.add
                        local.tee 7
                        i32.load offset=4
                        local.set 3
                      end
                      local.get 7
                      local.get 3
                      i32.const -2
                      i32.and
                      i32.store offset=4
                      local.get 5
                      local.get 4
                      i32.add
                      local.get 4
                      i32.store
                      local.get 5
                      local.get 4
                      i32.const 1
                      i32.or
                      i32.store offset=4
                      block  ;; label = @10
                        local.get 4
                        i32.const 255
                        i32.gt_u
                        br_if 0 (;@10;)
                        local.get 4
                        i32.const -8
                        i32.and
                        i32.const 1059364
                        i32.add
                        local.set 3
                        block  ;; label = @11
                          block  ;; label = @12
                            i32.const 0
                            i32.load offset=1059324
                            local.tee 6
                            i32.const 1
                            local.get 4
                            i32.const 3
                            i32.shr_u
                            i32.shl
                            local.tee 4
                            i32.and
                            br_if 0 (;@12;)
                            i32.const 0
                            local.get 6
                            local.get 4
                            i32.or
                            i32.store offset=1059324
                            local.get 3
                            local.set 4
                            br 1 (;@11;)
                          end
                          local.get 3
                          i32.load offset=8
                          local.set 4
                        end
                        local.get 4
                        local.get 5
                        i32.store offset=12
                        local.get 3
                        local.get 5
                        i32.store offset=8
                        local.get 5
                        local.get 3
                        i32.store offset=12
                        local.get 5
                        local.get 4
                        i32.store offset=8
                        br 3 (;@7;)
                      end
                      i32.const 31
                      local.set 3
                      block  ;; label = @10
                        local.get 4
                        i32.const 16777215
                        i32.gt_u
                        br_if 0 (;@10;)
                        local.get 4
                        i32.const 8
                        i32.shr_u
                        local.tee 3
                        local.get 3
                        i32.const 1048320
                        i32.add
                        i32.const 16
                        i32.shr_u
                        i32.const 8
                        i32.and
                        local.tee 3
                        i32.shl
                        local.tee 6
                        local.get 6
                        i32.const 520192
                        i32.add
                        i32.const 16
                        i32.shr_u
                        i32.const 4
                        i32.and
                        local.tee 6
                        i32.shl
                        local.tee 0
                        local.get 0
                        i32.const 245760
                        i32.add
                        i32.const 16
                        i32.shr_u
                        i32.const 2
                        i32.and
                        local.tee 0
                        i32.shl
                        i32.const 15
                        i32.shr_u
                        local.get 3
                        local.get 6
                        i32.or
                        local.get 0
                        i32.or
                        i32.sub
                        local.tee 3
                        i32.const 1
                        i32.shl
                        local.get 4
                        local.get 3
                        i32.const 21
                        i32.add
                        i32.shr_u
                        i32.const 1
                        i32.and
                        i32.or
                        i32.const 28
                        i32.add
                        local.set 3
                      end
                      local.get 5
                      local.get 3
                      i32.store offset=28
                      local.get 5
                      i64.const 0
                      i64.store offset=16 align=4
                      local.get 3
                      i32.const 2
                      i32.shl
                      i32.const 1059628
                      i32.add
                      local.set 6
                      block  ;; label = @10
                        i32.const 0
                        i32.load offset=1059328
                        local.tee 0
                        i32.const 1
                        local.get 3
                        i32.shl
                        local.tee 9
                        i32.and
                        br_if 0 (;@10;)
                        local.get 6
                        local.get 5
                        i32.store
                        i32.const 0
                        local.get 0
                        local.get 9
                        i32.or
                        i32.store offset=1059328
                        local.get 5
                        local.get 6
                        i32.store offset=24
                        local.get 5
                        local.get 5
                        i32.store offset=8
                        local.get 5
                        local.get 5
                        i32.store offset=12
                        br 3 (;@7;)
                      end
                      local.get 4
                      i32.const 0
                      i32.const 25
                      local.get 3
                      i32.const 1
                      i32.shr_u
                      i32.sub
                      local.get 3
                      i32.const 31
                      i32.eq
                      select
                      i32.shl
                      local.set 3
                      local.get 6
                      i32.load
                      local.set 0
                      loop  ;; label = @10
                        local.get 0
                        local.tee 6
                        i32.load offset=4
                        i32.const -8
                        i32.and
                        local.get 4
                        i32.eq
                        br_if 2 (;@8;)
                        local.get 3
                        i32.const 29
                        i32.shr_u
                        local.set 0
                        local.get 3
                        i32.const 1
                        i32.shl
                        local.set 3
                        local.get 6
                        local.get 0
                        i32.const 4
                        i32.and
                        i32.add
                        i32.const 16
                        i32.add
                        local.tee 9
                        i32.load
                        local.tee 0
                        br_if 0 (;@10;)
                      end
                      local.get 9
                      local.get 5
                      i32.store
                      local.get 5
                      local.get 6
                      i32.store offset=24
                      local.get 5
                      local.get 5
                      i32.store offset=12
                      local.get 5
                      local.get 5
                      i32.store offset=8
                      br 2 (;@7;)
                    end
                    local.get 0
                    i32.const -8
                    local.get 0
                    i32.sub
                    i32.const 15
                    i32.and
                    i32.const 0
                    local.get 0
                    i32.const 8
                    i32.add
                    i32.const 15
                    i32.and
                    select
                    local.tee 4
                    i32.add
                    local.tee 2
                    local.get 7
                    i32.const -56
                    i32.add
                    local.tee 9
                    local.get 4
                    i32.sub
                    local.tee 4
                    i32.const 1
                    i32.or
                    i32.store offset=4
                    local.get 0
                    local.get 9
                    i32.add
                    i32.const 56
                    i32.store offset=4
                    local.get 3
                    local.get 6
                    i32.const 55
                    local.get 6
                    i32.sub
                    i32.const 15
                    i32.and
                    i32.const 0
                    local.get 6
                    i32.const -55
                    i32.add
                    i32.const 15
                    i32.and
                    select
                    i32.add
                    i32.const -63
                    i32.add
                    local.tee 9
                    local.get 9
                    local.get 3
                    i32.const 16
                    i32.add
                    i32.lt_u
                    select
                    local.tee 9
                    i32.const 35
                    i32.store offset=4
                    i32.const 0
                    i32.const 0
                    i32.load offset=1059812
                    i32.store offset=1059352
                    i32.const 0
                    local.get 4
                    i32.store offset=1059336
                    i32.const 0
                    local.get 2
                    i32.store offset=1059348
                    local.get 9
                    i32.const 16
                    i32.add
                    i32.const 0
                    i64.load offset=1059780 align=4
                    i64.store align=4
                    local.get 9
                    i32.const 0
                    i64.load offset=1059772 align=4
                    i64.store offset=8 align=4
                    i32.const 0
                    local.get 9
                    i32.const 8
                    i32.add
                    i32.store offset=1059780
                    i32.const 0
                    local.get 7
                    i32.store offset=1059776
                    i32.const 0
                    local.get 0
                    i32.store offset=1059772
                    i32.const 0
                    i32.const 0
                    i32.store offset=1059784
                    local.get 9
                    i32.const 36
                    i32.add
                    local.set 4
                    loop  ;; label = @9
                      local.get 4
                      i32.const 7
                      i32.store
                      local.get 4
                      i32.const 4
                      i32.add
                      local.tee 4
                      local.get 6
                      i32.lt_u
                      br_if 0 (;@9;)
                    end
                    local.get 9
                    local.get 3
                    i32.eq
                    br_if 3 (;@5;)
                    local.get 9
                    local.get 9
                    i32.load offset=4
                    i32.const -2
                    i32.and
                    i32.store offset=4
                    local.get 9
                    local.get 9
                    local.get 3
                    i32.sub
                    local.tee 0
                    i32.store
                    local.get 3
                    local.get 0
                    i32.const 1
                    i32.or
                    i32.store offset=4
                    block  ;; label = @9
                      local.get 0
                      i32.const 255
                      i32.gt_u
                      br_if 0 (;@9;)
                      local.get 0
                      i32.const -8
                      i32.and
                      i32.const 1059364
                      i32.add
                      local.set 4
                      block  ;; label = @10
                        block  ;; label = @11
                          i32.const 0
                          i32.load offset=1059324
                          local.tee 6
                          i32.const 1
                          local.get 0
                          i32.const 3
                          i32.shr_u
                          i32.shl
                          local.tee 0
                          i32.and
                          br_if 0 (;@11;)
                          i32.const 0
                          local.get 6
                          local.get 0
                          i32.or
                          i32.store offset=1059324
                          local.get 4
                          local.set 6
                          br 1 (;@10;)
                        end
                        local.get 4
                        i32.load offset=8
                        local.set 6
                      end
                      local.get 6
                      local.get 3
                      i32.store offset=12
                      local.get 4
                      local.get 3
                      i32.store offset=8
                      local.get 3
                      local.get 4
                      i32.store offset=12
                      local.get 3
                      local.get 6
                      i32.store offset=8
                      br 4 (;@5;)
                    end
                    i32.const 31
                    local.set 4
                    block  ;; label = @9
                      local.get 0
                      i32.const 16777215
                      i32.gt_u
                      br_if 0 (;@9;)
                      local.get 0
                      i32.const 8
                      i32.shr_u
                      local.tee 4
                      local.get 4
                      i32.const 1048320
                      i32.add
                      i32.const 16
                      i32.shr_u
                      i32.const 8
                      i32.and
                      local.tee 4
                      i32.shl
                      local.tee 6
                      local.get 6
                      i32.const 520192
                      i32.add
                      i32.const 16
                      i32.shr_u
                      i32.const 4
                      i32.and
                      local.tee 6
                      i32.shl
                      local.tee 9
                      local.get 9
                      i32.const 245760
                      i32.add
                      i32.const 16
                      i32.shr_u
                      i32.const 2
                      i32.and
                      local.tee 9
                      i32.shl
                      i32.const 15
                      i32.shr_u
                      local.get 4
                      local.get 6
                      i32.or
                      local.get 9
                      i32.or
                      i32.sub
                      local.tee 4
                      i32.const 1
                      i32.shl
                      local.get 0
                      local.get 4
                      i32.const 21
                      i32.add
                      i32.shr_u
                      i32.const 1
                      i32.and
                      i32.or
                      i32.const 28
                      i32.add
                      local.set 4
                    end
                    local.get 3
                    local.get 4
                    i32.store offset=28
                    local.get 3
                    i64.const 0
                    i64.store offset=16 align=4
                    local.get 4
                    i32.const 2
                    i32.shl
                    i32.const 1059628
                    i32.add
                    local.set 6
                    block  ;; label = @9
                      i32.const 0
                      i32.load offset=1059328
                      local.tee 9
                      i32.const 1
                      local.get 4
                      i32.shl
                      local.tee 7
                      i32.and
                      br_if 0 (;@9;)
                      local.get 6
                      local.get 3
                      i32.store
                      i32.const 0
                      local.get 9
                      local.get 7
                      i32.or
                      i32.store offset=1059328
                      local.get 3
                      local.get 6
                      i32.store offset=24
                      local.get 3
                      local.get 3
                      i32.store offset=8
                      local.get 3
                      local.get 3
                      i32.store offset=12
                      br 4 (;@5;)
                    end
                    local.get 0
                    i32.const 0
                    i32.const 25
                    local.get 4
                    i32.const 1
                    i32.shr_u
                    i32.sub
                    local.get 4
                    i32.const 31
                    i32.eq
                    select
                    i32.shl
                    local.set 4
                    local.get 6
                    i32.load
                    local.set 9
                    loop  ;; label = @9
                      local.get 9
                      local.tee 6
                      i32.load offset=4
                      i32.const -8
                      i32.and
                      local.get 0
                      i32.eq
                      br_if 3 (;@6;)
                      local.get 4
                      i32.const 29
                      i32.shr_u
                      local.set 9
                      local.get 4
                      i32.const 1
                      i32.shl
                      local.set 4
                      local.get 6
                      local.get 9
                      i32.const 4
                      i32.and
                      i32.add
                      i32.const 16
                      i32.add
                      local.tee 7
                      i32.load
                      local.tee 9
                      br_if 0 (;@9;)
                    end
                    local.get 7
                    local.get 3
                    i32.store
                    local.get 3
                    local.get 6
                    i32.store offset=24
                    local.get 3
                    local.get 3
                    i32.store offset=12
                    local.get 3
                    local.get 3
                    i32.store offset=8
                    br 3 (;@5;)
                  end
                  local.get 6
                  i32.load offset=8
                  local.tee 4
                  local.get 5
                  i32.store offset=12
                  local.get 6
                  local.get 5
                  i32.store offset=8
                  local.get 5
                  i32.const 0
                  i32.store offset=24
                  local.get 5
                  local.get 6
                  i32.store offset=12
                  local.get 5
                  local.get 4
                  i32.store offset=8
                end
                local.get 2
                i32.const 8
                i32.add
                local.set 4
                br 5 (;@1;)
              end
              local.get 6
              i32.load offset=8
              local.tee 4
              local.get 3
              i32.store offset=12
              local.get 6
              local.get 3
              i32.store offset=8
              local.get 3
              i32.const 0
              i32.store offset=24
              local.get 3
              local.get 6
              i32.store offset=12
              local.get 3
              local.get 4
              i32.store offset=8
            end
            i32.const 0
            i32.load offset=1059336
            local.tee 4
            local.get 5
            i32.le_u
            br_if 0 (;@4;)
            i32.const 0
            i32.load offset=1059348
            local.tee 3
            local.get 5
            i32.add
            local.tee 6
            local.get 4
            local.get 5
            i32.sub
            local.tee 4
            i32.const 1
            i32.or
            i32.store offset=4
            i32.const 0
            local.get 4
            i32.store offset=1059336
            i32.const 0
            local.get 6
            i32.store offset=1059348
            local.get 3
            local.get 5
            i32.const 3
            i32.or
            i32.store offset=4
            local.get 3
            i32.const 8
            i32.add
            local.set 4
            br 3 (;@1;)
          end
          i32.const 0
          local.set 4
          i32.const 0
          i32.const 48
          i32.store offset=1059820
          br 2 (;@1;)
        end
        block  ;; label = @3
          local.get 2
          i32.eqz
          br_if 0 (;@3;)
          block  ;; label = @4
            block  ;; label = @5
              local.get 9
              local.get 9
              i32.load offset=28
              local.tee 6
              i32.const 2
              i32.shl
              i32.const 1059628
              i32.add
              local.tee 4
              i32.load
              i32.ne
              br_if 0 (;@5;)
              local.get 4
              local.get 0
              i32.store
              local.get 0
              br_if 1 (;@4;)
              i32.const 0
              local.get 10
              i32.const -2
              local.get 6
              i32.rotl
              i32.and
              local.tee 10
              i32.store offset=1059328
              br 2 (;@3;)
            end
            local.get 2
            i32.const 16
            i32.const 20
            local.get 2
            i32.load offset=16
            local.get 9
            i32.eq
            select
            i32.add
            local.get 0
            i32.store
            local.get 0
            i32.eqz
            br_if 1 (;@3;)
          end
          local.get 0
          local.get 2
          i32.store offset=24
          block  ;; label = @4
            local.get 9
            i32.load offset=16
            local.tee 4
            i32.eqz
            br_if 0 (;@4;)
            local.get 0
            local.get 4
            i32.store offset=16
            local.get 4
            local.get 0
            i32.store offset=24
          end
          local.get 9
          i32.const 20
          i32.add
          i32.load
          local.tee 4
          i32.eqz
          br_if 0 (;@3;)
          local.get 0
          i32.const 20
          i32.add
          local.get 4
          i32.store
          local.get 4
          local.get 0
          i32.store offset=24
        end
        block  ;; label = @3
          block  ;; label = @4
            local.get 3
            i32.const 15
            i32.gt_u
            br_if 0 (;@4;)
            local.get 9
            local.get 3
            local.get 5
            i32.add
            local.tee 4
            i32.const 3
            i32.or
            i32.store offset=4
            local.get 9
            local.get 4
            i32.add
            local.tee 4
            local.get 4
            i32.load offset=4
            i32.const 1
            i32.or
            i32.store offset=4
            br 1 (;@3;)
          end
          local.get 9
          local.get 5
          i32.add
          local.tee 0
          local.get 3
          i32.const 1
          i32.or
          i32.store offset=4
          local.get 9
          local.get 5
          i32.const 3
          i32.or
          i32.store offset=4
          local.get 0
          local.get 3
          i32.add
          local.get 3
          i32.store
          block  ;; label = @4
            local.get 3
            i32.const 255
            i32.gt_u
            br_if 0 (;@4;)
            local.get 3
            i32.const -8
            i32.and
            i32.const 1059364
            i32.add
            local.set 4
            block  ;; label = @5
              block  ;; label = @6
                i32.const 0
                i32.load offset=1059324
                local.tee 6
                i32.const 1
                local.get 3
                i32.const 3
                i32.shr_u
                i32.shl
                local.tee 3
                i32.and
                br_if 0 (;@6;)
                i32.const 0
                local.get 6
                local.get 3
                i32.or
                i32.store offset=1059324
                local.get 4
                local.set 3
                br 1 (;@5;)
              end
              local.get 4
              i32.load offset=8
              local.set 3
            end
            local.get 3
            local.get 0
            i32.store offset=12
            local.get 4
            local.get 0
            i32.store offset=8
            local.get 0
            local.get 4
            i32.store offset=12
            local.get 0
            local.get 3
            i32.store offset=8
            br 1 (;@3;)
          end
          i32.const 31
          local.set 4
          block  ;; label = @4
            local.get 3
            i32.const 16777215
            i32.gt_u
            br_if 0 (;@4;)
            local.get 3
            i32.const 8
            i32.shr_u
            local.tee 4
            local.get 4
            i32.const 1048320
            i32.add
            i32.const 16
            i32.shr_u
            i32.const 8
            i32.and
            local.tee 4
            i32.shl
            local.tee 6
            local.get 6
            i32.const 520192
            i32.add
            i32.const 16
            i32.shr_u
            i32.const 4
            i32.and
            local.tee 6
            i32.shl
            local.tee 5
            local.get 5
            i32.const 245760
            i32.add
            i32.const 16
            i32.shr_u
            i32.const 2
            i32.and
            local.tee 5
            i32.shl
            i32.const 15
            i32.shr_u
            local.get 4
            local.get 6
            i32.or
            local.get 5
            i32.or
            i32.sub
            local.tee 4
            i32.const 1
            i32.shl
            local.get 3
            local.get 4
            i32.const 21
            i32.add
            i32.shr_u
            i32.const 1
            i32.and
            i32.or
            i32.const 28
            i32.add
            local.set 4
          end
          local.get 0
          local.get 4
          i32.store offset=28
          local.get 0
          i64.const 0
          i64.store offset=16 align=4
          local.get 4
          i32.const 2
          i32.shl
          i32.const 1059628
          i32.add
          local.set 6
          block  ;; label = @4
            local.get 10
            i32.const 1
            local.get 4
            i32.shl
            local.tee 5
            i32.and
            br_if 0 (;@4;)
            local.get 6
            local.get 0
            i32.store
            i32.const 0
            local.get 10
            local.get 5
            i32.or
            i32.store offset=1059328
            local.get 0
            local.get 6
            i32.store offset=24
            local.get 0
            local.get 0
            i32.store offset=8
            local.get 0
            local.get 0
            i32.store offset=12
            br 1 (;@3;)
          end
          local.get 3
          i32.const 0
          i32.const 25
          local.get 4
          i32.const 1
          i32.shr_u
          i32.sub
          local.get 4
          i32.const 31
          i32.eq
          select
          i32.shl
          local.set 4
          local.get 6
          i32.load
          local.set 5
          block  ;; label = @4
            loop  ;; label = @5
              local.get 5
              local.tee 6
              i32.load offset=4
              i32.const -8
              i32.and
              local.get 3
              i32.eq
              br_if 1 (;@4;)
              local.get 4
              i32.const 29
              i32.shr_u
              local.set 5
              local.get 4
              i32.const 1
              i32.shl
              local.set 4
              local.get 6
              local.get 5
              i32.const 4
              i32.and
              i32.add
              i32.const 16
              i32.add
              local.tee 7
              i32.load
              local.tee 5
              br_if 0 (;@5;)
            end
            local.get 7
            local.get 0
            i32.store
            local.get 0
            local.get 6
            i32.store offset=24
            local.get 0
            local.get 0
            i32.store offset=12
            local.get 0
            local.get 0
            i32.store offset=8
            br 1 (;@3;)
          end
          local.get 6
          i32.load offset=8
          local.tee 4
          local.get 0
          i32.store offset=12
          local.get 6
          local.get 0
          i32.store offset=8
          local.get 0
          i32.const 0
          i32.store offset=24
          local.get 0
          local.get 6
          i32.store offset=12
          local.get 0
          local.get 4
          i32.store offset=8
        end
        local.get 9
        i32.const 8
        i32.add
        local.set 4
        br 1 (;@1;)
      end
      block  ;; label = @2
        local.get 11
        i32.eqz
        br_if 0 (;@2;)
        block  ;; label = @3
          block  ;; label = @4
            local.get 0
            local.get 0
            i32.load offset=28
            local.tee 6
            i32.const 2
            i32.shl
            i32.const 1059628
            i32.add
            local.tee 4
            i32.load
            i32.ne
            br_if 0 (;@4;)
            local.get 4
            local.get 9
            i32.store
            local.get 9
            br_if 1 (;@3;)
            i32.const 0
            local.get 10
            i32.const -2
            local.get 6
            i32.rotl
            i32.and
            i32.store offset=1059328
            br 2 (;@2;)
          end
          local.get 11
          i32.const 16
          i32.const 20
          local.get 11
          i32.load offset=16
          local.get 0
          i32.eq
          select
          i32.add
          local.get 9
          i32.store
          local.get 9
          i32.eqz
          br_if 1 (;@2;)
        end
        local.get 9
        local.get 11
        i32.store offset=24
        block  ;; label = @3
          local.get 0
          i32.load offset=16
          local.tee 4
          i32.eqz
          br_if 0 (;@3;)
          local.get 9
          local.get 4
          i32.store offset=16
          local.get 4
          local.get 9
          i32.store offset=24
        end
        local.get 0
        i32.const 20
        i32.add
        i32.load
        local.tee 4
        i32.eqz
        br_if 0 (;@2;)
        local.get 9
        i32.const 20
        i32.add
        local.get 4
        i32.store
        local.get 4
        local.get 9
        i32.store offset=24
      end
      block  ;; label = @2
        block  ;; label = @3
          local.get 3
          i32.const 15
          i32.gt_u
          br_if 0 (;@3;)
          local.get 0
          local.get 3
          local.get 5
          i32.add
          local.tee 4
          i32.const 3
          i32.or
          i32.store offset=4
          local.get 0
          local.get 4
          i32.add
          local.tee 4
          local.get 4
          i32.load offset=4
          i32.const 1
          i32.or
          i32.store offset=4
          br 1 (;@2;)
        end
        local.get 0
        local.get 5
        i32.add
        local.tee 6
        local.get 3
        i32.const 1
        i32.or
        i32.store offset=4
        local.get 0
        local.get 5
        i32.const 3
        i32.or
        i32.store offset=4
        local.get 6
        local.get 3
        i32.add
        local.get 3
        i32.store
        block  ;; label = @3
          local.get 8
          i32.eqz
          br_if 0 (;@3;)
          local.get 8
          i32.const -8
          i32.and
          i32.const 1059364
          i32.add
          local.set 5
          i32.const 0
          i32.load offset=1059344
          local.set 4
          block  ;; label = @4
            block  ;; label = @5
              i32.const 1
              local.get 8
              i32.const 3
              i32.shr_u
              i32.shl
              local.tee 9
              local.get 7
              i32.and
              br_if 0 (;@5;)
              i32.const 0
              local.get 9
              local.get 7
              i32.or
              i32.store offset=1059324
              local.get 5
              local.set 9
              br 1 (;@4;)
            end
            local.get 5
            i32.load offset=8
            local.set 9
          end
          local.get 9
          local.get 4
          i32.store offset=12
          local.get 5
          local.get 4
          i32.store offset=8
          local.get 4
          local.get 5
          i32.store offset=12
          local.get 4
          local.get 9
          i32.store offset=8
        end
        i32.const 0
        local.get 6
        i32.store offset=1059344
        i32.const 0
        local.get 3
        i32.store offset=1059332
      end
      local.get 0
      i32.const 8
      i32.add
      local.set 4
    end
    local.get 1
    i32.const 16
    i32.add
    global.set $__stack_pointer
    local.get 4)
  (func $free (type 2) (param i32)
    local.get 0
    call $dlfree)
  (func $dlfree (type 2) (param i32)
    (local i32 i32 i32 i32 i32 i32 i32)
    block  ;; label = @1
      local.get 0
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      i32.const -8
      i32.add
      local.tee 1
      local.get 0
      i32.const -4
      i32.add
      i32.load
      local.tee 2
      i32.const -8
      i32.and
      local.tee 0
      i32.add
      local.set 3
      block  ;; label = @2
        local.get 2
        i32.const 1
        i32.and
        br_if 0 (;@2;)
        local.get 2
        i32.const 3
        i32.and
        i32.eqz
        br_if 1 (;@1;)
        local.get 1
        local.get 1
        i32.load
        local.tee 2
        i32.sub
        local.tee 1
        i32.const 0
        i32.load offset=1059340
        local.tee 4
        i32.lt_u
        br_if 1 (;@1;)
        local.get 2
        local.get 0
        i32.add
        local.set 0
        block  ;; label = @3
          local.get 1
          i32.const 0
          i32.load offset=1059344
          i32.eq
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 2
            i32.const 255
            i32.gt_u
            br_if 0 (;@4;)
            local.get 1
            i32.load offset=8
            local.tee 4
            local.get 2
            i32.const 3
            i32.shr_u
            local.tee 5
            i32.const 3
            i32.shl
            i32.const 1059364
            i32.add
            local.tee 6
            i32.eq
            drop
            block  ;; label = @5
              local.get 1
              i32.load offset=12
              local.tee 2
              local.get 4
              i32.ne
              br_if 0 (;@5;)
              i32.const 0
              i32.const 0
              i32.load offset=1059324
              i32.const -2
              local.get 5
              i32.rotl
              i32.and
              i32.store offset=1059324
              br 3 (;@2;)
            end
            local.get 2
            local.get 6
            i32.eq
            drop
            local.get 2
            local.get 4
            i32.store offset=8
            local.get 4
            local.get 2
            i32.store offset=12
            br 2 (;@2;)
          end
          local.get 1
          i32.load offset=24
          local.set 7
          block  ;; label = @4
            block  ;; label = @5
              local.get 1
              i32.load offset=12
              local.tee 6
              local.get 1
              i32.eq
              br_if 0 (;@5;)
              local.get 1
              i32.load offset=8
              local.tee 2
              local.get 4
              i32.lt_u
              drop
              local.get 6
              local.get 2
              i32.store offset=8
              local.get 2
              local.get 6
              i32.store offset=12
              br 1 (;@4;)
            end
            block  ;; label = @5
              local.get 1
              i32.const 20
              i32.add
              local.tee 2
              i32.load
              local.tee 4
              br_if 0 (;@5;)
              local.get 1
              i32.const 16
              i32.add
              local.tee 2
              i32.load
              local.tee 4
              br_if 0 (;@5;)
              i32.const 0
              local.set 6
              br 1 (;@4;)
            end
            loop  ;; label = @5
              local.get 2
              local.set 5
              local.get 4
              local.tee 6
              i32.const 20
              i32.add
              local.tee 2
              i32.load
              local.tee 4
              br_if 0 (;@5;)
              local.get 6
              i32.const 16
              i32.add
              local.set 2
              local.get 6
              i32.load offset=16
              local.tee 4
              br_if 0 (;@5;)
            end
            local.get 5
            i32.const 0
            i32.store
          end
          local.get 7
          i32.eqz
          br_if 1 (;@2;)
          block  ;; label = @4
            block  ;; label = @5
              local.get 1
              local.get 1
              i32.load offset=28
              local.tee 4
              i32.const 2
              i32.shl
              i32.const 1059628
              i32.add
              local.tee 2
              i32.load
              i32.ne
              br_if 0 (;@5;)
              local.get 2
              local.get 6
              i32.store
              local.get 6
              br_if 1 (;@4;)
              i32.const 0
              i32.const 0
              i32.load offset=1059328
              i32.const -2
              local.get 4
              i32.rotl
              i32.and
              i32.store offset=1059328
              br 3 (;@2;)
            end
            local.get 7
            i32.const 16
            i32.const 20
            local.get 7
            i32.load offset=16
            local.get 1
            i32.eq
            select
            i32.add
            local.get 6
            i32.store
            local.get 6
            i32.eqz
            br_if 2 (;@2;)
          end
          local.get 6
          local.get 7
          i32.store offset=24
          block  ;; label = @4
            local.get 1
            i32.load offset=16
            local.tee 2
            i32.eqz
            br_if 0 (;@4;)
            local.get 6
            local.get 2
            i32.store offset=16
            local.get 2
            local.get 6
            i32.store offset=24
          end
          local.get 1
          i32.load offset=20
          local.tee 2
          i32.eqz
          br_if 1 (;@2;)
          local.get 6
          i32.const 20
          i32.add
          local.get 2
          i32.store
          local.get 2
          local.get 6
          i32.store offset=24
          br 1 (;@2;)
        end
        local.get 3
        i32.load offset=4
        local.tee 2
        i32.const 3
        i32.and
        i32.const 3
        i32.ne
        br_if 0 (;@2;)
        local.get 3
        local.get 2
        i32.const -2
        i32.and
        i32.store offset=4
        i32.const 0
        local.get 0
        i32.store offset=1059332
        local.get 1
        local.get 0
        i32.add
        local.get 0
        i32.store
        local.get 1
        local.get 0
        i32.const 1
        i32.or
        i32.store offset=4
        return
      end
      local.get 1
      local.get 3
      i32.ge_u
      br_if 0 (;@1;)
      local.get 3
      i32.load offset=4
      local.tee 2
      i32.const 1
      i32.and
      i32.eqz
      br_if 0 (;@1;)
      block  ;; label = @2
        block  ;; label = @3
          local.get 2
          i32.const 2
          i32.and
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 3
            i32.const 0
            i32.load offset=1059348
            i32.ne
            br_if 0 (;@4;)
            i32.const 0
            local.get 1
            i32.store offset=1059348
            i32.const 0
            i32.const 0
            i32.load offset=1059336
            local.get 0
            i32.add
            local.tee 0
            i32.store offset=1059336
            local.get 1
            local.get 0
            i32.const 1
            i32.or
            i32.store offset=4
            local.get 1
            i32.const 0
            i32.load offset=1059344
            i32.ne
            br_if 3 (;@1;)
            i32.const 0
            i32.const 0
            i32.store offset=1059332
            i32.const 0
            i32.const 0
            i32.store offset=1059344
            return
          end
          block  ;; label = @4
            local.get 3
            i32.const 0
            i32.load offset=1059344
            i32.ne
            br_if 0 (;@4;)
            i32.const 0
            local.get 1
            i32.store offset=1059344
            i32.const 0
            i32.const 0
            i32.load offset=1059332
            local.get 0
            i32.add
            local.tee 0
            i32.store offset=1059332
            local.get 1
            local.get 0
            i32.const 1
            i32.or
            i32.store offset=4
            local.get 1
            local.get 0
            i32.add
            local.get 0
            i32.store
            return
          end
          local.get 2
          i32.const -8
          i32.and
          local.get 0
          i32.add
          local.set 0
          block  ;; label = @4
            block  ;; label = @5
              local.get 2
              i32.const 255
              i32.gt_u
              br_if 0 (;@5;)
              local.get 3
              i32.load offset=8
              local.tee 4
              local.get 2
              i32.const 3
              i32.shr_u
              local.tee 5
              i32.const 3
              i32.shl
              i32.const 1059364
              i32.add
              local.tee 6
              i32.eq
              drop
              block  ;; label = @6
                local.get 3
                i32.load offset=12
                local.tee 2
                local.get 4
                i32.ne
                br_if 0 (;@6;)
                i32.const 0
                i32.const 0
                i32.load offset=1059324
                i32.const -2
                local.get 5
                i32.rotl
                i32.and
                i32.store offset=1059324
                br 2 (;@4;)
              end
              local.get 2
              local.get 6
              i32.eq
              drop
              local.get 2
              local.get 4
              i32.store offset=8
              local.get 4
              local.get 2
              i32.store offset=12
              br 1 (;@4;)
            end
            local.get 3
            i32.load offset=24
            local.set 7
            block  ;; label = @5
              block  ;; label = @6
                local.get 3
                i32.load offset=12
                local.tee 6
                local.get 3
                i32.eq
                br_if 0 (;@6;)
                local.get 3
                i32.load offset=8
                local.tee 2
                i32.const 0
                i32.load offset=1059340
                i32.lt_u
                drop
                local.get 6
                local.get 2
                i32.store offset=8
                local.get 2
                local.get 6
                i32.store offset=12
                br 1 (;@5;)
              end
              block  ;; label = @6
                local.get 3
                i32.const 20
                i32.add
                local.tee 2
                i32.load
                local.tee 4
                br_if 0 (;@6;)
                local.get 3
                i32.const 16
                i32.add
                local.tee 2
                i32.load
                local.tee 4
                br_if 0 (;@6;)
                i32.const 0
                local.set 6
                br 1 (;@5;)
              end
              loop  ;; label = @6
                local.get 2
                local.set 5
                local.get 4
                local.tee 6
                i32.const 20
                i32.add
                local.tee 2
                i32.load
                local.tee 4
                br_if 0 (;@6;)
                local.get 6
                i32.const 16
                i32.add
                local.set 2
                local.get 6
                i32.load offset=16
                local.tee 4
                br_if 0 (;@6;)
              end
              local.get 5
              i32.const 0
              i32.store
            end
            local.get 7
            i32.eqz
            br_if 0 (;@4;)
            block  ;; label = @5
              block  ;; label = @6
                local.get 3
                local.get 3
                i32.load offset=28
                local.tee 4
                i32.const 2
                i32.shl
                i32.const 1059628
                i32.add
                local.tee 2
                i32.load
                i32.ne
                br_if 0 (;@6;)
                local.get 2
                local.get 6
                i32.store
                local.get 6
                br_if 1 (;@5;)
                i32.const 0
                i32.const 0
                i32.load offset=1059328
                i32.const -2
                local.get 4
                i32.rotl
                i32.and
                i32.store offset=1059328
                br 2 (;@4;)
              end
              local.get 7
              i32.const 16
              i32.const 20
              local.get 7
              i32.load offset=16
              local.get 3
              i32.eq
              select
              i32.add
              local.get 6
              i32.store
              local.get 6
              i32.eqz
              br_if 1 (;@4;)
            end
            local.get 6
            local.get 7
            i32.store offset=24
            block  ;; label = @5
              local.get 3
              i32.load offset=16
              local.tee 2
              i32.eqz
              br_if 0 (;@5;)
              local.get 6
              local.get 2
              i32.store offset=16
              local.get 2
              local.get 6
              i32.store offset=24
            end
            local.get 3
            i32.load offset=20
            local.tee 2
            i32.eqz
            br_if 0 (;@4;)
            local.get 6
            i32.const 20
            i32.add
            local.get 2
            i32.store
            local.get 2
            local.get 6
            i32.store offset=24
          end
          local.get 1
          local.get 0
          i32.add
          local.get 0
          i32.store
          local.get 1
          local.get 0
          i32.const 1
          i32.or
          i32.store offset=4
          local.get 1
          i32.const 0
          i32.load offset=1059344
          i32.ne
          br_if 1 (;@2;)
          i32.const 0
          local.get 0
          i32.store offset=1059332
          return
        end
        local.get 3
        local.get 2
        i32.const -2
        i32.and
        i32.store offset=4
        local.get 1
        local.get 0
        i32.add
        local.get 0
        i32.store
        local.get 1
        local.get 0
        i32.const 1
        i32.or
        i32.store offset=4
      end
      block  ;; label = @2
        local.get 0
        i32.const 255
        i32.gt_u
        br_if 0 (;@2;)
        local.get 0
        i32.const -8
        i32.and
        i32.const 1059364
        i32.add
        local.set 2
        block  ;; label = @3
          block  ;; label = @4
            i32.const 0
            i32.load offset=1059324
            local.tee 4
            i32.const 1
            local.get 0
            i32.const 3
            i32.shr_u
            i32.shl
            local.tee 0
            i32.and
            br_if 0 (;@4;)
            i32.const 0
            local.get 4
            local.get 0
            i32.or
            i32.store offset=1059324
            local.get 2
            local.set 0
            br 1 (;@3;)
          end
          local.get 2
          i32.load offset=8
          local.set 0
        end
        local.get 0
        local.get 1
        i32.store offset=12
        local.get 2
        local.get 1
        i32.store offset=8
        local.get 1
        local.get 2
        i32.store offset=12
        local.get 1
        local.get 0
        i32.store offset=8
        return
      end
      i32.const 31
      local.set 2
      block  ;; label = @2
        local.get 0
        i32.const 16777215
        i32.gt_u
        br_if 0 (;@2;)
        local.get 0
        i32.const 8
        i32.shr_u
        local.tee 2
        local.get 2
        i32.const 1048320
        i32.add
        i32.const 16
        i32.shr_u
        i32.const 8
        i32.and
        local.tee 2
        i32.shl
        local.tee 4
        local.get 4
        i32.const 520192
        i32.add
        i32.const 16
        i32.shr_u
        i32.const 4
        i32.and
        local.tee 4
        i32.shl
        local.tee 6
        local.get 6
        i32.const 245760
        i32.add
        i32.const 16
        i32.shr_u
        i32.const 2
        i32.and
        local.tee 6
        i32.shl
        i32.const 15
        i32.shr_u
        local.get 2
        local.get 4
        i32.or
        local.get 6
        i32.or
        i32.sub
        local.tee 2
        i32.const 1
        i32.shl
        local.get 0
        local.get 2
        i32.const 21
        i32.add
        i32.shr_u
        i32.const 1
        i32.and
        i32.or
        i32.const 28
        i32.add
        local.set 2
      end
      local.get 1
      local.get 2
      i32.store offset=28
      local.get 1
      i64.const 0
      i64.store offset=16 align=4
      local.get 2
      i32.const 2
      i32.shl
      i32.const 1059628
      i32.add
      local.set 4
      block  ;; label = @2
        block  ;; label = @3
          i32.const 0
          i32.load offset=1059328
          local.tee 6
          i32.const 1
          local.get 2
          i32.shl
          local.tee 3
          i32.and
          br_if 0 (;@3;)
          local.get 4
          local.get 1
          i32.store
          i32.const 0
          local.get 6
          local.get 3
          i32.or
          i32.store offset=1059328
          local.get 1
          local.get 4
          i32.store offset=24
          local.get 1
          local.get 1
          i32.store offset=8
          local.get 1
          local.get 1
          i32.store offset=12
          br 1 (;@2;)
        end
        local.get 0
        i32.const 0
        i32.const 25
        local.get 2
        i32.const 1
        i32.shr_u
        i32.sub
        local.get 2
        i32.const 31
        i32.eq
        select
        i32.shl
        local.set 2
        local.get 4
        i32.load
        local.set 6
        block  ;; label = @3
          loop  ;; label = @4
            local.get 6
            local.tee 4
            i32.load offset=4
            i32.const -8
            i32.and
            local.get 0
            i32.eq
            br_if 1 (;@3;)
            local.get 2
            i32.const 29
            i32.shr_u
            local.set 6
            local.get 2
            i32.const 1
            i32.shl
            local.set 2
            local.get 4
            local.get 6
            i32.const 4
            i32.and
            i32.add
            i32.const 16
            i32.add
            local.tee 3
            i32.load
            local.tee 6
            br_if 0 (;@4;)
          end
          local.get 3
          local.get 1
          i32.store
          local.get 1
          local.get 4
          i32.store offset=24
          local.get 1
          local.get 1
          i32.store offset=12
          local.get 1
          local.get 1
          i32.store offset=8
          br 1 (;@2;)
        end
        local.get 4
        i32.load offset=8
        local.tee 0
        local.get 1
        i32.store offset=12
        local.get 4
        local.get 1
        i32.store offset=8
        local.get 1
        i32.const 0
        i32.store offset=24
        local.get 1
        local.get 4
        i32.store offset=12
        local.get 1
        local.get 0
        i32.store offset=8
      end
      i32.const 0
      i32.const 0
      i32.load offset=1059356
      i32.const -1
      i32.add
      local.tee 1
      i32.const -1
      local.get 1
      select
      i32.store offset=1059356
    end)
  (func $calloc (type 1) (param i32 i32) (result i32)
    (local i32 i64)
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        br_if 0 (;@2;)
        i32.const 0
        local.set 2
        br 1 (;@1;)
      end
      local.get 0
      i64.extend_i32_u
      local.get 1
      i64.extend_i32_u
      i64.mul
      local.tee 3
      i32.wrap_i64
      local.set 2
      local.get 1
      local.get 0
      i32.or
      i32.const 65536
      i32.lt_u
      br_if 0 (;@1;)
      i32.const -1
      local.get 2
      local.get 3
      i64.const 32
      i64.shr_u
      i32.wrap_i64
      i32.const 0
      i32.ne
      select
      local.set 2
    end
    block  ;; label = @1
      local.get 2
      call $dlmalloc
      local.tee 0
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      i32.const -4
      i32.add
      i32.load8_u
      i32.const 3
      i32.and
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      i32.const 0
      local.get 2
      call $memset
      drop
    end
    local.get 0)
  (func $realloc (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    block  ;; label = @1
      local.get 0
      br_if 0 (;@1;)
      local.get 1
      call $dlmalloc
      return
    end
    block  ;; label = @1
      local.get 1
      i32.const -64
      i32.lt_u
      br_if 0 (;@1;)
      i32.const 0
      i32.const 48
      i32.store offset=1059820
      i32.const 0
      return
    end
    i32.const 16
    local.get 1
    i32.const 19
    i32.add
    i32.const -16
    i32.and
    local.get 1
    i32.const 11
    i32.lt_u
    select
    local.set 2
    local.get 0
    i32.const -4
    i32.add
    local.tee 3
    i32.load
    local.tee 4
    i32.const -8
    i32.and
    local.set 5
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 4
          i32.const 3
          i32.and
          br_if 0 (;@3;)
          local.get 2
          i32.const 256
          i32.lt_u
          br_if 1 (;@2;)
          local.get 5
          local.get 2
          i32.const 4
          i32.or
          i32.lt_u
          br_if 1 (;@2;)
          local.get 5
          local.get 2
          i32.sub
          i32.const 0
          i32.load offset=1059804
          i32.const 1
          i32.shl
          i32.le_u
          br_if 2 (;@1;)
          br 1 (;@2;)
        end
        local.get 0
        i32.const -8
        i32.add
        local.tee 6
        local.get 5
        i32.add
        local.set 7
        block  ;; label = @3
          local.get 5
          local.get 2
          i32.lt_u
          br_if 0 (;@3;)
          local.get 5
          local.get 2
          i32.sub
          local.tee 1
          i32.const 16
          i32.lt_u
          br_if 2 (;@1;)
          local.get 3
          local.get 2
          local.get 4
          i32.const 1
          i32.and
          i32.or
          i32.const 2
          i32.or
          i32.store
          local.get 6
          local.get 2
          i32.add
          local.tee 2
          local.get 1
          i32.const 3
          i32.or
          i32.store offset=4
          local.get 7
          local.get 7
          i32.load offset=4
          i32.const 1
          i32.or
          i32.store offset=4
          local.get 2
          local.get 1
          call $dispose_chunk
          local.get 0
          return
        end
        block  ;; label = @3
          local.get 7
          i32.const 0
          i32.load offset=1059348
          i32.ne
          br_if 0 (;@3;)
          i32.const 0
          i32.load offset=1059336
          local.get 5
          i32.add
          local.tee 5
          local.get 2
          i32.le_u
          br_if 1 (;@2;)
          local.get 3
          local.get 2
          local.get 4
          i32.const 1
          i32.and
          i32.or
          i32.const 2
          i32.or
          i32.store
          i32.const 0
          local.get 6
          local.get 2
          i32.add
          local.tee 1
          i32.store offset=1059348
          i32.const 0
          local.get 5
          local.get 2
          i32.sub
          local.tee 2
          i32.store offset=1059336
          local.get 1
          local.get 2
          i32.const 1
          i32.or
          i32.store offset=4
          local.get 0
          return
        end
        block  ;; label = @3
          local.get 7
          i32.const 0
          i32.load offset=1059344
          i32.ne
          br_if 0 (;@3;)
          i32.const 0
          i32.load offset=1059332
          local.get 5
          i32.add
          local.tee 5
          local.get 2
          i32.lt_u
          br_if 1 (;@2;)
          block  ;; label = @4
            block  ;; label = @5
              local.get 5
              local.get 2
              i32.sub
              local.tee 1
              i32.const 16
              i32.lt_u
              br_if 0 (;@5;)
              local.get 3
              local.get 2
              local.get 4
              i32.const 1
              i32.and
              i32.or
              i32.const 2
              i32.or
              i32.store
              local.get 6
              local.get 2
              i32.add
              local.tee 2
              local.get 1
              i32.const 1
              i32.or
              i32.store offset=4
              local.get 6
              local.get 5
              i32.add
              local.tee 5
              local.get 1
              i32.store
              local.get 5
              local.get 5
              i32.load offset=4
              i32.const -2
              i32.and
              i32.store offset=4
              br 1 (;@4;)
            end
            local.get 3
            local.get 4
            i32.const 1
            i32.and
            local.get 5
            i32.or
            i32.const 2
            i32.or
            i32.store
            local.get 6
            local.get 5
            i32.add
            local.tee 1
            local.get 1
            i32.load offset=4
            i32.const 1
            i32.or
            i32.store offset=4
            i32.const 0
            local.set 1
            i32.const 0
            local.set 2
          end
          i32.const 0
          local.get 2
          i32.store offset=1059344
          i32.const 0
          local.get 1
          i32.store offset=1059332
          local.get 0
          return
        end
        local.get 7
        i32.load offset=4
        local.tee 8
        i32.const 2
        i32.and
        br_if 0 (;@2;)
        local.get 8
        i32.const -8
        i32.and
        local.get 5
        i32.add
        local.tee 9
        local.get 2
        i32.lt_u
        br_if 0 (;@2;)
        local.get 9
        local.get 2
        i32.sub
        local.set 10
        block  ;; label = @3
          block  ;; label = @4
            local.get 8
            i32.const 255
            i32.gt_u
            br_if 0 (;@4;)
            local.get 7
            i32.load offset=8
            local.tee 1
            local.get 8
            i32.const 3
            i32.shr_u
            local.tee 11
            i32.const 3
            i32.shl
            i32.const 1059364
            i32.add
            local.tee 8
            i32.eq
            drop
            block  ;; label = @5
              local.get 7
              i32.load offset=12
              local.tee 5
              local.get 1
              i32.ne
              br_if 0 (;@5;)
              i32.const 0
              i32.const 0
              i32.load offset=1059324
              i32.const -2
              local.get 11
              i32.rotl
              i32.and
              i32.store offset=1059324
              br 2 (;@3;)
            end
            local.get 5
            local.get 8
            i32.eq
            drop
            local.get 5
            local.get 1
            i32.store offset=8
            local.get 1
            local.get 5
            i32.store offset=12
            br 1 (;@3;)
          end
          local.get 7
          i32.load offset=24
          local.set 12
          block  ;; label = @4
            block  ;; label = @5
              local.get 7
              i32.load offset=12
              local.tee 8
              local.get 7
              i32.eq
              br_if 0 (;@5;)
              local.get 7
              i32.load offset=8
              local.tee 1
              i32.const 0
              i32.load offset=1059340
              i32.lt_u
              drop
              local.get 8
              local.get 1
              i32.store offset=8
              local.get 1
              local.get 8
              i32.store offset=12
              br 1 (;@4;)
            end
            block  ;; label = @5
              local.get 7
              i32.const 20
              i32.add
              local.tee 1
              i32.load
              local.tee 5
              br_if 0 (;@5;)
              local.get 7
              i32.const 16
              i32.add
              local.tee 1
              i32.load
              local.tee 5
              br_if 0 (;@5;)
              i32.const 0
              local.set 8
              br 1 (;@4;)
            end
            loop  ;; label = @5
              local.get 1
              local.set 11
              local.get 5
              local.tee 8
              i32.const 20
              i32.add
              local.tee 1
              i32.load
              local.tee 5
              br_if 0 (;@5;)
              local.get 8
              i32.const 16
              i32.add
              local.set 1
              local.get 8
              i32.load offset=16
              local.tee 5
              br_if 0 (;@5;)
            end
            local.get 11
            i32.const 0
            i32.store
          end
          local.get 12
          i32.eqz
          br_if 0 (;@3;)
          block  ;; label = @4
            block  ;; label = @5
              local.get 7
              local.get 7
              i32.load offset=28
              local.tee 5
              i32.const 2
              i32.shl
              i32.const 1059628
              i32.add
              local.tee 1
              i32.load
              i32.ne
              br_if 0 (;@5;)
              local.get 1
              local.get 8
              i32.store
              local.get 8
              br_if 1 (;@4;)
              i32.const 0
              i32.const 0
              i32.load offset=1059328
              i32.const -2
              local.get 5
              i32.rotl
              i32.and
              i32.store offset=1059328
              br 2 (;@3;)
            end
            local.get 12
            i32.const 16
            i32.const 20
            local.get 12
            i32.load offset=16
            local.get 7
            i32.eq
            select
            i32.add
            local.get 8
            i32.store
            local.get 8
            i32.eqz
            br_if 1 (;@3;)
          end
          local.get 8
          local.get 12
          i32.store offset=24
          block  ;; label = @4
            local.get 7
            i32.load offset=16
            local.tee 1
            i32.eqz
            br_if 0 (;@4;)
            local.get 8
            local.get 1
            i32.store offset=16
            local.get 1
            local.get 8
            i32.store offset=24
          end
          local.get 7
          i32.load offset=20
          local.tee 1
          i32.eqz
          br_if 0 (;@3;)
          local.get 8
          i32.const 20
          i32.add
          local.get 1
          i32.store
          local.get 1
          local.get 8
          i32.store offset=24
        end
        block  ;; label = @3
          local.get 10
          i32.const 15
          i32.gt_u
          br_if 0 (;@3;)
          local.get 3
          local.get 4
          i32.const 1
          i32.and
          local.get 9
          i32.or
          i32.const 2
          i32.or
          i32.store
          local.get 6
          local.get 9
          i32.add
          local.tee 1
          local.get 1
          i32.load offset=4
          i32.const 1
          i32.or
          i32.store offset=4
          local.get 0
          return
        end
        local.get 3
        local.get 2
        local.get 4
        i32.const 1
        i32.and
        i32.or
        i32.const 2
        i32.or
        i32.store
        local.get 6
        local.get 2
        i32.add
        local.tee 1
        local.get 10
        i32.const 3
        i32.or
        i32.store offset=4
        local.get 6
        local.get 9
        i32.add
        local.tee 2
        local.get 2
        i32.load offset=4
        i32.const 1
        i32.or
        i32.store offset=4
        local.get 1
        local.get 10
        call $dispose_chunk
        local.get 0
        return
      end
      block  ;; label = @2
        local.get 1
        call $dlmalloc
        local.tee 2
        br_if 0 (;@2;)
        i32.const 0
        return
      end
      local.get 2
      local.get 0
      i32.const -4
      i32.const -8
      local.get 3
      i32.load
      local.tee 5
      i32.const 3
      i32.and
      select
      local.get 5
      i32.const -8
      i32.and
      i32.add
      local.tee 5
      local.get 1
      local.get 5
      local.get 1
      i32.lt_u
      select
      call $memcpy
      local.set 1
      local.get 0
      call $dlfree
      local.get 1
      local.set 0
    end
    local.get 0)
  (func $dispose_chunk (type 3) (param i32 i32)
    (local i32 i32 i32 i32 i32 i32)
    local.get 0
    local.get 1
    i32.add
    local.set 2
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.load offset=4
        local.tee 3
        i32.const 1
        i32.and
        br_if 0 (;@2;)
        local.get 3
        i32.const 3
        i32.and
        i32.eqz
        br_if 1 (;@1;)
        local.get 0
        i32.load
        local.tee 3
        local.get 1
        i32.add
        local.set 1
        block  ;; label = @3
          block  ;; label = @4
            local.get 0
            local.get 3
            i32.sub
            local.tee 0
            i32.const 0
            i32.load offset=1059344
            i32.eq
            br_if 0 (;@4;)
            block  ;; label = @5
              local.get 3
              i32.const 255
              i32.gt_u
              br_if 0 (;@5;)
              local.get 0
              i32.load offset=8
              local.tee 4
              local.get 3
              i32.const 3
              i32.shr_u
              local.tee 5
              i32.const 3
              i32.shl
              i32.const 1059364
              i32.add
              local.tee 6
              i32.eq
              drop
              local.get 0
              i32.load offset=12
              local.tee 3
              local.get 4
              i32.ne
              br_if 2 (;@3;)
              i32.const 0
              i32.const 0
              i32.load offset=1059324
              i32.const -2
              local.get 5
              i32.rotl
              i32.and
              i32.store offset=1059324
              br 3 (;@2;)
            end
            local.get 0
            i32.load offset=24
            local.set 7
            block  ;; label = @5
              block  ;; label = @6
                local.get 0
                i32.load offset=12
                local.tee 6
                local.get 0
                i32.eq
                br_if 0 (;@6;)
                local.get 0
                i32.load offset=8
                local.tee 3
                i32.const 0
                i32.load offset=1059340
                i32.lt_u
                drop
                local.get 6
                local.get 3
                i32.store offset=8
                local.get 3
                local.get 6
                i32.store offset=12
                br 1 (;@5;)
              end
              block  ;; label = @6
                local.get 0
                i32.const 20
                i32.add
                local.tee 3
                i32.load
                local.tee 4
                br_if 0 (;@6;)
                local.get 0
                i32.const 16
                i32.add
                local.tee 3
                i32.load
                local.tee 4
                br_if 0 (;@6;)
                i32.const 0
                local.set 6
                br 1 (;@5;)
              end
              loop  ;; label = @6
                local.get 3
                local.set 5
                local.get 4
                local.tee 6
                i32.const 20
                i32.add
                local.tee 3
                i32.load
                local.tee 4
                br_if 0 (;@6;)
                local.get 6
                i32.const 16
                i32.add
                local.set 3
                local.get 6
                i32.load offset=16
                local.tee 4
                br_if 0 (;@6;)
              end
              local.get 5
              i32.const 0
              i32.store
            end
            local.get 7
            i32.eqz
            br_if 2 (;@2;)
            block  ;; label = @5
              block  ;; label = @6
                local.get 0
                local.get 0
                i32.load offset=28
                local.tee 4
                i32.const 2
                i32.shl
                i32.const 1059628
                i32.add
                local.tee 3
                i32.load
                i32.ne
                br_if 0 (;@6;)
                local.get 3
                local.get 6
                i32.store
                local.get 6
                br_if 1 (;@5;)
                i32.const 0
                i32.const 0
                i32.load offset=1059328
                i32.const -2
                local.get 4
                i32.rotl
                i32.and
                i32.store offset=1059328
                br 4 (;@2;)
              end
              local.get 7
              i32.const 16
              i32.const 20
              local.get 7
              i32.load offset=16
              local.get 0
              i32.eq
              select
              i32.add
              local.get 6
              i32.store
              local.get 6
              i32.eqz
              br_if 3 (;@2;)
            end
            local.get 6
            local.get 7
            i32.store offset=24
            block  ;; label = @5
              local.get 0
              i32.load offset=16
              local.tee 3
              i32.eqz
              br_if 0 (;@5;)
              local.get 6
              local.get 3
              i32.store offset=16
              local.get 3
              local.get 6
              i32.store offset=24
            end
            local.get 0
            i32.load offset=20
            local.tee 3
            i32.eqz
            br_if 2 (;@2;)
            local.get 6
            i32.const 20
            i32.add
            local.get 3
            i32.store
            local.get 3
            local.get 6
            i32.store offset=24
            br 2 (;@2;)
          end
          local.get 2
          i32.load offset=4
          local.tee 3
          i32.const 3
          i32.and
          i32.const 3
          i32.ne
          br_if 1 (;@2;)
          local.get 2
          local.get 3
          i32.const -2
          i32.and
          i32.store offset=4
          i32.const 0
          local.get 1
          i32.store offset=1059332
          local.get 2
          local.get 1
          i32.store
          local.get 0
          local.get 1
          i32.const 1
          i32.or
          i32.store offset=4
          return
        end
        local.get 3
        local.get 6
        i32.eq
        drop
        local.get 3
        local.get 4
        i32.store offset=8
        local.get 4
        local.get 3
        i32.store offset=12
      end
      block  ;; label = @2
        block  ;; label = @3
          local.get 2
          i32.load offset=4
          local.tee 3
          i32.const 2
          i32.and
          br_if 0 (;@3;)
          block  ;; label = @4
            local.get 2
            i32.const 0
            i32.load offset=1059348
            i32.ne
            br_if 0 (;@4;)
            i32.const 0
            local.get 0
            i32.store offset=1059348
            i32.const 0
            i32.const 0
            i32.load offset=1059336
            local.get 1
            i32.add
            local.tee 1
            i32.store offset=1059336
            local.get 0
            local.get 1
            i32.const 1
            i32.or
            i32.store offset=4
            local.get 0
            i32.const 0
            i32.load offset=1059344
            i32.ne
            br_if 3 (;@1;)
            i32.const 0
            i32.const 0
            i32.store offset=1059332
            i32.const 0
            i32.const 0
            i32.store offset=1059344
            return
          end
          block  ;; label = @4
            local.get 2
            i32.const 0
            i32.load offset=1059344
            i32.ne
            br_if 0 (;@4;)
            i32.const 0
            local.get 0
            i32.store offset=1059344
            i32.const 0
            i32.const 0
            i32.load offset=1059332
            local.get 1
            i32.add
            local.tee 1
            i32.store offset=1059332
            local.get 0
            local.get 1
            i32.const 1
            i32.or
            i32.store offset=4
            local.get 0
            local.get 1
            i32.add
            local.get 1
            i32.store
            return
          end
          local.get 3
          i32.const -8
          i32.and
          local.get 1
          i32.add
          local.set 1
          block  ;; label = @4
            block  ;; label = @5
              local.get 3
              i32.const 255
              i32.gt_u
              br_if 0 (;@5;)
              local.get 2
              i32.load offset=8
              local.tee 4
              local.get 3
              i32.const 3
              i32.shr_u
              local.tee 5
              i32.const 3
              i32.shl
              i32.const 1059364
              i32.add
              local.tee 6
              i32.eq
              drop
              block  ;; label = @6
                local.get 2
                i32.load offset=12
                local.tee 3
                local.get 4
                i32.ne
                br_if 0 (;@6;)
                i32.const 0
                i32.const 0
                i32.load offset=1059324
                i32.const -2
                local.get 5
                i32.rotl
                i32.and
                i32.store offset=1059324
                br 2 (;@4;)
              end
              local.get 3
              local.get 6
              i32.eq
              drop
              local.get 3
              local.get 4
              i32.store offset=8
              local.get 4
              local.get 3
              i32.store offset=12
              br 1 (;@4;)
            end
            local.get 2
            i32.load offset=24
            local.set 7
            block  ;; label = @5
              block  ;; label = @6
                local.get 2
                i32.load offset=12
                local.tee 6
                local.get 2
                i32.eq
                br_if 0 (;@6;)
                local.get 2
                i32.load offset=8
                local.tee 3
                i32.const 0
                i32.load offset=1059340
                i32.lt_u
                drop
                local.get 6
                local.get 3
                i32.store offset=8
                local.get 3
                local.get 6
                i32.store offset=12
                br 1 (;@5;)
              end
              block  ;; label = @6
                local.get 2
                i32.const 20
                i32.add
                local.tee 4
                i32.load
                local.tee 3
                br_if 0 (;@6;)
                local.get 2
                i32.const 16
                i32.add
                local.tee 4
                i32.load
                local.tee 3
                br_if 0 (;@6;)
                i32.const 0
                local.set 6
                br 1 (;@5;)
              end
              loop  ;; label = @6
                local.get 4
                local.set 5
                local.get 3
                local.tee 6
                i32.const 20
                i32.add
                local.tee 4
                i32.load
                local.tee 3
                br_if 0 (;@6;)
                local.get 6
                i32.const 16
                i32.add
                local.set 4
                local.get 6
                i32.load offset=16
                local.tee 3
                br_if 0 (;@6;)
              end
              local.get 5
              i32.const 0
              i32.store
            end
            local.get 7
            i32.eqz
            br_if 0 (;@4;)
            block  ;; label = @5
              block  ;; label = @6
                local.get 2
                local.get 2
                i32.load offset=28
                local.tee 4
                i32.const 2
                i32.shl
                i32.const 1059628
                i32.add
                local.tee 3
                i32.load
                i32.ne
                br_if 0 (;@6;)
                local.get 3
                local.get 6
                i32.store
                local.get 6
                br_if 1 (;@5;)
                i32.const 0
                i32.const 0
                i32.load offset=1059328
                i32.const -2
                local.get 4
                i32.rotl
                i32.and
                i32.store offset=1059328
                br 2 (;@4;)
              end
              local.get 7
              i32.const 16
              i32.const 20
              local.get 7
              i32.load offset=16
              local.get 2
              i32.eq
              select
              i32.add
              local.get 6
              i32.store
              local.get 6
              i32.eqz
              br_if 1 (;@4;)
            end
            local.get 6
            local.get 7
            i32.store offset=24
            block  ;; label = @5
              local.get 2
              i32.load offset=16
              local.tee 3
              i32.eqz
              br_if 0 (;@5;)
              local.get 6
              local.get 3
              i32.store offset=16
              local.get 3
              local.get 6
              i32.store offset=24
            end
            local.get 2
            i32.load offset=20
            local.tee 3
            i32.eqz
            br_if 0 (;@4;)
            local.get 6
            i32.const 20
            i32.add
            local.get 3
            i32.store
            local.get 3
            local.get 6
            i32.store offset=24
          end
          local.get 0
          local.get 1
          i32.add
          local.get 1
          i32.store
          local.get 0
          local.get 1
          i32.const 1
          i32.or
          i32.store offset=4
          local.get 0
          i32.const 0
          i32.load offset=1059344
          i32.ne
          br_if 1 (;@2;)
          i32.const 0
          local.get 1
          i32.store offset=1059332
          return
        end
        local.get 2
        local.get 3
        i32.const -2
        i32.and
        i32.store offset=4
        local.get 0
        local.get 1
        i32.add
        local.get 1
        i32.store
        local.get 0
        local.get 1
        i32.const 1
        i32.or
        i32.store offset=4
      end
      block  ;; label = @2
        local.get 1
        i32.const 255
        i32.gt_u
        br_if 0 (;@2;)
        local.get 1
        i32.const -8
        i32.and
        i32.const 1059364
        i32.add
        local.set 3
        block  ;; label = @3
          block  ;; label = @4
            i32.const 0
            i32.load offset=1059324
            local.tee 4
            i32.const 1
            local.get 1
            i32.const 3
            i32.shr_u
            i32.shl
            local.tee 1
            i32.and
            br_if 0 (;@4;)
            i32.const 0
            local.get 4
            local.get 1
            i32.or
            i32.store offset=1059324
            local.get 3
            local.set 1
            br 1 (;@3;)
          end
          local.get 3
          i32.load offset=8
          local.set 1
        end
        local.get 1
        local.get 0
        i32.store offset=12
        local.get 3
        local.get 0
        i32.store offset=8
        local.get 0
        local.get 3
        i32.store offset=12
        local.get 0
        local.get 1
        i32.store offset=8
        return
      end
      i32.const 31
      local.set 3
      block  ;; label = @2
        local.get 1
        i32.const 16777215
        i32.gt_u
        br_if 0 (;@2;)
        local.get 1
        i32.const 8
        i32.shr_u
        local.tee 3
        local.get 3
        i32.const 1048320
        i32.add
        i32.const 16
        i32.shr_u
        i32.const 8
        i32.and
        local.tee 3
        i32.shl
        local.tee 4
        local.get 4
        i32.const 520192
        i32.add
        i32.const 16
        i32.shr_u
        i32.const 4
        i32.and
        local.tee 4
        i32.shl
        local.tee 6
        local.get 6
        i32.const 245760
        i32.add
        i32.const 16
        i32.shr_u
        i32.const 2
        i32.and
        local.tee 6
        i32.shl
        i32.const 15
        i32.shr_u
        local.get 3
        local.get 4
        i32.or
        local.get 6
        i32.or
        i32.sub
        local.tee 3
        i32.const 1
        i32.shl
        local.get 1
        local.get 3
        i32.const 21
        i32.add
        i32.shr_u
        i32.const 1
        i32.and
        i32.or
        i32.const 28
        i32.add
        local.set 3
      end
      local.get 0
      local.get 3
      i32.store offset=28
      local.get 0
      i64.const 0
      i64.store offset=16 align=4
      local.get 3
      i32.const 2
      i32.shl
      i32.const 1059628
      i32.add
      local.set 4
      block  ;; label = @2
        i32.const 0
        i32.load offset=1059328
        local.tee 6
        i32.const 1
        local.get 3
        i32.shl
        local.tee 2
        i32.and
        br_if 0 (;@2;)
        local.get 4
        local.get 0
        i32.store
        i32.const 0
        local.get 6
        local.get 2
        i32.or
        i32.store offset=1059328
        local.get 0
        local.get 4
        i32.store offset=24
        local.get 0
        local.get 0
        i32.store offset=8
        local.get 0
        local.get 0
        i32.store offset=12
        return
      end
      local.get 1
      i32.const 0
      i32.const 25
      local.get 3
      i32.const 1
      i32.shr_u
      i32.sub
      local.get 3
      i32.const 31
      i32.eq
      select
      i32.shl
      local.set 3
      local.get 4
      i32.load
      local.set 6
      block  ;; label = @2
        loop  ;; label = @3
          local.get 6
          local.tee 4
          i32.load offset=4
          i32.const -8
          i32.and
          local.get 1
          i32.eq
          br_if 1 (;@2;)
          local.get 3
          i32.const 29
          i32.shr_u
          local.set 6
          local.get 3
          i32.const 1
          i32.shl
          local.set 3
          local.get 4
          local.get 6
          i32.const 4
          i32.and
          i32.add
          i32.const 16
          i32.add
          local.tee 2
          i32.load
          local.tee 6
          br_if 0 (;@3;)
        end
        local.get 2
        local.get 0
        i32.store
        local.get 0
        local.get 4
        i32.store offset=24
        local.get 0
        local.get 0
        i32.store offset=12
        local.get 0
        local.get 0
        i32.store offset=8
        return
      end
      local.get 4
      i32.load offset=8
      local.tee 1
      local.get 0
      i32.store offset=12
      local.get 4
      local.get 0
      i32.store offset=8
      local.get 0
      i32.const 0
      i32.store offset=24
      local.get 0
      local.get 4
      i32.store offset=12
      local.get 0
      local.get 1
      i32.store offset=8
    end)
  (func $internal_memalign (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.const 16
        local.get 0
        i32.const 16
        i32.gt_u
        select
        local.tee 2
        local.get 2
        i32.const -1
        i32.add
        i32.and
        br_if 0 (;@2;)
        local.get 2
        local.set 0
        br 1 (;@1;)
      end
      i32.const 32
      local.set 3
      loop  ;; label = @2
        local.get 3
        local.tee 0
        i32.const 1
        i32.shl
        local.set 3
        local.get 0
        local.get 2
        i32.lt_u
        br_if 0 (;@2;)
      end
    end
    block  ;; label = @1
      i32.const -64
      local.get 0
      i32.sub
      local.get 1
      i32.gt_u
      br_if 0 (;@1;)
      i32.const 0
      i32.const 48
      i32.store offset=1059820
      i32.const 0
      return
    end
    block  ;; label = @1
      local.get 0
      i32.const 16
      local.get 1
      i32.const 19
      i32.add
      i32.const -16
      i32.and
      local.get 1
      i32.const 11
      i32.lt_u
      select
      local.tee 1
      i32.add
      i32.const 12
      i32.add
      call $dlmalloc
      local.tee 3
      br_if 0 (;@1;)
      i32.const 0
      return
    end
    local.get 3
    i32.const -8
    i32.add
    local.set 2
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.const -1
        i32.add
        local.get 3
        i32.and
        br_if 0 (;@2;)
        local.get 2
        local.set 0
        br 1 (;@1;)
      end
      local.get 3
      i32.const -4
      i32.add
      local.tee 4
      i32.load
      local.tee 5
      i32.const -8
      i32.and
      local.get 3
      local.get 0
      i32.add
      i32.const -1
      i32.add
      i32.const 0
      local.get 0
      i32.sub
      i32.and
      i32.const -8
      i32.add
      local.tee 3
      i32.const 0
      local.get 0
      local.get 3
      local.get 2
      i32.sub
      i32.const 15
      i32.gt_u
      select
      i32.add
      local.tee 0
      local.get 2
      i32.sub
      local.tee 3
      i32.sub
      local.set 6
      block  ;; label = @2
        local.get 5
        i32.const 3
        i32.and
        br_if 0 (;@2;)
        local.get 0
        local.get 6
        i32.store offset=4
        local.get 0
        local.get 2
        i32.load
        local.get 3
        i32.add
        i32.store
        br 1 (;@1;)
      end
      local.get 0
      local.get 6
      local.get 0
      i32.load offset=4
      i32.const 1
      i32.and
      i32.or
      i32.const 2
      i32.or
      i32.store offset=4
      local.get 0
      local.get 6
      i32.add
      local.tee 6
      local.get 6
      i32.load offset=4
      i32.const 1
      i32.or
      i32.store offset=4
      local.get 4
      local.get 3
      local.get 4
      i32.load
      i32.const 1
      i32.and
      i32.or
      i32.const 2
      i32.or
      i32.store
      local.get 2
      local.get 3
      i32.add
      local.tee 6
      local.get 6
      i32.load offset=4
      i32.const 1
      i32.or
      i32.store offset=4
      local.get 2
      local.get 3
      call $dispose_chunk
    end
    block  ;; label = @1
      local.get 0
      i32.load offset=4
      local.tee 3
      i32.const 3
      i32.and
      i32.eqz
      br_if 0 (;@1;)
      local.get 3
      i32.const -8
      i32.and
      local.tee 2
      local.get 1
      i32.const 16
      i32.add
      i32.le_u
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      local.get 3
      i32.const 1
      i32.and
      i32.or
      i32.const 2
      i32.or
      i32.store offset=4
      local.get 0
      local.get 1
      i32.add
      local.tee 3
      local.get 2
      local.get 1
      i32.sub
      local.tee 1
      i32.const 3
      i32.or
      i32.store offset=4
      local.get 0
      local.get 2
      i32.add
      local.tee 2
      local.get 2
      i32.load offset=4
      i32.const 1
      i32.or
      i32.store offset=4
      local.get 3
      local.get 1
      call $dispose_chunk
    end
    local.get 0
    i32.const 8
    i32.add)
  (func $aligned_alloc (type 1) (param i32 i32) (result i32)
    block  ;; label = @1
      local.get 0
      i32.const 16
      i32.gt_u
      br_if 0 (;@1;)
      local.get 1
      call $dlmalloc
      return
    end
    local.get 0
    local.get 1
    call $internal_memalign)
  (func $abort (type 14)
    unreachable
    unreachable)
  (func $getcwd (type 1) (param i32 i32) (result i32)
    (local i32)
    i32.const 0
    i32.load offset=1059244
    local.set 2
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        br_if 0 (;@2;)
        local.get 2
        call $strdup
        local.tee 0
        br_if 1 (;@1;)
        i32.const 0
        i32.const 48
        i32.store offset=1059820
        i32.const 0
        return
      end
      block  ;; label = @2
        local.get 2
        call $strlen
        i32.const 1
        i32.add
        local.get 1
        i32.gt_u
        br_if 0 (;@2;)
        local.get 0
        local.get 2
        call $strcpy
        return
      end
      i32.const 0
      local.set 0
      i32.const 0
      i32.const 68
      i32.store offset=1059820
    end
    local.get 0)
  (func $sbrk (type 5) (param i32) (result i32)
    block  ;; label = @1
      local.get 0
      br_if 0 (;@1;)
      memory.size
      i32.const 16
      i32.shl
      return
    end
    block  ;; label = @1
      local.get 0
      i32.const 65535
      i32.and
      br_if 0 (;@1;)
      local.get 0
      i32.const -1
      i32.le_s
      br_if 0 (;@1;)
      block  ;; label = @2
        local.get 0
        i32.const 16
        i32.shr_u
        memory.grow
        local.tee 0
        i32.const -1
        i32.ne
        br_if 0 (;@2;)
        i32.const 0
        i32.const 48
        i32.store offset=1059820
        i32.const -1
        return
      end
      local.get 0
      i32.const 16
      i32.shl
      return
    end
    call $abort
    unreachable)
  (func $__wasi_environ_get (type 1) (param i32 i32) (result i32)
    local.get 0
    local.get 1
    call $__imported_wasi_snapshot_preview1_environ_get
    i32.const 65535
    i32.and)
  (func $__wasi_environ_sizes_get (type 1) (param i32 i32) (result i32)
    local.get 0
    local.get 1
    call $__imported_wasi_snapshot_preview1_environ_sizes_get
    i32.const 65535
    i32.and)
  (func $__wasi_proc_exit (type 2) (param i32)
    local.get 0
    call $__imported_wasi_snapshot_preview1_proc_exit
    unreachable)
  (func $_Exit (type 2) (param i32)
    local.get 0
    call $__wasi_proc_exit
    unreachable)
  (func $__wasilibc_ensure_environ (type 14)
    block  ;; label = @1
      i32.const 0
      i32.load offset=1059248
      i32.const -1
      i32.ne
      br_if 0 (;@1;)
      call $__wasilibc_initialize_environ
    end)
  (func $__wasilibc_initialize_environ (type 14)
    (local i32 i32 i32)
    global.get $__stack_pointer
    i32.const 16
    i32.sub
    local.tee 0
    global.set $__stack_pointer
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.const 12
        i32.add
        local.get 0
        i32.const 8
        i32.add
        call $__wasi_environ_sizes_get
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 0
          i32.load offset=12
          local.tee 1
          br_if 0 (;@3;)
          i32.const 1059824
          local.set 1
          br 2 (;@1;)
        end
        block  ;; label = @3
          block  ;; label = @4
            local.get 1
            i32.const 1
            i32.add
            local.tee 1
            i32.eqz
            br_if 0 (;@4;)
            local.get 0
            i32.load offset=8
            call $malloc
            local.tee 2
            i32.eqz
            br_if 0 (;@4;)
            local.get 1
            i32.const 4
            call $calloc
            local.tee 1
            br_if 1 (;@3;)
            local.get 2
            call $free
          end
          i32.const 70
          call $_Exit
          unreachable
        end
        local.get 1
        local.get 2
        call $__wasi_environ_get
        i32.eqz
        br_if 1 (;@1;)
        local.get 2
        call $free
        local.get 1
        call $free
      end
      i32.const 71
      call $_Exit
      unreachable
    end
    i32.const 0
    local.get 1
    i32.store offset=1059248
    local.get 0
    i32.const 16
    i32.add
    global.set $__stack_pointer)
  (func $getenv (type 5) (param i32) (result i32)
    (local i32 i32 i32 i32)
    call $__wasilibc_ensure_environ
    block  ;; label = @1
      local.get 0
      i32.const 61
      call $__strchrnul
      local.tee 1
      local.get 0
      i32.ne
      br_if 0 (;@1;)
      i32.const 0
      return
    end
    i32.const 0
    local.set 2
    block  ;; label = @1
      local.get 0
      local.get 1
      local.get 0
      i32.sub
      local.tee 3
      i32.add
      i32.load8_u
      br_if 0 (;@1;)
      i32.const 0
      i32.load offset=1059248
      local.tee 4
      i32.eqz
      br_if 0 (;@1;)
      local.get 4
      i32.load
      local.tee 1
      i32.eqz
      br_if 0 (;@1;)
      local.get 4
      i32.const 4
      i32.add
      local.set 4
      block  ;; label = @2
        loop  ;; label = @3
          block  ;; label = @4
            local.get 0
            local.get 1
            local.get 3
            call $strncmp
            br_if 0 (;@4;)
            local.get 1
            local.get 3
            i32.add
            local.tee 1
            i32.load8_u
            i32.const 61
            i32.eq
            br_if 2 (;@2;)
          end
          local.get 4
          i32.load
          local.set 1
          local.get 4
          i32.const 4
          i32.add
          local.set 4
          local.get 1
          br_if 0 (;@3;)
          br 2 (;@1;)
        end
      end
      local.get 1
      i32.const 1
      i32.add
      local.set 2
    end
    local.get 2)
  (func $strdup (type 5) (param i32) (result i32)
    (local i32 i32)
    block  ;; label = @1
      local.get 0
      call $strlen
      i32.const 1
      i32.add
      local.tee 1
      call $malloc
      local.tee 2
      i32.eqz
      br_if 0 (;@1;)
      local.get 2
      local.get 0
      local.get 1
      call $memcpy
      drop
    end
    local.get 2)
  (func $memmove (type 0) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 2
          i32.const 33
          i32.ge_u
          br_if 0 (;@3;)
          local.get 0
          local.get 1
          i32.eq
          br_if 2 (;@1;)
          local.get 1
          local.get 0
          local.get 2
          i32.add
          local.tee 3
          i32.sub
          i32.const 0
          local.get 2
          i32.const 1
          i32.shl
          i32.sub
          i32.gt_u
          br_if 1 (;@2;)
        end
        local.get 0
        local.get 1
        local.get 2
        memory.copy
        br 1 (;@1;)
      end
      local.get 1
      local.get 0
      i32.xor
      i32.const 3
      i32.and
      local.set 4
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            local.get 0
            local.get 1
            i32.ge_u
            br_if 0 (;@4;)
            block  ;; label = @5
              local.get 4
              i32.eqz
              br_if 0 (;@5;)
              local.get 2
              local.set 4
              local.get 0
              local.set 3
              br 3 (;@2;)
            end
            block  ;; label = @5
              local.get 0
              i32.const 3
              i32.and
              br_if 0 (;@5;)
              local.get 2
              local.set 4
              local.get 0
              local.set 3
              br 2 (;@3;)
            end
            local.get 2
            i32.eqz
            br_if 3 (;@1;)
            local.get 0
            local.get 1
            i32.load8_u
            i32.store8
            local.get 2
            i32.const -1
            i32.add
            local.set 4
            block  ;; label = @5
              local.get 0
              i32.const 1
              i32.add
              local.tee 3
              i32.const 3
              i32.and
              br_if 0 (;@5;)
              local.get 1
              i32.const 1
              i32.add
              local.set 1
              br 2 (;@3;)
            end
            local.get 4
            i32.eqz
            br_if 3 (;@1;)
            local.get 0
            local.get 1
            i32.load8_u offset=1
            i32.store8 offset=1
            local.get 2
            i32.const -2
            i32.add
            local.set 4
            block  ;; label = @5
              local.get 0
              i32.const 2
              i32.add
              local.tee 3
              i32.const 3
              i32.and
              br_if 0 (;@5;)
              local.get 1
              i32.const 2
              i32.add
              local.set 1
              br 2 (;@3;)
            end
            local.get 4
            i32.eqz
            br_if 3 (;@1;)
            local.get 0
            local.get 1
            i32.load8_u offset=2
            i32.store8 offset=2
            local.get 2
            i32.const -3
            i32.add
            local.set 4
            block  ;; label = @5
              local.get 0
              i32.const 3
              i32.add
              local.tee 3
              i32.const 3
              i32.and
              br_if 0 (;@5;)
              local.get 1
              i32.const 3
              i32.add
              local.set 1
              br 2 (;@3;)
            end
            local.get 4
            i32.eqz
            br_if 3 (;@1;)
            local.get 0
            local.get 1
            i32.load8_u offset=3
            i32.store8 offset=3
            local.get 0
            i32.const 4
            i32.add
            local.set 3
            local.get 1
            i32.const 4
            i32.add
            local.set 1
            local.get 2
            i32.const -4
            i32.add
            local.set 4
            br 1 (;@3;)
          end
          block  ;; label = @4
            local.get 4
            br_if 0 (;@4;)
            block  ;; label = @5
              local.get 3
              i32.const 3
              i32.and
              i32.eqz
              br_if 0 (;@5;)
              local.get 2
              i32.eqz
              br_if 4 (;@1;)
              local.get 0
              local.get 2
              i32.const -1
              i32.add
              local.tee 3
              i32.add
              local.tee 4
              local.get 1
              local.get 3
              i32.add
              i32.load8_u
              i32.store8
              block  ;; label = @6
                local.get 4
                i32.const 3
                i32.and
                br_if 0 (;@6;)
                local.get 3
                local.set 2
                br 1 (;@5;)
              end
              local.get 3
              i32.eqz
              br_if 4 (;@1;)
              local.get 0
              local.get 2
              i32.const -2
              i32.add
              local.tee 3
              i32.add
              local.tee 4
              local.get 1
              local.get 3
              i32.add
              i32.load8_u
              i32.store8
              block  ;; label = @6
                local.get 4
                i32.const 3
                i32.and
                br_if 0 (;@6;)
                local.get 3
                local.set 2
                br 1 (;@5;)
              end
              local.get 3
              i32.eqz
              br_if 4 (;@1;)
              local.get 0
              local.get 2
              i32.const -3
              i32.add
              local.tee 3
              i32.add
              local.tee 4
              local.get 1
              local.get 3
              i32.add
              i32.load8_u
              i32.store8
              block  ;; label = @6
                local.get 4
                i32.const 3
                i32.and
                br_if 0 (;@6;)
                local.get 3
                local.set 2
                br 1 (;@5;)
              end
              local.get 3
              i32.eqz
              br_if 4 (;@1;)
              local.get 0
              local.get 2
              i32.const -4
              i32.add
              local.tee 2
              i32.add
              local.get 1
              local.get 2
              i32.add
              i32.load8_u
              i32.store8
            end
            local.get 2
            i32.const 4
            i32.lt_u
            br_if 0 (;@4;)
            block  ;; label = @5
              local.get 2
              i32.const -4
              i32.add
              local.tee 5
              i32.const 2
              i32.shr_u
              i32.const 1
              i32.add
              i32.const 3
              i32.and
              local.tee 3
              i32.eqz
              br_if 0 (;@5;)
              local.get 1
              i32.const -4
              i32.add
              local.set 4
              local.get 0
              i32.const -4
              i32.add
              local.set 6
              loop  ;; label = @6
                local.get 6
                local.get 2
                i32.add
                local.get 4
                local.get 2
                i32.add
                i32.load
                i32.store
                local.get 2
                i32.const -4
                i32.add
                local.set 2
                local.get 3
                i32.const -1
                i32.add
                local.tee 3
                br_if 0 (;@6;)
              end
            end
            local.get 5
            i32.const 12
            i32.lt_u
            br_if 0 (;@4;)
            local.get 1
            i32.const -16
            i32.add
            local.set 6
            local.get 0
            i32.const -16
            i32.add
            local.set 5
            loop  ;; label = @5
              local.get 5
              local.get 2
              i32.add
              local.tee 3
              i32.const 12
              i32.add
              local.get 6
              local.get 2
              i32.add
              local.tee 4
              i32.const 12
              i32.add
              i32.load
              i32.store
              local.get 3
              i32.const 8
              i32.add
              local.get 4
              i32.const 8
              i32.add
              i32.load
              i32.store
              local.get 3
              i32.const 4
              i32.add
              local.get 4
              i32.const 4
              i32.add
              i32.load
              i32.store
              local.get 3
              local.get 4
              i32.load
              i32.store
              local.get 2
              i32.const -16
              i32.add
              local.tee 2
              i32.const 3
              i32.gt_u
              br_if 0 (;@5;)
            end
          end
          local.get 2
          i32.eqz
          br_if 2 (;@1;)
          local.get 2
          i32.const -1
          i32.add
          local.set 5
          block  ;; label = @4
            local.get 2
            i32.const 3
            i32.and
            local.tee 3
            i32.eqz
            br_if 0 (;@4;)
            local.get 1
            i32.const -1
            i32.add
            local.set 4
            local.get 0
            i32.const -1
            i32.add
            local.set 6
            loop  ;; label = @5
              local.get 6
              local.get 2
              i32.add
              local.get 4
              local.get 2
              i32.add
              i32.load8_u
              i32.store8
              local.get 2
              i32.const -1
              i32.add
              local.set 2
              local.get 3
              i32.const -1
              i32.add
              local.tee 3
              br_if 0 (;@5;)
            end
          end
          local.get 5
          i32.const 3
          i32.lt_u
          br_if 2 (;@1;)
          local.get 1
          i32.const -4
          i32.add
          local.set 4
          local.get 0
          i32.const -4
          i32.add
          local.set 6
          loop  ;; label = @4
            local.get 6
            local.get 2
            i32.add
            local.tee 1
            i32.const 3
            i32.add
            local.get 4
            local.get 2
            i32.add
            local.tee 3
            i32.const 3
            i32.add
            i32.load8_u
            i32.store8
            local.get 1
            i32.const 2
            i32.add
            local.get 3
            i32.const 2
            i32.add
            i32.load8_u
            i32.store8
            local.get 1
            i32.const 1
            i32.add
            local.get 3
            i32.const 1
            i32.add
            i32.load8_u
            i32.store8
            local.get 1
            local.get 3
            i32.load8_u
            i32.store8
            local.get 2
            i32.const -4
            i32.add
            local.tee 2
            br_if 0 (;@4;)
            br 3 (;@1;)
          end
        end
        local.get 4
        i32.const 4
        i32.lt_u
        br_if 0 (;@2;)
        block  ;; label = @3
          local.get 4
          i32.const -4
          i32.add
          local.tee 6
          i32.const 2
          i32.shr_u
          i32.const 1
          i32.add
          i32.const 7
          i32.and
          local.tee 2
          i32.eqz
          br_if 0 (;@3;)
          loop  ;; label = @4
            local.get 3
            local.get 1
            i32.load
            i32.store
            local.get 1
            i32.const 4
            i32.add
            local.set 1
            local.get 3
            i32.const 4
            i32.add
            local.set 3
            local.get 4
            i32.const -4
            i32.add
            local.set 4
            local.get 2
            i32.const -1
            i32.add
            local.tee 2
            br_if 0 (;@4;)
          end
        end
        local.get 6
        i32.const 28
        i32.lt_u
        br_if 0 (;@2;)
        loop  ;; label = @3
          local.get 3
          local.get 1
          i32.load
          i32.store
          local.get 3
          local.get 1
          i32.load offset=4
          i32.store offset=4
          local.get 3
          local.get 1
          i32.load offset=8
          i32.store offset=8
          local.get 3
          local.get 1
          i32.load offset=12
          i32.store offset=12
          local.get 3
          local.get 1
          i32.load offset=16
          i32.store offset=16
          local.get 3
          local.get 1
          i32.load offset=20
          i32.store offset=20
          local.get 3
          local.get 1
          i32.load offset=24
          i32.store offset=24
          local.get 3
          local.get 1
          i32.load offset=28
          i32.store offset=28
          local.get 1
          i32.const 32
          i32.add
          local.set 1
          local.get 3
          i32.const 32
          i32.add
          local.set 3
          local.get 4
          i32.const -32
          i32.add
          local.tee 4
          i32.const 3
          i32.gt_u
          br_if 0 (;@3;)
        end
      end
      local.get 4
      i32.eqz
      br_if 0 (;@1;)
      local.get 4
      i32.const -1
      i32.add
      local.set 6
      block  ;; label = @2
        local.get 4
        i32.const 7
        i32.and
        local.tee 2
        i32.eqz
        br_if 0 (;@2;)
        loop  ;; label = @3
          local.get 3
          local.get 1
          i32.load8_u
          i32.store8
          local.get 4
          i32.const -1
          i32.add
          local.set 4
          local.get 3
          i32.const 1
          i32.add
          local.set 3
          local.get 1
          i32.const 1
          i32.add
          local.set 1
          local.get 2
          i32.const -1
          i32.add
          local.tee 2
          br_if 0 (;@3;)
        end
      end
      local.get 6
      i32.const 7
      i32.lt_u
      br_if 0 (;@1;)
      loop  ;; label = @2
        local.get 3
        local.get 1
        i32.load8_u
        i32.store8
        local.get 3
        local.get 1
        i32.load8_u offset=1
        i32.store8 offset=1
        local.get 3
        local.get 1
        i32.load8_u offset=2
        i32.store8 offset=2
        local.get 3
        local.get 1
        i32.load8_u offset=3
        i32.store8 offset=3
        local.get 3
        local.get 1
        i32.load8_u offset=4
        i32.store8 offset=4
        local.get 3
        local.get 1
        i32.load8_u offset=5
        i32.store8 offset=5
        local.get 3
        local.get 1
        i32.load8_u offset=6
        i32.store8 offset=6
        local.get 3
        local.get 1
        i32.load8_u offset=7
        i32.store8 offset=7
        local.get 3
        i32.const 8
        i32.add
        local.set 3
        local.get 1
        i32.const 8
        i32.add
        local.set 1
        local.get 4
        i32.const -8
        i32.add
        local.tee 4
        br_if 0 (;@2;)
      end
    end
    local.get 0)
  (func $memcpy (type 0) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 2
          i32.const 32
          i32.gt_u
          br_if 0 (;@3;)
          local.get 1
          i32.const 3
          i32.and
          i32.eqz
          br_if 1 (;@2;)
          local.get 2
          i32.eqz
          br_if 1 (;@2;)
          local.get 0
          local.get 1
          i32.load8_u
          i32.store8
          local.get 2
          i32.const -1
          i32.add
          local.set 3
          local.get 0
          i32.const 1
          i32.add
          local.set 4
          local.get 1
          i32.const 1
          i32.add
          local.tee 5
          i32.const 3
          i32.and
          i32.eqz
          br_if 2 (;@1;)
          local.get 3
          i32.eqz
          br_if 2 (;@1;)
          local.get 0
          local.get 1
          i32.load8_u offset=1
          i32.store8 offset=1
          local.get 2
          i32.const -2
          i32.add
          local.set 3
          local.get 0
          i32.const 2
          i32.add
          local.set 4
          local.get 1
          i32.const 2
          i32.add
          local.tee 5
          i32.const 3
          i32.and
          i32.eqz
          br_if 2 (;@1;)
          local.get 3
          i32.eqz
          br_if 2 (;@1;)
          local.get 0
          local.get 1
          i32.load8_u offset=2
          i32.store8 offset=2
          local.get 2
          i32.const -3
          i32.add
          local.set 3
          local.get 0
          i32.const 3
          i32.add
          local.set 4
          local.get 1
          i32.const 3
          i32.add
          local.tee 5
          i32.const 3
          i32.and
          i32.eqz
          br_if 2 (;@1;)
          local.get 3
          i32.eqz
          br_if 2 (;@1;)
          local.get 0
          local.get 1
          i32.load8_u offset=3
          i32.store8 offset=3
          local.get 2
          i32.const -4
          i32.add
          local.set 3
          local.get 0
          i32.const 4
          i32.add
          local.set 4
          local.get 1
          i32.const 4
          i32.add
          local.set 5
          br 2 (;@1;)
        end
        local.get 0
        local.get 1
        local.get 2
        memory.copy
        local.get 0
        return
      end
      local.get 2
      local.set 3
      local.get 0
      local.set 4
      local.get 1
      local.set 5
    end
    block  ;; label = @1
      block  ;; label = @2
        local.get 4
        i32.const 3
        i32.and
        local.tee 2
        br_if 0 (;@2;)
        block  ;; label = @3
          block  ;; label = @4
            local.get 3
            i32.const 16
            i32.ge_u
            br_if 0 (;@4;)
            local.get 3
            local.set 2
            br 1 (;@3;)
          end
          block  ;; label = @4
            local.get 3
            i32.const -16
            i32.add
            local.tee 2
            i32.const 16
            i32.and
            br_if 0 (;@4;)
            local.get 4
            local.get 5
            i64.load align=4
            i64.store align=4
            local.get 4
            local.get 5
            i64.load offset=8 align=4
            i64.store offset=8 align=4
            local.get 4
            i32.const 16
            i32.add
            local.set 4
            local.get 5
            i32.const 16
            i32.add
            local.set 5
            local.get 2
            local.set 3
          end
          local.get 2
          i32.const 16
          i32.lt_u
          br_if 0 (;@3;)
          local.get 3
          local.set 2
          loop  ;; label = @4
            local.get 4
            local.get 5
            i64.load align=4
            i64.store align=4
            local.get 4
            local.get 5
            i64.load offset=8 align=4
            i64.store offset=8 align=4
            local.get 4
            local.get 5
            i64.load offset=16 align=4
            i64.store offset=16 align=4
            local.get 4
            local.get 5
            i64.load offset=24 align=4
            i64.store offset=24 align=4
            local.get 4
            i32.const 32
            i32.add
            local.set 4
            local.get 5
            i32.const 32
            i32.add
            local.set 5
            local.get 2
            i32.const -32
            i32.add
            local.tee 2
            i32.const 15
            i32.gt_u
            br_if 0 (;@4;)
          end
        end
        block  ;; label = @3
          local.get 2
          i32.const 8
          i32.and
          i32.eqz
          br_if 0 (;@3;)
          local.get 4
          local.get 5
          i64.load align=4
          i64.store align=4
          local.get 5
          i32.const 8
          i32.add
          local.set 5
          local.get 4
          i32.const 8
          i32.add
          local.set 4
        end
        block  ;; label = @3
          local.get 2
          i32.const 4
          i32.and
          i32.eqz
          br_if 0 (;@3;)
          local.get 4
          local.get 5
          i32.load
          i32.store
          local.get 5
          i32.const 4
          i32.add
          local.set 5
          local.get 4
          i32.const 4
          i32.add
          local.set 4
        end
        block  ;; label = @3
          local.get 2
          i32.const 2
          i32.and
          i32.eqz
          br_if 0 (;@3;)
          local.get 4
          local.get 5
          i32.load16_u align=1
          i32.store16 align=1
          local.get 4
          i32.const 2
          i32.add
          local.set 4
          local.get 5
          i32.const 2
          i32.add
          local.set 5
        end
        local.get 2
        i32.const 1
        i32.and
        i32.eqz
        br_if 1 (;@1;)
        local.get 4
        local.get 5
        i32.load8_u
        i32.store8
        local.get 0
        return
      end
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            block  ;; label = @5
              block  ;; label = @6
                local.get 3
                i32.const 32
                i32.lt_u
                br_if 0 (;@6;)
                block  ;; label = @7
                  block  ;; label = @8
                    local.get 2
                    i32.const -1
                    i32.add
                    br_table 3 (;@5;) 0 (;@8;) 1 (;@7;) 7 (;@1;)
                  end
                  local.get 4
                  local.get 5
                  i32.load
                  i32.store16 align=1
                  local.get 4
                  local.get 5
                  i32.const 2
                  i32.add
                  i32.load align=2
                  i32.store offset=2
                  local.get 4
                  local.get 5
                  i32.const 6
                  i32.add
                  i64.load align=2
                  i64.store offset=6 align=4
                  local.get 4
                  i32.const 18
                  i32.add
                  local.set 2
                  local.get 5
                  i32.const 18
                  i32.add
                  local.set 1
                  i32.const 14
                  local.set 6
                  local.get 5
                  i32.const 14
                  i32.add
                  i32.load align=2
                  local.set 5
                  i32.const 14
                  local.set 3
                  br 3 (;@4;)
                end
                local.get 4
                local.get 5
                i32.load
                i32.store8
                local.get 4
                local.get 5
                i32.const 1
                i32.add
                i32.load align=1
                i32.store offset=1
                local.get 4
                local.get 5
                i32.const 5
                i32.add
                i64.load align=1
                i64.store offset=5 align=4
                local.get 4
                i32.const 17
                i32.add
                local.set 2
                local.get 5
                i32.const 17
                i32.add
                local.set 1
                i32.const 13
                local.set 6
                local.get 5
                i32.const 13
                i32.add
                i32.load align=1
                local.set 5
                i32.const 15
                local.set 3
                br 2 (;@4;)
              end
              block  ;; label = @6
                block  ;; label = @7
                  local.get 3
                  i32.const 16
                  i32.and
                  br_if 0 (;@7;)
                  local.get 4
                  local.set 2
                  local.get 5
                  local.set 1
                  br 1 (;@6;)
                end
                local.get 4
                local.get 5
                i32.load8_u
                i32.store8
                local.get 4
                local.get 5
                i32.load offset=1 align=1
                i32.store offset=1 align=1
                local.get 4
                local.get 5
                i64.load offset=5 align=1
                i64.store offset=5 align=1
                local.get 4
                local.get 5
                i32.load16_u offset=13 align=1
                i32.store16 offset=13 align=1
                local.get 4
                local.get 5
                i32.load8_u offset=15
                i32.store8 offset=15
                local.get 4
                i32.const 16
                i32.add
                local.set 2
                local.get 5
                i32.const 16
                i32.add
                local.set 1
              end
              local.get 3
              i32.const 8
              i32.and
              br_if 2 (;@3;)
              br 3 (;@2;)
            end
            local.get 4
            local.get 5
            i32.load
            local.tee 2
            i32.store8
            local.get 4
            local.get 2
            i32.const 16
            i32.shr_u
            i32.store8 offset=2
            local.get 4
            local.get 2
            i32.const 8
            i32.shr_u
            i32.store8 offset=1
            local.get 4
            local.get 5
            i32.const 3
            i32.add
            i32.load align=1
            i32.store offset=3
            local.get 4
            local.get 5
            i32.const 7
            i32.add
            i64.load align=1
            i64.store offset=7 align=4
            local.get 4
            i32.const 19
            i32.add
            local.set 2
            local.get 5
            i32.const 19
            i32.add
            local.set 1
            i32.const 15
            local.set 6
            local.get 5
            i32.const 15
            i32.add
            i32.load align=1
            local.set 5
            i32.const 13
            local.set 3
          end
          local.get 4
          local.get 6
          i32.add
          local.get 5
          i32.store
        end
        local.get 2
        local.get 1
        i64.load align=1
        i64.store align=1
        local.get 2
        i32.const 8
        i32.add
        local.set 2
        local.get 1
        i32.const 8
        i32.add
        local.set 1
      end
      block  ;; label = @2
        local.get 3
        i32.const 4
        i32.and
        i32.eqz
        br_if 0 (;@2;)
        local.get 2
        local.get 1
        i32.load align=1
        i32.store align=1
        local.get 2
        i32.const 4
        i32.add
        local.set 2
        local.get 1
        i32.const 4
        i32.add
        local.set 1
      end
      block  ;; label = @2
        local.get 3
        i32.const 2
        i32.and
        i32.eqz
        br_if 0 (;@2;)
        local.get 2
        local.get 1
        i32.load16_u align=1
        i32.store16 align=1
        local.get 2
        i32.const 2
        i32.add
        local.set 2
        local.get 1
        i32.const 2
        i32.add
        local.set 1
      end
      local.get 3
      i32.const 1
      i32.and
      i32.eqz
      br_if 0 (;@1;)
      local.get 2
      local.get 1
      i32.load8_u
      i32.store8
    end
    local.get 0)
  (func $__strchrnul (type 1) (param i32 i32) (result i32)
    (local i32 i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          block  ;; label = @4
            local.get 1
            i32.const 255
            i32.and
            local.tee 2
            i32.eqz
            br_if 0 (;@4;)
            local.get 0
            i32.const 3
            i32.and
            i32.eqz
            br_if 2 (;@2;)
            block  ;; label = @5
              local.get 0
              i32.load8_u
              local.tee 3
              br_if 0 (;@5;)
              local.get 0
              return
            end
            local.get 3
            local.get 1
            i32.const 255
            i32.and
            i32.ne
            br_if 1 (;@3;)
            local.get 0
            return
          end
          local.get 0
          local.get 0
          call $strlen
          i32.add
          return
        end
        block  ;; label = @3
          local.get 0
          i32.const 1
          i32.add
          local.tee 3
          i32.const 3
          i32.and
          br_if 0 (;@3;)
          local.get 3
          local.set 0
          br 1 (;@2;)
        end
        local.get 3
        i32.load8_u
        local.tee 4
        i32.eqz
        br_if 1 (;@1;)
        local.get 4
        local.get 1
        i32.const 255
        i32.and
        i32.eq
        br_if 1 (;@1;)
        block  ;; label = @3
          local.get 0
          i32.const 2
          i32.add
          local.tee 3
          i32.const 3
          i32.and
          br_if 0 (;@3;)
          local.get 3
          local.set 0
          br 1 (;@2;)
        end
        local.get 3
        i32.load8_u
        local.tee 4
        i32.eqz
        br_if 1 (;@1;)
        local.get 4
        local.get 1
        i32.const 255
        i32.and
        i32.eq
        br_if 1 (;@1;)
        block  ;; label = @3
          local.get 0
          i32.const 3
          i32.add
          local.tee 3
          i32.const 3
          i32.and
          br_if 0 (;@3;)
          local.get 3
          local.set 0
          br 1 (;@2;)
        end
        local.get 3
        i32.load8_u
        local.tee 4
        i32.eqz
        br_if 1 (;@1;)
        local.get 4
        local.get 1
        i32.const 255
        i32.and
        i32.eq
        br_if 1 (;@1;)
        local.get 0
        i32.const 4
        i32.add
        local.set 0
      end
      block  ;; label = @2
        local.get 0
        i32.load
        local.tee 3
        i32.const -1
        i32.xor
        local.get 3
        i32.const -16843009
        i32.add
        i32.and
        i32.const -2139062144
        i32.and
        br_if 0 (;@2;)
        local.get 2
        i32.const 16843009
        i32.mul
        local.set 2
        loop  ;; label = @3
          local.get 3
          local.get 2
          i32.xor
          local.tee 3
          i32.const -1
          i32.xor
          local.get 3
          i32.const -16843009
          i32.add
          i32.and
          i32.const -2139062144
          i32.and
          br_if 1 (;@2;)
          local.get 0
          i32.const 4
          i32.add
          local.tee 0
          i32.load
          local.tee 3
          i32.const -1
          i32.xor
          local.get 3
          i32.const -16843009
          i32.add
          i32.and
          i32.const -2139062144
          i32.and
          i32.eqz
          br_if 0 (;@3;)
        end
      end
      local.get 0
      i32.const -1
      i32.add
      local.set 3
      loop  ;; label = @2
        local.get 3
        i32.const 1
        i32.add
        local.tee 3
        i32.load8_u
        local.tee 0
        i32.eqz
        br_if 1 (;@1;)
        local.get 0
        local.get 1
        i32.const 255
        i32.and
        i32.ne
        br_if 0 (;@2;)
      end
    end
    local.get 3)
  (func $memset (type 0) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i64)
    block  ;; label = @1
      local.get 2
      i32.const 33
      i32.lt_u
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      local.get 2
      memory.fill
      local.get 0
      return
    end
    block  ;; label = @1
      local.get 2
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      i32.store8
      local.get 2
      local.get 0
      i32.add
      local.tee 3
      i32.const -1
      i32.add
      local.get 1
      i32.store8
      local.get 2
      i32.const 3
      i32.lt_u
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      i32.store8 offset=2
      local.get 0
      local.get 1
      i32.store8 offset=1
      local.get 3
      i32.const -3
      i32.add
      local.get 1
      i32.store8
      local.get 3
      i32.const -2
      i32.add
      local.get 1
      i32.store8
      local.get 2
      i32.const 7
      i32.lt_u
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      i32.store8 offset=3
      local.get 3
      i32.const -4
      i32.add
      local.get 1
      i32.store8
      local.get 2
      i32.const 9
      i32.lt_u
      br_if 0 (;@1;)
      local.get 0
      i32.const 0
      local.get 0
      i32.sub
      i32.const 3
      i32.and
      local.tee 4
      i32.add
      local.tee 5
      local.get 1
      i32.const 255
      i32.and
      i32.const 16843009
      i32.mul
      local.tee 3
      i32.store
      local.get 5
      local.get 2
      local.get 4
      i32.sub
      i32.const -4
      i32.and
      local.tee 1
      i32.add
      local.tee 2
      i32.const -4
      i32.add
      local.get 3
      i32.store
      local.get 1
      i32.const 9
      i32.lt_u
      br_if 0 (;@1;)
      local.get 5
      local.get 3
      i32.store offset=8
      local.get 5
      local.get 3
      i32.store offset=4
      local.get 2
      i32.const -8
      i32.add
      local.get 3
      i32.store
      local.get 2
      i32.const -12
      i32.add
      local.get 3
      i32.store
      local.get 1
      i32.const 25
      i32.lt_u
      br_if 0 (;@1;)
      local.get 5
      local.get 3
      i32.store offset=24
      local.get 5
      local.get 3
      i32.store offset=20
      local.get 5
      local.get 3
      i32.store offset=16
      local.get 5
      local.get 3
      i32.store offset=12
      local.get 2
      i32.const -16
      i32.add
      local.get 3
      i32.store
      local.get 2
      i32.const -20
      i32.add
      local.get 3
      i32.store
      local.get 2
      i32.const -24
      i32.add
      local.get 3
      i32.store
      local.get 2
      i32.const -28
      i32.add
      local.get 3
      i32.store
      local.get 1
      local.get 5
      i32.const 4
      i32.and
      i32.const 24
      i32.or
      local.tee 2
      i32.sub
      local.tee 1
      i32.const 32
      i32.lt_u
      br_if 0 (;@1;)
      local.get 3
      i64.extend_i32_u
      i64.const 4294967297
      i64.mul
      local.set 6
      local.get 5
      local.get 2
      i32.add
      local.set 2
      loop  ;; label = @2
        local.get 2
        local.get 6
        i64.store offset=24
        local.get 2
        local.get 6
        i64.store offset=16
        local.get 2
        local.get 6
        i64.store offset=8
        local.get 2
        local.get 6
        i64.store
        local.get 2
        i32.const 32
        i32.add
        local.set 2
        local.get 1
        i32.const -32
        i32.add
        local.tee 1
        i32.const 31
        i32.gt_u
        br_if 0 (;@2;)
      end
    end
    local.get 0)
  (func $strncmp (type 0) (param i32 i32 i32) (result i32)
    (local i32 i32 i32)
    block  ;; label = @1
      local.get 2
      br_if 0 (;@1;)
      i32.const 0
      return
    end
    i32.const 0
    local.set 3
    block  ;; label = @1
      local.get 0
      i32.load8_u
      local.tee 4
      i32.eqz
      br_if 0 (;@1;)
      local.get 0
      i32.const 1
      i32.add
      local.set 0
      local.get 2
      i32.const -1
      i32.add
      local.set 2
      loop  ;; label = @2
        block  ;; label = @3
          local.get 1
          i32.load8_u
          local.tee 5
          br_if 0 (;@3;)
          local.get 4
          local.set 3
          br 2 (;@1;)
        end
        block  ;; label = @3
          local.get 2
          br_if 0 (;@3;)
          local.get 4
          local.set 3
          br 2 (;@1;)
        end
        block  ;; label = @3
          local.get 4
          i32.const 255
          i32.and
          local.get 5
          i32.eq
          br_if 0 (;@3;)
          local.get 4
          local.set 3
          br 2 (;@1;)
        end
        local.get 2
        i32.const -1
        i32.add
        local.set 2
        local.get 1
        i32.const 1
        i32.add
        local.set 1
        local.get 0
        i32.load8_u
        local.set 4
        local.get 0
        i32.const 1
        i32.add
        local.set 0
        local.get 4
        br_if 0 (;@2;)
      end
    end
    local.get 3
    i32.const 255
    i32.and
    local.get 1
    i32.load8_u
    i32.sub)
  (func $__stpcpy (type 1) (param i32 i32) (result i32)
    (local i32 i32)
    block  ;; label = @1
      block  ;; label = @2
        block  ;; label = @3
          local.get 1
          local.get 0
          i32.xor
          i32.const 3
          i32.and
          i32.eqz
          br_if 0 (;@3;)
          local.get 1
          i32.load8_u
          local.set 2
          br 1 (;@2;)
        end
        block  ;; label = @3
          local.get 1
          i32.const 3
          i32.and
          i32.eqz
          br_if 0 (;@3;)
          local.get 0
          local.get 1
          i32.load8_u
          local.tee 2
          i32.store8
          block  ;; label = @4
            local.get 2
            br_if 0 (;@4;)
            local.get 0
            return
          end
          local.get 0
          i32.const 1
          i32.add
          local.set 2
          block  ;; label = @4
            local.get 1
            i32.const 1
            i32.add
            local.tee 3
            i32.const 3
            i32.and
            br_if 0 (;@4;)
            local.get 2
            local.set 0
            local.get 3
            local.set 1
            br 1 (;@3;)
          end
          local.get 2
          local.get 3
          i32.load8_u
          local.tee 3
          i32.store8
          local.get 3
          i32.eqz
          br_if 2 (;@1;)
          local.get 0
          i32.const 2
          i32.add
          local.set 2
          block  ;; label = @4
            local.get 1
            i32.const 2
            i32.add
            local.tee 3
            i32.const 3
            i32.and
            br_if 0 (;@4;)
            local.get 2
            local.set 0
            local.get 3
            local.set 1
            br 1 (;@3;)
          end
          local.get 2
          local.get 3
          i32.load8_u
          local.tee 3
          i32.store8
          local.get 3
          i32.eqz
          br_if 2 (;@1;)
          local.get 0
          i32.const 3
          i32.add
          local.set 2
          block  ;; label = @4
            local.get 1
            i32.const 3
            i32.add
            local.tee 3
            i32.const 3
            i32.and
            br_if 0 (;@4;)
            local.get 2
            local.set 0
            local.get 3
            local.set 1
            br 1 (;@3;)
          end
          local.get 2
          local.get 3
          i32.load8_u
          local.tee 3
          i32.store8
          local.get 3
          i32.eqz
          br_if 2 (;@1;)
          local.get 0
          i32.const 4
          i32.add
          local.set 0
          local.get 1
          i32.const 4
          i32.add
          local.set 1
        end
        local.get 1
        i32.load
        local.tee 2
        i32.const -1
        i32.xor
        local.get 2
        i32.const -16843009
        i32.add
        i32.and
        i32.const -2139062144
        i32.and
        br_if 0 (;@2;)
        loop  ;; label = @3
          local.get 0
          local.get 2
          i32.store
          local.get 0
          i32.const 4
          i32.add
          local.set 0
          local.get 1
          i32.const 4
          i32.add
          local.tee 1
          i32.load
          local.tee 2
          i32.const -1
          i32.xor
          local.get 2
          i32.const -16843009
          i32.add
          i32.and
          i32.const -2139062144
          i32.and
          i32.eqz
          br_if 0 (;@3;)
        end
      end
      local.get 0
      local.get 2
      i32.store8
      block  ;; label = @2
        local.get 2
        i32.const 255
        i32.and
        br_if 0 (;@2;)
        local.get 0
        return
      end
      local.get 1
      i32.const 1
      i32.add
      local.set 1
      local.get 0
      local.set 2
      loop  ;; label = @2
        local.get 2
        local.get 1
        i32.load8_u
        local.tee 0
        i32.store8 offset=1
        local.get 1
        i32.const 1
        i32.add
        local.set 1
        local.get 2
        i32.const 1
        i32.add
        local.set 2
        local.get 0
        br_if 0 (;@2;)
      end
    end
    local.get 2)
  (func $strcpy (type 1) (param i32 i32) (result i32)
    local.get 0
    local.get 1
    call $__stpcpy
    drop
    local.get 0)
  (func $strlen (type 5) (param i32) (result i32)
    (local i32 i32)
    local.get 0
    local.set 1
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.const 3
        i32.and
        i32.eqz
        br_if 0 (;@2;)
        local.get 0
        local.set 1
        local.get 0
        i32.load8_u
        i32.eqz
        br_if 1 (;@1;)
        local.get 0
        i32.const 1
        i32.add
        local.tee 1
        i32.const 3
        i32.and
        i32.eqz
        br_if 0 (;@2;)
        local.get 1
        i32.load8_u
        i32.eqz
        br_if 1 (;@1;)
        local.get 0
        i32.const 2
        i32.add
        local.tee 1
        i32.const 3
        i32.and
        i32.eqz
        br_if 0 (;@2;)
        local.get 1
        i32.load8_u
        i32.eqz
        br_if 1 (;@1;)
        local.get 0
        i32.const 3
        i32.add
        local.tee 1
        i32.const 3
        i32.and
        i32.eqz
        br_if 0 (;@2;)
        local.get 1
        i32.load8_u
        i32.eqz
        br_if 1 (;@1;)
        local.get 0
        i32.const 4
        i32.add
        local.set 1
      end
      local.get 1
      i32.const -5
      i32.add
      local.set 1
      loop  ;; label = @2
        local.get 1
        i32.const 5
        i32.add
        local.set 2
        local.get 1
        i32.const 4
        i32.add
        local.set 1
        local.get 2
        i32.load
        local.tee 2
        i32.const -1
        i32.xor
        local.get 2
        i32.const -16843009
        i32.add
        i32.and
        i32.const -2139062144
        i32.and
        i32.eqz
        br_if 0 (;@2;)
      end
      loop  ;; label = @2
        local.get 1
        i32.const 1
        i32.add
        local.tee 1
        i32.load8_u
        br_if 0 (;@2;)
      end
    end
    local.get 1
    local.get 0
    i32.sub)
  (func $dummy (type 14))
  (func $__wasm_call_dtors (type 14)
    call $dummy
    call $dummy)
  (func $unregister_strategy.command_export (type 5) (param i32) (result i32)
    local.get 0
    call $unregister_strategy
    call $__wasm_call_dtors)
  (func $strategy_parameters.command_export (type 7) (param i32) (result i32 i32)
    local.get 0
    call $strategy_parameters
    call $__wasm_call_dtors)
  (func $strategy_next.command_export (type 23) (param i32 i32 f32 f32 f32 f32 f32)
    local.get 0
    local.get 1
    local.get 2
    local.get 3
    local.get 4
    local.get 5
    local.get 6
    call $strategy_next
    call $__wasm_call_dtors)
  (func $register_crossma.command_export (type 1) (param i32 i32) (result i32)
    local.get 0
    local.get 1
    call $register_crossma
    call $__wasm_call_dtors)
  (table (;0;) 76 76 funcref)
  (memory (;0;) 17)
  (global $__stack_pointer (mut i32) (i32.const 1048576))
  (export "memory" (memory 0))
  (export "unregister_strategy" (func $unregister_strategy.command_export))
  (export "strategy_parameters" (func $strategy_parameters.command_export))
  (export "strategy_next" (func $strategy_next.command_export))
  (export "register_crossma" (func $register_crossma.command_export))
  (elem (;0;) (i32.const 1) func $_ZN4core3fmt3num3imp52_$LT$impl$u20$core..fmt..Display$u20$for$u20$u32$GT$3fmt17h4be59bab036c1886E $_ZN60_$LT$alloc..string..String$u20$as$u20$core..fmt..Display$GT$3fmt17h44520808cb144237E $_ZN4core3ops8function6FnOnce9call_once17h55447dbbde76805eE $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17he1e3e02f5fc28a55E $_ZN44_$LT$$RF$T$u20$as$u20$core..fmt..Display$GT$3fmt17h3efcc4100aab223eE $_ZN59_$LT$core..fmt..Arguments$u20$as$u20$core..fmt..Display$GT$3fmt17h2a7274ab74be954aE $_ZN44_$LT$$RF$T$u20$as$u20$core..fmt..Display$GT$3fmt17hf33a8949ac184540E $_ZN44_$LT$$RF$T$u20$as$u20$core..fmt..Display$GT$3fmt17h6d756373b98cd7c1E $_ZN71_$LT$core..ops..range..Range$LT$Idx$GT$$u20$as$u20$core..fmt..Debug$GT$3fmt17ha38900d092035ca2E $_ZN41_$LT$char$u20$as$u20$core..fmt..Debug$GT$3fmt17h23bf9b2886472963E $_ZN91_$LT$std..sys_common..backtrace.._print..DisplayBacktrace$u20$as$u20$core..fmt..Display$GT$3fmt17h65a078f2606287d9E $_ZN73_$LT$core..panic..panic_info..PanicInfo$u20$as$u20$core..fmt..Display$GT$3fmt17hcc3487ec06dc686aE $_ZN44_$LT$$RF$T$u20$as$u20$core..fmt..Display$GT$3fmt17h3cd999b848d69bd1E $_ZN4core3fmt3num50_$LT$impl$u20$core..fmt..Debug$u20$for$u20$u16$GT$3fmt17h860941a58acd0572E.524 $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17h5e15663af5b05b89E $_ZN4core3ptr100drop_in_place$LT$$RF$mut$u20$std..io..Write..write_fmt..Adapter$LT$alloc..vec..Vec$LT$u8$GT$$GT$$GT$17hdd0e3e29f1eafbe5E $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h888e990a606ca8ccE $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17h4767d155bdd14fe0E $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17hb6baedc2fce95264E $_ZN4core3ptr29drop_in_place$LT$$LP$$RP$$GT$17h83ff458eb0202b31E $_ZN53_$LT$core..fmt..Error$u20$as$u20$core..fmt..Debug$GT$3fmt17h8ca99f446535e2f5E $_ZN4core3ptr52drop_in_place$LT$std..thread..local..AccessError$GT$17h57a975f821e6c1ebE $_ZN68_$LT$std..thread..local..AccessError$u20$as$u20$core..fmt..Debug$GT$3fmt17h2a97b2ac10eb69a0E $_ZN4core3ptr104drop_in_place$LT$$RF$mut$u20$std..io..Write..write_fmt..Adapter$LT$std..sys..wasi..stdio..Stderr$GT$$GT$17h653c62b9b22bc166E $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17h0eeb836dede051ecE $_ZN4core3ops8function6FnOnce40call_once$u7b$$u7b$vtable.shim$u7d$$u7d$17h803462a5d051c192E $_ZN9once_cell3imp17OnceCell$LT$T$GT$10initialize28_$u7b$$u7b$closure$u7d$$u7d$17h08719884d15d3caaE $_ZN4core3ops8function6FnOnce40call_once$u7b$$u7b$vtable.shim$u7d$$u7d$17h6534dce3e0201b30E $_ZN9once_cell3imp17OnceCell$LT$T$GT$10initialize28_$u7b$$u7b$closure$u7d$$u7d$17hecb0bdfae7ba818bE $_ZN69_$LT$core..alloc..layout..LayoutError$u20$as$u20$core..fmt..Debug$GT$3fmt17h8c527b937ccb019eE $_ZN4core3ptr105drop_in_place$LT$std..sync..poison..PoisonError$LT$std..sync..rwlock..RwLockWriteGuard$LT$i32$GT$$GT$$GT$17heec6d4163f504738E $_ZN76_$LT$std..sync..poison..PoisonError$LT$T$GT$$u20$as$u20$core..fmt..Debug$GT$3fmt17h31b1c977533811acE $_ZN4core3ptr261drop_in_place$LT$std..sync..poison..PoisonError$LT$std..sync..rwlock..RwLockReadGuard$LT$std..collections..hash..map..HashMap$LT$i32$C$alloc..boxed..Box$LT$dyn$u20$base..strategy..TradingStrategy$u2b$core..marker..Sync$u2b$core..marker..Send$GT$$GT$$GT$$GT$$GT$17h30417aeeed91d393E $_ZN4core3ops8function6FnOnce9call_once17h2296aeb300a7e9bdE $_ZN4core3ops8function6FnOnce9call_once17hced0e244dbb5386bE $_ZN4core3ptr92drop_in_place$LT$std..io..Write..write_fmt..Adapter$LT$std..sys..wasi..stdio..Stderr$GT$$GT$17h82f1e3f018af5003E $_ZN80_$LT$std..io..Write..write_fmt..Adapter$LT$T$GT$$u20$as$u20$core..fmt..Write$GT$9write_str17ha20c17e383239b1fE $_ZN4core3fmt5Write10write_char17h1167d2a5cfccbbddE $_ZN4core3fmt5Write9write_fmt17hea1dcd8ca86a27a6E $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h594ada18edc2cc2aE $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17hd153e54c623bbe7bE $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17h2960215ccf17f2d3E $_ZN36_$LT$T$u20$as$u20$core..any..Any$GT$7type_id17h27298964b5ba96aaE $_ZN68_$LT$core..fmt..builders..PadAdapter$u20$as$u20$core..fmt..Write$GT$9write_str17hd4ac5b916bf4e0b0E $_ZN4core3fmt5Write10write_char17ha7c13b4705496bbdE $_ZN4core3fmt5Write9write_fmt17h99728a0a28fde9f9E $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h3bfd604354950662E $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17heffbb38722d0b741E $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17hbdaf748e5c297b7aE $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17hfa244fbfe149e5b0E $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h27459983c441be4dE $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17hd182b41fe69b70caE $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17h74d01cc6236fab0bE $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_str17h1cfe241be326fd2fE $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$10write_char17he4fbd911983151ddE $_ZN50_$LT$$RF$mut$u20$W$u20$as$u20$core..fmt..Write$GT$9write_fmt17h0ac08c1e052d4e5eE $_ZN42_$LT$$RF$T$u20$as$u20$core..fmt..Debug$GT$3fmt17h60f47e1d406afabfE $_ZN63_$LT$core..cell..BorrowMutError$u20$as$u20$core..fmt..Debug$GT$3fmt17h5ce61f4bcde0325cE $_ZN4core3ptr88drop_in_place$LT$std..io..Write..write_fmt..Adapter$LT$alloc..vec..Vec$LT$u8$GT$$GT$$GT$17hca98a9d3138cd957E $_ZN80_$LT$std..io..Write..write_fmt..Adapter$LT$T$GT$$u20$as$u20$core..fmt..Write$GT$9write_str17hffeb84cbbad34c0bE $_ZN4core3fmt5Write10write_char17h35bf3a19560abc4fE $_ZN4core3fmt5Write9write_fmt17hd267ee56f623e382E $_ZN4core3ptr39drop_in_place$LT$std..path..PathBuf$GT$17h6b2ac406cb2d3acfE $_ZN36_$LT$T$u20$as$u20$core..any..Any$GT$7type_id17h4c4ad1a2d5b40bf7E $_ZN36_$LT$T$u20$as$u20$core..any..Any$GT$7type_id17ha906ab4a92d8e02fE $_ZN4core3ptr70drop_in_place$LT$std..panicking..begin_panic_handler..PanicPayload$GT$17h017685081936aa35E $_ZN90_$LT$std..panicking..begin_panic_handler..PanicPayload$u20$as$u20$core..panic..BoxMeUp$GT$8take_box17h571d43091b181743E $_ZN90_$LT$std..panicking..begin_panic_handler..PanicPayload$u20$as$u20$core..panic..BoxMeUp$GT$3get17h570121d24b9b06c6E $_ZN93_$LT$std..panicking..begin_panic_handler..StrPanicPayload$u20$as$u20$core..panic..BoxMeUp$GT$8take_box17hc0dcc5abb65c5495E $_ZN93_$LT$std..panicking..begin_panic_handler..StrPanicPayload$u20$as$u20$core..panic..BoxMeUp$GT$3get17hadfa6298e70556caE $_ZN4core3ptr24drop_in_place$LT$u16$GT$17hb2b91af30d5c58eeE $_ZN63_$LT$wasi..lib_generated..Errno$u20$as$u20$core..fmt..Debug$GT$3fmt17h6aa6cc5efc0069feE $_ZN4core3ptr96drop_in_place$LT$base..strategy..BaseStrategy$LT$trend_follow..cross_ma..CrossMAStrategy$GT$$GT$17h48bb8f367846860fE $_ZN89_$LT$base..strategy..BaseStrategy$LT$S$GT$$u20$as$u20$base..strategy..TradingStrategy$GT$11strategy_id17he477e15cd4143f5fE $_ZN89_$LT$base..strategy..BaseStrategy$LT$S$GT$$u20$as$u20$base..strategy..TradingStrategy$GT$4next17h814055e7e1141c1fE)
  (data $.rodata (i32.const 1048576) "_STRTG\00\00\00\00\10\00\06\00\00\00\00\00\c0\7f\10\00\00\00\04\00\00\00\04\00\00\00\11\00\00\00\12\00\00\00\13\00\00\00library/alloc/src/raw_vec.rs,\00\10\00\1c\00\00\00\0c\02\00\00\05\00\00\00a formatting trait implementation returned an error\00\14\00\00\00\00\00\00\00\01\00\00\00\15\00\00\00library/alloc/src/fmt.rs\9c\00\10\00\18\00\00\00b\02\00\00 \00\00\00cannot access a Thread Local Storage value during or after destruction\00\00\16\00\00\00\00\00\00\00\01\00\00\00\17\00\00\00/rustc/eb26296b556cef10fb713a38f3d16b9886080f26/library/std/src/thread/local.rs\00\1c\01\10\00O\00\00\00\f6\00\00\00\1a\00\00\00\18\00\00\00\04\00\00\00\04\00\00\00\19\00\00\00PoisonError\00\18\00\00\00\0c\00\00\00\04\00\00\00\1a\00\00\00\1b\00\00\00\18\00\00\00\0c\00\00\00\04\00\00\00\1c\00\00\00\1d\00\00\00Lazy instance has previously been poisoned\00\00\c0\01\10\00*\00\00\00/Users/siarheimelnik/.cargo/registry/src/index.crates.io-6f17d22bba15001f/once_cell-1.18.0/src/lib.rs\00\00\00\f4\01\10\00e\00\00\00!\05\00\00\19\00\00\00\00\00\00\00\ff\ff\ff\ff\ff\ff\ff\fffatal runtime error: rwlock locked for reading\0a\00x\02\10\00/\00\00\00called `Result::unwrap()` on an `Err` value\00\16\00\00\00\00\00\00\00\01\00\00\00\1e\00\00\00\1f\00\00\00\08\00\00\00\04\00\00\00 \00\00\00\1f\00\00\00\08\00\00\00\04\00\00\00 \00\00\00!\00\00\00\08\00\00\00\04\00\00\00 \00\00\00strategies/base/src/ffi.rs\00\00\1c\03\10\00\1a\00\00\00\0e\00\00\006\00\00\00\1c\03\10\00\1a\00\00\00\14\00\00\00\0a\00\00\00\1c\03\10\00\1a\00\00\00\1c\00\00\00:\00\00\00\1c\03\10\00\1a\00\00\00\22\00\00\005\00\00\00\1c\03\10\00\1a\00\00\00)\00\00\00S\00\00\00\1c\03\10\00\1a\00\00\00=\00\00\00:\00\00\00\ff\ff\ff\ff/rustc/eb26296b556cef10fb713a38f3d16b9886080f26/library/std/src/sys/wasi/../unsupported/locks/rwlock.rs\00\9c\03\10\00g\00\00\00?\00\00\00\09\00\00\00/rustc/eb26296b556cef10fb713a38f3d16b9886080f26/library/std/src/io/mod.rs\00\00\00\14\04\10\00I\00\00\00,\06\00\00!\00\00\00$\00\00\00\0c\00\00\00\04\00\00\00%\00\00\00&\00\00\00'\00\00\00\18\00\00\00\04\00\00\00\04\00\00\00(\00\00\00)\00\00\00*\00\00\00library/core/src/fmt/mod.rs..\00\00\00\bb\04\10\00\02\00\00\00BorrowMutError:\00\d4\15\10\00\00\00\00\00\d6\04\10\00\01\00\00\00\d6\04\10\00\01\00\00\00panicked at '\00\00\00\fc\04\10\00\01\00\00\00\e4\18\10\00\03\00\00\00\14\00\00\00\00\00\00\00\01\00\00\00+\00\00\00index out of bounds: the len is  but the index is \00\00 \05\10\00 \00\00\00@\05\10\00\12\00\00\00==assertion failed: `(left  right)`\0a  left: ``,\0a right: ``: f\05\10\00\19\00\00\00\7f\05\10\00\12\00\00\00\91\05\10\00\0c\00\00\00\9d\05\10\00\03\00\00\00`\00\00\00f\05\10\00\19\00\00\00\7f\05\10\00\12\00\00\00\91\05\10\00\0c\00\00\00\c0\05\10\00\01\00\00\00: \00\00\d4\15\10\00\00\00\00\00\e4\05\10\00\02\00\00\00\10\00\00\00\0c\00\00\00\04\00\00\00,\00\00\00-\00\00\00.\00\00\00     {\0a,\0a,  { ..\0a}, .. } { .. } }library/core/src/fmt/num.rs1\06\10\00\1b\00\00\00i\00\00\00\14\00\00\000x00010203040506070809101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899\00\00\10\00\00\00\04\00\00\00\04\00\00\00/\00\00\000\00\00\001\00\00\00truefalse\00\00\00\a0\04\10\00\1b\00\00\00\14\09\00\00\1e\00\00\00\a0\04\10\00\1b\00\00\00\1b\09\00\00\16\00\00\00range start index  out of range for slice of length l\07\10\00\12\00\00\00~\07\10\00\22\00\00\00range end index \b0\07\10\00\10\00\00\00~\07\10\00\22\00\00\00slice index starts at  but ends at \00\d0\07\10\00\16\00\00\00\e6\07\10\00\0d\00\00\00[...]byte index  is out of bounds of `\00\00\09\08\10\00\0b\00\00\00\14\08\10\00\16\00\00\00\c0\05\10\00\01\00\00\00begin <= end ( <= ) when slicing `\00\00D\08\10\00\0e\00\00\00R\08\10\00\04\00\00\00V\08\10\00\10\00\00\00\c0\05\10\00\01\00\00\00 is not a char boundary; it is inside  (bytes ) of `\09\08\10\00\0b\00\00\00\88\08\10\00&\00\00\00\ae\08\10\00\08\00\00\00\b6\08\10\00\06\00\00\00\c0\05\10\00\01\00\00\00library/core/src/str/mod.rs\00\e4\08\10\00\1b\00\00\00\07\01\00\00\1d\00\00\00library/core/src/unicode/printable.rs\00\00\00\10\09\10\00%\00\00\00\0a\00\00\00\1c\00\00\00\10\09\10\00%\00\00\00\1a\00\00\006\00\00\00\00\01\03\05\05\06\06\02\07\06\08\07\09\11\0a\1c\0b\19\0c\1a\0d\10\0e\0c\0f\04\10\03\12\12\13\09\16\01\17\04\18\01\19\03\1a\07\1b\01\1c\02\1f\16 \03+\03-\0b.\010\031\022\01\a7\02\a9\02\aa\04\ab\08\fa\02\fb\05\fd\02\fe\03\ff\09\adxy\8b\8d\a20WX\8b\8c\90\1c\dd\0e\0fKL\fb\fc./?\5c]_\e2\84\8d\8e\91\92\a9\b1\ba\bb\c5\c6\c9\ca\de\e4\e5\ff\00\04\11\12)147:;=IJ]\84\8e\92\a9\b1\b4\ba\bb\c6\ca\ce\cf\e4\e5\00\04\0d\0e\11\12)14:;EFIJ^de\84\91\9b\9d\c9\ce\cf\0d\11):;EIW[\5c^_de\8d\91\a9\b4\ba\bb\c5\c9\df\e4\e5\f0\0d\11EIde\80\84\b2\bc\be\bf\d5\d7\f0\f1\83\85\8b\a4\a6\be\bf\c5\c7\cf\da\dbH\98\bd\cd\c6\ce\cfINOWY^_\89\8e\8f\b1\b6\b7\bf\c1\c6\c7\d7\11\16\17[\5c\f6\f7\fe\ff\80mq\de\df\0e\1fno\1c\1d_}~\ae\af\7f\bb\bc\16\17\1e\1fFGNOXZ\5c^~\7f\b5\c5\d4\d5\dc\f0\f1\f5rs\8ftu\96&./\a7\af\b7\bf\c7\cf\d7\df\9a@\97\980\8f\1f\d2\d4\ce\ffNOZ[\07\08\0f\10'/\ee\efno7=?BE\90\91Sgu\c8\c9\d0\d1\d8\d9\e7\fe\ff\00 _\22\82\df\04\82D\08\1b\04\06\11\81\ac\0e\80\ab\05\1f\09\81\1b\03\19\08\01\04/\044\04\07\03\01\07\06\07\11\0aP\0f\12\07U\07\03\04\1c\0a\09\03\08\03\07\03\02\03\03\03\0c\04\05\03\0b\06\01\0e\15\05N\07\1b\07W\07\02\06\17\0cP\04C\03-\03\01\04\11\06\0f\0c:\04\1d%_ m\04j%\80\c8\05\82\b0\03\1a\06\82\fd\03Y\07\16\09\18\09\14\0c\14\0cj\06\0a\06\1a\06Y\07+\05F\0a,\04\0c\04\01\031\0b,\04\1a\06\0b\03\80\ac\06\0a\06/1M\03\80\a4\08<\03\0f\03<\078\08+\05\82\ff\11\18\08/\11-\03!\0f!\0f\80\8c\04\82\97\19\0b\15\88\94\05/\05;\07\02\0e\18\09\80\be\22t\0c\80\d6\1a\0c\05\80\ff\05\80\df\0c\f2\9d\037\09\81\5c\14\80\b8\08\80\cb\05\0a\18;\03\0a\068\08F\08\0c\06t\0b\1e\03Z\04Y\09\80\83\18\1c\0a\16\09L\04\80\8a\06\ab\a4\0c\17\041\a1\04\81\da&\07\0c\05\05\80\a6\10\81\f5\07\01 *\06L\04\80\8d\04\80\be\03\1b\03\0f\0d\00\06\01\01\03\01\04\02\05\07\07\02\08\08\09\02\0a\05\0b\02\0e\04\10\01\11\02\12\05\13\11\14\01\15\02\17\02\19\0d\1c\05\1d\08\1f\01$\01j\04k\02\af\03\b1\02\bc\02\cf\02\d1\02\d4\0c\d5\09\d6\02\d7\02\da\01\e0\05\e1\02\e7\04\e8\02\ee \f0\04\f8\02\fa\03\fb\01\0c';>NO\8f\9e\9e\9f{\8b\93\96\a2\b2\ba\86\b1\06\07\096=>V\f3\d0\d1\04\14\1867VW\7f\aa\ae\af\bd5\e0\12\87\89\8e\9e\04\0d\0e\11\12)14:EFIJNOde\5c\b6\b7\1b\1c\07\08\0a\0b\14\1769:\a8\a9\d8\d9\097\90\91\a8\07\0a;>fi\8f\92\11o_\bf\ee\efZb\f4\fc\ffST\9a\9b./'(U\9d\a0\a1\a3\a4\a7\a8\ad\ba\bc\c4\06\0b\0c\15\1d:?EQ\a6\a7\cc\cd\a0\07\19\1a\22%>?\e7\ec\ef\ff\c5\c6\04 #%&(38:HJLPSUVXZ\5c^`cefksx}\7f\8a\a4\aa\af\b0\c0\d0\ae\afno\be\93^\22{\05\03\04-\03f\03\01/.\80\82\1d\031\0f\1c\04$\09\1e\05+\05D\04\0e*\80\aa\06$\04$\04(\084\0bNC\817\09\16\0a\08\18;E9\03c\08\090\16\05!\03\1b\05\01@8\04K\05/\04\0a\07\09\07@ '\04\0c\096\03:\05\1a\07\04\0c\07PI73\0d3\07.\08\0a\81&RK+\08*\16\1a&\1c\14\17\09N\04$\09D\0d\19\07\0a\06H\08'\09u\0bB>*\06;\05\0a\06Q\06\01\05\10\03\05\80\8bb\1eH\08\0a\80\a6^\22E\0b\0a\06\0d\13:\06\0a6,\04\17\80\b9<dS\0cH\09\0aFE\1bH\08S\0dI\07\0a\80\f6F\0a\1d\03GI7\03\0e\08\0a\069\07\0a\816\19\07;\03\1cV\01\0f2\0d\83\9bfu\0b\80\c4\8aLc\0d\840\10\16\8f\aa\82G\a1\b9\829\07*\04\5c\06&\0aF\0a(\05\13\82\b0[eK\049\07\11@\05\0b\02\0e\97\f8\08\84\d6*\09\a2\e7\813\0f\01\1d\06\0e\04\08\81\8c\89\04k\05\0d\03\09\07\10\92`G\09t<\80\f6\0as\08p\15Fz\14\0c\14\0cW\09\19\80\87\81G\03\85B\0f\15\84P\1f\06\06\80\d5+\05>!\01p-\03\1a\04\02\81@\1f\11:\05\01\81\d0*\82\e6\80\f7)L\04\0a\04\02\83\11DL=\80\c2<\06\01\04U\05\1b4\02\81\0e,\04d\0cV\0a\80\ae8\1d\0d,\04\09\07\02\0e\06\80\9a\83\d8\04\11\03\0d\03w\04_\06\0c\04\01\0f\0c\048\08\0a\06(\08\22N\81T\0c\1d\03\09\076\08\0e\04\09\07\09\07\80\cb%\0a\84\06library/core/src/unicode/unicode_data.rs0123456789abcdeflibrary/core/src/escape.rs\00\00\0c\0f\10\00\1a\00\00\004\00\00\00\05\00\00\00\5cu{\00\0c\0f\10\00\1a\00\00\00b\00\00\00#\00\00\00Error\00\00\00\d4\0e\10\00(\00\00\00P\00\00\00(\00\00\00\d4\0e\10\00(\00\00\00\5c\00\00\00\16\00\00\00\00\03\00\00\83\04 \00\91\05`\00]\13\a0\00\12\17 \1f\0c `\1f\ef,\a0+*0 ,o\a6\e0,\02\a8`-\1e\fb`.\00\fe 6\9e\ff`6\fd\01\e16\01\0a!7$\0d\e17\ab\0ea9/\18\a190\1caH\f3\1e\a1L@4aP\f0j\a1QOo!R\9d\bc\a1R\00\cfaSe\d1\a1S\00\da!T\00\e0\e1U\ae\e2aW\ec\e4!Y\d0\e8\a1Y \00\eeY\f0\01\7fZ\00p\00\07\00-\01\01\01\02\01\02\01\01H\0b0\15\10\01e\07\02\06\02\02\01\04#\01\1e\1b[\0b:\09\09\01\18\04\01\09\01\03\01\05+\03<\08*\18\01 7\01\01\01\04\08\04\01\03\07\0a\02\1d\01:\01\01\01\02\04\08\01\09\01\0a\02\1a\01\02\029\01\04\02\04\02\02\03\03\01\1e\02\03\01\0b\029\01\04\05\01\02\04\01\14\02\16\06\01\01:\01\01\02\01\04\08\01\07\03\0a\02\1e\01;\01\01\01\0c\01\09\01(\01\03\017\01\01\03\05\03\01\04\07\02\0b\02\1d\01:\01\02\01\02\01\03\01\05\02\07\02\0b\02\1c\029\02\01\01\02\04\08\01\09\01\0a\02\1d\01H\01\04\01\02\03\01\01\08\01Q\01\02\07\0c\08b\01\02\09\0b\07I\02\1b\01\01\01\01\017\0e\01\05\01\02\05\0b\01$\09\01f\04\01\06\01\02\02\02\19\02\04\03\10\04\0d\01\02\02\06\01\0f\01\00\03\00\03\1d\02\1e\02\1e\02@\02\01\07\08\01\02\0b\09\01-\03\01\01u\02\22\01v\03\04\02\09\01\06\03\db\02\02\01:\01\01\07\01\01\01\01\02\08\06\0a\02\010\1f1\040\07\01\01\05\01(\09\0c\02 \04\02\02\01\038\01\01\02\03\01\01\03:\08\02\02\98\03\01\0d\01\07\04\01\06\01\03\02\c6@\00\01\c3!\00\03\8d\01` \00\06i\02\00\04\01\0a \02P\02\00\01\03\01\04\01\19\02\05\01\97\02\1a\12\0d\01&\08\19\0b.\030\01\02\04\02\02'\01C\06\02\02\02\02\0c\01\08\01/\013\01\01\03\02\02\05\02\01\01*\02\08\01\ee\01\02\01\04\01\00\01\00\10\10\10\00\02\00\01\e2\01\95\05\00\03\01\02\05\04(\03\04\01\a5\02\00\04\00\02P\03F\0b1\04{\016\0f)\01\02\02\0a\031\04\02\02\07\01=\03$\05\01\08>\01\0c\024\09\0a\04\02\01_\03\02\01\01\02\06\01\02\01\9d\01\03\08\15\029\02\01\01\01\01\16\01\0e\07\03\05\c3\08\02\03\01\01\17\01Q\01\02\06\01\01\02\01\01\02\01\02\eb\01\02\04\06\02\01\02\1b\02U\08\02\01\01\02j\01\01\01\02\06\01\01e\03\02\04\01\05\00\09\01\02\f5\01\0a\02\01\01\04\01\90\04\02\02\04\01 \0a(\06\02\04\08\01\09\06\02\03.\0d\01\02\00\07\01\06\01\01R\16\02\07\01\02\01\02z\06\03\01\01\02\01\07\01\01H\02\03\01\01\01\00\02\0b\024\05\05\01\01\01\00\01\06\0f\00\05;\07\00\01?\04Q\01\00\02\00.\02\17\00\01\01\03\04\05\08\08\02\07\1e\04\94\03\007\042\08\01\0e\01\16\05\01\0f\00\07\01\11\02\07\01\02\01\05d\01\a0\07\00\01=\04\00\04\00\07m\07\00`\80\f0\00LayoutErrorcore/src/series.rs\da\12\10\00\12\00\00\00-\00\00\00\0d\00\00\00\da\12\10\00\12\00\00\001\00\00\00\1c\00\00\00\da\12\10\00\12\00\00\001\00\00\00\0d\00\00\00\da\12\10\00\12\00\00\003\00\00\00\13\00\00\00\00\00\00\00attempt to calculate the remainder with a divisor of zerocapacity overflow\00\00i\13\10\00\11\00\00\00/rustc/eb26296b556cef10fb713a38f3d16b9886080f26/library/alloc/src/vec/spec_from_iter_nested.rs\00\00\84\13\10\00^\00\00\00;\00\00\00\12\00\00\00/rustc/eb26296b556cef10fb713a38f3d16b9886080f26/library/alloc/src/vec/mod.rs\f4\13\10\00L\00\00\00)\0b\00\00\0d\00\00\00Hash table capacity overflowP\14\10\00\1c\00\00\00/cargo/registry/src/index.crates.io-6f17d22bba15001f/hashbrown-0.13.1/src/raw/mod.rst\14\10\00T\00\00\00Z\00\00\00(\00\00\00\01\00\00\00/Users/siarheimelnik/.cargo/registry/src/index.crates.io-6f17d22bba15001f/once_cell-1.18.0/src/imp_std.rs\00\00\00\dc\14\10\00i\00\00\00\9b\00\00\00\09\00\00\00\dc\14\10\00i\00\00\00\a1\00\00\006\00\00\00\18\00\00\00\04\00\00\00\04\00\00\002\00\00\00called `Option::unwrap()` on a `None` value\00\10\00\00\00\04\00\00\00\04\00\00\003\00\00\004\00\00\005\00\00\00\10\00\00\00\04\00\00\00\04\00\00\006\00\00\007\00\00\008\00\00\00\00\00\00\00\10\00\00\00\04\00\00\00\04\00\00\009\00\00\00internal error: entered unreachable code\0aAccessErrorlibrary/std/src/thread/mod.rsfailed to generate unique thread ID: bitspace exhausted9\16\10\007\00\00\00\1c\16\10\00\1d\00\00\00@\04\00\00\0d\00\00\00RUST_BACKTRACE\00\00\d4\15\10\00\00\00\00\00already borrowed\14\00\00\00\00\00\00\00\01\00\00\00:\00\00\00library/std/src/io/mod.rs\00\00\00\c0\16\10\00\19\00\00\00,\06\00\00!\00\00\00failed to write whole buffer\ec\16\10\00\1c\00\00\00\17\00\00\00formatter error\00\14\17\10\00\0f\00\00\00(\00\00\00;\00\00\00\0c\00\00\00\04\00\00\00<\00\00\00=\00\00\00>\00\00\00library/std/src/panic.rsH\17\10\00\18\00\00\00\f5\00\00\00\12\00\00\00file name contained an unexpected NUL byte\00\00p\17\10\00*\00\00\00\14\00\00\00\02\00\00\00\9c\17\10\00stack backtrace:\0a\00\00\00\b0\17\10\00\11\00\00\00note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.\0a\cc\17\10\00X\00\00\00library/std/src/sys_common/thread_info.rs\00\00\00,\18\10\00)\00\00\00\16\00\00\003\00\00\00memory allocation of  bytes failed\0a\00h\18\10\00\15\00\00\00}\18\10\00\0e\00\00\00library/std/src/panicking.rsBox<dyn Any><unnamed>thread '' panicked at '', \00\cd\18\10\00\08\00\00\00\d5\18\10\00\0f\00\00\00\e4\18\10\00\03\00\00\00\10\16\10\00\01\00\00\00note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace\0a\00\00\08\19\10\00N\00\00\00\9c\18\10\00\1c\00\00\00P\02\00\00\1e\00\00\00?\00\00\00\0c\00\00\00\04\00\00\00@\00\00\00\10\00\00\00\08\00\00\00\04\00\00\00A\00\00\00B\00\00\00\10\00\00\00\04\00\00\00C\00\00\00D\00\00\00\10\00\00\00\08\00\00\00\04\00\00\00E\00\00\00F\00\00\00\14\00\00\00\00\00\00\00\01\00\00\00+\00\00\00thread caused non-unwinding panic. aborting.\0a\00\00\00\c8\19\10\00-\00\00\00thread panicked while processing panic. aborting.\0a\00\00\00\1a\10\002\00\00\00\0apanicked after panic::always_abort(), aborting.\0a\00\00\00\d4\15\10\00\00\00\00\00<\1a\10\001\00\00\00cannot recursively acquire mutex\80\1a\10\00 \00\00\00library/std/src/sys/wasi/../unsupported/locks/mutex.rs\00\00\a8\1a\10\006\00\00\00\14\00\00\00\09\00\00\00fatal runtime error: rwlock locked for writing\0a\00\f0\1a\10\00/\00\00\00G\00\00\00\02\00\00\00\02\00\00\00H\00\00\00random_get failurelibrary/std/src/sys/wasi/mod.rs\00\00\00J\1b\10\00\1f\00\00\00i\00\00\00%\00\00\00CROSSMA__\00\00\00|\1b\10\00\08\00\00\00\84\1b\10\00\01\00\00\00I\00\00\00\1c\00\00\00\04\00\00\00J\00\00\00K\00\00\00codenamemessageNOTCAPABLEXDEVTXTBSYTIMEDOUTSTALESRCHSPIPEROFSRANGEPROTOTYPEPROTONOSUPPORTPROTOPIPEPERMOWNERDEADOVERFLOWNXIONOTTYNOTSUPNOTSOCKNOTRECOVERABLENOTEMPTYNOTDIRNOTCONNNOSYSNOSPCNOPROTOOPTNOMSGNOMEMNOLINKNOLCKNOEXECNOENTNODEVNOBUFSNFILENETUNREACHNETRESETNETDOWNNAMETOOLONGMULTIHOPMSGSIZEMLINKMFILELOOPISDIRISCONNIOINVALINTRINPROGRESSILSEQIDRMHOSTUNREACHFBIGFAULTEXISTDQUOTDOMDESTADDRREQDEADLKCONNRESETCONNREFUSEDCONNABORTEDCHILDCANCELEDBUSYBADMSGBADFALREADYAGAINAFNOSUPPORTADDRNOTAVAILADDRINUSEACCES2BIGSUCCESSExtension: Capabilities insufficient.Cross-device link.Text file busy.Connection timed out.Reserved.No such process.Invalid seek.Read-only file system.Result too large.Protocol wrong type for socket.Protocol not supported.Protocol error.Broken pipe.Operation not permitted.Previous owner died.Value too large to be stored in data type.No such device or address.Inappropriate I/O control operation.Not supported, or operation not supported on socket.Not a socket.State not recoverable.Directory not empty.Not a directory or a symbolic link to a directory.The socket is not connected.Function not supported.No space left on device.Protocol not available.No message of the desired type.Not enough space.No locks available.Executable file format error.No such file or directory.No such device.No buffer space available.Too many files open in system.Network unreachable.Connection aborted by network.Network is down.Filename too long.Message too large.Too many links.File descriptor value too large.Too many levels of symbolic links.Is a directory.Socket is connected.I/O error.Invalid argument.Interrupted function.Operation in progress.Illegal byte sequence.Identifier removed.Host is unreachable.File too large.Bad address.File exists.Mathematics argument out of domain of function.Destination address required.Resource deadlock would occur.Connection reset.Connection refused.Connection aborted.No child processes.Operation canceled.Device or resource busy.Bad message.Bad file descriptor.Connection already in progress.Resource unavailable, or operation would block.Address family not supported.Address not available.Address in use.Permission denied.Argument list too long.No error occurred. System call completed successfully.Errno\00\00\07\00\00\00\04\00\00\00\05\00\00\00\09\00\00\00\0c\00\00\00\0b\00\00\00\05\00\00\00\07\00\00\00\04\00\00\00\06\00\00\00\04\00\00\00\08\00\00\00\05\00\00\00\0b\00\00\00\0b\00\00\00\09\00\00\00\06\00\00\00\0b\00\00\00\03\00\00\00\05\00\00\00\05\00\00\00\05\00\00\00\04\00\00\00\0b\00\00\00\04\00\00\00\05\00\00\00\0a\00\00\00\04\00\00\00\05\00\00\00\02\00\00\00\06\00\00\00\05\00\00\00\04\00\00\00\05\00\00\00\05\00\00\00\07\00\00\00\08\00\00\00\0b\00\00\00\07\00\00\00\08\00\00\00\0a\00\00\00\05\00\00\00\06\00\00\00\05\00\00\00\05\00\00\00\06\00\00\00\05\00\00\00\06\00\00\00\05\00\00\00\05\00\00\00\0a\00\00\00\05\00\00\00\05\00\00\00\07\00\00\00\06\00\00\00\08\00\00\00\0e\00\00\00\07\00\00\00\06\00\00\00\05\00\00\00\04\00\00\00\08\00\00\00\09\00\00\00\04\00\00\00\04\00\00\00\05\00\00\00\0e\00\00\00\09\00\00\00\05\00\00\00\04\00\00\00\05\00\00\00\04\00\00\00\05\00\00\00\08\00\00\00\06\00\00\00\04\00\00\00\0a\00\00\00\ab\1d\10\00\a7\1d\10\00\a2\1d\10\00\99\1d\10\00\8d\1d\10\00\82\1d\10\00}\1d\10\00v\1d\10\00r\1d\10\00l\1d\10\00h\1d\10\00`\1d\10\00[\1d\10\00P\1d\10\00E\1d\10\00<\1d\10\006\1d\10\00+\1d\10\00(\1d\10\00#\1d\10\00\1e\1d\10\00\19\1d\10\00\15\1d\10\00\0a\1d\10\00\06\1d\10\00\01\1d\10\00\f7\1c\10\00\f3\1c\10\00\ee\1c\10\00\ec\1c\10\00\e6\1c\10\00\e1\1c\10\00\dd\1c\10\00\d8\1c\10\00\d3\1c\10\00\cc\1c\10\00\c4\1c\10\00\b9\1c\10\00\b2\1c\10\00\aa\1c\10\00\a0\1c\10\00\9b\1c\10\00\95\1c\10\00\90\1c\10\00\8b\1c\10\00\85\1c\10\00\80\1c\10\00z\1c\10\00u\1c\10\00p\1c\10\00f\1c\10\00a\1c\10\00\5c\1c\10\00U\1c\10\00O\1c\10\00G\1c\10\009\1c\10\002\1c\10\00,\1c\10\00'\1c\10\00#\1c\10\00\1b\1c\10\00\12\1c\10\00\0e\1c\10\00\0a\1c\10\00\05\1c\10\00\f7\1b\10\00\ee\1b\10\00\e9\1b\10\00\e5\1b\10\00\e0\1b\10\00\dc\1b\10\00\d7\1b\10\00\cf\1b\10\00\c9\1b\10\00\c5\1b\10\00\bb\1b\10\006\00\00\00\17\00\00\00\12\00\00\00\0f\00\00\00\16\00\00\00\1d\00\00\00/\00\00\00\1f\00\00\00\14\00\00\00\0c\00\00\00\18\00\00\00\13\00\00\00\13\00\00\00\13\00\00\00\13\00\00\00\11\00\00\00\1e\00\00\00\1d\00\00\00/\00\00\00\09\00\00\00\0c\00\00\00\0c\00\00\00\0f\00\00\00\14\00\00\00\13\00\00\00\16\00\00\00\16\00\00\00\15\00\00\00\11\00\00\00\0a\00\00\00\14\00\00\00\0f\00\00\00\22\00\00\00 \00\00\00\0f\00\00\00\12\00\00\00\09\00\00\00\12\00\00\00\10\00\00\00\1e\00\00\00\14\00\00\00\1e\00\00\00\1a\00\00\00\0f\00\00\00\1a\00\00\00\1d\00\00\00\13\00\00\00\09\00\00\00\11\00\00\00\1f\00\00\00\17\00\00\00\18\00\00\00\17\00\00\00\1c\00\00\002\00\00\00\14\00\00\00\16\00\00\00\0d\00\00\004\00\00\00$\00\00\00\1a\00\00\00*\00\00\00\14\00\00\00\18\00\00\00\0c\00\00\00\0f\00\00\00\17\00\00\00\1f\00\00\00\11\00\00\00\16\00\00\00\0d\00\00\00\10\00\00\00\09\00\00\00\15\00\00\00\0f\00\00\00\12\00\00\00%\00\00\00;$\10\00$$\10\00\12$\10\00\03$\10\00\ed#\10\00\d0#\10\00\a1#\10\00\82#\10\00n#\10\00b#\10\00J#\10\007#\10\00$#\10\00\11#\10\00\fe\22\10\00\ed\22\10\00\cf\22\10\00\b2\22\10\00\83\22\10\00\0d\1e\10\00w\22\10\00k\22\10\00\5c\22\10\00H\22\10\005\22\10\00\1f\22\10\00\09\22\10\00\f4!\10\00\e3!\10\00\d9!\10\00\c5!\10\00\b6!\10\00\94!\10\00t!\10\00e!\10\00S!\10\00\0d\1e\10\00A!\10\001!\10\00\13!\10\00\ff \10\00\e1 \10\00\c7 \10\00\b8 \10\00\9e \10\00\81 \10\00n \10\00\0d\1e\10\00] \10\00> \10\00' \10\00\0f \10\00\f8\1f\10\00\dc\1f\10\00\aa\1f\10\00\96\1f\10\00\80\1f\10\00s\1f\10\00?\1f\10\00\1b\1f\10\00\01\1f\10\00\d7\1e\10\00\c3\1e\10\00\ab\1e\10\00\9f\1e\10\00\90\1e\10\00y\1e\10\00Z\1e\10\00I\1e\10\003\1e\10\00&\1e\10\00\16\1e\10\00\0d\1e\10\00\f8\1d\10\00\e9\1d\10\00\d7\1d\10\00\b2\1d\10\00/\00")
  (data $.data (i32.const 1059152) "\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\22\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00#\00\00\00\01\00\00\00H)\10\00\ff\ff\ff\ff"))
