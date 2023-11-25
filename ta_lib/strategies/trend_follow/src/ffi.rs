use crate::baseline_mapper::{map_to_baseline, BaseLineConfig};
use crate::exit_mapper::{map_to_exit, ExitConfig};
use crate::filter_mapper::{map_to_filter, FilterConfig};
use crate::pulse_mapper::{map_to_pulse, PulseConfig};
use crate::signal_mapper::{map_to_signal, SignalConfig};
use crate::stop_loss_mapper::{map_to_stoploss, StopLossConfig};
use base::register_strategy;

fn read_from_memory(ptr: *const u8, len: usize) -> Vec<u8> {
    unsafe {
        let slice = std::slice::from_raw_parts(ptr, len);
        slice.to_vec()
    }
}

#[no_mangle]
pub fn register(
    signal_ptr: *const u8,
    signal_len: usize,
    filter_ptr: *const u8,
    filter_len: usize,
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
    let filter_buffer = read_from_memory(filter_ptr, filter_len);
    let pulse_buffer = read_from_memory(pulse_ptr, pulse_len);
    let baseline_buffer = read_from_memory(baseline_ptr, baseline_len);
    let stop_loss_buffer = read_from_memory(stop_loss_ptr, stop_loss_len);
    let exit_buffer = read_from_memory(exit_ptr, exit_len);

    let signal: SignalConfig = serde_json::from_slice(&signal_buffer).unwrap();
    let filter: FilterConfig = serde_json::from_slice(&filter_buffer).unwrap();
    let pulse: PulseConfig = serde_json::from_slice(&pulse_buffer).unwrap();
    let baseline: BaseLineConfig = serde_json::from_slice(&baseline_buffer).unwrap();
    let stop_loss: StopLossConfig = serde_json::from_slice(&stop_loss_buffer).unwrap();
    let exit: ExitConfig = serde_json::from_slice(&exit_buffer).unwrap();

    let mapped_signal = map_to_signal(signal);
    let mapped_filter = map_to_filter(filter);
    let mapped_pulse = map_to_pulse(pulse);
    let mapped_baseline = map_to_baseline(baseline);
    let mapped_stoploss = map_to_stoploss(stop_loss);
    let mapped_exit = map_to_exit(exit);

    register_strategy(
        mapped_signal,
        mapped_filter,
        mapped_pulse,
        mapped_baseline,
        mapped_stoploss,
        mapped_exit,
    )
}
