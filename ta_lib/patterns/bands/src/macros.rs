#[macro_export]
macro_rules! a {
    ($upper_band:expr, $lower_band:expr, $source:expr) => {{
        let prev_source = $source.shift(1);

        (
            $source.slt(&$lower_band) & prev_source.sgt(&$lower_band.shift(1)),
            $source.sgt(&$upper_band) & prev_source.slt(&$upper_band.shift(1)),
        )
    }};
}

#[macro_export]
macro_rules! c {
    ($upper_band:expr, $middle_band:expr, $lower_band:expr, $source:expr) => {{
        let prev_source = $source.shift(1);

        (
            $source.sgt(&$lower_band)
                & prev_source.slt(&$lower_band.shift(1))
                & $source.slt(&$middle_band),
            $source.slt(&$upper_band)
                & prev_source.sgt(&$upper_band.shift(1))
                & $source.sgt(&$middle_band),
        )
    }};
}
