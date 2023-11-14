use crate::exit_mapper::{map_to_exit, ExitConfig};
use crate::regime_mapper::{map_to_regime, RegimeConfig};
use crate::signal_mapper::{map_to_signal, SignalConfig};
use crate::stop_loss_mapper::{map_to_stoploss, StopLossConfig};
use crate::volume_mapper::{map_to_volume, VolumeConfig};
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
    regime_ptr: *const u8,
    regime_len: usize,
    volume_ptr: *const u8,
    volume_len: usize,
    stop_loss_ptr: *const u8,
    stop_loss_len: usize,
    exit_ptr: *const u8,
    exit_len: usize,
) -> i32 {
    let signal_buffer = read_from_memory(signal_ptr, signal_len);
    let regime_buffer = read_from_memory(regime_ptr, regime_len);
    let volume_buffer = read_from_memory(volume_ptr, volume_len);
    let stop_loss_buffer = read_from_memory(stop_loss_ptr, stop_loss_len);
    let exit_buffer = read_from_memory(exit_ptr, exit_len);

    let signal: SignalConfig = serde_json::from_slice(&signal_buffer).unwrap();
    let regime: RegimeConfig = serde_json::from_slice(&regime_buffer).unwrap();
    let volume: VolumeConfig = serde_json::from_slice(&volume_buffer).unwrap();
    let stop_loss: StopLossConfig = serde_json::from_slice(&stop_loss_buffer).unwrap();
    let exit: ExitConfig = serde_json::from_slice(&exit_buffer).unwrap();

    let mapped_signal = map_to_signal(signal);
    let mapped_regime = map_to_regime(regime);
    let mapped_volume = map_to_volume(volume);
    let mapped_stoploss = map_to_stoploss(stop_loss);
    let mapped_exit = map_to_exit(exit);

    register_strategy(
        mapped_signal,
        mapped_regime,
        mapped_volume,
        mapped_stoploss,
        mapped_exit,
    )
}
