use crate::config::{
    BaseLineConfig, ConfirmConfig, ExitConfig, PulseConfig, SignalConfig, StopLossConfig,
};
use crate::mapper::{
    map_to_baseline, map_to_confirm, map_to_exit, map_to_pulse, map_to_signal, map_to_stoploss,
};
use base::prelude::*;
use timeseries::prelude::*;

fn read_from_memory(ptr: *const u8, len: usize) -> &'static [u8] {
    unsafe { std::slice::from_raw_parts(ptr, len) }
}

#[no_mangle]
pub fn register(
    signal_ptr: *const u8,
    signal_len: usize,
    primary_confirm_ptr: *const u8,
    primary_confirm_len: usize,
    secondary_confirm_ptr: *const u8,
    secondary_confirm_len: usize,
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
    let primary_confirm_buffer = read_from_memory(primary_confirm_ptr, primary_confirm_len);
    let secondary_confirm_buffer = read_from_memory(secondary_confirm_ptr, secondary_confirm_len);
    let pulse_buffer = read_from_memory(pulse_ptr, pulse_len);
    let baseline_buffer = read_from_memory(baseline_ptr, baseline_len);
    let stop_loss_buffer = read_from_memory(stop_loss_ptr, stop_loss_len);
    let exit_buffer = read_from_memory(exit_ptr, exit_len);

    let signal: SignalConfig = serde_json::from_slice(signal_buffer).unwrap();
    let primary_confirm: ConfirmConfig = serde_json::from_slice(primary_confirm_buffer).unwrap();
    let secondary_confirm: ConfirmConfig =
        serde_json::from_slice(secondary_confirm_buffer).unwrap();
    let pulse: PulseConfig = serde_json::from_slice(pulse_buffer).unwrap();
    let baseline: BaseLineConfig = serde_json::from_slice(baseline_buffer).unwrap();
    let stop_loss: StopLossConfig = serde_json::from_slice(stop_loss_buffer).unwrap();
    let exit: ExitConfig = serde_json::from_slice(exit_buffer).unwrap();

    register_strategy(
        Box::<BaseTimeSeries>::default(),
        map_to_signal(signal),
        map_to_confirm(primary_confirm),
        map_to_confirm(secondary_confirm),
        map_to_pulse(pulse),
        map_to_baseline(baseline),
        map_to_stoploss(stop_loss),
        map_to_exit(exit),
    )
}
