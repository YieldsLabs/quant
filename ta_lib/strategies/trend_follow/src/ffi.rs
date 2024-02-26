use crate::baseline_mapper::{map_to_baseline, BaseLineConfig};
use crate::confirm_mapper::{map_to_confirm, ConfirmConfig};
use crate::exit_mapper::{map_to_exit, ExitConfig};
use crate::pulse_mapper::{map_to_pulse, PulseConfig};
use crate::signal_mapper::{map_to_signal, SignalConfig};
use crate::stop_loss_mapper::{map_to_stoploss, StopLossConfig};
use base::prelude::*;

fn read_from_memory(ptr: *const u8, len: usize) -> &'static [u8] {
    unsafe { std::slice::from_raw_parts(ptr, len) }
}

#[no_mangle]
pub fn register(
    signal_ptr: *const u8,
    signal_len: usize,
    confirm_ptr: *const u8,
    confirm_len: usize,
    pulse_ptr: *const u8,
    pulse_len: usize,
    baseline_ptr: *const u8,
    baseline_len: usize,
    stop_loss_ptr: *const u8,
    stop_loss_len: usize,
    exit_ptr: *const u8,
    exit_len: usize,
) -> i32 {
    let signal_buffer = read_from_memory(signal_ptr, signal_len);
    let confirm_buffer = read_from_memory(confirm_ptr, confirm_len);
    let pulse_buffer = read_from_memory(pulse_ptr, pulse_len);
    let baseline_buffer = read_from_memory(baseline_ptr, baseline_len);
    let stop_loss_buffer = read_from_memory(stop_loss_ptr, stop_loss_len);
    let exit_buffer = read_from_memory(exit_ptr, exit_len);

    let signal: SignalConfig = serde_json::from_slice(signal_buffer).unwrap();
    let confirm: ConfirmConfig = serde_json::from_slice(confirm_buffer).unwrap();
    let pulse: PulseConfig = serde_json::from_slice(pulse_buffer).unwrap();
    let baseline: BaseLineConfig = serde_json::from_slice(baseline_buffer).unwrap();
    let stop_loss: StopLossConfig = serde_json::from_slice(stop_loss_buffer).unwrap();
    let exit: ExitConfig = serde_json::from_slice(exit_buffer).unwrap();

    register_strategy(
        map_to_signal(signal),
        map_to_confirm(confirm),
        map_to_pulse(pulse),
        map_to_baseline(baseline),
        map_to_stoploss(stop_loss),
        map_to_exit(exit),
    )
}
