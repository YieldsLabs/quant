use core::prelude::*;

#[inline]
pub fn smooth_deserialize(smooth: usize) -> Smooth {
    match smooth {
        1 => Smooth::EMA,
        2 => Smooth::SMA,
        3 => Smooth::SMMA,
        4 => Smooth::KAMA,
        5 => Smooth::HMA,
        6 => Smooth::WMA,
        7 => Smooth::ZLEMA,
        8 => Smooth::LSMA,
        9 => Smooth::TEMA,
        10 => Smooth::DEMA,
        11 => Smooth::ULTS,
        _ => Smooth::EMA,
    }
}
