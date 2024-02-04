use core::prelude::*;

pub fn map_to_smooth(smooth: usize) -> Smooth {
    match smooth {
        1 => Smooth::EMA,
        2 => Smooth::SMA,
        3 => Smooth::SMMA,
        4 => Smooth::KAMA,
        5 => Smooth::HMA,
        6 => Smooth::WMA,
        7 => Smooth::ZLEMA,
        8 => Smooth::LSMA,
        _ => Smooth::EMA,
    }
}
