use core::prelude::*;

#[macro_export]
macro_rules! f {
    ($direction:expr) => {{
        ($direction.cross_over(&ZERO), $direction.cross_under(&ZERO))
    }};
}

#[macro_export]
macro_rules! p {
    ($trend:expr, $high:expr, $low:expr, $close:expr) => {{
        let prev_trend = $trend.shift(1);

        (
            $low.shift(1).cross_under(&prev_trend) & $close.sgt(&$trend),
            $high.shift(1).cross_over(&prev_trend) & $close.slt(&$trend),
        )
    }};
}
