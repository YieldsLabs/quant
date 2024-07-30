#[macro_export]
macro_rules! a {
    ($upper_channel:expr, $lower_channel:expr, $high:expr, $low:expr) => {{
        let prev_lwch = $lower_channel.shift(1);
        let prev_upch = $upper_channel.shift(1);

        (
            $low.slt(&$prev_lwch) & $low.shift(1).sgt(&$prev_lwch),
            $high.sgt(&$prev_upch) & $high.shift(1).slt(&$prev_upch),
        )
    }};
}
