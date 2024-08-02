#[macro_export]
macro_rules! a {
    ($source:expr, $upper_channel:expr, $lower_channel:expr) => {{
        let prev_source = $source.shift(1);

        (
            $source.sgt(&$lower_channel) & prev_source.slt(&$lower_channel.shift(1)),
            $source.slt(&$upper_channel) & prev_source.sgt(&$upper_channel.shift(1)),
        )
    }};
}

#[macro_export]
macro_rules! c {
    ($low:expr, $high:expr, $upper_channel:expr, $lower_channel:expr) => {{
        let prev_lwch = $lower_channel.shift(1);
        let prev_upch = $upper_channel.shift(1);

        (
            $low.slt(&prev_lwch) & $low.shift(1).sgt(&prev_lwch),
            $high.sgt(&prev_upch) & $high.shift(1).slt(&prev_upch),
        )
    }};
}
